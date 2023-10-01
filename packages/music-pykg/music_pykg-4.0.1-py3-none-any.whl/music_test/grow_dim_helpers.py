"""Helper classes for grow_dim tool tests."""
from __future__ import annotations

import typing
from dataclasses import asdict, dataclass

import f90nml
import numpy as np
from music_pykg.grid import Points

from .dumps import ConcreteDump, Dump
from .ic_gen import Problem, State

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Dict, List, Tuple, Union

    from numpy.typing import NDArray

    from .ic_gen import DumpOnDiskFromProblem


@dataclass(frozen=True)
class RandomBox(Problem):
    rng: np.random.Generator
    nvel: int

    def state_at(self, time: float, points: Points) -> State:
        return State(
            density=self.rng.standard_normal(points.shape),
            e_int_spec=self.rng.standard_normal(points.shape),
            vel_1=self.rng.standard_normal(points.shape),
            vel_2=self.rng.standard_normal(points.shape),
            vel_3=self.rng.standard_normal(points.shape) if self.nvel == 3 else None,
        )


@dataclass(frozen=True)
class GrowDim(Dump):
    ref_dump: Dump
    ax3_params: Tuple[float, float, int]
    mode: Tuple[Tuple[str, str], ...]
    fill_vel_3: float = 0.0

    def with_path(self, path: Path) -> ConcreteGrowDim:
        return ConcreteGrowDim(
            self.ref_dump.with_path(path),
            self.ax3_params,
            self.mode,
            self.fill_vel_3,
        )


@dataclass(frozen=True)
class ConcreteGrowDim(ConcreteDump):
    """Extend 2d into 3d"""

    ref_dump: ConcreteDump
    ax3_params: Tuple[float, float, int]
    mode: Tuple[Tuple[str, str], ...]
    fill_vel_3: float = 0.0

    def volume(self, header: Dict[str, Any]) -> NDArray:
        if header["geometry"] == 1:  # spherical
            costheta = np.cos(header["face_loc_2"])
            vol = (
                np.diff(header["face_loc_1"] ** 3)[:, None] * np.diff(costheta)[None, :]
            ) / 3
            if "face_loc_3" in header:
                vol = vol[:, :, None] * np.diff(header["face_loc_3"])[None, None, :]
            else:
                vol = vol * 2 * np.pi
        else:  # cartesian
            vol = (
                np.diff(header["face_loc_1"])[:, None]
                * np.diff(header["face_loc_2"])[None, :]
            )
            if "face_loc_3" in header:
                vol = vol[:, :, None] * np.diff(header["face_loc_3"])[None, None, :]
        return np.abs(vol)

    def ax3_coord(self, geometry: bool) -> NDArray:
        if geometry == 1:
            # for spherical convert from degrees to rad
            xmin = self.ax3_params[0] / 180 * np.pi
            xmax = self.ax3_params[1] / 180 * np.pi
            nx = self.ax3_params[2]
            return np.linspace(xmin, xmax, nx)
        else:
            return np.linspace(*self.ax3_params)

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header, data = self.ref_dump.header_and_data()
        vol = self.volume(header)
        # update header
        header["face_loc_3"] = self.ax3_coord(header["geometry"])
        header.update(nfaces=[len(header[f"face_loc_{i}"]) for i in range(1, 4)])
        ncells_3d = [x - 1 for x in header["nfaces"]]
        # update fields
        for f, m in self.mode:
            if m == "copy":
                data[f] = np.tile(data[f][..., None], ncells_3d[2])
            elif m == "1d_mean":
                fmean = np.average(data[f], weights=vol, axis=1)
                data[f] = np.tile(fmean[:, None, None], ncells_3d[1:])
            elif m == "zero":
                data[f] = np.zeros(ncells_3d)
            else:
                raise ValueError("unrecognized mode")

        # fill in new fields
        if not ("vel_3" in data):
            data["vel_3"] = np.ones(ncells_3d) * self.fill_vel_3
        return header, data


@dataclass(frozen=True)
class DumpAndNamelistOnDisk:
    dump_on_disk: DumpOnDiskFromProblem
    nml_fname: Union[str, Path]
    nml_parameters: Params

    def create_in_dir(self, path: Path) -> None:
        self.nml_parameters.to_nml(path / self.nml_fname)
        self.dump_on_disk.create_in_dir(path)


@dataclass(frozen=True)
class Params:
    dd_in: str
    dd_out: str
    nmom_in: int
    nscalars: int
    with_mhd: bool
    ax3_nfaces: int
    ax3_min: float
    ax3_max: float
    mode: List[str]
    fill_vel_3: float = 0.0

    def as_nml_dict(self) -> Dict[str, Dict[str, Any]]:
        return dict(main=asdict(self))

    def to_nml(self, path: Path) -> None:
        f90nml.write(self.as_nml_dict(), path, force=True)
