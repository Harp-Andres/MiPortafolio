"""
Logging Utilities and Helpers

Provides centralized logging patterns for all skills.
Ensures consistent structured logging across the agent.
"""

import logging
from typing import Any, Dict, Optional
from pathlib import Path


def log_skill_start(logger: logging.Logger, skill_name: str, **context) -> None:
    """Log skill execution start with context"""
    logger.debug(
        f"[{skill_name}] Starting execution",
        extra={"skill": skill_name, **context}
    )


def log_skill_success(logger: logging.Logger, skill_name: str, duration_ms: float, **context) -> None:
    """Log skill execution success with duration"""
    logger.info(
        f"[{skill_name}] Execution successful",
        extra={"skill": skill_name, "duration_ms": duration_ms, **context}
    )


def log_skill_failure(logger: logging.Logger, skill_name: str, error: str, duration_ms: float, **context) -> None:
    """Log skill execution failure"""
    logger.error(
        f"[{skill_name}] Execution failed: {error}",
        exc_info=True,
        extra={"skill": skill_name, "duration_ms": duration_ms, "error": error, **context}
    )


def log_skill_warning(logger: logging.Logger, skill_name: str, warning: str, **context) -> None:
    """Log skill warning"""
    logger.warning(
        f"[{skill_name}] {warning}",
        extra={"skill": skill_name, "warning": warning, **context}
    )


def log_tool_execution(logger: logging.Logger, tool_name: str, command: str, **context) -> None:
    """Log tool/command execution"""
    logger.debug(
        f"[Tool] Executing {tool_name}",
        extra={"tool": tool_name, "command": command, **context}
    )


def log_tool_result(logger: logging.Logger, tool_name: str, success: bool, result: Any, duration_ms: float, **context) -> None:
    """Log tool/command result"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"[Tool] {tool_name} completed: {status}",
        extra={"tool": tool_name, "success": success, "duration_ms": duration_ms, "result": str(result)[:100], **context}
    )


def log_validation_error(logger: logging.Logger, validator_name: str, error: str, **context) -> None:
    """Log validation error"""
    logger.error(
        f"[Validation] {validator_name} failed: {error}",
        extra={"validator": validator_name, "error": error, **context}
    )


def log_security_event(logger: logging.Logger, event_type: str, severity: str, details: str, **context) -> None:
    """Log security-related event"""
    logger.warning(
        f"[Security] {event_type}: {details}",
        extra={"event_type": event_type, "severity": severity, "details": details, **context}
    )


def log_operation_metric(logger: logging.Logger, operation_name: str, metric_name: str, metric_value: float, **context) -> None:
    """Log operation metrics"""
    logger.info(
        f"[Metric] {operation_name} {metric_name}: {metric_value}",
        extra={"operation": operation_name, "metric": metric_name, "value": metric_value, **context}
    )


class StructuredLogger:
    """
    Wrapper for structured logging with consistent patterns.
    
    Example:
        logger = StructuredLogger("MySkill")
        logger.start()
        logger.info("Doing work", file_count=42)
        logger.success(duration_ms=1234, output="result.txt")
    """
    
    def __init__(self, skill_name: str, base_logger: Optional[logging.Logger] = None):
        self.skill_name = skill_name
        self.base_logger = base_logger or logging.getLogger(__name__)
    
    def debug(self, message: str, **context) -> None:
        """Log debug message"""
        self.base_logger.debug(
            f"[{self.skill_name}] {message}",
            extra={"skill": self.skill_name, **context}
        )
    
    def info(self, message: str, **context) -> None:
        """Log info message"""
        self.base_logger.info(
            f"[{self.skill_name}] {message}",
            extra={"skill": self.skill_name, **context}
        )
    
    def warning(self, message: str, **context) -> None:
        """Log warning message"""
        self.base_logger.warning(
            f"[{self.skill_name}] {message}",
            extra={"skill": self.skill_name, **context}
        )
    
    def error(self, message: str, exc_info: bool = False, **context) -> None:
        """Log error message"""
        self.base_logger.error(
            f"[{self.skill_name}] {message}",
            exc_info=exc_info,
            extra={"skill": self.skill_name, **context}
        )
    
    def start(self, **context) -> None:
        """Log skill start"""
        self.debug("Starting execution", **context)
    
    def success(self, **context) -> None:
        """Log skill success"""
        self.info("Execution successful", **context)
    
    def failure(self, error: str, **context) -> None:
        """Log skill failure"""
        self.error(f"Execution failed: {error}", exc_info=True, **context)
    
    def operation(self, operation_name: str, **context) -> None:
        """Log operation progress"""
        self.debug(f"Executing: {operation_name}", **context)
    
    def metric(self, metric_name: str, value: float, **context) -> None:
        """Log metric"""
        self.info(f"Metric {metric_name}: {value}", **context)


__all__ = [
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
