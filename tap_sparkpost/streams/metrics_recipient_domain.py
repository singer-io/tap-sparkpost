"""Metrics Recipient Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsRecipientDomain(MetricsBaseStream):
    """Stream for retrieving recipient domain metrics."""
    tap_stream_id = "metrics_recipient_domain"
    key_properties = ["timestamp", "domain"]
    data_key = "results"
    path = "metrics/deliverability/domain"
