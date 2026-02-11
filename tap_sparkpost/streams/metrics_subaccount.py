"""Metrics Subaccount stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsSubaccount(MetricsBaseStream):
    """Stream for retrieving subaccount metrics."""
    tap_stream_id = "metrics_subaccount"
    key_properties = ["timestamp", "subaccount_id"]
    data_key = "results"
    path = "metrics/deliverability/subaccount"
