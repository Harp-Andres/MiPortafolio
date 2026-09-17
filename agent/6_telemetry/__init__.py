"""
Master Orchestrator Agent - Layer 6: Telemetry

Logging, metrics, and distributed tracing.

Modules:
  - logger.py: Structured logging configuration
  - metrics.py: Performance metrics collection
  - tracer.py: Distributed tracing for debugging
"""

from agent_6_telemetry.logger import (
    setup_logging,
    get_logger,
    ensure_log_dir,
    get_file_handler,
    get_console_handler,
    JSONFormatter,
    StructuredFormatter,
    RichFormatter,
    LogContext,
    LogRecord,
)

from agent_6_telemetry.metrics import (
    Metric,
    Counter,
    Gauge,
    Histogram,
    Timer,
    MetricsCollector,
    BuildMetrics,
    TestMetrics,
)

from agent_6_telemetry.tracer import (
    SpanStatus,
    SpanEvent,
    Span,
    Tracer,
    TraceContext,
    SpanContext,
    get_tracer,
    reset_tracer,
)

__version__ = "0.1.0"

__all__ = [
    # Logger
    "setup_logging",
    "get_logger",
    "ensure_log_dir",
    "get_file_handler",
    "get_console_handler",
    "JSONFormatter",
    "StructuredFormatter",
    "RichFormatter",
    "LogContext",
    "LogRecord",
    # Metrics
    "Metric",
    "Counter",
    "Gauge",
    "Histogram",
    "Timer",
    "MetricsCollector",
    "BuildMetrics",
    "TestMetrics",
    # Tracing
    "SpanStatus",
    "SpanEvent",
    "Span",
    "Tracer",
    "TraceContext",
    "SpanContext",
    "get_tracer",
    "reset_tracer",
]
