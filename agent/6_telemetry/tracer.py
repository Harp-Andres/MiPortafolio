"""
Distributed tracing for debugging complex skill execution chains.

This module provides:
- Trace spans for operations
- Trace context propagation
- Async tracing support
- Trace exporting and visualization support

Usage:
    from agent_6_telemetry.tracer import Tracer, Span

    # Create tracer
    tracer = Tracer("my-service")

    # Create root span
    with tracer.start_span("ci_pipeline") as root_span:
        root_span.add_attribute("env", "production")

        # Create child spans
        with tracer.start_span("dependencies", parent=root_span) as span:
            span.add_event("resolving_dependencies")
            span.set_status("success")

        with tracer.start_span("build", parent=root_span) as span:
            span.add_event("building_artifacts")
            span.set_status("success")

    # Export traces
    traces = tracer.export_traces()
"""

import uuid
import time
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field


# ============================================================================
# Status Enum
# ============================================================================


class SpanStatus:
    """Status codes for spans."""

    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


# ============================================================================
# Span Event
# ============================================================================


@dataclass
class SpanEvent:
    """Event within a span."""

    name: str
    timestamp: datetime = field(default_factory=datetime.now)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "attributes": self.attributes,
        }


# ============================================================================
# Span
# ============================================================================


@dataclass
class Span:
    """A single span in a trace."""

    name: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    parent_id: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[SpanEvent] = field(default_factory=list)
    status: str = SpanStatus.UNSET

    def duration_ms(self) -> float:
        """Get span duration in milliseconds.

        Returns:
            Duration or 0 if still running.
        """
        if self.end_time is None:
            return 0.0

        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000

    def add_attribute(self, key: str, value: Any):
        """Add attribute to span.

        Args:
            key: Attribute name.
            value: Attribute value.
        """
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Dict[str, Any] = None):
        """Add event to span.

        Args:
            name: Event name.
            attributes: Optional event attributes.
        """
        event = SpanEvent(name, attributes=attributes or {})
        self.events.append(event)

    def set_status(self, status: str):
        """Set span status.

        Args:
            status: Status (UNSET, OK, ERROR).
        """
        self.status = status

    def end(self):
        """End the span."""
        self.end_time = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms(),
            "attributes": self.attributes,
            "events": [e.to_dict() for e in self.events],
            "status": self.status,
        }


# ============================================================================
# Trace Context
# ============================================================================


class TraceContext:
    """Context for trace propagation.

    Usage:
        ctx = TraceContext()
        ctx.trace_id = trace_id
        ctx.span_id = span_id

        # Propagate context to async tasks, remote calls, etc.
        headers = ctx.to_headers()
    """

    def __init__(self, trace_id: str = None, span_id: str = None):
        """Initialize trace context.

        Args:
            trace_id: Trace ID (generated if not provided).
            span_id: Span ID (generated if not provided).
        """
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = span_id or str(uuid.uuid4())

    def to_headers(self) -> Dict[str, str]:
        """Convert to HTTP headers for propagation.

        Returns:
            Dictionary of headers.
        """
        return {
            "traceparent": f"00-{self.trace_id}-{self.span_id}-01",
            "x-trace-id": self.trace_id,
            "x-span-id": self.span_id,
        }

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> "TraceContext":
        """Create from HTTP headers.

        Args:
            headers: Headers dictionary.

        Returns:
            TraceContext instance.
        """
        trace_id = headers.get("x-trace-id") or str(uuid.uuid4())
        span_id = headers.get("x-span-id") or str(uuid.uuid4())
        return cls(trace_id=trace_id, span_id=span_id)


# ============================================================================
# Tracer
# ============================================================================


