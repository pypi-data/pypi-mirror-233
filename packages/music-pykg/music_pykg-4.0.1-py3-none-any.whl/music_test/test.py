from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Callable, FrozenSet, Optional, Tuple

    from .cmake_builder import Target
    from .comparison_checks import ComparisonCheck
    from .runs import Run
    from .self_checks import SelfCheck


@dataclass(frozen=True)
class Test:
    """A test to run"""

    preparation: Optional[Callable[[Path], None]]
    run: Run
    self_check: Optional[SelfCheck]
    comparison_check: Optional[ComparisonCheck]
    description: str
    tags: Tuple[str, ...]

    def build_targets(self) -> FrozenSet[Target]:
        return frozenset(self.run.build_targets())

    def with_name_and_path(self, name: str, path: Path) -> ConcreteTest:
        return ConcreteTest(
            preparation=self.preparation,
            run=self.run,
            self_check=self.self_check,
            comparison_check=self.comparison_check,
            description=self.description,
            tags=self.tags,
            name=name,
            path=path,
        )


@dataclass(frozen=True)
class ConcreteTest(Test):
    name: str
    path: Path

    def setup_dir_for_run(self, dst_path: Path) -> None:
        """Setup given path for this test's run"""
        if self.preparation is not None:
            self.preparation(dst_path)
        self.run.setup_run_dir(dst_path)
