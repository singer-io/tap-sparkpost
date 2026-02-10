"""Metrics Bounce Classification stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream, BOUNCE_METRICS

class MetricsBounceClassification(MetricsBaseStream):
    """Stream for retrieving bounce classification metrics."""
    tap_stream_id = "metrics_bounce_classification"
    key_properties = ["classification_id"]
    data_key = "results"
    path = "metrics/deliverability/bounce-classification"

    # Override with bounce-specific metrics
    default_metrics = BOUNCE_METRICS