class Tracer:
    """Tracer for creating and managing spans.

    Usage:
        tracer = Tracer("service-name")

        with tracer.start_span("operation") as span:
            span.add_attribute("key", "value")
            # ... do work ...
    """

    def __init__(self, service_name: str):
        """Initialize tracer.

        Args:
            service_name: Name of the service.
        """
        self.service_name = service_name
        self.spans: List[Span] = []
        self.active_span: Optional[Span] = None
        self.root_span: Optional[Span] = None

    def start_span(
        self,
        name: str,
        parent: Optional[Span] = None,
        attributes: Dict[str, Any] = None,
    ) -> "SpanContext":
        """Start a new span.

        Args:
            name: Span name.
            parent: Parent span (if any).
            attributes: Optional initial attributes.

        Returns:
            SpanContext context manager.
        """
        trace_id = self.root_span.trace_id if self.root_span else str(uuid.uuid4())
        parent_id = parent.span_id if parent else None

        span = Span(
            name=name,
            trace_id=trace_id,
            parent_id=parent_id,
            attributes=attributes or {},
        )

        if not self.root_span:
            self.root_span = span

        return SpanContext(self, span)

    def end_span(self, span: Span):
        """End a span.

        Args:
            span: Span to end.
        """
        span.end()
        self.spans.append(span)

    def export_traces(self) -> List[Dict[str, Any]]:
        """Export all recorded spans.

        Returns:
            List of span dictionaries.
        """
        return [span.to_dict() for span in self.spans]

    def export_json(self) -> str:
        """Export traces as JSON.

        Returns:
            JSON string.
        """
        import json

        return json.dumps(self.export_traces(), indent=2, default=str)

    def get_trace_tree(self) -> Dict[str, Any]:
        """Get trace as tree structure.

        Returns:
            Tree structure with spans.
        """
        def build_tree(parent_id: Optional[str]) -> Dict[str, Any]:
            children = []
            for span in self.spans:
                if span.parent_id == parent_id:
                    children.append({
                        "name": span.name,
                        "span_id": span.span_id,
                        "duration_ms": span.duration_ms(),
                        "status": span.status,
                        "attributes": span.attributes,
                        "children": build_tree(span.span_id),
                    })
            return children

        if not self.root_span:
            return {}

        return {
            "name": self.root_span.name,
            "trace_id": self.root_span.trace_id,
            "span_id": self.root_span.span_id,
            "duration_ms": self.root_span.duration_ms(),
            "status": self.root_span.status,
            "attributes": self.root_span.attributes,
            "children": build_tree(self.root_span.span_id),
        }

    def get_summary(self) -> str:
        """Get summary of traces.

        Returns:
            Summary string.
        """
        total_duration = sum(span.duration_ms() for span in self.spans)
        errors = sum(1 for span in self.spans if span.status == SpanStatus.ERROR)

        return (
            f"Trace: {self.root_span.name if self.root_span else 'unknown'}\n"
            f"  Total duration: {total_duration:.2f}ms\n"
            f"  Spans: {len(self.spans)}\n"
            f"  Errors: {errors}"
        )


# ============================================================================
# SpanContext
# ============================================================================


class SpanContext:
    """Context manager for spans.

    Usage:
        with tracer.start_span("operation") as span:
            span.add_event("step_1")
            # ... work ...
    """

    def __init__(self, tracer: Tracer, span: Span):
        """Initialize span context.

        Args:
            tracer: Parent tracer.
            span: Span object.
        """
        self.tracer = tracer
        self.span = span
        self.tracer.active_span = span

    def __enter__(self) -> Span:
        """Enter context."""
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        if exc_type is not None:
            self.span.set_status(SpanStatus.ERROR)
            self.span.add_event(
                "exception",
                {
                    "exception.type": exc_type.__name__,
                    "exception.message": str(exc_val),
                },
            )
        else:
            self.span.set_status(SpanStatus.OK)

        self.tracer.end_span(self.span)
        self.tracer.active_span = None


# ============================================================================
# Global Tracer Instance
# ============================================================================

_global_tracer: Optional[Tracer] = None


def get_tracer(service_name: str = "agent") -> Tracer:
    """Get or create global tracer.

    Args:
        service_name: Service name for tracer.

    Returns:
        Global tracer instance.
    """
    global _global_tracer

    if _global_tracer is None:
        _global_tracer = Tracer(service_name)

    return _global_tracer


def reset_tracer():
    """Reset global tracer."""
    global _global_tracer
    _global_tracer = None


# Export public API
__all__ = [
    # Status
    "SpanStatus",
    # Classes
    "SpanEvent",
    "Span",
    "Tracer",
    "TraceContext",
    "SpanContext",
    # Functions
    "get_tracer",
    "reset_tracer",
]
