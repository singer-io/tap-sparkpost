"""Events stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import IncrementalStream

class Events(IncrementalStream):
    """Stream for retrieving message events."""
    tap_stream_id = "events"
    key_properties = ["event_id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["timestamp"]
    data_key = "results"
    path = "events/message"
