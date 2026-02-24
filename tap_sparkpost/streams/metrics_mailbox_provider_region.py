"""Metrics Mailbox Provider Region stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsMailboxProviderRegion(MetricsBaseStream):
    """Stream for retrieving mailbox provider region metrics."""
    tap_stream_id = "metrics_mailbox_provider_region"
    key_properties = ["timestamp", "mailbox_provider_region"]
    data_key = "results"
    path = "metrics/deliverability/mailbox-provider-region"
