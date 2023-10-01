from __future__ import annotations

import operator
import subprocess
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from music_pykg.prof1d import Prof1d

from .term import err_msg, info_msg
from .validation import ValidationResult

if typing.TYPE_CHECKING:
    from typing import Callable, Mapping, Optional, Sequence

    from numpy.typing import ArrayLike

    from .dumps import FileDump


class ComparisonCheck(ABC):
    @abstractmethod
    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        raise NotImplementedError()

    def __and__(self, other: ComparisonCheck) -> ComparisonCheck:
        return CombinedComparisonCheck(self, other, operator.and_)

    def __or__(self, other: ComparisonCheck) -> ComparisonCheck:
        return CombinedComparisonCheck(self, other, operator.or_)


@dataclass(frozen=True)
class CombinedComparisonCheck(ComparisonCheck):
    comp1: ComparisonCheck
    comp2: ComparisonCheck
    binary_op: Callable

    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        return self.binary_op(
            self.comp1.compare_run_to_ref(music_dir, run_dir, ref_dir),
            self.comp2.compare_run_to_ref(music_dir, run_dir, ref_dir),
        )


@dataclass(frozen=True)
class _DictComparison:
    atol: float = 1e-13
    rtol: float = 1e-13

    def _allclose(
        self, a: Optional[ArrayLike], b: Optional[ArrayLike]
    ) -> ValidationResult:
        """a is current run, b is reference"""
        if a is None or b is None:
            if a is b:
                return ValidationResult(True)
            return ValidationResult(
                False,
                message=err_msg(f"a is {a!r}, b is {b!r}"),
            )
        a, b = np.atleast_1d(a, b)
        assert np.shape(a) == np.shape(b)
        delta = np.abs(a - b)
        mag = 0.5 * (np.abs(a) + np.abs(b))
        delta_max = self.atol + mag * self.rtol
        discr = delta / delta_max
        allclose = np.all(discr <= 1.0)
        if not allclose:
            imax = np.unravel_index(np.argmax(discr), discr.shape)
            return ValidationResult(
                False,
                message=err_msg(
                    f"above tol: @argmax={imax} "
                    f"run={a[imax]:.15e} ref={b[imax]:.15e} "
                    f"discrepancy={discr[imax]:.2e}"
                ),
            )

        return ValidationResult(True)

    def approx_equal(
        self, d1: Mapping[str, ArrayLike], d2: Mapping[str, ArrayLike]
    ) -> ValidationResult:
        """d1 is current run, d2 is reference"""
        # Compare dictionary keys
        sk1, sk2 = set(d1.keys()), set(d2.keys())
        if sk1 != sk2:
            return ValidationResult(
                False,
                message=err_msg(
                    f"keys differ, run\\ref={sk1 - sk2}, ref\\run={sk2 - sk1}"
                ),
            )

        # Compare entries
        result = ValidationResult(True)
        for k in d1:
            result &= self._allclose(d1[k], d2[k]).with_header_msg(
                info_msg(f"Comparing entry '{k}': ")
            )

        return result


@dataclass(frozen=True)
class CompareDumps(ComparisonCheck):
    dump: FileDump
    atol: float = 1e-13
    rtol: float = 1e-13
    compare_headers: bool = True
    ignored_keys: Sequence[str] = ("dtn", "gamma", "ikap", "eos")

    def _drop(self, d: Mapping[str, ArrayLike]) -> Mapping[str, ArrayLike]:
        """Returns copy of dict d with ignored keys dropped"""
        return {k: v for k, v in d.items() if k not in self.ignored_keys}

    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        dump_run = self.dump.with_path(Path(run_dir))
        dump_ref = self.dump.with_path(Path(ref_dir))

        header_run, data_run = dump_run.header_and_data()
        header_ref, data_ref = dump_ref.header_and_data()

        compare = _DictComparison(self.atol, self.rtol)

        if self.compare_headers:
            result = compare.approx_equal(
                self._drop(header_run), self._drop(header_ref)
            )
        else:
            result = ValidationResult(True)

        result &= compare.approx_equal(self._drop(data_run), self._drop(data_ref))
        return result.with_header_msg(
            info_msg(
                f"CompareDumps: run='{dump_run.full_filename}' ref='{dump_ref.full_filename}'"
            )
        )


@dataclass(frozen=True)
class CompareProf1d(ComparisonCheck):
    filename: str
    atol: float = 1e-13
    rtol: float = 1e-13

    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        p1d_run = Prof1d(run_dir / self.filename)
        p1d_ref = Prof1d(ref_dir / self.filename)

        compare = _DictComparison(self.atol, self.rtol)

        result = compare.approx_equal(
            p1d_run.params, p1d_ref.params
        ) & compare.approx_equal(p1d_run.profs, p1d_ref.profs)
        return result.with_header_msg(
            info_msg(f"CompareProf1d: run='{p1d_run.path}' ref='{p1d_ref.path}'")
        )


@dataclass(frozen=True)
class CustomToolComparison(ComparisonCheck):
    """Compares two files using an external tool.

    Will invoke {tool_command} {tool_args} {run_file} {ref_file}
    and check the return code; 0 will pass the comparison, any other will fail.
    """

    tool_command: str
    file_name: str
    tool_args: Sequence[str] = tuple()

    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        tool_cmd = Path(music_dir) / self.tool_command
        file_run = Path(run_dir) / self.file_name
        file_ref = Path(ref_dir) / self.file_name

        cmd = (
            [tool_cmd]
            + list(self.tool_args)
            + [
                file_run,
                file_ref,
            ]
        )
        cmd = [str(c) for c in cmd]
        try:
            subprocess.check_call(cmd)
        except Exception as err:
            return ValidationResult(
                False, message=err_msg(f"external tool comparison failed: {err}")
            )

        return ValidationResult(True)
