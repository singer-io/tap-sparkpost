"""Metrics Sending IP stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsSendingIp(MetricsBaseStream):
    """Stream for retrieving sending IP metrics."""
    tap_stream_id = "metrics_sending_ip"
    key_properties = ["timestamp", "sending_ip"]
    data_key = "results"
    path = "metrics/deliverability/sending-ip"
