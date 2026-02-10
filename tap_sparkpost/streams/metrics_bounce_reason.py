"""Metrics Bounce Reason stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream, BOUNCE_METRICS

class MetricsBounceReason(MetricsBaseStream):
    """Stream for retrieving bounce reason metrics."""
    tap_stream_id = "metrics_bounce_reason"
    key_properties = ["reason", "classification_id"]
    data_key = "results"
    path = "metrics/deliverability/bounce-reason"

    # Override default metrics with bounce-specific metrics
    default_metrics = BOUNCE_METRICS
