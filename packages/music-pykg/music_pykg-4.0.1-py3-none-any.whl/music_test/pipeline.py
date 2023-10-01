from __future__ import annotations

import filecmp
import shutil
import traceback
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

from .term import (
    TERMCOLOR_BLUE,
    TERMCOLOR_DEFAULT,
    TERMCOLOR_GREEN,
    TERMCOLOR_RED,
    TERMCOLOR_YELLOW,
    Chars,
    CharsBase,
    CharsWithAsciiAlternate,
    Message,
    NullMsg,
    StrMsg,
    TermBase,
    err_msg,
    warn_msg,
)
from .test import ConcreteTest
from .utils import Timer

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Dict, Optional, Sequence, Tuple

    from .cmake_builder import BuildOutcome
    from .dirs import BuildsDirectory, TestsOutputDirectory


@dataclass(frozen=True, eq=True)
class Outcome:
    label: str
    symbol: str
    ascii_symbol: str
    termcolor: str
    stops_pipeline: bool
    changed: bool
    is_failure: bool

    @property
    def char(self) -> CharsWithAsciiAlternate:
        return CharsWithAsciiAlternate(
            self.symbol,
            self.ascii_symbol,
            self.termcolor,
        )


PASS = Outcome(
    label="Passed",
    symbol="✔",
    ascii_symbol=".",
    termcolor=TERMCOLOR_GREEN,
    stops_pipeline=False,
    changed=True,
    is_failure=False,
)

