"""Subaccounts stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class Subaccounts(FullTableStream):
    """Stream for retrieving subaccount configurations."""
    tap_stream_id = "subaccounts"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "subaccounts"
    page_size = 100  # Subaccounts endpoint max per_page is 100
