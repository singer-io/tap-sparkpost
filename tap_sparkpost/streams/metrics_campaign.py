"""Metrics Campaign stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsCampaign(MetricsBaseStream):
    """Stream for retrieving campaign metrics."""
    tap_stream_id = "metrics_campaign"
    key_properties = ["timestamp", "campaign_id"]
    data_key = "results"
    path = "metrics/deliverability/campaign"
