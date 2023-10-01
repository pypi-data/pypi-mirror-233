from __future__ import annotations

import shutil
import subprocess
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from .pipeline import FAIL, PASS, StageResult
from .source_tree import MusicSourceTree
from .term import err_msg
from .test import ConcreteTest
from .utils import Timer, check_call_tee

if typing.TYPE_CHECKING:
    from .cmake_builder import Target


@dataclass(frozen=True)
class TestRunDirectory:
    test: ConcreteTest
    path: Path

    @property
    def _run_tag_path(self) -> Path:
        return self.path / "run_successful.tag"

    def is_ready(self) -> bool:
        return self._run_tag_path.is_file()

    def run(self, verbose: bool = False) -> StageResult:
        self._run_tag_path.unlink(missing_ok=True)

        # Run the test
        timer = Timer()
        run_log = self.path / self.test.run.log_filename
        with run_log.open("w") as run_log_file:
            try:
                check_call_tee(
                    self.test.run.command(self.path).build(),
                    run_log_file,
                    also_to_stdout=verbose,
                    cwd=self.path,
                )
            except subprocess.CalledProcessError as err:
                return StageResult(FAIL, message=err_msg(f"See {run_log}", str(err)))

        # Touch the run successful flag
        self._run_tag_path.touch()
        return StageResult(PASS, timing=timer.time())


@dataclass(frozen=True)
class BuildsDirectory:
    path: Path

    def preset_path(self, preset: str) -> Path:
        return self.path / preset

    def target_path(self, target: Target) -> Path:
        return self.preset_path(target.preset) / target.name


@dataclass(frozen=True)
class TestsOutputDirectory:
    music_tree: MusicSourceTree
    path: Path

    def prepare(self, wipe: bool = True) -> None:
        if wipe and self.path.is_dir():
            shutil.rmtree(self.path)
        self.builds_directory.path.mkdir(parents=True, exist_ok=True)

        # Capture VCS revision and diff
        self.music_tree.store_vcs_info(
            vcs_head_fname=self.path / "git_head.log",
            vcs_diff_fname=self.path / "git_diff.log",
        )

    @cached_property
    def builds_directory(self) -> BuildsDirectory:
        """Location of builds with given preset."""
        return BuildsDirectory(self.path / "builds")

    def run_path(self, test: ConcreteTest) -> Path:
        """Location of the run for a given path."""
        return self.path / "runs" / test.name

    def test_run_directory(self, test: ConcreteTest) -> TestRunDirectory:
        return TestRunDirectory(
            test=test,
            path=self.run_path(test),
        )
