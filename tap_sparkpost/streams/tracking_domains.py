"""Tracking Domains stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class TrackingDomains(FullTableStream):
    """Stream for retrieving tracking domain configurations."""
    tap_stream_id = "tracking_domains"
    key_properties = ["domain"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "tracking-domains"
