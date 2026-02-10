"""Metrics Engagement Details stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsEngagementDetails(MetricsBaseStream):
    """Stream for retrieving engagement details metrics."""
    tap_stream_id = "metrics_engagement_details"
    key_properties = ["link_name"]
    data_key = "results"
    path = "metrics/deliverability/link-name"
    default_metrics = ["count_clicked", "count_raw_clicked"]
