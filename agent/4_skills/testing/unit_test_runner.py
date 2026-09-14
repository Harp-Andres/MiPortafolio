"""
Unit Test Runner Skill - Run unit tests (Vitest + PyTest).

Executes unit tests for both frontend (Vitest) and backend (PyTest).
Generates test reports and coverage metrics.

Expected Input:
    {
        "workspace_root": str,
        "watch_mode": bool (default: False),
        "update_snapshots": bool (default: False)
    }

Returns:
    {
        "status": "success" | "failed",
        "frontend_tests": int,
        "frontend_passed": int,
        "frontend_failed": int,
        "backend_tests": int,
        "backend_passed": int,
        "backend_failed": int,
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
from agent.utils.parsers import CentralizedParser, VitestParser, PyTestParser


logger = get_logger(__name__)


class UnitTestRunner(BaseSkill):
    """Run unit tests (Vitest + PyTest).

    This skill:
    1. Runs Vitest for frontend unit tests
    2. Runs PyTest for backend unit tests
    3. Aggregates results
    4. Generates reports
    """

    def __init__(self, workspace_root: str):
        """Initialize UnitTestRunner.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "UnitTestRunner"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Run unit tests.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with test results.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting unit tests",
                extra={"workspace": str(self.workspace_root)},
            )

            params = request.parameters
            watch_mode = params.get("watch_mode", skill_defaults.WATCH_MODE)
            update_snapshots = params.get("update_snapshots", skill_defaults.UPDATE_SNAPSHOTS)

            with Timer(metrics, "unit_tests_total_ms"):
                # Frontend tests
                fe_results = await self._run_vitest(
                    watch_mode=watch_mode,
                    update_snapshots=update_snapshots,
                )

                # Backend tests
                be_results = await self._run_pytest(
                    watch_mode=watch_mode,
                )

            duration = (datetime.now() - start_time).total_seconds() * 1000
            total_failed = fe_results["failed"] + be_results["failed"]
            status = SkillStatus.SUCCESS if total_failed == 0 else SkillStatus.FAILED

            logger.info(
                f"[{self.skill_name}] Unit tests completed",
                extra={
                    "frontend_passed": fe_results["passed"],
                    "frontend_failed": fe_results["failed"],
                    "backend_passed": be_results["passed"],
                    "backend_failed": be_results["failed"],
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=status,
                output={
                    "frontend_tests": fe_results["total"],
                    "frontend_passed": fe_results["passed"],
                    "frontend_failed": fe_results["failed"],
                    "backend_tests": be_results["total"],
                    "backend_passed": be_results["passed"],
                    "backend_failed": be_results["failed"],
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Unit tests failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _run_vitest(
        self,
        watch_mode: bool = False,
        update_snapshots: bool = False,
    ) -> dict:
        """Run Vitest for frontend.

        Args:
            watch_mode: Run in watch mode.
            update_snapshots: Update snapshots.

        Returns:
            Test results dict.
        """
        logger.debug(f"[{self.skill_name}] Running Vitest")
        
        package_json = self.workspace_root / "package.json"
        if not package_json.exists():
            logger.warning(f"[{self.skill_name}] package.json not found, skipping Vitest")
            return {"total": 0, "passed": 0, "failed": 0}
        
        try:
            # Validate file path for security
            self.security_filter.validate_file_operation(str(package_json), "read")
            
            cmd = ["npm", "run", "test:unit"]
            if watch_mode:
                cmd = ["npm", "run", "test:unit", "--", "--watch"]
            if update_snapshots:
                cmd.extend(["--", "-u"])
            
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="vitest execution",
                capture_errors=True
            )
            
            report_path = self.workspace_root / "coverage" / "vitest-report.json"
            if report_path.exists():
                test_results = CentralizedParser.parse_test_results("vitest", report_path)
            else:
                test_results = VitestParser.parse_output(result)
            
            logger.info(
                f"[{self.skill_name}] Vitest completed",
                extra=test_results
            )
            return test_results
            
        except Exception as e:
            logger.error(f"[{self.skill_name}] Vitest failed", exc_info=True)
            return {"total": 0, "passed": 0, "failed": 0}

    async def _run_pytest(self, watch_mode: bool = False) -> dict:
        """Run PyTest for backend.

        Args:
            watch_mode: Run in watch mode (ignored for PyTest).

        Returns:
            Test results dict.
        """
        logger.debug(f"[{self.skill_name}] Running PyTest")
        
        if not self._verify_tools("pytest"):
            logger.warning(f"[{self.skill_name}] pytest not found, skipping PyTest")
            return {"total": 0, "passed": 0, "failed": 0}
        
        try:
            test_files = list(self.workspace_root.glob("**/test_*.py")) + \
                        list(self.workspace_root.glob("**/*_test.py"))
            test_files = [f for f in test_files 
                         if not any(part in f.parts for part in ['.venv', 'venv', 'node_modules', '.git', '__pycache__', 'dist', 'build'])]
            
            if not test_files:
                logger.debug(f"[{self.skill_name}] No pytest test files found")
                return {"total": 0, "passed": 0, "failed": 0}
            
            cmd = ["pytest", "--json-report", "--json-report-file=report.json", "-v", "--tb=short"]
            test_dir = "tests" if (self.workspace_root / "tests").exists() else "test"
            if (self.workspace_root / test_dir).exists():
                cmd.append(test_dir)
            else:
                cmd.append(".")
            
            # Validate subprocess command for security
            cmd = self.security_filter.validate_subprocess_command(cmd)
            
            result = await self._run_command(
                cmd,
                cwd=str(self.workspace_root),
                description="pytest execution",
                capture_errors=True
            )
            
            report_path = self.workspace_root / "report.json"
            if report_path.exists():
                test_results = CentralizedParser.parse_test_results("pytest", report_path)
            else:
                test_results = PyTestParser.parse_output(result)
            
            logger.info(f"[{self.skill_name}] PyTest completed", extra=test_results)
            return test_results
            
        except Exception as e:
            logger.error(f"[{self.skill_name}] PyTest failed", exc_info=True)
            return {"total": 0, "passed": 0, "failed": 0}


__all__ = ["UnitTestRunner"]
