"""
Test Aggregator Skill - Aggregate and report test results.

Combines results from unit tests, E2E tests, and coverage analysis.
Generates consolidated test report for deployment decisions.

Expected Input:
    {
        "workspace_root": str,
        "generate_html_report": bool (default: True)
    }

Returns:
    {
        "status": "success" | "failed",
        "total_tests": int,
        "total_passed": int,
        "total_failed": int,
        "skipped": int,
        "average_coverage": float,
        "report_path": str,
        "duration_ms": float
    }
"""

import asyncio
from pathlib import Path
from datetime import datetime

from agent_4_skills.base_skill import BaseSkill, SkillResult, SkillStatus
from agent_5_guardrails.security_filters import SecurityFilter
from agent_6_telemetry import get_logger, Timer, MetricsCollector
from agent.config import project_config, skill_defaults
from agent.utils.parsers import CentralizedParser, CoverageParser


logger = get_logger(__name__)


class TestAggregator(BaseSkill):
    """Aggregate test results from all test types.

    This skill:
    1. Reads test results from multiple sources
    2. Aggregates into unified report
    3. Generates HTML report
    4. Provides summary metrics
    """

    def __init__(self, workspace_root: str):
        """Initialize TestAggregator.

        Args:
            workspace_root: Root directory of the project.
        """
        super().__init__(workspace_root)
        self.skill_name = "TestAggregator"
        self.security_filter = SecurityFilter(workspace_root=workspace_root)

    async def _run_implementation(self, request) -> SkillResult:
        """Aggregate test results.

        Args:
            request: SkillRequest with parameters.

        Returns:
            SkillResult with aggregated results.
        """
        start_time = datetime.now()
        metrics = MetricsCollector()

        try:
            logger.info(
                f"[{self.skill_name}] Starting test aggregation",
                extra={"workspace": str(self.workspace_root)},
            )

            params = request.parameters
            generate_html = params.get("generate_html_report", skill_defaults.GENERATE_HTML_REPORT)

            with Timer(metrics, "test_aggregation_ms"):
                aggregated = await self._aggregate_results(
                    generate_html_report=generate_html,
                )

            duration = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"[{self.skill_name}] Test aggregation completed",
                extra={
                    "total_tests": aggregated["total_tests"],
                    "total_failed": aggregated["total_failed"],
                    "duration_ms": duration,
                },
            )

            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.SUCCESS,
                output={
                    "total_tests": aggregated["total_tests"],
                    "total_passed": aggregated["total_passed"],
                    "total_failed": aggregated["total_failed"],
                    "skipped": aggregated["skipped"],
                    "average_coverage": aggregated["avg_coverage"],
                    "report_path": aggregated["report_path"],
                    "duration_ms": duration,
                },
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(
                f"[{self.skill_name}] Test aggregation failed",
                extra={"error": str(e), "duration_ms": duration},
                exc_info=True,
            )
            return SkillResult(
                skill_name=self.skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                output={"duration_ms": duration},
            )

    async def _aggregate_results(self, generate_html_report: bool = True) -> dict:
        """Aggregate results from all test types.

        Args:
            generate_html_report: Generate HTML report.

        Returns:
            Aggregated results dict.
        """
        logger.debug(f"[{self.skill_name}] Aggregating test results")
        
        try:
            # Collect results from various sources
            unit_tests = self._read_unit_test_results()
            e2e_tests = self._read_e2e_test_results()
            coverage_data = self._read_coverage_data()
            
            # Aggregate counts
            total_tests = unit_tests["total"] + e2e_tests["total"]
            total_passed = unit_tests["passed"] + e2e_tests["passed"]
            total_failed = unit_tests["failed"] + e2e_tests["failed"]
            skipped = unit_tests.get("skipped", 0) + e2e_tests.get("skipped", 0)
            
            # Calculate average coverage
            avg_coverage = coverage_data.get("total_coverage", 0.0)
            
            # Generate HTML report if requested
            report_path = str(project_config.REPORTS_DIR / "test-report.html")
            if generate_html_report:
                report_path = self._generate_html_report(
                    total_tests=total_tests,
                    total_passed=total_passed,
                    total_failed=total_failed,
                    skipped=skipped,
                    coverage=avg_coverage,
                    unit_results=unit_tests,
                    e2e_results=e2e_tests
                )
            
            logger.info(
                f"[{self.skill_name}] Test aggregation completed",
                extra={
                    "total_tests": total_tests,
                    "total_passed": total_passed,
                    "total_failed": total_failed,
                    "avg_coverage": avg_coverage
                }
            )
            
            return {
                "total_tests": total_tests,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "skipped": skipped,
                "avg_coverage": avg_coverage,
                "report_path": report_path,
            }
            
        except Exception as e:
            logger.error(f"[{self.skill_name}] Test aggregation failed", exc_info=True)
            return {
                "total_tests": 0,
                "total_passed": 0,
                "total_failed": 0,
                "skipped": 0,
                "avg_coverage": 0.0,
                "report_path": "",
            }
    
    def _read_unit_test_results(self) -> dict:
        """Read unit test results from JSON reports."""
        total = passed = failed = skipped = 0
        
        try:
            # Try Vitest report
            vitest_report = self.workspace_root / "coverage" / "vitest-report.json"
            if vitest_report.exists():
                try:
                    # Validate file path for security
                    self.security_filter.validate_file_operation(str(vitest_report), "read")
                    vitest_results = CentralizedParser.parse_test_results("vitest", vitest_report)
                    total += vitest_results.get("total", 0)
                    passed += vitest_results.get("passed", 0)
                    failed += vitest_results.get("failed", 0)
                    skipped += vitest_results.get("skipped", 0)
                except Exception as e:
                    logger.debug(f"[{self.skill_name}] Failed to parse vitest report: {e}")
            
            # Try PyTest report
            pytest_report = self.workspace_root / "report.json"
            if pytest_report.exists():
                try:
                    # Validate file path for security
                    self.security_filter.validate_file_operation(str(pytest_report), "read")
                    pytest_results = CentralizedParser.parse_test_results("pytest", pytest_report)
                    total += pytest_results.get("total", 0)
                    passed += pytest_results.get("passed", 0)
                    failed += pytest_results.get("failed", 0)
                    skipped += pytest_results.get("skipped", 0)
                except Exception as e:
                    logger.debug(f"[{self.skill_name}] Failed to parse pytest report: {e}")
        except Exception as e:
            logger.debug(f"[{self.skill_name}] Failed to read unit test results: {e}")
        
        return {"total": total, "passed": passed, "failed": failed, "skipped": skipped}
    
    def _read_e2e_test_results(self) -> dict:
        """Read E2E test results from Playwright."""
        total = passed = failed = 0
        
        try:
            # Look for Playwright results
            results_dir = self.workspace_root / "test-results"
            if results_dir.exists():
                try:
                    e2e_results = CentralizedParser.parse_test_results("playwright", results_dir)
                    total = e2e_results.get("total", 0)
                    passed = e2e_results.get("passed", 0)
                    failed = e2e_results.get("failed", 0)
                except Exception as e:
                    logger.debug(f"[{self.skill_name}] Failed to parse playwright results: {e}")
        except Exception as e:
            logger.debug(f"[{self.skill_name}] Failed to read E2E test results: {e}")
        
        return {"total": total, "passed": passed, "failed": failed}
    
    def _read_coverage_data(self) -> dict:
        """Read coverage data from reports."""
        total_coverage = 0.0
        
        try:
            # Try frontend coverage
            fe_coverage_path = self.workspace_root / "coverage"
            if fe_coverage_path.exists():
                try:
                    fe_coverage = CentralizedParser.parse_coverage("vitest", fe_coverage_path)
                    total_coverage = fe_coverage
                except Exception as e:
                    logger.debug(f"[{self.skill_name}] Failed to parse frontend coverage: {e}")
            
            # Try backend coverage
            be_coverage_path = self.workspace_root / ".coverage.json"
            if be_coverage_path.exists():
                try:
                    be_coverage = CentralizedParser.parse_coverage("pytest", be_coverage_path)
                    if total_coverage > 0:
                        total_coverage = (total_coverage + be_coverage) / 2
                    else:
                        total_coverage = be_coverage
                except Exception as e:
                    logger.debug(f"[{self.skill_name}] Failed to parse backend coverage: {e}")
        except Exception as e:
            logger.debug(f"[{self.skill_name}] Failed to read coverage data: {e}")
        
        return {"total_coverage": total_coverage}
    
    def _generate_html_report(self, total_tests: int, total_passed: int, total_failed: int,
                            skipped: int, coverage: float, unit_results: dict, 
                            e2e_results: dict) -> str:
        """Generate HTML test report."""
        from datetime import datetime
        
        # Create reports directory
        reports_dir = self.workspace_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_path = reports_dir / "test-report.html"
        
        # Generate HTML report
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background-color: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .passed {{ color: #27ae60; font-weight: bold; }}
        .failed {{ color: #e74c3c; font-weight: bold; }}
        .coverage {{ color: #3498db; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; background-color: white; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #34495e; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <div class="stat-box">
            <h3>Total Tests</h3>
            <p style="font-size: 28px; margin: 0;">{total_tests}</p>
        </div>
        <div class="stat-box">
            <h3>Passed</h3>
            <p class="passed" style="font-size: 28px; margin: 0;">{total_passed}</p>
        </div>
        <div class="stat-box">
            <h3>Failed</h3>
            <p class="failed" style="font-size: 28px; margin: 0;">{total_failed}</p>
        </div>
        <div class="stat-box">
            <h3>Code Coverage</h3>
            <p class="coverage" style="font-size: 28px; margin: 0;">{coverage:.1f}%</p>
        </div>
    </div>
    
    <table>
        <tr>
            <th>Test Type</th>
            <th>Total</th>
            <th>Passed</th>
            <th>Failed</th>
        </tr>
        <tr>
            <td>Unit Tests</td>
            <td>{unit_results['total']}</td>
            <td class="passed">{unit_results['passed']}</td>
            <td class="failed">{unit_results['failed']}</td>
        </tr>
        <tr>
            <td>E2E Tests</td>
            <td>{e2e_results['total']}</td>
            <td class="passed">{e2e_results['passed']}</td>
            <td class="failed">{e2e_results['failed']}</td>
        </tr>
    </table>
</body>
</html>"""
        
        try:
            report_path.write_text(html_content)
            logger.info(f"[{self.skill_name}] Generated HTML report at {report_path}")
        except Exception as e:
            logger.error(f"[{self.skill_name}] Failed to generate HTML report: {e}")
        
        return str(report_path.relative_to(self.workspace_root))


__all__ = ["TestAggregator"]
