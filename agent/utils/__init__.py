"""
Agent Utilities Package

Helper functions and utilities for the Master Orchestrator Agent.
"""

from agent.utils.parsers import (
    VitestParser,
    PyTestParser,
    PlaywrightParser,
    CoverageParser,
    SecurityParser,
    BuildParser,
    TestStatus,
    CoverageFormat,
    parse_test_results,
    parse_coverage,
)

from agent.utils.logging_helpers import (
    log_skill_start,
    log_skill_success,
    log_skill_failure,
    log_skill_warning,
    log_tool_execution,
    log_tool_result,
    log_validation_error,
    log_security_event,
    log_operation_metric,
    StructuredLogger,
)

__version__ = "0.1.0"

__all__ = [
    # Parsers
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
    # Logging
    "log_skill_start",
    "log_skill_success",
    "log_skill_failure",
    "log_skill_warning",
    "log_tool_execution",
    "log_tool_result",
    "log_validation_error",
    "log_security_event",
    "log_operation_metric",
    "StructuredLogger",
]
