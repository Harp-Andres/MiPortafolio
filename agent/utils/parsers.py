"""
Centralized Parser Module - Single Source of Truth for Data Parsing

This module provides agnóstico, reusable parsing functions for all report types.
No skill should implement its own parsing logic - all must use this centralized module.

Features:
- JSON deserialize with automatic repair for malformed payloads
- Pydantic-based schema validation with strict enforcement
- Fallback parsing strategies (JSON → Regex → Default)
- Generic schema-based parsing (DTOs passed by parameter)
- No assumptions about business domain (data-agnostic)

Supported Report Types:
- Vitest JSON reports (frontend testing)
- PyTest JSON reports (backend testing)
- Playwright JSON reports (E2E testing)
- Coverage reports (coverage-final.json, .coverage.json, HTML)
- Bandit security reports (Python)
- npm audit reports (JavaScript)
- Build artifacts and outputs
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Type, Union, Callable
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

try:
    from pydantic import BaseModel, ValidationError, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

logger = logging.getLogger(__name__)


class TestStatus(str, Enum):
    """Test result status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"


class CoverageFormat(str, Enum):
    """Coverage report formats"""
    VITEST = "vitest"  # coverage-final.json
    PYTEST = "pytest"  # .coverage.json
    HTML = "html"      # index.html


# ============================================================================
# PYDANTIC SCHEMAS (Generic DTOs)
# ============================================================================

if HAS_PYDANTIC:
    class TestResultSchema(BaseModel):
        """Generic test result schema"""
        total: int = 0
        passed: int = 0
        failed: int = 0
        skipped: int = 0
        error: Optional[str] = None
        
        class Config:
            extra = "allow"  # Allow additional fields

    class CoverageDataSchema(BaseModel):
        """Generic coverage data schema"""
        percentage: float = 0.0
        lines_covered: int = 0
        lines_total: int = 0
        uncovered_lines: int = 0
        
        class Config:
            extra = "allow"

    class SecurityResultSchema(BaseModel):
        """Generic security scan result"""
        critical: int = 0
        high: int = 0
        medium: int = 0
        low: int = 0
        total: int = 0
        
        class Config:
            extra = "allow"


# ============================================================================
# JSON REPAIR AND DESERIALIZATION UTILITIES
# ============================================================================

class JSONRepairStrategy:
    """Strategies for repairing malformed JSON"""
    
    @staticmethod
    def repair_single_quotes(text: str) -> str:
        """Convert single quotes to double quotes"""
        try:
            return text.replace("'", '"')
        except Exception:
            return text
    
    @staticmethod
    def repair_trailing_commas(text: str) -> str:
        """Remove trailing commas in arrays/objects"""
        try:
            # Remove trailing commas before ] or }
            text = re.sub(r',(\s*[}\]])', r'\1', text)
            return text
        except Exception:
            return text
    
    @staticmethod
    def repair_unquoted_keys(text: str) -> str:
        """Add quotes around unquoted keys"""
        try:
            # Match key: value pattern and quote the key
            pattern = r'([{,]\s*)(\w+)(\s*:)'
            replacement = r'\1"\2"\3'
            return re.sub(pattern, replacement, text)
        except Exception:
            return text
    
    @staticmethod
    def repair_missing_quotes(text: str) -> str:
        """Attempt to quote unquoted string values"""
        try:
            # This is a best-effort approach
            pattern = r':\s*([A-Za-z_][A-Za-z0-9_]*)'
            replacement = r': "\1"'
            return re.sub(pattern, replacement, text)
        except Exception:
            return text


