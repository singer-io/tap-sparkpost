"""Metrics IP Pool stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsIpPool(MetricsBaseStream):
    """Stream for retrieving IP pool metrics."""
    tap_stream_id = "metrics_ip_pool"
    key_properties = ["ip_pool"]
    data_key = "results"
    path = "metrics/deliverability/ip-pool"
