from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple, TypeVar

import f90nml

T = TypeVar("T")


@dataclass(frozen=True)
class MusicNamelist:
    """A Fortran namelist file with MUSIC syntax"""

    path: Path

    @cached_property
    def nml(self) -> f90nml.Namelist:
        return f90nml.read(self.path)

    def get(self, section: str, option: str, default: T) -> T:
        """Get an given parameter or return the provided default value."""
        sec = self.nml.get(section, {})
        return sec.get(option, default)

    @property
    def proc_shape(self) -> Tuple[int, int, int]:
        """Returns the number of processors along each dimension as a tuple (npx, npy, npz).
        Returns (1, 1, 1) if processor count not specified in namelist.
        """
        return (
            self.get("grid", "nprocx", 1),
            self.get("grid", "nprocy", 1),
            self.get("grid", "nprocz", 1),
        )

    @property
    def num_procs(self) -> int:
        """Return number of processors"""
        npx, npy, npz = self.proc_shape
        return npx * npy * npz

    @property
    def eos(self) -> str:
        return self.nml["microphysics"]["eos"]

    @property
    def gamma(self) -> float:
        """Return adiabatic index"""
        return self.nml["physics"]["gamma"]

    @property
    def is_cartesian(self) -> bool:
        return self.nml["geometry"]["cartesian"]

    @property
    def nscalars(self) -> int:
        return self.get("scalars", "nscalars", 0)

    @property
    def nactive_scalars(self) -> int:
        return self.get("scalars", "nactive_scalars", 0)

    @property
    def gravity(self) -> float:
        return self.nml["physics"]["gravity"]

    @property
    def gravity_file(self) -> str:
        return self.get("physics", "gravity_file", "")

    @property
    def consistent_gravity(self) -> bool:
        return self.get("physics", "consistent_gravity", False)

    @property
    def mhd_enabled(self) -> bool:
        return self.get("physics", "mhd_enabled", False)

    @property
    def has_rotation(self) -> bool:
        return any(
            [
                self.get("physics", "omegax", 0.0) != 0.0,
                self.get("physics", "omegay", 0.0) != 0.0,
                self.get("physics", "omegaz", 0.0) != 0.0,
            ]
        )