REUSE = Outcome(
    label="Reused",
    symbol="♻",
    ascii_symbol="o",
    termcolor=TERMCOLOR_BLUE,
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

FAIL = Outcome(
    label="Failed",
    symbol="✗",
    ascii_symbol="!",
    termcolor=TERMCOLOR_RED,
    stops_pipeline=True,
    changed=True,
    is_failure=True,
)

SKIP = Outcome(
    label="Skipped",
    symbol="⮞",
    ascii_symbol=">",
    termcolor=TERMCOLOR_YELLOW,
    stops_pipeline=True,
    changed=False,
    is_failure=False,
)

NA = Outcome(
    label="N/A",
    symbol="-",
    ascii_symbol="-",
    termcolor=TERMCOLOR_DEFAULT,
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

ALL_OUTCOMES = [PASS, REUSE, FAIL, SKIP, NA]


class TestsTally:
    def __init__(self, tests: Sequence[ConcreteTest], stages: Sequence[str]):
        self.tests = tests
        self.stages = stages

        self._outcomes: Dict[ConcreteTest, Dict[str, Outcome]] = {
            t: {} for t in tests
        }  # outcome[test][stage]

    def register(self, test: ConcreteTest, stage: str, outcome: Outcome) -> None:
        assert stage in self.stages
        assert stage not in self._outcomes[test]
        self._outcomes[test][stage] = outcome

    def _finalize_matrix(self) -> None:
        for test in self.tests:
            for i, stage in enumerate(self.stages):
                if stage not in self._outcomes[test]:
                    assert i > 0
                    prev_outcome = self._outcomes[test][self.stages[i - 1]]
                    assert prev_outcome.stops_pipeline
                    self._outcomes[test][stage] = SKIP

    def print_report_to(self, term: TermBase, print_key: bool = True) -> None:
        self._finalize_matrix()
        cols: Sequence[CharsBase] = [Chars(f"{' ':40}")] + [
            Chars(f"{stage:^13s}") for stage in self.stages
        ]
        term.print_line_of_chars(cols)
        sym_pad = Chars((13 - 1) // 2 * " ")
        for test in self.tests:
            cols = [Chars(f"{test.name:40}")]
            for stage in self.stages:
                cols += [sym_pad, self._outcomes[test][stage].char, sym_pad]
            term.print_line_of_chars(cols)

        if print_key:
            term.print_line("\nKey:")
            for outcome in ALL_OUTCOMES:
                term.print_line_of_chars(
                    [outcome.char, Chars(f" : {outcome.label}")], indent=1
                )

    def count_failures(self) -> int:
        """Count number of tests that have at least one failure in their pipeline"""
        self._finalize_matrix()
        return sum(
            any(self._outcomes[test][stage].is_failure for stage in self.stages)
            for test in self.tests
        )

    @property
    def num_tests(self) -> int:
        return len(self.tests)


@dataclass(frozen=True)
class StageResult:
    outcome: Outcome
    message: Message = NullMsg()
    timing: Optional[float] = None

    @property
    def stops_pipeline(self) -> bool:
        return self.outcome.stops_pipeline

    @property
    def is_failure(self) -> bool:
        return self.outcome.is_failure

    @property
    def changed(self) -> bool:
        return self.outcome.changed

    def log_to(self, term: TermBase, header: str, indent: int = 0) -> None:
        timer_str = f" [{self.timing:.2f} s]" if self.timing is not None else ""
        StrMsg(
            f"{self.outcome.label}{timer_str}: {header}",
            termcolor=self.outcome.termcolor,
        ).print_to(term, indent)
        self.message.print_to(term, indent + 1)


@dataclass(frozen=True)
class PipelineByTest:
    stages: Sequence[PipelineStage]

    def process(self, tests: Sequence[ConcreteTest], term: TermBase) -> TestsTally:
        tally = TestsTally(tests, [stage.describe() for stage in self.stages])
        # Loop over tests
        for test in tests:
            StrMsg(f"Test={test.name}").print_to(term, 1)

            # Loop over stages for this test
            force_downstream_update = False
            for stage in self.stages:
                try:
                    result = stage.execute(test, force_downstream_update)
                except Exception:
                    result = StageResult(
                        FAIL,
                        err_msg(
                            "Unexpected error! The following exception was raised:",
                            *traceback.format_exc().splitlines(),
                        ),
                    )
                force_downstream_update = result.changed
                tally.register(test, stage.describe(), result.outcome)
                result.log_to(term, f"{stage.describe()}({test.name})", indent=2)
                if result.stops_pipeline:
                    break  # Break from pipeline stage loop

        return tally


class PipelineStage(ABC):
    @abstractmethod
    def describe(self) -> str:
        """Short description of the stage."""

    @abstractmethod
    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        raise NotImplementedError


def _same_file_contents(path1: Path, path2: Path) -> bool:
    return path1.is_file() and path2.is_file() and filecmp.cmp(path1, path2)


@dataclass(frozen=True)
class PrepStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory
    build_outcome: BuildOutcome
    reuse_if_ready: bool

    def describe(self) -> str:
        return "Preparation"

    @cached_property
    def builds_dir(self) -> BuildsDirectory:
        return self.tests_out_dir.builds_directory

    def _files_out_of_date(self, test: ConcreteTest) -> Sequence[Tuple[Path, Path]]:
        # files from the test configuration directory
        required_files = [file for file in test.path.iterdir() if file.is_file()]
        # build targets
        required_files.extend(
            self.builds_dir.target_path(tgt) for tgt in test.build_targets()
        )

        run_path = self.tests_out_dir.run_path(test)
        return [
            (file, out_file)
            for file in required_files
            if not _same_file_contents(file, out_file := run_path / file.name)
        ]

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if not test.build_targets() <= self.build_outcome.built_targets:
            return StageResult(FAIL)

        run_path = self.tests_out_dir.run_path(test)
        if not self.reuse_if_ready:
            shutil.rmtree(run_path, ignore_errors=True)

        run_path.mkdir(parents=True, exist_ok=True)

        files_to_copy = self._files_out_of_date(test)
        if self.reuse_if_ready and not files_to_copy:
            return StageResult(REUSE)

        for file1, file2 in files_to_copy:
            shutil.copy(file1, file2)

        # additional setup defined by the test itself
        test.setup_dir_for_run(run_path)

        return StageResult(PASS)


@dataclass(frozen=True)
class RunStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory
    reuse_if_ready: bool
    verbose: bool

    def describe(self) -> str:
        return "Run"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        run_dir = self.tests_out_dir.test_run_directory(test)
        attempt_reuse = (not force_exec) and self.reuse_if_ready

        if attempt_reuse and run_dir.is_ready():
            return StageResult(REUSE)

        return run_dir.run(verbose=self.verbose)


@dataclass(frozen=True)
class SelfCheckStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Self-check"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if test.self_check is None:
            return StageResult(NA)

        timer = Timer()
        run_path = self.tests_out_dir.run_path(test)
        result = test.self_check.check_run(run_path)
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())


@dataclass(frozen=True)
class CompareStage(PipelineStage):
    music_dir: Path
    tests_out_dir: TestsOutputDirectory
    ref_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Comparison"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if test.comparison_check is None:  # Test prescribes no comparison
            return StageResult(NA)

        ref_run_dir = self.ref_dir.test_run_directory(test)
        if not ref_run_dir.is_ready():  # No matching run in ref output dir
            return StageResult(
                SKIP,
                message=warn_msg(
                    f"reference run directory '{ref_run_dir.path}' not found"
                ),
            )

        timer = Timer()
        run_path = self.tests_out_dir.run_path(test)
        result = test.comparison_check.compare_run_to_ref(
            self.music_dir, run_path, ref_run_dir.path
        )
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())
