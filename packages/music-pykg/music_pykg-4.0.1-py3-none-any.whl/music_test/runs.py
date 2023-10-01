from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from music_pykg.namelist import MusicNamelist

from .cmake_builder import Target

if typing.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
    from typing import ClassVar, Iterable, Optional, Sequence, Union

    from .namelist import NmlFile
    from .utils import RelativePath

    FinalPathSegment = Union[str, PathLike, RelativePath]


class Command(ABC):
    @abstractmethod
    def required_targets(self) -> Iterable[Target]:
        """Targets required for this command."""

    @abstractmethod
    def build(self) -> Sequence[str]:
        """The command itself."""


@dataclass(frozen=True)
class BareCmd(Command):
    exe: Target
    args: Sequence[str] = ()

    def required_targets(self) -> Iterable[Target]:
        yield self.exe

    def build(self) -> Sequence[str]:
        return f"./{self.exe.name}", *self.args


@dataclass(frozen=True)
class MpiCmd(Command):
    nprocs: int
    cmd: Command

    def required_targets(self) -> Iterable[Target]:
        return self.cmd.required_targets()

    def build(self) -> Sequence[str]:
        return "mpirun", "-np", f"{self.nprocs}", *self.cmd.build()


class Run(ABC):
    @property
    def log_filename(self) -> str:
        return "run.log"

    @abstractmethod
    def command(self, run_path: Path) -> Command:
        """Command to run."""

    @abstractmethod
    def build_targets(self) -> Iterable[Target]:
        """Required build targets for the run."""

    def setup_run_dir(self, run_dir: Path) -> None:
        """Prepare the run directory.

        This hook is called right before executing the run, and after files
        from the test directory have been copied over to the run directory.
        This is useful to create files dynamically right before the run.
        """

    def auto_tags(self, path: Path) -> Sequence[str]:
        """Return a sequence of automatic tags determined from the run properties."""
        return ()


@dataclass(frozen=True)
class CmdRun(Run):
    cmd: Command

    def build_targets(self) -> Iterable[Target]:
        return self.cmd.required_targets()

    def command(self, run_path: Path) -> Command:
        return self.cmd


@dataclass(frozen=True)
class ConvertRun(Run):
    preset: str
    namelist: str

    @property
    def target(self) -> Target:
        return Target(preset=self.preset, name="model1d_to_music")

    def build_targets(self) -> Iterable[Target]:
        yield self.target

    def command(self, run_path: Path) -> Command:
        return BareCmd(
            exe=self.target,
            args=(self.namelist,),
        )


@dataclass(frozen=True)
class MusicRun(Run):
    """A (serial or parallel) run of MUSIC.

    The number of cores to run on is obtained from the namelist.
    """

    preset: str
    namelist: NmlFile
    skip_self_tests: Optional[bool] = None
    skip_self_tests_dflt: ClassVar[bool] = True

    def __post_init__(self) -> None:
        if self.skip_self_tests is None:
            object.__setattr__(self, "skip_self_tests", self.skip_self_tests_dflt)

    def nml_in(self, path: Path) -> MusicNamelist:
        return self.namelist.read_in(path)

    @property
    def target(self) -> Target:
        return Target(preset=self.preset, name="music")

    def build_targets(self) -> Iterable[Target]:
        yield self.target

    def command(self, run_path: Path) -> Command:
        nml_file = str(self.namelist.path_in(run_path).relative_to(run_path))
        args = [nml_file]
        if self.skip_self_tests:
            args.append("--skip-self-tests")
        return MpiCmd(
            nprocs=self.nml_in(run_path).num_procs,
            cmd=BareCmd(exe=self.target, args=args),
        )

    def setup_run_dir(self, dst_path: Path) -> None:
        self.namelist.ensure_present_in(dst_path)
        # Create directory for output files; important otherwise MUSIC crashes weirdly
        output = self.nml_in(dst_path).get("io", "dataoutput", "")
        if "/" in output:
            output_dir = output.rsplit("/", 1)[0]
            (dst_path / output_dir).mkdir(exist_ok=True, parents=True)

    def auto_tags(self, path: Path) -> Sequence[str]:
        namelist = self.nml_in(path)

        tags = [
            "serial" if namelist.num_procs == 1 else "parallel",
            namelist.eos + "_eos",
        ]

        tags.extend(
            tag
            for predicate, tag in (
                (namelist.is_cartesian, "cart"),
                (namelist.nscalars > 0, "scalars"),
                (namelist.nactive_scalars > 0, "activescalars"),
                (namelist.has_rotation, "rot"),
                (namelist.mhd_enabled, "mhd"),
            )
            if predicate
        )

        # Gravity, mind the order of those, see gravitation.f90
        if namelist.gravity_file.strip() != "":
            tags.append("gravity_external")
        elif namelist.consistent_gravity:
            tags.append("gravity_from_hse")
        elif namelist.gravity < 0:
            tags.append("gravity_mass_shells")
        elif namelist.gravity > 0:
            tags.append("gravity_const")
        else:
            tags.append("gravity_none")

        return tags
