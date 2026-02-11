"""Metrics Mailbox Provider stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsMailboxProvider(MetricsBaseStream):
    """Stream for retrieving mailbox provider metrics."""
    tap_stream_id = "metrics_mailbox_provider"
    key_properties = ["timestamp", "mailbox_provider"]
    data_key = "results"
    path = "metrics/deliverability/mailbox-provider"
