"""Metrics Rejection Reason By Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsRejectionReasonByDomain(MetricsBaseStream):
    """Stream for retrieving rejection reason by domain metrics."""
    tap_stream_id = "metrics_rejection_reason_by_domain"
    key_properties = ["reason", "domain", "rejection_category_id"]
    data_key = "results"
    path = "metrics/deliverability/rejection-reason/domain"

    # Override with rejection-specific metrics
    default_metrics = [
        "count_policy_rejection",
        "count_generation_rejection",
        "count_generation_failed"
    ]
