"""
Structured logging for the Master Orchestrator Agent.

This module provides:
- Centralized logging configuration
- Multiple output formats (console, file, JSON)
- Contextual logging with request IDs
- Async logging for performance
- Color-coded output for different log levels

Usage:
    from agent_6_telemetry.logger import setup_logging, get_logger

    # Setup at application startup
    setup_logging(level="INFO", json_output=True)

    # Get logger for module
    logger = get_logger(__name__)

    # Log with context
    logger.info("Task started", extra={"task_id": "123", "user": "john"})

    # Structured logging
    logger.error(
        "Skill execution failed",
        extra={
            "skill": "type_checker",
            "duration_ms": 1500,
            "error_type": "TypeCheckError",
        }
    )
"""

import logging
import logging.handlers
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Rich for colored output
from rich.logging import RichHandler
from rich.console import Console


# ============================================================================
# Constants
# ============================================================================

LOG_DIR = Path.cwd() / "logs"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
JSON_LOG_FORMAT = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"%(context)s}'

# Color mapping for log levels
LOG_COLORS = {
    "DEBUG": "blue",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red bold",
}


# ============================================================================
# Custom Formatters
# ============================================================================


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format record as JSON.

        Args:
            record: Log record to format.

        Returns:
            JSON string.
        """
        log_obj = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_obj.update(record.extra)

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


class StructuredFormatter(logging.Formatter):
    """Structured text formatter with context."""

    def __init__(self, fmt: str = None, use_colors: bool = True):
        """Initialize formatter.

        Args:
            fmt: Format string.
            use_colors: Use colored output.
        """
        super().__init__(fmt or LOG_FORMAT)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format record with structured context.

        Args:
            record: Log record to format.

        Returns:
            Formatted string.
        """
        # Format base message
        msg = super().format(record)

        # Add extra context if present
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            extra_str = " | " + " ".join(
                f"{k}={v}" for k, v in record.extra.items()
            )
            msg += extra_str

        # Add exception if present
        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"

        return msg


class RichFormatter(logging.Formatter):
    """Rich-formatted logging for console output."""

    def __init__(self):
        """Initialize Rich formatter."""
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format record with Rich styling.

        Args:
            record: Log record to format.

        Returns:
            Formatted string.
        """
        level_name = record.levelname
        level_color = LOG_COLORS.get(level_name, "white")

        # Format message
        msg = record.getMessage()

        # Add extra context
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            context = " | ".join(
                f"[cyan]{k}[/cyan]=[yellow]{v}[/yellow]"
                for k, v in record.extra.items()
            )
            msg += f" | {context}"

        return msg


# ============================================================================
# Logger Setup
# ============================================================================


def ensure_log_dir():
    """Ensure log directory exists."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_file_handler(
    log_file: Optional[Path] = None,
    level: int = logging.DEBUG,
    json_format: bool = False,
) -> logging.FileHandler:
    """Create file handler for logging.

    Args:
        log_file: Path to log file (default: logs/agent.log).
        level: Logging level.
        json_format: Use JSON format.

    Returns:
        Configured FileHandler.
    """
    ensure_log_dir()

    if log_file is None:
        log_file = LOG_DIR / "agent.log"

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = StructuredFormatter()

    handler.setFormatter(formatter)
    return handler