def deserialize_json_with_repair(
    json_content: Union[str, bytes],
    max_repair_attempts: int = 3,
    logger_instance: Optional[logging.Logger] = None
) -> Tuple[Optional[Dict[str, Any]], bool]:
    """
    Deserialize JSON with automatic repair attempts.
    
    Args:
        json_content: JSON string or bytes to deserialize
        max_repair_attempts: Maximum repair attempts before giving up
        logger_instance: Logger for debugging
        
    Returns:
        Tuple of (parsed_data, was_repaired)
    """
    if isinstance(json_content, bytes):
        json_content = json_content.decode('utf-8', errors='replace')
    
    json_content = json_content.strip()
    
    # Try direct parsing first
    try:
        data = json.loads(json_content)
        return data, False
    except json.JSONDecodeError as e:
        if logger_instance:
            logger_instance.debug(f"Initial JSON parse failed: {e}")
    
    # Try repair strategies
    repair_strategies = [
        JSONRepairStrategy.repair_trailing_commas,
        JSONRepairStrategy.repair_single_quotes,
        JSONRepairStrategy.repair_unquoted_keys,
    ]
    
    for attempt, strategy in enumerate(repair_strategies):
        if attempt >= max_repair_attempts:
            break
        
        try:
            repaired = strategy(json_content)
            data = json.loads(repaired)
            if logger_instance:
                logger_instance.debug(f"JSON repair successful using strategy {attempt}")
            return data, True
        except Exception as e:
            if logger_instance:
                logger_instance.debug(f"Repair attempt {attempt} failed: {e}")
    
    return None, False


# ============================================================================
# SCHEMA-BASED VALIDATION
# ============================================================================

