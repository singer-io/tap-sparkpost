"""Metrics Delay Reason stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsDelayReason(MetricsBaseStream):
    """Stream for retrieving delay reason metrics."""
    tap_stream_id = "metrics_delay_reason"
    key_properties = ["reason"]
    data_key = "results"
    path = "metrics/deliverability/delay-reason"

    # Override with delay-specific metrics
    default_metrics = ["count_delayed", "count_delayed_first"]
