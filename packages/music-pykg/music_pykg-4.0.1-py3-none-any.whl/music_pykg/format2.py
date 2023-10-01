from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, overload

import numpy as np

if TYPE_CHECKING:
    from os import PathLike
    from typing import (
        Any,
        Callable,
        Dict,
        Generator,
        Literal,
        Mapping,
        Optional,
        Sequence,
        Set,
        Tuple,
        Union,
    )

    from numpy.typing import DTypeLike, NDArray

    FileName = Union[str, PathLike]


@dataclass(frozen=True)
class LogFileArrayRecord:
    log_file: MusicLogFile
    name: str
    data_pos: int
    dtype: DTypeLike
    squeeze: bool = True

    def read(self) -> np.ndarray:
        self.log_file.seek(self.data_pos)
        return self.log_file._read_array_data(self.dtype, self.squeeze)


class MusicLogFile:
    def __init__(
        self, file_name: FileName, mode: str = "rb", int_t: DTypeLike = "int32"
    ):
        self.f = open(file_name, mode)
        self.file_size = Path(file_name).stat().st_size
        self.int_t = int_t

    def close(self) -> None:
        self.f.close()

    def __del__(self) -> None:
        self.close()

    def seek(self, pos: int) -> None:
        self.f.seek(pos)

    def tell(self) -> int:
        return self.f.tell()

    def seek_start(self) -> None:
        self.seek(0)

    def at_eof(self) -> bool:
        return self.f.tell() >= self.file_size

    def read(self, dtype: DTypeLike, count: int) -> np.ndarray:
        return np.fromfile(self.f, dtype=dtype, count=count).squeeze()

    def _read_name_record(self) -> str:
        # NameRecord:
        #   size     int32[1]
        #   chars    char[size]
        length = int(self.read(self.int_t, 1))
        name_bytes = self.f.read(length)
        return name_bytes.decode(encoding="ascii")

    def _read_type_record(self) -> np.ndarray:
        # TypeRecord:
        #   type     char[1]
        return self.read("byte", 1)

    def _read_data_record(self, dtype: DTypeLike, count: int) -> np.ndarray:
        return self.read(dtype, count).squeeze()

    def _skip_data_record(self, dtype: DTypeLike, count: int) -> None:
        self.seek(self.tell() + np.dtype(dtype).itemsize * count)

    def read_scalar(self, dtype: DTypeLike) -> Tuple[str, np.ndarray]:
        # ScalarItem:
        #   NameRecord
        #   TypeRecord
        #   DataRecord
        name = self._read_name_record()
        _ = self._read_type_record()
        scalar = self._read_data_record(dtype, 1)
        return name, scalar

    @overload
    def read_named_scalar(self, name: str, dtype: Literal["float64"]) -> np.float64:
        ...

    @overload
    def read_named_scalar(self, name: str, dtype: Literal["int32"]) -> np.int32:
        ...

    def read_named_scalar(self, name: str, dtype: DTypeLike) -> np.number:
        name2, scalar = self.read_scalar(dtype)
        if name != name2:
            raise ValueError(f"invalid log item name, expected '{name}', got '{name2}'")
        return scalar.item()

    def _read_transpose_record_as_order(self) -> Literal["C", "F"]:
        # TransposeRecord:
        #   flag     char[1]
        flag = int(self.read("byte", 1))
        assert flag in [0, 1]
        if flag == 0:
            return "C"
        else:
            return "F"

    def _read_dims_record(self) -> np.ndarray:
        # DimsRecord:
        #   dims     int32[3]
        return self.read(np.int32, 3)

    def _read_array_data(self, dtype: DTypeLike, squeeze: bool = True) -> np.ndarray:
        # ArrayDataItem
        #   TypeRecord
        #   TransposeRecord
        #   DimsRecord
        #   DataRecord
        _ = self._read_type_record()
        order = self._read_transpose_record_as_order()
        dims = self._read_dims_record()
        array = self._read_data_record(dtype, np.prod(dims))
        array = array.reshape(dims, order=order)
        if squeeze:
            array = array.squeeze()
        return array

    def _skip_array_data(self, dtype: DTypeLike) -> None:
        _ = self._read_type_record()
        _ = self._read_transpose_record_as_order()
        dims = self._read_dims_record()
        self._skip_data_record(dtype, np.prod(dims))

    def read_array(
        self, dtype: DTypeLike, squeeze: bool = True
    ) -> Tuple[str, np.ndarray]:
        # ArrayItem:
        #   NameRecord
        #   ArrayDataItem
        name = self._read_name_record()
        return name, self._read_array_data(dtype, squeeze)

    def read_lazy_array(
        self,
        dtype: DTypeLike,
        squeeze: bool = True,
    ) -> LogFileArrayRecord:
        # ArrayItem:
        #   NameRecord
        #   ArrayDataItem
        name = self._read_name_record()
        lazy_array = LogFileArrayRecord(self, name, self.tell(), dtype, squeeze)
        self._skip_array_data(dtype)
        return lazy_array

    def read_named_array(
        self, name: str, dtype: DTypeLike, squeeze: bool = True
    ) -> np.ndarray:
        name2, array = self.read_array(dtype, squeeze)
        if name != name2:
            raise ValueError(f"invalid log item name, expected '{name}', got '{name2}'")
        return array


