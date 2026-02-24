"""Metrics Sending Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsSendingDomain(MetricsBaseStream):
    """Stream for retrieving sending domain metrics."""
    tap_stream_id = "metrics_sending_domain"
    key_properties = ["timestamp", "sending_domain"]
    data_key = "results"
    path = "metrics/deliverability/sending-domain"
