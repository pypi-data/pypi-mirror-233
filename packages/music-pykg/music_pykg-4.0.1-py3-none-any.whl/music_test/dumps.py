from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, Mapping, Tuple, Union

import h5py
import numpy as np
from music_pykg.format1 import MusicFormat1DumpFile
from music_pykg.format2 import MusicNewFormatDumpFile
from music_pykg.grid import Grid
from music_pykg.known_variables import KnownMusicVariables

from .ic_gen import CachedStateAtNodes, Problem
from .utils import RelativePath


class Dump(ABC):
    """Base class for dump definition without knowing its concrete location."""

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteDump:
        """Return a concrete dump relative to the provided location."""

    def __sub__(self, other: Dump) -> Dump:
        """Represent the difference between two dumps."""
        return DiffDump(self, other)


class ConcreteDump(ABC):
    """Dump knowing its concrete location."""

    @abstractmethod
    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        """Return a tuple (header, data) of two dictionaries,
        which map entry names to numerical values for the dump
        (typically of type `int`, `float` or `numpy.ndarray`).
        """


class FileDump(Dump, ABC):
    """A dump which corresponds to an actual file on disk"""

    filename: Union[str, PathLike, RelativePath]

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteFileDump:
        ...


class ConcreteFileDump(ConcreteDump, ABC):
    fdump: FileDump
    path: Path

    @property
    def full_filename(self) -> Path:
        return self.path / self.fdump.filename


@dataclass(frozen=True)
class MusicDump1(FileDump):
    """Old-style MUSIC dump (output_method=1)"""

    filename: Union[str, PathLike, RelativePath]
    ndim: int
    idump: int = -1
    trim_last_cell: bool = True

    def with_path(self, path: Path) -> ConcreteDump1:
        return ConcreteDump1(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDump1(ConcreteFileDump):
    fdump: MusicDump1
    path: Path

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        with MusicFormat1DumpFile(self.full_filename, self.fdump.ndim) as dump:
            header, data = dump.read(self.fdump.idump)

        def trim(arr: np.ndarray) -> np.ndarray:
            for ax in range(arr.ndim):
                arr = np.take(arr, range(arr.shape[ax] - 1), axis=ax)
            return arr

        if self.fdump.trim_last_cell:
            data = {k: trim(arr) for k, arr in data.items()}
        return header, data


@dataclass(frozen=True)
class MusicDump2(FileDump):
    """New-style MUSIC dump (output_method=2)"""

    filename: Union[str, PathLike, RelativePath]

    def with_path(self, path: Path) -> ConcreteDump2:
        return ConcreteDump2(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDump2(ConcreteFileDump):
    fdump: MusicDump2
    path: Path

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        music_vars = KnownMusicVariables()
        hdr, data = MusicNewFormatDumpFile(self.full_filename).read()
        data = {music_vars.legacy(name).name: vals for name, vals in data.items()}
        return hdr.as_dict(), data


@dataclass(frozen=True)
class MusicDumpH5(FileDump):
    """MUSIC dump in HDF5 format."""

    filename: Union[str, PathLike, RelativePath]

    def with_path(self, path: Path) -> ConcreteDumpH5:
        return ConcreteDumpH5(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDumpH5(ConcreteFileDump):
    fdump: MusicDumpH5
    path: Path

    def namelist(self) -> Mapping[str, Mapping[str, Any]]:
        nml = {}
        with h5py.File(self.full_filename) as h5f:
            for sec_name, sec in h5f["parameters_nml"].items():
                nml[sec_name] = MappingProxyType(
                    {opt: val[()].squeeze for opt, val in sec.items()}
                )
        return MappingProxyType(nml)

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header = {}
        data = {}
        with h5py.File(self.full_filename) as h5f:
            for name, values in h5f["fields"].items():
                data[name] = values[()].squeeze().T
            ndim = data[name].ndim
            header["nfaces"] = h5f["geometry/ncells"][()][:ndim] + 1
            xsmin = h5f["geometry/xmin"][()]
            xsmax = h5f["geometry/xmax"][()]
        for idim, (nfaces, xmin, xmax) in enumerate(
            zip(header["nfaces"], xsmin, xsmax), 1
        ):
            header[f"face_loc_{idim}"] = np.linspace(xmin, xmax, nfaces)
        return header, data


@dataclass(frozen=True)
class DiffDump(Dump):
    """A dump formed by selecting the header of either `dump_left` or `dump_right`,
    and taking the differences of the data arrays.
    """

    dump_left: Dump
    dump_right: Dump
    which_header: str = "left"  # select header from dump_left or dump_right

    def with_path(self, path: Path) -> ConcreteDiffDump:
        return ConcreteDiffDump(
            self.dump_left.with_path(path),
            self.dump_right.with_path(path),
            which_header=self.which_header,
        )


@dataclass(frozen=True)
class ConcreteDiffDump(ConcreteDump):
    dump_left: ConcreteDump
    dump_right: ConcreteDump
    which_header: str = "left"  # select header from dump_left or dump_right

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header_left, data_left = self.dump_left.header_and_data()
        header_right, data_right = self.dump_right.header_and_data()
        if self.which_header == "left":
            header = header_left
        elif self.which_header == "right":
            header = header_right
        else:
            raise ValueError(
                f"DiffDumpData: expected which_header to be "
                f"either 'left' or 'right', got '{self.which_header}'"
            )

        if not set(data_left.keys()) == set(data_right.keys()):
            raise ValueError(
                "DiffDumpData: non-identical data keys, got "
                f"keys_left={list(data_left.keys())}, "
                f"keys_right={list(data_right.keys())}"
            )

        return header, {k: data_left[k] - data_right[k] for k in data_left}


@dataclass(frozen=True)
class AnalyticalSolution(Dump):
    problem: Problem
    ref_dump: Dump

    def with_path(self, path: Path) -> ConcreteAnalyticalSolution:
        return ConcreteAnalyticalSolution(self.problem, self.ref_dump.with_path(path))


@dataclass(frozen=True)
class ConcreteAnalyticalSolution(ConcreteDump):
    problem: Problem
    ref_dump: ConcreteDump

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header, data = self.ref_dump.header_and_data()

        music_vars = KnownMusicVariables()
        unknown_vars = set(name for name in data.keys() if name not in music_vars)
        if unknown_vars:
            raise ValueError(
                f"{self.ref_dump} has variables {sorted(unknown_vars)}"
                " whose mesh centering cannot be inferred"
            )

        cached_state = CachedStateAtNodes(
            problem=self.problem,
            time=header["time"],
            grid=Grid.from_header(header),
        )

        def sol(var: str) -> np.ndarray:
            fields = cached_state.at(music_vars[var].nodes).as_data_dict()
            if var not in fields:
                raise ValueError(
                    f"field '{var}' is present in '{self.ref_dump}' but not in analytical solution"
                )
            return fields[var].squeeze()

        return header, {k: sol(k) for k in data}
