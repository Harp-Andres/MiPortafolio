"""E2E Test Runner - runs Playwright end-to-end tests."""

import logging
from pathlib import Path

import importlib.util as _ilu
_bs = _ilu.spec_from_file_location('_base_skill', Path(__file__).parent.parent / 'base_skill.py')
_bsm = _ilu.module_from_spec(_bs)
_bs.loader.exec_module(_bsm)
BaseSkill = _bsm.BaseSkill
SkillRequest = _bsm.SkillRequest

logger = logging.getLogger(__name__)


class E2ETestRunner(BaseSkill):
    """Run end-to-end tests with Playwright."""

    SKILL_NAME = "E2ETestRunner"
    SKILL_DESCRIPTION = "Runs Playwright E2E tests against the web app"

    async def _run_implementation(self, request: SkillRequest) -> str:
        """Run E2E tests.

        Args:
            request: SkillRequest with parameters.

        Returns:
            String with E2E test results.
        """
        workspace = self.workspace_root
        web_dir = workspace / "apps" / "web"

        if not web_dir.exists():
            return "E2E tests: No apps/web directory found, skipping"

        try:
            if not self.has_tool("pnpm"):
                return "E2E tests: pnpm not found, skipping"

            result = self._run_command(
                ["pnpm", "--filter", "web", "playwright", "test", "--reporter=list"],
                timeout=180,
                cwd=workspace,
            )

            output = (result.stdout or "") + (result.stderr or "")
            if result.returncode != 0:
                logger.warning(f"E2E tests had issues (exit {result.returncode})")
                return f"E2E tests completed with status {result.returncode}"

            return "E2E tests passed successfully"
        except FileNotFoundError:
            return "E2E tests: pnpm not available, skipping"
        except Exception as e:
            logger.error(f"E2E test error: {e}", exc_info=True)
            raise
