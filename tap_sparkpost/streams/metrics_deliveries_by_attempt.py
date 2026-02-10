"""Metrics Deliveries By Attempt stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsDeliveriesByAttempt(MetricsBaseStream):
    """Stream for retrieving deliveries by attempt metrics."""
    tap_stream_id = "metrics_deliveries_by_attempt"
    key_properties = ["attempt"]
    data_key = "results"
    path = "metrics/deliverability/attempt"

    # Override with delivery-specific metrics
    default_metrics = [
        "count_delivered",
        "count_delivered_first",
        "count_delivered_subsequent"
    ]
