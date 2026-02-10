"""Metrics Watched Domain stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsWatchedDomain(MetricsBaseStream):
    """Stream for retrieving watched domain metrics."""
    tap_stream_id = "metrics_watched_domain"
    key_properties = ["watched_domain"]
    data_key = "results"
    path = "metrics/deliverability/watched-domain"
