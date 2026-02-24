"""Sending Domains stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class SendingDomains(FullTableStream):
    """Stream for retrieving sending domain configurations."""
    tap_stream_id = "sending_domains"
    key_properties = ["domain"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "sending-domains"
