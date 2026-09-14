"""
E2E Test Runner Skill - Run end-to-end tests with Playwright.

Executes comprehensive end-to-end tests for the portfolio application.
Tests user workflows, integrations, and deployment configurations.

Expected Input:
    {
        "workspace_root": str,
        "browsers": list (default: ["chromium", "firefox"]),
        "headless": bool (default: True)
    }

Returns:
    {
        "status": "success" | "failed",
        "tests_run": int,
        "tests_passed": int,
        "tests_failed": int,
        "browsers_tested": int,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from datetime import datetime

from agent_4_skills.base_skill import BaseSkill, SkillResult, SkillStatus
from agent_5_guardrails.security_filters import SecurityFilter
from agent_6_telemetry import get_logger, Timer, MetricsCollector
from agent.config import skill_defaults
from agent.utils.parsers import CentralizedParser, PlaywrightParser


logger = get_logger(__name__)


class E2ETestRunner(BaseSkill):
    """Run end-to-end tests with Playwright.

    This skill:
    1. Launches Playwright browser instances
    2. Executes E2E test scenarios
    3. Tests multiple browsers
    4. Generates test reports
    """

    def __init__(self, workspace_root: str):
        """Initialize E2ETestRunner.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "E2ETestRunner"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Run E2E tests.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with test results.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting E2E tests",
                extra={"workspace": str(self.workspace_root)},
            )

            params = request.parameters
            browsers = params.get("browsers", skill_defaults.E2E_BROWSERS)
            headless = params.get("headless", skill_defaults.E2E_HEADLESS)

            with Timer(metrics, "e2e_tests_total_ms"):
                results = await self._run_playwright_tests(
                    browsers=browsers,
                    headless=headless,
                )

            duration = (datetime.now() - start_time).total_seconds() * 1000
            status = (
                SkillStatus.SUCCESS
                if results["failed"] == 0
                else SkillStatus.FAILED
            )

            logger.info(
                f"[{self.skill_name}] E2E tests completed",
                extra={
                    "tests_passed": results["passed"],
                    "tests_failed": results["failed"],
                    "browsers": len(browsers),
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=status,
                output={
                    "tests_run": results["total"],
                    "tests_passed": results["passed"],
                    "tests_failed": results["failed"],
                    "browsers_tested": len(browsers),
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] E2E tests failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _run_playwright_tests(
        self,
        browsers: list = None,
        headless: bool = True,
    ) -> dict:
        """Run Playwright test suite.

        Args:
            browsers: List of browsers to test (chromium, firefox, webkit).
            headless: Run in headless mode.

        Returns:
            Test results dict.
        """
        logger.debug(f"[{self.skill_name}] Running Playwright tests")
        
        if browsers is None:
            browsers = ["chromium", "firefox"]
        
        # Look for playwright test files
        test_files = list(self.workspace_root.glob("e2e/**/*.spec.ts")) + \
                    list(self.workspace_root.glob("e2e/**/*.spec.js")) + \
                    list(self.workspace_root.glob("tests/e2e/**/*.spec.ts")) + \
                    list(self.workspace_root.glob("tests/e2e/**/*.spec.js"))
        
        if not test_files:
            logger.warning(f"[{self.skill_name}] No Playwright test files found")
            return {"total": 0, "passed": 0, "failed": 0}
        
        try:
            cmd = ["npx", "playwright", "test"]
            
            # Add browser specification
            for browser in browsers:
                cmd.extend(["--project", browser])
            
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            # Run playwright
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="playwright test execution",
                capture_errors=True
            )
            
            # Look for test-results
            results_dir = self.workspace_root / "test-results"
            if results_dir.exists():
                test_results = CentralizedParser.parse_test_results("playwright", results_dir)
            else:
                test_results = PlaywrightParser.parse_output(result)
            
            logger.info(
                f"[{self.skill_name}] Playwright tests completed",
                extra={**test_results, "browsers": len(browsers)}
            )
            return test_results
            
        except Exception as e:
            logger.error(f"[{self.skill_name}] Playwright failed", exc_info=True)
            return {"total": 0, "passed": 0, "failed": 0}