@dataclass(frozen=True)
class Header:
    xmcore: np.float64
    model: np.int32
    dtn: np.float64
    time: np.float64
    nfaces: NDArray[np.int32]
    num_ghost: np.int32
    geometry: np.int32
    eos: np.int32
    gamma: Optional[np.float64]
    ikap: np.int32
    yy: np.float64
    zz: np.float64
    face_loc: Tuple[NDArray[np.float64], ...]

    def as_dict(self) -> Dict[str, Any]:
        dct = asdict(self)
        for iface, face_loc in enumerate(dct.pop("face_loc"), 1):
            dct[f"face_loc_{iface}"] = face_loc
        dct["Y"] = dct.pop("yy")
        dct["Z"] = dct.pop("zz")
        return dct


class MusicNewFormatDumpFile:
    """See readwrite_new_format.90:read_new_model_helium{2d,3d}"""

    header_string = "MUSIC Log File version 1.2"

    def __init__(
        self,
        file_name: FileName,
        keep_field: Callable[[str], bool] = lambda s: True,
    ):
        self.file_name = file_name
        self.keep_field = keep_field

    def _read_header(self, f: MusicLogFile) -> Header:
        f.seek_start()
        header_size = f.read(np.int32, 1)
        if header_size != len(self.header_string):
            warnings.warn(
                f"MUSIC header size mismatch in {self.file_name}, "
                f"expected {len(self.header_string)}, got {header_size}. "
                "File might be damaged. Trying to read anyway."
            )

        f.read("byte", len(self.header_string))
        return Header(
            xmcore=f.read_named_scalar("xmcore", "float64"),
            model=f.read_named_scalar("model", "int32"),
            dtn=f.read_named_scalar("dtn", "float64"),
            time=f.read_named_scalar("time", "float64"),
            nfaces=(nfaces := f.read_named_array("dims", "int32")),
            num_ghost=f.read_named_scalar("num_ghost", "int32"),
            geometry=f.read_named_scalar("geometry", "int32"),
            eos=(eos := f.read_named_scalar("eos", "int32")),
            gamma=f.read_named_scalar("gamma", "float64") if eos == 0 else None,
            ikap=f.read_named_scalar("ikap", "int32"),
            yy=f.read_named_scalar("Y", "float64"),
            zz=f.read_named_scalar("Z", "float64"),
            face_loc=tuple(
                f.read_named_array(ax, "float64")
                for nf, ax in zip(nfaces, ["r", "theta", "phi"])
                if nf > 2
            ),
        )

    def _read_header_and_toc(
        self, f: MusicLogFile
    ) -> Tuple[Header, Mapping[str, LogFileArrayRecord]]:
        header = self._read_header(f)

        def gen_toc() -> Generator[LogFileArrayRecord, None, None]:
            seen: Set[str] = set()
            while not f.at_eof():
                toc_entry = f.read_lazy_array(np.float64)
                assert (
                    toc_entry.name not in seen
                ), "Duplicate entries for field '{toc_entry.name}' in file '{self.file_name}'"
                seen.add(toc_entry.name)
                if self.keep_field(toc_entry.name):
                    yield toc_entry

        toc = {toc_entry.name: toc_entry for toc_entry in gen_toc()}
        return header, MappingProxyType(toc)

    def read(self) -> Tuple[Header, Mapping[str, np.ndarray]]:
        f = MusicLogFile(self.file_name)
        header, toc = self._read_header_and_toc(f)
        data = {name: toc_entry.read() for name, toc_entry in toc.items()}
        f.close()
        return header, MappingProxyType(data)

    def write(self, data: Mapping[str, Any]) -> None:
        writer = _MusicNewFormatDumpWriter(self.file_name)
        writer.write(data)
        writer.close()

    def read_header(self) -> Header:
        f = MusicLogFile(self.file_name)
        header = self._read_header(f)
        f.close()
        return header

    @cached_property
    def field_names(self) -> Sequence[str]:
        f = MusicLogFile(self.file_name)
        _, toc = self._read_header_and_toc(f)
        f.close()
        return list(toc.keys())

    @cached_property
    def num_space_dims(self) -> int:
        return len(self.read_header().face_loc)

    @cached_property
    def num_velocities(self) -> int:
        fields = set(self.field_names)
        return sum(vname in fields for vname in ["v_r", "v_t", "v_p"])

    @cached_property
    def num_scalars(self) -> int:
        fields = set(self.field_names)
        i = 1
        while f"Scalar{i}" in fields:
            i += 1
        return i - 1

    def keeping_only(self, keep: Callable[[str], bool]) -> MusicNewFormatDumpFile:
        return MusicNewFormatDumpFile(
            self.file_name,
            keep_field=lambda field: self.keep_field(field) and keep(field),
        )


