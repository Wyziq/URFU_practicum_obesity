"""Smoke tests that ensure every Python module under ``src`` executes."""

from __future__ import annotations

import runpy
import sys
import unittest
from pathlib import Path
from typing import List

PROFILE_ROOT = Path(__file__).resolve().parents[1]
if str(PROFILE_ROOT) not in sys.path:
    sys.path.insert(0, str(PROFILE_ROOT))

from src import project_root


def _collect_modules() -> List[str]:
    src_dir = project_root() / "src"
    modules: List[str] = []
    for path in src_dir.glob("*.py"):
        if path.name == "__init__.py":
            continue
        modules.append(f"src.{path.stem}")
    return sorted(modules)


class TestModuleExecution(unittest.TestCase):
    def test_every_module_runs(self) -> None:
        modules = _collect_modules()
        self.assertTrue(
            modules,
            "В каталоге src не найдено ни одного python-модуля для тестирования.",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                runpy.run_module(module_name, run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    unittest.main()
