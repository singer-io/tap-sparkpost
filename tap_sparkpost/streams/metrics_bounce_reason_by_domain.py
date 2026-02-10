"""Metrics Bounce Reason By Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream, BOUNCE_METRICS

class MetricsBounceReasonByDomain(MetricsBaseStream):
    """Stream for retrieving bounce reason by domain metrics."""
    tap_stream_id = "metrics_bounce_reason_by_domain"
    key_properties = ["reason", "domain", "classification_id"]
    data_key = "results"
    path = "metrics/deliverability/bounce-reason/domain"

    # Override default metrics with bounce-specific metrics
    default_metrics = BOUNCE_METRICS
