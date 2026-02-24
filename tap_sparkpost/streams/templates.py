"""Templates stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class Templates(FullTableStream):
    """Stream for retrieving email templates."""
    tap_stream_id = "templates"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "templates"