def get_console_handler(
    level: int = logging.INFO,
    use_rich: bool = True,
) -> logging.Handler:
    """Create console handler for logging.

    Args:
        level: Logging level.
        use_rich: Use Rich formatting.

    Returns:
        Configured console handler.
    """
    if use_rich:
        console = Console(file=sys.stderr)
        handler = RichHandler(console=console, show_time=True, show_path=False)
        handler.setFormatter(RichFormatter())
    else:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(StructuredFormatter(use_colors=False))

    handler.setLevel(level)
    return handler


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    json_output: bool = False,
    use_rich: bool = True,
    debug: bool = False,
) -> logging.Logger:
    """Setup logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file (default: logs/agent.log).
        json_output: Use JSON format for file output.
        use_rich: Use Rich formatting for console.
        debug: Enable debug mode (sets level to DEBUG).

    Returns:
        Configured root logger.
    """
    # Convert string level to int
    if debug:
        level_int = logging.DEBUG
    else:
        level_int = getattr(logging, level.upper(), logging.INFO)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all, filter at handlers

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add console handler
    console_level = logging.DEBUG if debug else level_int
    console_handler = get_console_handler(level=console_level, use_rich=use_rich)
    root_logger.addHandler(console_handler)

    # Add file handler
    if log_file or not json_output:
        file_handler = get_file_handler(
            log_file=log_file,
            level=logging.DEBUG,
            json_format=json_output,
        )
        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: str, context: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """Get logger for a module.

    Args:
        name: Logger name (typically __name__).
        context: Default context to add to all logs.

    Returns:
        Configured logger.

    Usage:
        logger = get_logger(__name__)
        logger.info("Message", extra={"key": "value"})
    """
    logger = logging.getLogger(name)

    if context:
        # Create a custom filter to add context
        class ContextFilter(logging.Filter):
            def filter(self, record):
                if not hasattr(record, "extra"):
                    record.extra = {}
                record.extra.update(context)
                return True

        logger.addFilter(ContextFilter())

    return logger


# ============================================================================
# Contextual Logging
# ============================================================================


class LogContext:
    """Context manager for adding context to logs.

    Usage:
        with LogContext(task_id="123", stage="build"):
            logger.info("Building...")  # Will include task_id and stage
    """

    _context = {}

    def __init__(self, **context):
        """Initialize context.

        Args:
            **context: Context key-value pairs.
        """
        self.context = context
        self.saved = {}

    def __enter__(self):
        """Enter context."""
        # Save current context
        self.saved = self._context.copy()
        # Merge new context
        self._context.update(self.context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        # Restore previous context
        self._context = self.saved

    @classmethod
    def get_context(cls) -> Dict[str, Any]:
        """Get current context.

        Returns:
            Current context dictionary.
        """
        return cls._context.copy()


class LogRecord:
    """Helper for structured log records."""

    @staticmethod
    def skill_started(skill_name: str, params: Dict[str, Any] = None) -> Dict:
        """Create log record for skill start.

        Args:
            skill_name: Name of skill.
            params: Skill parameters.

        Returns:
            Log record dictionary.
        """
        return {
            "event": "skill_started",
            "skill": skill_name,
            "params": params or {},
        }

    @staticmethod
    def skill_completed(
        skill_name: str,
        duration_ms: float,
        result: Any = None,
    ) -> Dict:
        """Create log record for skill completion.

        Args:
            skill_name: Name of skill.
            duration_ms: Execution time in milliseconds.
            result: Execution result.

        Returns:
            Log record dictionary.
        """
        return {
            "event": "skill_completed",
            "skill": skill_name,
            "duration_ms": duration_ms,
            "result": result,
        }

    @staticmethod
    def skill_failed(
        skill_name: str,
        duration_ms: float,
        error: str,
        error_type: str = None,
    ) -> Dict:
        """Create log record for skill failure.

        Args:
            skill_name: Name of skill.
            duration_ms: Execution time in milliseconds.
            error: Error message.
            error_type: Type of error.

        Returns:
            Log record dictionary.
        """
        return {
            "event": "skill_failed",
            "skill": skill_name,
            "duration_ms": duration_ms,
            "error": error,
            "error_type": error_type,
        }

    @staticmethod
    def api_call(
        provider: str,
        model: str,
        tokens_used: int,
        cost_usd: float,
    ) -> Dict:
        """Create log record for API call.

        Args:
            provider: LLM provider (openai, anthropic, ollama).
            model: Model name.
            tokens_used: Tokens used.
            cost_usd: Cost in USD.

        Returns:
            Log record dictionary.
        """
        return {
            "event": "api_call",
            "provider": provider,
            "model": model,
            "tokens": tokens_used,
            "cost": f"${cost_usd:.4f}",
        }


# Export public API
__all__ = [
    # Setup functions
    "setup_logging",
    "get_logger",
    "ensure_log_dir",
    # Handlers
    "get_file_handler",
    "get_console_handler",
    # Formatters
    "JSONFormatter",
    "StructuredFormatter",
    "RichFormatter",
    # Context
    "LogContext",
    "LogRecord",
    # Constants
    "LOG_DIR",
    "LOG_FORMAT",
    "JSON_LOG_FORMAT",
]
