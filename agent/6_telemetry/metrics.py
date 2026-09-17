"""
Performance metrics collection and reporting.

This module provides:
- Timing measurements for operations
- Counter tracking for events
- Gauge tracking for current values
- Metrics aggregation and reporting
- Export to different formats

Usage:
    from agent_6_telemetry.metrics import MetricsCollector, Timer

    # Create global metrics collector
    metrics = MetricsCollector()

    # Time an operation
    with Timer(metrics, "build_time_ms"):
        run_build()

    # Increment counter
    metrics.increment("tests_passed")
    metrics.increment("tests_failed")

    # Set gauge
    metrics.set_gauge("memory_mb", 512)

    # Get report
    report = metrics.get_report()
    print(report)
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
from statistics import mean, median, stdev


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class Metric:
    """Single metric value."""

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    unit: str = ""
    labels: Dict[str, str] = field(default_factory=dict)

    def __repr__(self) -> str:
        """String representation."""
        unit_str = f" {self.unit}" if self.unit else ""
        return f"{self.name}={self.value}{unit_str}"


@dataclass
class Counter:
    """Counter metric (monotonically increasing)."""

    name: str
    value: int = 0
    created: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

    def increment(self, amount: int = 1):
        """Increment counter.

        Args:
            amount: Amount to increment by.
        """
        self.value += amount

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.name}={self.value}"


@dataclass
class Gauge:
    """Gauge metric (current value)."""

    name: str
    value: float = 0
    updated: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

    def set(self, value: float):
        """Set gauge value.

        Args:
            value: New value.
        """
        self.value = value
        self.updated = datetime.now()

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.name}={self.value}"


@dataclass
class Histogram:
    """Histogram metric (distribution of values)."""

    name: str
    values: List[float] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

    def observe(self, value: float):
        """Record value.

        Args:
            value: Value to record.
        """
        self.values.append(value)

    def count(self) -> int:
        """Get count of observations.

        Returns:
            Number of observations.
        """
        return len(self.values)

    def sum(self) -> float:
        """Get sum of values.

        Returns:
            Sum of all values.
        """
        return sum(self.values) if self.values else 0.0

    def mean(self) -> float:
        """Get mean of values.

        Returns:
            Mean value.
        """
        return mean(self.values) if self.values else 0.0

    def median(self) -> float:
        """Get median of values.

        Returns:
            Median value.
        """
        return median(self.values) if self.values else 0.0

    def min(self) -> float:
        """Get minimum value.

        Returns:
            Minimum value.
        """
        return min(self.values) if self.values else 0.0

    def max(self) -> float:
        """Get maximum value.

        Returns:
            Maximum value.
        """
        return max(self.values) if self.values else 0.0

    def stdev(self) -> float:
        """Get standard deviation.

        Returns:
            Standard deviation.
        """
        if len(self.values) < 2:
            return 0.0
        return stdev(self.values)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"{self.name}(count={self.count()}, "
            f"mean={self.mean():.2f}, "
            f"median={self.median():.2f})"
        )


# ============================================================================
# Timer Context Manager
# ============================================================================


class Timer:
    """Context manager for timing operations.

    Usage:
        with Timer(metrics, "operation_time_ms"):
            do_something()
    """

    def __init__(
        self,
        metrics: "MetricsCollector",
        metric_name: str,
        labels: Optional[Dict[str, str]] = None,
    ):
        """Initialize timer.

        Args:
            metrics: MetricsCollector instance.
            metric_name: Name of metric to record to.
            labels: Optional labels for metric.
        """
        self.metrics = metrics
        self.metric_name = metric_name
        self.labels = labels or {}
        self.start_time = None
        self.duration_ms = None

    def __enter__(self):
        """Enter context."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        self.duration_ms = (time.time() - self.start_time) * 1000
        self.metrics.observe_histogram(
            self.metric_name,
            self.duration_ms,
            labels=self.labels,
        )


# ============================================================================
# MetricsCollector
# ============================================================================


