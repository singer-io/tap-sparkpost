"""Recipient Lists stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class RecipientLists(FullTableStream):
    """Stream for retrieving recipient lists."""
    tap_stream_id = "recipient_lists"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "recipient-lists"
