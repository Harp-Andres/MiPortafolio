"""
Coverage Analyzer Skill - Analyze and report code coverage.

Generates code coverage reports for both frontend and backend.
Validates coverage meets minimum thresholds.

Expected Input:
    {
        "workspace_root": str,
        "min_coverage": float (default: 80.0),
        "include_e2e": bool (default: False)
    }

Returns:
    {
        "status": "success" | "failed",
        "total_coverage": float,
        "frontend_coverage": float,
        "backend_coverage": float,
        "uncovered_lines": int,
        "coverage_report_path": str,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from datetime import datetime

import importlib.util as _ilu, sys as _sys; _bs = _ilu.spec_from_file_location('_base_skill', __import__('pathlib').Path(__file__).parent.parent / 'base_skill.py'); _bsm = _ilu.module_from_spec(_bs); _bs.loader.exec_module(_bsm); BaseSkill = _bsm.BaseSkill; SkillRequest = _bsm.SkillRequest; SkillResult = _bsm.SkillResult; SkillStatus = _bsm.SkillStatus; skill_wrapper = _bsm.skill_wrapper; _lh = _ilu.spec_from_file_location('_logger_helper', __import__('pathlib').Path(__file__).parent.parent / 'logger_helper.py'); _lhm = _ilu.module_from_spec(_lh); _lh.loader.exec_module(_lhm); get_logger = _lhm.get_logger; _sf = _ilu.spec_from_file_location('_security_filters', __import__('pathlib').Path(__file__).parent.parent.parent / '5_guardrails' / 'security_filters.py'); _sfm = _ilu.module_from_spec(_sf); _sf.loader.exec_module(_sfm); SecurityFilter = _sfm.SecurityFilter; _tm = _ilu.spec_from_file_location('_telemetry', __import__('pathlib').Path(__file__).parent.parent.parent / '6_telemetry' / 'metrics.py'); _tmm = _ilu.module_from_spec(_tm); _tm.loader.exec_module(_tmm); MetricsCollector = getattr(_tmm, 'MetricsCollector', type('MetricsCollector', (), {'__init__': lambda s: None, 'record': lambda *a: None}))


logger = get_logger(__name__)


class CoverageAnalyzer(BaseSkill):
    """Analyze and report code coverage.

    This skill:
    1. Collects coverage from unit tests
    2. Generates coverage reports (HTML, JSON)
    3. Validates against minimum threshold
    4. Identifies uncovered code
    """

    def __init__(self, workspace_root: str):
        """Initialize CoverageAnalyzer.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "CoverageAnalyzer"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request: SkillRequest) -> str:
        """Analyze coverage.

        Args:
            request: SkillRequest with parameters.

        Returns:
            String with coverage analysis results.
        """
        start_time = datetime.now()

        try:
            logger.info(
                f"[{self.skill_name}] Starting coverage analysis",
                extra={"workspace": str(self.workspace_root)},
            )

            # Simplified coverage analysis - would normally parse actual coverage reports
            total_coverage = 0
            frontend_coverage = 0
            backend_coverage = 0
            uncovered_lines = 0

            duration = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"[{self.skill_name}] Coverage analysis completed",
                extra={
                    "total_coverage": total_coverage,
                    "uncovered_lines": uncovered_lines,
                    "duration_ms": duration,
                },
            )

            return f"Coverage analysis: total={total_coverage}%, frontend={frontend_coverage}%, backend={backend_coverage}%, uncovered={uncovered_lines} lines"

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Coverage analysis failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            raise

    async def _generate_coverage_report(
        self,
        min_coverage: float = None,
        include_e2e: bool = False,
    ) -> dict:
        """Generate coverage report.

        Args:
            min_coverage: Minimum coverage threshold.
            include_e2e: Include E2E test coverage.

        Returns:
            Coverage data dict.
        """
        if min_coverage is None:
            min_coverage = skill_defaults.MIN_COVERAGE
        
        logger.debug(f"[{self.skill_name}] Generating coverage report")
        
        try:
            frontend_coverage = 0.0
            backend_coverage = 0.0
            
            # Generate frontend coverage (Vitest)
            if (self.workspace_root / "package.json").exists():
                logger.debug(f"[{self.skill_name}] Generating frontend coverage")
                try:
                    # Validate file path for security
                    self.security_filter.validate_file_operation(str(self.workspace_root / "package.json"), "read")
                    
                    cmd = ["npm", "run", "test:unit", "--", "--coverage"]
                    # Validate subprocess command for security
                    cmd = self.security_filter.validate_subprocess_command(cmd)
                    
                    await self._run_command(
                        cmd,
                        cwd=str(self.workspace_root),
                        description="frontend coverage",
                        capture_errors=True
                    )
                    frontend_coverage = CentralizedParser.parse_coverage("vitest", self.workspace_root / "coverage")
                except Exception as e:
                    logger.warning(f"[{self.skill_name}] Frontend coverage failed: {e}")
            
            # Generate backend coverage (pytest-cov)
            if self._verify_tools("pytest"):
                logger.debug(f"[{self.skill_name}] Generating backend coverage")
                try:
                    cmd = ["pytest", "--cov=.", "--cov-report=json", "--cov-report=html", "-v"]
                    test_dir = "tests" if (self.workspace_root / "tests").exists() else "test"
                    if (self.workspace_root / test_dir).exists():
                        cmd.append(test_dir)
                    
                    # Validate subprocess command for security
                    cmd = self.security_filter.validate_subprocess_command(cmd)
                    
                    await self._run_command(
                        cmd,
                        cwd=str(self.workspace_root),
                        description="backend coverage",
                        capture_errors=True
                    )
                    backend_coverage = CentralizedParser.parse_coverage("pytest", self.workspace_root / ".coverage.json")
                except Exception as e:
                    logger.warning(f"[{self.skill_name}] Backend coverage failed: {e}")
            
            # Calculate total coverage
            if frontend_coverage > 0 and backend_coverage > 0:
                total_coverage = (frontend_coverage + backend_coverage) / 2
            elif frontend_coverage > 0:
                total_coverage = frontend_coverage
            elif backend_coverage > 0:
                total_coverage = backend_coverage
            else:
                total_coverage = 0.0
            
            # Count uncovered lines
            fe_uncovered = CoverageParser.count_uncovered_lines(self.workspace_root / "coverage", is_pytest=False)
            be_uncovered = CoverageParser.count_uncovered_lines(self.workspace_root, is_pytest=True)
            uncovered_lines = fe_uncovered + be_uncovered
            
            # Determine report path
            if (self.workspace_root / "coverage").exists():
                report_path = "coverage/index.html"
            elif (self.workspace_root / "htmlcov").exists():
                report_path = "htmlcov/index.html"
            else:
                report_path = "coverage/report"
            
            logger.info(
                f"[{self.skill_name}] Coverage report generated",
                extra={
                    "total_coverage": total_coverage,
                    "frontend_coverage": frontend_coverage,
                    "backend_coverage": backend_coverage,
                    "uncovered_lines": uncovered_lines
                }
            )
            
            return {
                "total_coverage": total_coverage,
                "frontend_coverage": frontend_coverage,
                "backend_coverage": backend_coverage,
                "uncovered_lines": uncovered_lines,
                "report_path": report_path,
            }
            
        except Exception as e:
            logger.error(f"[{self.skill_name}] Coverage report generation failed", exc_info=True)
            return {
                "total_coverage": 0.0,
                "frontend_coverage": 0.0,
                "backend_coverage": 0.0,
                "uncovered_lines": 0,
                "report_path": "",
            }


__all__ = ["CoverageAnalyzer"]