class MetricsCollector:
    """Central metrics collection system.

    Collects counters, gauges, histograms, and timing information.
    """

    def __init__(self):
        """Initialize metrics collector."""
        self.counters: Dict[str, Counter] = {}
        self.gauges: Dict[str, Gauge] = {}
        self.histograms: Dict[str, Histogram] = {}
        self.created = datetime.now()

    # ========== Counters ==========

    def increment(self, name: str, amount: int = 1, labels: Dict[str, str] = None):
        """Increment counter.

        Args:
            name: Counter name.
            amount: Amount to increment by.
            labels: Optional labels.
        """
        if name not in self.counters:
            self.counters[name] = Counter(name, labels=labels or {})

        self.counters[name].increment(amount)

    def get_counter(self, name: str) -> Optional[int]:
        """Get counter value.

        Args:
            name: Counter name.

        Returns:
            Counter value or None if not found.
        """
        return self.counters[name].value if name in self.counters else None

    # ========== Gauges ==========

    def set_gauge(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] = None,
    ):
        """Set gauge value.

        Args:
            name: Gauge name.
            value: Value to set.
            labels: Optional labels.
        """
        if name not in self.gauges:
            self.gauges[name] = Gauge(name, labels=labels or {})

        self.gauges[name].set(value)

    def get_gauge(self, name: str) -> Optional[float]:
        """Get gauge value.

        Args:
            name: Gauge name.

        Returns:
            Gauge value or None if not found.
        """
        return self.gauges[name].value if name in self.gauges else None

    # ========== Histograms ==========

    def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] = None,
    ):
        """Record histogram value.

        Args:
            name: Histogram name.
            value: Value to record.
            labels: Optional labels.
        """
        if name not in self.histograms:
            self.histograms[name] = Histogram(name, labels=labels or {})

        self.histograms[name].observe(value)

    def get_histogram(self, name: str) -> Optional[Histogram]:
        """Get histogram.

        Args:
            name: Histogram name.

        Returns:
            Histogram object or None if not found.
        """
        return self.histograms.get(name)

    # ========== Reporting ==========

    def get_report(self) -> Dict[str, Any]:
        """Get metrics report.

        Returns:
            Dictionary with all metrics.
        """
        uptime = datetime.now() - self.created

        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime.total_seconds(),
            "counters": {
                name: counter.value
                for name, counter in self.counters.items()
            },
            "gauges": {
                name: gauge.value
                for name, gauge in self.gauges.items()
            },
            "histograms": {
                name: {
                    "count": hist.count(),
                    "sum": hist.sum(),
                    "mean": hist.mean(),
                    "median": hist.median(),
                    "min": hist.min(),
                    "max": hist.max(),
                    "stdev": hist.stdev(),
                }
                for name, hist in self.histograms.items()
            },
        }

    def get_summary(self) -> str:
        """Get summary string for logging.

        Returns:
            Summary string.
        """
        lines = ["=== Metrics Summary ==="]

        if self.counters:
            lines.append("Counters:")
            for name, counter in self.counters.items():
                lines.append(f"  {name}: {counter.value}")

        if self.gauges:
            lines.append("Gauges:")
            for name, gauge in self.gauges.items():
                lines.append(f"  {name}: {gauge.value}")

        if self.histograms:
            lines.append("Histograms:")
            for name, hist in self.histograms.items():
                lines.append(
                    f"  {name}: count={hist.count()}, "
                    f"mean={hist.mean():.2f}, "
                    f"median={hist.median():.2f}, "
                    f"min={hist.min():.2f}, "
                    f"max={hist.max():.2f}"
                )

        return "\n".join(lines)

    def reset(self):
        """Reset all metrics."""
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
        self.created = datetime.now()


# ============================================================================
# Specialized Metrics
# ============================================================================


class BuildMetrics:
    """Metrics specific to build operations."""

    def __init__(self, collector: MetricsCollector):
        """Initialize build metrics.

        Args:
            collector: MetricsCollector instance.
        """
        self.collector = collector

    def record_build_start(self, stage: str):
        """Record build stage start.

        Args:
            stage: Build stage name.
        """
        pass  # Marker for logging

    def record_build_stage_complete(self, stage: str, duration_ms: float):
        """Record build stage completion.

        Args:
            stage: Build stage name.
            duration_ms: Duration in milliseconds.
        """
        self.collector.observe_histogram(
            f"build_stage_{stage}_ms",
            duration_ms,
        )
        self.collector.increment(f"build_stage_{stage}_count")

    def record_build_artifact(self, name: str, size_bytes: int):
        """Record build artifact.

        Args:
            name: Artifact name.
            size_bytes: Artifact size in bytes.
        """
        self.collector.set_gauge(
            f"artifact_{name}_bytes",
            size_bytes,
        )

    def record_build_error(self, stage: str):
        """Record build error.

        Args:
            stage: Build stage where error occurred.
        """
        self.collector.increment(f"build_errors_{stage}")


class TestMetrics:
    """Metrics specific to test execution."""

    def __init__(self, collector: MetricsCollector):
        """Initialize test metrics.

        Args:
            collector: MetricsCollector instance.
        """
        self.collector = collector

    def record_test_result(
        self,
        suite: str,
        passed: int,
        failed: int,
        skipped: int,
        duration_ms: float,
    ):
        """Record test suite results.

        Args:
            suite: Test suite name.
            passed: Number of passed tests.
            failed: Number of failed tests.
            skipped: Number of skipped tests.
            duration_ms: Duration in milliseconds.
        """
        self.collector.increment(f"tests_passed", passed)
        self.collector.increment(f"tests_failed", failed)
        self.collector.increment(f"tests_skipped", skipped)
        self.collector.observe_histogram(
            f"test_suite_{suite}_ms",
            duration_ms,
        )

    def record_coverage(self, suite: str, coverage_percent: float):
        """Record code coverage.

        Args:
            suite: Test suite name.
            coverage_percent: Coverage percentage.
        """
        self.collector.set_gauge(f"coverage_{suite}_percent", coverage_percent)


# Export public API
__all__ = [
    # Data classes
    "Metric",
    "Counter",
    "Gauge",
    "Histogram",
    # Timer
    "Timer",
    # Collector
    "MetricsCollector",
    # Specialized
    "BuildMetrics",
    "TestMetrics",
]
