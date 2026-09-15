"""Unit Test Runner - runs Vitest (frontend) and PyTest (backend)."""

import logging
from pathlib import Path

import importlib.util as _ilu, sys as _sys; _bs = _ilu.spec_from_file_location('_base_skill', __import__('pathlib').Path(__file__).parent.parent / 'base_skill.py'); _bsm = _ilu.module_from_spec(_bs); _bs.loader.exec_module(_bsm); BaseSkill = _bsm.BaseSkill; SkillRequest = _bsm.SkillRequest; SkillResult = _bsm.SkillResult; SkillStatus = _bsm.SkillStatus; skill_wrapper = _bsm.skill_wrapper

logger = logging.getLogger(__name__)


class UnitTestRunner(BaseSkill):
    SKILL_NAME = "UnitTestRunner"
    SKILL_DESCRIPTION = "Runs Vitest (web) and PyTest (api) unit tests"

    async def _run_implementation(self, request: SkillRequest) -> str:
        workspace = self.workspace_root
        lines: list[str] = []
        errors: list[str] = []

        # Frontend: pnpm test --run
        web_dir = workspace / "apps" / "web"
        if web_dir.exists():
            result = self._run_command(
                ["pnpm", "--filter", "web", "test", "--run"],
                timeout=120,
                cwd=workspace,
            )
            lines.append("=== Frontend (Vitest) ===")
            lines.append(result.stdout or "")
            if result.returncode != 0:
                errors.append(f"Frontend tests failed (exit {result.returncode})")
                lines.append(result.stderr or "")

        # Backend: uv run pytest
        api_dir = workspace / "apps" / "api"
        if api_dir.exists():
            result = self._run_command(
                ["uv", "run", "pytest", "-v", "--tb=short"],
                timeout=120,
                cwd=api_dir,
            )
            lines.append("=== Backend (PyTest) ===")
            lines.append(result.stdout or "")
            if result.returncode != 0:
                errors.append(f"Backend tests failed (exit {result.returncode})")
                lines.append(result.stderr or "")

        if errors:
            raise RuntimeError("\n".join(errors))

        return "\n".join(lines)

