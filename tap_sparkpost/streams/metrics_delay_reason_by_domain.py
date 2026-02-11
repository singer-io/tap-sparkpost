"""Metrics Delay Reason By Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsDelayReasonByDomain(MetricsBaseStream):
    """Stream for retrieving delay reason by domain metrics."""
    tap_stream_id = "metrics_delay_reason_by_domain"
    key_properties = ["timestamp", "reason", "domain"]
    data_key = "results"
    path = "metrics/deliverability/delay-reason/domain"

    # Override with delay-specific metrics
    default_metrics = ["count_delayed", "count_delayed_first"]
