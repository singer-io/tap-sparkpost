"""Webhooks stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import IncrementalStream

class Webhooks(IncrementalStream):
    """Stream for retrieving webhook configurations."""
    tap_stream_id = "webhooks"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["last_successful"]
    data_key = "results"
    path = "webhooks"
