from __future__ import annotations

import operator
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from music_pykg.namelist import MusicNamelist
from music_pykg.prof1d import Prof1d

from .term import CollectedMsgs, Message, err_msg, info_msg
from .validation import ValidationResult

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import Callable, Mapping, Union

    from numpy.typing import ArrayLike, NDArray

    from .dumps import Dump, FileDump, MusicDumpH5
    from .utils import RelativePath


class SelfCheck(ABC):
    @abstractmethod
    def check_run(self, run_dir: Path) -> ValidationResult:
        raise NotImplementedError

    def __and__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.and_)

    def __or__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.or_)


@dataclass(frozen=True)
class CombinedSelfCheck(SelfCheck):
    check1: SelfCheck
    check2: SelfCheck
    binary_op: Callable[[ValidationResult, ValidationResult], ValidationResult]

    def check_run(self, run_dir: Path) -> ValidationResult:
        return self.binary_op(
            self.check1.check_run(run_dir), self.check2.check_run(run_dir)
        )


def _mapping_norm_msg(mapping: Mapping[str, ArrayLike]) -> Message:
    def norm_1(x: ArrayLike) -> np.number:
        return np.mean(np.abs(x))

    def norm_2(x: ArrayLike) -> np.number:
        return np.sqrt(np.mean(np.abs(x) ** 2))

    def norm_inf(x: ArrayLike) -> np.number:
        return np.max(np.abs(x))

    q = "'"
    return CollectedMsgs(
        [
            info_msg(
                f"norms({q + k + q:12s}): "
                f"L1={norm_1(v):.4e}, "
                f"L2={norm_2(v):.4e}, "
                f"Linf={norm_inf(v):.4e}"
            )
            for k, v in mapping.items()
        ],
    )


@dataclass(frozen=True)
class CheckAgainstRefDump(SelfCheck):
    dump1: Dump
    dump2: Dump

    @abstractmethod
    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool:
        raise NotImplementedError

    def check_run(self, run_dir: Path) -> ValidationResult:
        hdr1, data1 = self.dump1.with_path(run_dir).header_and_data()
        hdr2, data2 = self.dump2.with_path(run_dir).header_and_data()
        if data1.keys() != data2.keys():
            return ValidationResult(
                False,
                err_msg(
                    "Dumps hold different fields:",
                    "dump1: " + str(sorted(data1.keys())),
                    "dump2: " + str(sorted(data2.keys())),
                ),
            )
        fields_identical = all(
            self.array_comparison(fld1, data2[name]) for name, fld1 in data1.items()
        )
        if not fields_identical:
            _, diff = (self.dump1 - self.dump2).with_path(run_dir).header_and_data()
            return ValidationResult(False, _mapping_norm_msg(diff))
        ndim = data1["density"].ndim
        coords_identical = all(
            np.array_equal(hdr1[coord], hdr2[coord])
            for coord in map(lambda i: f"face_loc_{i}", range(1, ndim + 1))
        )
        if not coords_identical:
            diff = {
                coord: hdr1[coord] - hdr2[coord]
                for coord in map(lambda i: f"face_loc_{i}", range(1, ndim + 1))
            }
            return ValidationResult(False, _mapping_norm_msg(diff))
        return ValidationResult(
            True, info_msg("dumps are identical (fields and coord)")
        )


@dataclass(frozen=True)
class CheckWithPrecision(CheckAgainstRefDump):
    rtol: float = 1e-15
    atol: float = 1e-15

    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool:
        return np.allclose(arr1, arr2, rtol=self.rtol, atol=self.atol)


@dataclass(frozen=True)
class CheckBitIdentical(CheckAgainstRefDump):
    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool:
        return np.array_equal(arr1, arr2)


@dataclass(frozen=True)
class ReportNorms(SelfCheck):
    """Report norms of input dump object to log messages, always returning a successful status.

    NOTE: the norms are computed pointwise naively, i.e. they are seen as norms on data arrays,
    not as proper integral norms e.g. on the sphere.
    """

    dump: Dump
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        _, data = self.dump.with_path(run_dir).header_and_data()
        message = _mapping_norm_msg(data)

        return ValidationResult(True, message).with_header_msg(
            info_msg("ReportNorms" + (f"[{self.label}]" if self.label else "") + ":")
        )


@dataclass(frozen=True)
class ReportProf1dDiff(SelfCheck):
    """Report difference between two prof1d."""

    prof1d_left: str
    prof1d_right: str
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        p1dl = Prof1d(run_dir / self.prof1d_left)
        p1dr = Prof1d(run_dir / self.prof1d_right)

        params = {k: p1dl.params[k] - rval for k, rval in p1dr.params.items()}
        message = _mapping_norm_msg(params)
        result = ValidationResult(True, message).with_header_msg(
            info_msg(
                "ReportProf1dDiff-params"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )

        profs = p1dl.profs - p1dr.profs
        message = _mapping_norm_msg(profs)
        result &= ValidationResult(True, message).with_header_msg(
            info_msg(
                "ReportProf1dDiff-profs"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )
        return result


@dataclass(frozen=True)
class CheckTimeOfDump(SelfCheck):
    dump: FileDump
    time: float

    def check_run(self, run_dir: Path) -> ValidationResult:
        dump = self.dump.with_path(run_dir)
        header, _ = dump.header_and_data()
        t = header["time"]
        if not np.isclose(t, self.time):
            return ValidationResult(
                False,
                message=err_msg(
                    f"dump '{dump.full_filename}': expected time={self.time} but found {t}"
                ),
            )
        return ValidationResult(
            True,
            info_msg(
                f"dump '{dump.full_filename}': expected time={self.time}, found {t}"
            ),
        )
