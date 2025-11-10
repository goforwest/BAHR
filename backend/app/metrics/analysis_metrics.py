"""Prometheus metrics stubs for verse analysis.
Implement instrumentation in main application later.
"""
try:
    from prometheus_client import Histogram, Counter
except ImportError:  # allow import even if dependency not installed yet
    Histogram = Counter = None  # type: ignore

VERSE_ANALYSIS_LATENCY = Histogram(
    "verse_analysis_latency_seconds",
    "Latency of single verse prosody analysis",
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1, 2, 3)
) if Histogram else None

ANALYSIS_TIMEOUTS = Counter(
    "analysis_timeouts_total",
    "Total analysis timeouts triggering fallback"
) if Counter else None

def record_latency(seconds: float) -> None:
    if VERSE_ANALYSIS_LATENCY:
        VERSE_ANALYSIS_LATENCY.observe(seconds)

def inc_timeout() -> None:
    if ANALYSIS_TIMEOUTS:
        ANALYSIS_TIMEOUTS.inc()