def shape3(shape: Sequence[int], fill_value: int = 1) -> Tuple[int, int, int]:
    shape = tuple(shape)
    # TYPE SAFETY: length of returned tuple is guaranteed to be three
    assert len(shape) <= 3
    return tuple(shape) + (3 - len(shape)) * (fill_value,)  # type: ignore


class _MusicNewFormatDumpWriter:
    """
    A quick and dirty implementation of dump file writing,
    initially written for the Stellar Hydro Days code comparison project.

    This class is meant for internal use only to this `io` module.
    Currently, it's bad OO design, as it cares about too many things:

     * the details of low-level storage (this should be delegated to MusicLogFile)

     * the sequence of records in the dump (this should be in MusicNewFormatDumpFile)

    Ideally this class should be split and integrated between MusicLogFile and MusicNewFormatDumpFile,
    but for now at least MusicNewFormatDumpFile works and provides a clean interface to the outside world.
    """

    def __init__(self, fname: Union[str, PathLike]):
        self.fd = open(fname, "wb")

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self.fd.close()

    def write(self, data: Mapping[str, Any]) -> None:
        # Magic header
        self.write_rawarr(np.array([26], dtype="int32"))
        self.write_rawstr("MUSIC Log File version 1.2")

        # Header data
        self.write_double("xmcore", data["xmcore"])
        self.write_int("model", data["model"])
        self.write_double("dtn", data["dtn"])
        self.write_double("time", data["time"])
        self.write_nfaces(data["nfaces"])
        self.write_int("num_ghost", data["num_ghost"])
        self.write_int("geometry", data["geometry"])
        self.write_int("eos", data["eos"])
        if data["eos"] == 0:
            self.write_double("gamma", data["gamma"])
        self.write_int("ikap", data["ikap"])
        self.write_double("Y", data["Y"])
        self.write_double("Z", data["Z"])

        # Grid
        self.write_gridarr("r", data["face_loc_1"])
        self.write_gridarr("theta", data["face_loc_2"])
        if (fl3 := data.get("face_loc_3")) is not None:
            self.write_gridarr("phi", fl3)

        # Variables
        self.write_cube("rho", data["rho"])
        self.write_cube("e", data["e"])
        self.write_cube("v_r", data["v_r"])
        self.write_cube("v_t", data["v_t"])
        if (v_p := data.get("v_p")) is not None:
            self.write_cube("v_p", v_p)

        if "b_r" in data:
            self.write_cube("b_r", data["b_r"])
            self.write_cube("b_t", data["b_t"])
            self.write_cube("b_p", data["b_p"])

        # Scalars
        i = 1
        while (scalar_i := data.get(name := f"Scalar{i}")) is not None:
            self.write_cube(name, scalar_i)
            i += 1

    def write_rawarr(self, arr: np.ndarray) -> None:
        self.fd.write(arr.tobytes(order="F"))

    def write_rawbytes(self, b: Sequence[int]) -> None:
        self.write_rawarr(np.array(b, dtype="byte"))

    def write_rawstr(self, s: str) -> None:
        self.fd.write(s.encode("ascii"))

    def write_nametag(self, name: str) -> None:
        self.fd.write(np.array(len(name), dtype="int32").tobytes())
        self.fd.write(name.encode("ascii"))

    def write_double(self, name: str, x: float) -> None:
        x_arr = np.array(x, dtype="float64")
        assert x_arr.size == 1
        self.write_nametag(name)
        self.write_rawbytes([2])
        self.write_rawarr(x_arr)

    def write_int(self, name: str, x: int) -> None:
        x_arr = np.array(x, dtype="int32")
        assert x_arr.size == 1
        self.write_nametag(name)
        self.write_rawbytes([0])
        self.write_rawarr(x_arr)

    def write_nfaces(self, dims: Tuple[int, ...]) -> None:
        self.write_nametag("dims")
        self.write_rawbytes([4, 0])
        self.write_rawarr(np.array([3, 1, 1], dtype="int32"))
        # fill_value=2 here since we have 2 faces along nonexistent dimensions
        self.write_rawarr(np.array(shape3(dims, fill_value=2), dtype="int32"))

    def write_gridarr(self, name: str, arr: np.ndarray) -> None:
        self.write_nametag(name)
        self.write_rawbytes([6, 0])
        self.write_rawarr(np.array([len(arr), 1, 1], dtype="int32"))
        self.write_rawarr(arr.astype("float64"))

    def write_cube(self, name: str, cube: np.ndarray) -> None:
        self.write_nametag(name)
        self.write_rawbytes([6, 1])
        self.write_rawarr(np.array(shape3(cube.shape, fill_value=1), dtype="int32"))
        self.write_rawarr(cube.astype("float64"))
