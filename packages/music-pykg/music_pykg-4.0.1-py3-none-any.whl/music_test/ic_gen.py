from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from types import MappingProxyType

from music_pykg.format2 import MusicNewFormatDumpFile
from music_pykg.grid import NODES_CENTER, Nodes
from music_pykg.known_variables import KnownMusicVariables

if typing.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
    from typing import Dict, Mapping, Optional, Tuple, Union

    from music_pykg.grid import Grid, Points
    from numpy.typing import NDArray

    from .utils import RelativePath


@dataclass(frozen=True)
class State:
    density: NDArray
    e_int_spec: NDArray
    vel_1: NDArray
    vel_2: NDArray
    vel_3: Optional[NDArray] = None
    scalars: Mapping[str, NDArray] = field(default_factory=dict)
    magfield: Optional[Tuple[NDArray, NDArray, NDArray]] = None

    def as_data_dict(self) -> Mapping[str, NDArray]:
        # temporary function to simplify interaction with the rest
        # of the code and in particular Dumps that represent data
        # with a dict
        data = dict(
            density=self.density,
            e_int_spec=self.e_int_spec,
            vel_1=self.vel_1,
            vel_2=self.vel_2,
            **self.scalars,
        )
        if self.vel_3 is not None:
            data["vel_3"] = self.vel_3
        if self.magfield is not None:
            data.update(
                magfield_1=self.magfield[0],
                magfield_2=self.magfield[1],
                magfield_3=self.magfield[2],
            )
        return MappingProxyType(data)


class Problem(ABC):
    @abstractmethod
    def state_at(self, time: float, points: Points) -> State:
        """Evaluate state at the given time and location."""


@dataclass(frozen=True)
class CachedStateAtNodes:
    problem: Problem
    time: float
    grid: Grid

    @cached_property
    def _cache(self) -> Dict[Nodes, State]:
        return {}

    def at(self, nodes: Nodes) -> State:
        if (state := self._cache.get(nodes)) is not None:
            return state
        points = self.grid.points_at(nodes)
        return self._cache.setdefault(nodes, self.problem.state_at(self.time, points))


@dataclass(frozen=True)
class DumpOnDiskFromProblem:
    filename: Union[str, PathLike, RelativePath]
    problem: Problem
    grid: Grid
    time: float
    music_vars: KnownMusicVariables = KnownMusicVariables()

    @cached_property
    def _state(self) -> CachedStateAtNodes:
        return CachedStateAtNodes(
            problem=self.problem,
            time=self.time,
            grid=self.grid,
        )

    def create_in_dir(self, path: Path) -> None:
        data = dict(
            xmcore=0,
            model=1,
            num_ghost=0,
            eos=0,
            gamma=5 / 3,
            ikap=2,
            Y=0.28,
            Z=2e-2,
            geometry=self.grid.geometry_flag,
            dtn=0.0,
            time=self.time,
            nfaces=self.grid.nfaces,
            face_loc_1=self.grid.faces_along_axis[0],
            face_loc_2=self.grid.faces_along_axis[1],
        )
        if not self.grid.is_2d():
            data["face_loc_3"] = self.grid.faces_along_axis[2]

        state = self._state
        mvars = self.music_vars

        data.update(
            rho=state.at(mvars["density"].nodes).density,
            e=state.at(mvars["e_int_spec"].nodes).e_int_spec,
            v_r=state.at(mvars["vel_1"].nodes).vel_1,
            v_t=state.at(mvars["vel_2"].nodes).vel_2,
        )

        if (v3 := state.at(mvars["vel_3"].nodes).vel_3) is not None:
            data.update(v_p=v3)

        state_c = state.at(NODES_CENTER)  # only to check what scalars exist
        for scalar_name in state_c.scalars.keys():
            mvar = self.music_vars[scalar_name]
            data[mvar.legacy_name] = state.at(mvar.nodes).scalars[scalar_name]

        for i, bname in enumerate(("b_r", "b_t", "b_p")):
            state_i = state.at(mvars.legacy(bname).nodes)
            if state_i.magfield is not None:
                data[bname] = state_i.magfield[i]

        dump_file = MusicNewFormatDumpFile(path / self.filename)
        dump_file.write(data)
