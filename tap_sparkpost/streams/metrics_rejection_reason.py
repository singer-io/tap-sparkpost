"""Metrics Rejection Reason stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsRejectionReason(MetricsBaseStream):
    """Stream for retrieving rejection reason metrics."""
    tap_stream_id = "metrics_rejection_reason"
    key_properties = ["reason", "rejection_category_id"]
    data_key = "results"
    path = "metrics/deliverability/rejection-reason"

    # Override with rejection-specific metrics
    default_metrics = [
        "count_policy_rejection",
        "count_generation_rejection",
        "count_generation_failed"
    ]