class SchemaValidator:
    """Validate parsed data against schemas"""
    
    @staticmethod
    def validate_with_pydantic(
        data: Dict[str, Any],
        schema: Type[BaseModel],
        strict: bool = False
    ) -> Tuple[Optional[BaseModel], Optional[str]]:
        """
        Validate data using Pydantic schema.
        
        Args:
            data: Parsed data to validate
            schema: Pydantic model to validate against
            strict: Enforce strict validation
            
        Returns:
            Tuple of (validated_model, error_message)
        """
        if not HAS_PYDANTIC:
            return None, "Pydantic not available"
        
        try:
            validated = schema(**data)
            return validated, None
        except ValidationError as e:
            error_msg = f"Validation failed: {str(e)}"
            logger.warning(error_msg)
            return None, error_msg
    
    @staticmethod
    def apply_custom_validation(
        data: Dict[str, Any],
        validator_func: Callable[[Dict[str, Any]], bool],
        error_msg: str = "Custom validation failed"
    ) -> Tuple[bool, Optional[str]]:
        """
        Apply custom validation function.
        
        Args:
            data: Data to validate
            validator_func: Function that returns True if valid
            error_msg: Error message if validation fails
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if validator_func(data):
                return True, None
            return False, error_msg
        except Exception as e:
            return False, f"{error_msg}: {str(e)}"


# ============================================================================
# VITEST PARSER (Frontend Unit Tests)
# ============================================================================

class VitestParser:
    """Parse Vitest test reports"""
    
    @staticmethod
    def parse_json(json_path: Path, repair: bool = True) -> Dict[str, int]:
        """
        Parse vitest-report.json with automatic repair.
        
        Args:
            json_path: Path to vitest report JSON
            repair: Enable automatic JSON repair
            
        Returns:
            Parsed test results
        """
        if not json_path.exists():
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        
        try:
            json_content = json_path.read_text()
            
            if repair:
                data, was_repaired = deserialize_json_with_repair(json_content, logger_instance=logger)
                if data is None:
                    logger.warning(f"Failed to repair JSON in {json_path}")
                    return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            
            total = passed = failed = skipped = 0
            
            for test_file in data.get("testResults", []):
                for result in test_file.get("assertionResults", []):
                    total += 1
                    status = result.get("status", "").lower()
                    if status == "passed":
                        passed += 1
                    elif status == "failed":
                        failed += 1
                    elif status == "skipped":
                        skipped += 1
            
            return {"total": total, "passed": passed, "failed": failed, "skipped": skipped}
        except Exception as e:
            logger.error(f"Failed to parse Vitest JSON: {e}")
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": str(e)}
    
    @staticmethod
    def parse_output(output: str) -> Dict[str, int]:
        """
        Parse Vitest CLI output using regex fallback.
        
        Args:
            output: Vitest CLI output
            
        Returns:
            Parsed test results
        """
        passed = 0
        failed = 0
        
        # Match: "123 passed" or "123 pass"
        passed_match = re.search(r'(\d+)\s+pass(?:ed)?', output, re.IGNORECASE)
        if passed_match:
            passed = int(passed_match.group(1))
        
        # Match: "45 failed" or "45 fail"
        failed_match = re.search(r'(\d+)\s+fail(?:ed)?', output, re.IGNORECASE)
        if failed_match:
            failed = int(failed_match.group(1))
        
        return {"total": passed + failed, "passed": passed, "failed": failed}


# ============================================================================
# PYTEST PARSER (Backend Unit Tests)
# ============================================================================

class PyTestParser:
    """Parse PyTest test reports"""
    
    @staticmethod
    def parse_json(json_path: Path, repair: bool = True) -> Dict[str, int]:
        """
        Parse pytest report.json with automatic repair.
        
        Args:
            json_path: Path to pytest report JSON
            repair: Enable automatic JSON repair
            
        Returns:
            Parsed test results
        """
        if not json_path.exists():
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        
        try:
            json_content = json_path.read_text()
            
            if repair:
                data, was_repaired = deserialize_json_with_repair(json_content, logger_instance=logger)
                if data is None:
                    logger.warning(f"Failed to repair JSON in {json_path}")
                    return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            
            summary = data.get("summary", {})
            
            return {
                "total": summary.get("total", 0),
                "passed": summary.get("passed", 0),
                "failed": summary.get("failed", 0),
                "skipped": summary.get("skipped", 0),
            }
        except Exception as e:
            logger.error(f"Failed to parse PyTest JSON: {e}")
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": str(e)}
    
    @staticmethod
    def parse_output(output: str) -> Dict[str, int]:
        """
        Parse PyTest CLI output using regex fallback.
        
        Args:
            output: PyTest CLI output
            
        Returns:
            Parsed test results
        """
        passed = 0
        failed = 0
        skipped = 0
        
        # Match: "123 passed" or "123 pass"
        passed_match = re.search(r'(\d+)\s+pass(?:ed)?', output)
        if passed_match:
            passed = int(passed_match.group(1))
        
        # Match: "45 failed" or "45 fail"
        failed_match = re.search(r'(\d+)\s+fail(?:ed)?', output)
        if failed_match:
            failed = int(failed_match.group(1))
        
        # Match: "12 skipped"
        skipped_match = re.search(r'(\d+)\s+skip(?:ped)?', output)
        if skipped_match:
            skipped = int(skipped_match.group(1))
        
        return {"total": passed + failed + skipped, "passed": passed, "failed": failed, "skipped": skipped}


# ============================================================================
# PLAYWRIGHT PARSER (E2E Tests)
# ============================================================================

class PlaywrightParser:
    """Parse Playwright E2E test reports"""
    
    @staticmethod
    def parse_results_dir(results_dir: Path, repair: bool = True) -> Dict[str, int]:
        """
        Parse test-results/*.json files with automatic repair.
        
        Args:
            results_dir: Directory with Playwright JSON results
            repair: Enable automatic JSON repair
            
        Returns:
            Aggregated test results
        """
        total = passed = failed = 0
        
        if not results_dir.exists():
            return {"total": 0, "passed": 0, "failed": 0}
        
        try:
            for json_file in results_dir.glob("*.json"):
                try:
                    json_content = json_file.read_text()
                    
                    if repair:
                        data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
                    else:
                        try:
                            data = json.loads(json_content)
                        except json.JSONDecodeError:
                            continue
                    
                    if data and "stats" in data:
                        stats = data["stats"]
                        total += stats.get("expected", 0) + stats.get("unexpected", 0)
                        passed += stats.get("expected", 0)
                        failed += stats.get("unexpected", 0)
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Failed to parse Playwright results: {e}")
            return {"total": 0, "passed": 0, "failed": 0, "error": str(e)}
        
        return {"total": total, "passed": passed, "failed": failed}
    
    @staticmethod
    def parse_output(output: str) -> Dict[str, int]:
        """
        Parse Playwright CLI output using regex fallback.
        
        Args:
            output: Playwright CLI output
            
        Returns:
            Parsed test results
        """
        passed = 0
        failed = 0
        
        # Match: "123 passed"
        passed_match = re.search(r'(\d+)\s+passed', output)
        if passed_match:
            passed = int(passed_match.group(1))
        
        # Match: "45 failed"
        failed_match = re.search(r'(\d+)\s+failed', output)
        if failed_match:
            failed = int(failed_match.group(1))
        
        return {"total": passed + failed, "passed": passed, "failed": failed}


# ============================================================================
# COVERAGE PARSERS (Improved with repair)
# ============================================================================

class CoverageParser:
    """Parse code coverage reports"""
    
    @staticmethod
    def parse_vitest_coverage(coverage_dir: Path, repair: bool = True) -> float:
        """
        Parse Vitest coverage-final.json with automatic repair.
        
        Args:
            coverage_dir: Directory with coverage reports
            repair: Enable automatic JSON repair
            
        Returns:
            Coverage percentage (0.0-100.0)
        """
        coverage_json = coverage_dir / "coverage-final.json"
        
        if not coverage_json.exists():
            return 0.0
        
        try:
            json_content = coverage_json.read_text()
            
            if repair:
                data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return 0.0
            
            if data is None:
                return 0.0
            
            total_lines = covered_lines = 0
            
            for file_data in data.values():
                if isinstance(file_data, dict) and "lines" in file_data:
                    for line, coverage in file_data["lines"].items():
                        total_lines += 1
                        if coverage and coverage > 0:
                            covered_lines += 1
            
            if total_lines > 0:
                return (covered_lines / total_lines) * 100.0
        except Exception as e:
            logger.error(f"Failed to parse Vitest coverage: {e}")
        
        return 0.0
    
    @staticmethod
    def parse_pytest_coverage(coverage_file: Path, repair: bool = True) -> float:
        """
        Parse PyTest .coverage.json with automatic repair.
        
        Args:
            coverage_file: Path to .coverage.json
            repair: Enable automatic JSON repair
            
        Returns:
            Coverage percentage (0.0-100.0)
        """
        if not coverage_file.exists():
            return 0.0
        
        try:
            json_content = coverage_file.read_text()
            
            if repair:
                data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return 0.0
            
            if data and "totals" in data:
                return float(data["totals"].get("percent_covered", 0.0))
        except Exception as e:
            logger.error(f"Failed to parse PyTest coverage: {e}")
        
        return 0.0
    
    @staticmethod
    def parse_coverage_html(html_path: Path) -> float:
        """
        Parse coverage percentage from index.html.
        
        Args:
            html_path: Path to coverage HTML report
            
        Returns:
            Coverage percentage (0.0-100.0)
        """
        if not html_path.exists():
            return 0.0
        
        try:
            content = html_path.read_text()
            # Look for coverage percentage in HTML
            match = re.search(r'(\d+(?:\.\d+)?)[%\s]*coverage', content, re.IGNORECASE)
            if match:
                return float(match.group(1))
        except Exception as e:
            logger.error(f"Failed to parse HTML coverage: {e}")
        
        return 0.0
    
    @staticmethod
    def count_uncovered_lines(coverage_dir: Path, is_pytest: bool = False, repair: bool = True) -> int:
        """
        Count uncovered lines from coverage reports.
        
        Args:
            coverage_dir: Directory with coverage reports
            is_pytest: True for pytest coverage, False for vitest
            repair: Enable automatic JSON repair
            
        Returns:
            Number of uncovered lines
        """
        uncovered = 0
        
        try:
            if is_pytest:
                coverage_file = coverage_dir / ".coverage.json"
                if coverage_file.exists():
                    json_content = coverage_file.read_text()
                    
                    if repair:
                        data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
                    else:
                        try:
                            data = json.loads(json_content)
                        except json.JSONDecodeError:
                            return 0
                    
                    if data and "totals" in data:
                        uncovered = int(data["totals"].get("num_statements", 0) - 
                                       data["totals"].get("num_covered", 0))
            else:
                coverage_json = coverage_dir / "coverage-final.json"
                if coverage_json.exists():
                    json_content = coverage_json.read_text()
                    
                    if repair:
                        data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
                    else:
                        try:
                            data = json.loads(json_content)
                        except json.JSONDecodeError:
                            return 0
                    
                    if data:
                        for file_data in data.values():
                            if isinstance(file_data, dict) and "lines" in file_data:
                                for line, coverage in file_data["lines"].items():
                                    if not coverage or coverage == 0:
                                        uncovered += 1
        except Exception as e:
            logger.error(f"Failed to count uncovered lines: {e}")
        
        return uncovered


# ============================================================================
# SECURITY REPORT PARSERS (Improved with repair)
# ============================================================================

class SecurityParser:
    """Parse security scan reports"""
    
    @staticmethod
    def parse_bandit_json(json_path: Path, repair: bool = True) -> Dict[str, int]:
        """
        Parse Bandit JSON report (Python security) with automatic repair.
        
        Args:
            json_path: Path to bandit report JSON
            repair: Enable automatic JSON repair
            
        Returns:
            Security issues by severity
        """
        if not json_path.exists():
            return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
        
        try:
            json_content = json_path.read_text()
            
            if repair:
                data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
            
            if data is None:
                return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
            
            results = data.get("results", [])
            severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            
            for result in results:
                severity = result.get("severity", "low").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            severity_counts["total"] = sum(severity_counts.values())
            return severity_counts
        except Exception as e:
            logger.error(f"Failed to parse Bandit JSON: {e}")
        
        return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
    
    @staticmethod
    def parse_npm_audit_json(json_path: Path, repair: bool = True) -> Dict[str, int]:
        """
        Parse npm audit JSON report (JavaScript security) with automatic repair.
        
        Args:
            json_path: Path to npm audit report JSON
            repair: Enable automatic JSON repair
            
        Returns:
            Security issues by severity
        """
        if not json_path.exists():
            return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}
        
        try:
            json_content = json_path.read_text()
            
            if repair:
                data, _ = deserialize_json_with_repair(json_content, logger_instance=logger)
            else:
                try:
                    data = json.loads(json_content)
                except json.JSONDecodeError:
                    return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}
            
            if data is None:
                return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}
            
            vulnerabilities = data.get("vulnerabilities", {})
            severity_counts = {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0}
            
            for vuln in vulnerabilities.values():
                severity = vuln.get("severity", "low").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            severity_counts["total"] = sum(severity_counts.values())
            return severity_counts
        except Exception as e:
            logger.error(f"Failed to parse npm audit JSON: {e}")
        
        return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}


# ============================================================================
# BUILD PARSER (Improved with agnosticism)
# ============================================================================

class BuildParser:
    """Parse build outputs and artifacts"""
    
    @staticmethod
    def find_artifacts(build_dir: Path, artifact_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Find build artifacts in directory (agnóstico).
        
        Args:
            build_dir: Build output directory
            artifact_types: List of file extensions to search for
            
        Returns:
            List of artifact metadata
        """
        if artifact_types is None:
            artifact_types = [".js", ".css", ".html", ".json", ".whl", ".tar.gz", ".zip"]
        
        artifacts = []
        
        if not build_dir.exists():
            return artifacts
        
        try:
            for artifact_type in artifact_types:
                for file_path in build_dir.rglob(f"*{artifact_type}"):
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    artifacts.append({
                        "path": str(file_path.relative_to(build_dir)),
                        "type": artifact_type,
                        "size_mb": round(size_mb, 2),
                    })
        except Exception as e:
            logger.error(f"Failed to find artifacts: {e}")
        
        return sorted(artifacts, key=lambda x: x["size_mb"], reverse=True)


# ============================================================================
# CENTRALIZED PARSER ORCHESTRATOR
# ============================================================================

class CentralizedParser:
    """
    Centralized, agnóstico parser orchestrator.
    Single source of truth for all parsing operations.
    """
    
    @staticmethod
    def parse_test_results(
        test_framework: str,
        report_path: Path,
        repair: bool = True
    ) -> Dict[str, int]:
        """
        Parse test results - centralized entry point.
        
        Args:
            test_framework: Type of test framework (vitest, pytest, playwright)
            report_path: Path to test report file or directory
            repair: Enable automatic JSON repair
            
        Returns:
            Dictionary with test counts
        """
        if test_framework == "vitest":
            return VitestParser.parse_json(report_path, repair=repair)
        elif test_framework == "pytest":
            return PyTestParser.parse_json(report_path, repair=repair)
        elif test_framework == "playwright":
            return PlaywrightParser.parse_results_dir(report_path, repair=repair)
        else:
            logger.error(f"Unknown test framework: {test_framework}")
            return {"total": 0, "passed": 0, "failed": 0, "error": f"Unknown framework: {test_framework}"}
    
    @staticmethod
    def parse_coverage(
        coverage_type: Union[str, CoverageFormat],
        report_path: Path,
        repair: bool = True
    ) -> float:
        """
        Parse coverage percentage - centralized entry point.
        
        Args:
            coverage_type: Type of coverage format (vitest, pytest, html)
            report_path: Path to coverage report
            repair: Enable automatic JSON repair
            
        Returns:
            Coverage percentage (0.0-100.0)
        """
        if isinstance(coverage_type, str):
            coverage_type = CoverageFormat(coverage_type)
        
        if coverage_type == CoverageFormat.VITEST:
            return CoverageParser.parse_vitest_coverage(report_path, repair=repair)
        elif coverage_type == CoverageFormat.PYTEST:
            return CoverageParser.parse_pytest_coverage(report_path, repair=repair)
        elif coverage_type == CoverageFormat.HTML:
            return CoverageParser.parse_coverage_html(report_path)
        else:
            logger.error(f"Unknown coverage type: {coverage_type}")
            return 0.0
    
    @staticmethod
    def parse_security_report(
        tool: str,
        report_path: Path,
        repair: bool = True
    ) -> Dict[str, int]:
        """
        Parse security report - centralized entry point.
        
        Args:
            tool: Security tool (bandit, npm_audit)
            report_path: Path to security report JSON
            repair: Enable automatic JSON repair
            
        Returns:
            Dictionary with severity counts
        """
        if tool == "bandit":
            return SecurityParser.parse_bandit_json(report_path, repair=repair)
        elif tool == "npm_audit":
            return SecurityParser.parse_npm_audit_json(report_path, repair=repair)
        else:
            logger.error(f"Unknown security tool: {tool}")
            return {}
    
    @staticmethod
    def parse_json_generic(
        json_path: Path,
        schema: Optional[Type[BaseModel]] = None,
        repair: bool = True,
        strict: bool = False
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Generic JSON parsing with optional schema validation.
        
        Args:
            json_path: Path to JSON file
            schema: Optional Pydantic schema for validation
            repair: Enable automatic JSON repair
            strict: Enforce strict validation
            
        Returns:
            Tuple of (parsed_data, error_message)
        """
        if not json_path.exists():
            return None, f"File not found: {json_path}"
        
        try:
            json_content = json_path.read_text()
            
            if repair:
                data, was_repaired = deserialize_json_with_repair(json_content, logger_instance=logger)
            else:
                try:
                    data = json.loads(json_content)
                    was_repaired = False
                except json.JSONDecodeError as e:
                    return None, f"JSON decode error: {e}"
            
            if data is None:
                return None, "Failed to parse JSON even after repair attempts"
            
            # Validate against schema if provided
            if schema and HAS_PYDANTIC:
                validated, error = SchemaValidator.validate_with_pydantic(data, schema, strict=strict)
                if error:
                    return data, error  # Return raw data but note validation error
            
            return data, None
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"


# ============================================================================
# UTILITY FUNCTIONS (Legacy compatibility)
# ============================================================================

def parse_test_results(test_framework: str, report_path: Path) -> Dict[str, int]:
    """Backward compatible function - delegates to CentralizedParser"""
    return CentralizedParser.parse_test_results(test_framework, report_path)


def parse_coverage(coverage_type: Union[str, CoverageFormat], report_path: Path) -> float:
    """Backward compatible function - delegates to CentralizedParser"""
    return CentralizedParser.parse_coverage(coverage_type, report_path)


__all__ = [
    "VitestParser",
    "PyTestParser",
    "PlaywrightParser",
    "CoverageParser",
    "SecurityParser",
    "BuildParser",
    "CentralizedParser",
    "TestStatus",
    "CoverageFormat",
    "deserialize_json_with_repair",
    "JSONRepairStrategy",
    "SchemaValidator",
    "parse_test_results",
    "parse_coverage",
]
        
        if not results_dir.exists():
            return {"total": 0, "passed": 0, "failed": 0}
        
        try:
            for json_file in results_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "stats" in data:
                        stats = data["stats"]
                        total += stats.get("expected", 0) + stats.get("unexpected", 0)
                        passed += stats.get("expected", 0)
                        failed += stats.get("unexpected", 0)
                except Exception:
                    pass
        except Exception as e:
            return {"total": 0, "passed": 0, "failed": 0, "error": str(e)}
        
        return {"total": total, "passed": passed, "failed": failed}
    
    @staticmethod
    def parse_output(output: str) -> Dict[str, int]:
        """Parse Playwright CLI output for test counts"""
        passed = 0
        failed = 0
        
        # Match: "123 passed"
        passed_match = re.search(r'(\d+)\s+passed', output)
        if passed_match:
            passed = int(passed_match.group(1))
        
        # Match: "45 failed"
        failed_match = re.search(r'(\d+)\s+failed', output)
        if failed_match:
            failed = int(failed_match.group(1))
        
        return {"total": passed + failed, "passed": passed, "failed": failed}


# ============================================================================
# COVERAGE PARSERS
# ============================================================================

class CoverageParser:
    """Parse code coverage reports"""
    
    @staticmethod
    def parse_vitest_coverage(coverage_dir: Path) -> float:
        """Parse Vitest coverage-final.json"""
        coverage_json = coverage_dir / "coverage-final.json"
        
        if not coverage_json.exists():
            return 0.0
        
        try:
            data = json.loads(coverage_json.read_text())
            total_lines = covered_lines = 0
            
            for file_data in data.values():
                if isinstance(file_data, dict) and "lines" in file_data:
                    for line, coverage in file_data["lines"].items():
                        total_lines += 1
                        if coverage and coverage > 0:
                            covered_lines += 1
            
            if total_lines > 0:
                return (covered_lines / total_lines) * 100.0
        except Exception:
            pass
        
        return 0.0
    
    @staticmethod
    def parse_pytest_coverage(coverage_file: Path) -> float:
        """Parse PyTest .coverage.json"""
        if not coverage_file.exists():
            return 0.0
        
        try:
            data = json.loads(coverage_file.read_text())
            if "totals" in data:
                return float(data["totals"].get("percent_covered", 0.0))
        except Exception:
            pass
        
        return 0.0
    
    @staticmethod
    def parse_coverage_html(html_path: Path) -> float:
        """Parse coverage percentage from index.html"""
        if not html_path.exists():
            return 0.0
        
        try:
            content = html_path.read_text()
            # Look for coverage percentage in HTML
            match = re.search(r'(\d+(?:\.\d+)?)[%\s]*coverage', content, re.IGNORECASE)
            if match:
                return float(match.group(1))
        except Exception:
            pass
        
        return 0.0
    
    @staticmethod
    def count_uncovered_lines(coverage_dir: Path, is_pytest: bool = False) -> int:
        """Count uncovered lines from coverage reports"""
        uncovered = 0
        
        try:
            if is_pytest:
                coverage_file = coverage_dir / ".coverage.json"
                if coverage_file.exists():
                    data = json.loads(coverage_file.read_text())
                    if "totals" in data:
                        uncovered = int(data["totals"].get("num_statements", 0) - 
                                       data["totals"].get("num_covered", 0))
            else:
                coverage_json = coverage_dir / "coverage-final.json"
                if coverage_json.exists():
                    data = json.loads(coverage_json.read_text())
                    for file_data in data.values():
                        if isinstance(file_data, dict) and "lines" in file_data:
                            for line, coverage in file_data["lines"].items():
                                if not coverage or coverage == 0:
                                    uncovered += 1
        except Exception:
            pass
        
        return uncovered


# ============================================================================
# SECURITY REPORT PARSERS
# ============================================================================

class SecurityParser:
    """Parse security scan reports"""
    
    @staticmethod
    def parse_bandit_json(json_path: Path) -> Dict[str, int]:
        """Parse Bandit JSON report (Python security)"""
        if not json_path.exists():
            return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
        
        try:
            data = json.loads(json_path.read_text())
            results = data.get("results", [])
            
            severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            
            for result in results:
                severity = result.get("severity", "low").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            severity_counts["total"] = sum(severity_counts.values())
            return severity_counts
        except Exception:
            pass
        
        return {"critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0}
    
    @staticmethod
    def parse_npm_audit_json(json_path: Path) -> Dict[str, int]:
        """Parse npm audit JSON report (JavaScript security)"""
        if not json_path.exists():
            return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}
        
        try:
            data = json.loads(json_path.read_text())
            vulnerabilities = data.get("vulnerabilities", {})
            
            severity_counts = {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0}
            
            for vuln in vulnerabilities.values():
                severity = vuln.get("severity", "low").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            severity_counts["total"] = sum(severity_counts.values())
            return severity_counts
        except Exception:
            pass
        
        return {"critical": 0, "high": 0, "moderate": 0, "low": 0, "info": 0, "total": 0}


# ============================================================================
# BUILD PARSER
# ============================================================================

class BuildParser:
    """Parse build outputs and artifacts"""
    
    @staticmethod
    def find_artifacts(build_dir: Path, artifact_types: List[str] = None) -> List[Dict[str, Any]]:
        """Find build artifacts in directory"""
        if artifact_types is None:
            artifact_types = [".js", ".css", ".html", ".json", ".whl", ".tar.gz", ".zip"]
        
        artifacts = []
        
        if not build_dir.exists():
            return artifacts
        
        try:
            for artifact_type in artifact_types:
                for file_path in build_dir.rglob(f"*{artifact_type}"):
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    artifacts.append({
                        "path": str(file_path.relative_to(build_dir)),
                        "type": artifact_type,
                        "size_mb": round(size_mb, 2),
                    })
        except Exception:
            pass
        
        return sorted(artifacts, key=lambda x: x["size_mb"], reverse=True)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_test_results(test_framework: str, report_path: Path) -> Dict[str, int]:
    """
    Parse test results based on framework type.
    
    Args:
        test_framework: Type of test framework (vitest, pytest, playwright)
        report_path: Path to test report file or directory
        
    Returns:
        Dictionary with test counts
    """
    if test_framework == "vitest":
        return VitestParser.parse_json(report_path)
    elif test_framework == "pytest":
        return PyTestParser.parse_json(report_path)
    elif test_framework == "playwright":
        return PlaywrightParser.parse_results_dir(report_path)
    else:
        raise ValueError(f"Unknown test framework: {test_framework}")


def parse_coverage(coverage_type: CoverageFormat, report_path: Path) -> float:
    """
    Parse coverage percentage.
    
    Args:
        coverage_type: Type of coverage format
        report_path: Path to coverage report
        
    Returns:
        Coverage percentage (0.0-100.0)
    """
    if coverage_type == CoverageFormat.VITEST:
        return CoverageParser.parse_vitest_coverage(report_path)
    elif coverage_type == CoverageFormat.PYTEST:
        return CoverageParser.parse_pytest_coverage(report_path)
    elif coverage_type == CoverageFormat.HTML:
        return CoverageParser.parse_coverage_html(report_path)
    else:
        return 0.0


__all__ = [
    "VitestParser",
    "PyTestParser",
    "PlaywrightParser",
    "CoverageParser",
    "SecurityParser",
    "BuildParser",
    "TestStatus",
    "CoverageFormat",
    "parse_test_results",
    "parse_coverage",
]
