"""Suppression List stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class SuppressionList(FullTableStream):
    """Stream for retrieving suppression list entries."""
    tap_stream_id = "suppression_list"
    key_properties = ["recipient"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "suppression-list"
