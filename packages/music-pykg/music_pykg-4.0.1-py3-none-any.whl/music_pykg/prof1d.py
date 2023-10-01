"""Utility to read profile1d dat files."""
from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import MappingProxyType

import pandas as pd

if typing.TYPE_CHECKING:
    from typing import Mapping


@dataclass(frozen=True)
class Prof1d:
    """Prof1d parser."""

    path: Path

    @staticmethod
    def with_path_hint(path_hint: Path) -> Prof1d:
        """Find a profile file from the given hint.

        Args:
            path_hint: either the path to the profile file, or the path to the
                folder containing the profile file.  In the latter case, the
                parser tries to find a file and fails if none is found or there
                is ambiguity.
        """
        if path_hint.is_file():
            return Prof1d(path_hint)
        candidates = [
            path
            for p1d in ("profile1d.dat", "profile1d_scalars.dat")
            if (path := path_hint / p1d).is_file()
        ]
        if not candidates:
            raise RuntimeError("No profile1d file found in {self._path_hint}")
        if len(candidates) > 1:
            raise RuntimeError(f"More than one profile1d files found: {candidates}")
        return Prof1d(candidates[0])

    @cached_property
    def params(self) -> Mapping[str, float]:
        with self.path.open() as p1d:
            names = p1d.readline().split()
            values = map(float, p1d.readline().split())
        params = dict(zip(names, values))
        return MappingProxyType(params)

    @cached_property
    def profs(self) -> pd.DataFrame:
        return pd.read_csv(self.path, skiprows=2, delim_whitespace=True)
