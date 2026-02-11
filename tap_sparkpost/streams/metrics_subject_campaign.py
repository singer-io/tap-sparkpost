"""Metrics Subject Campaign stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsSubjectCampaign(MetricsBaseStream):
    """Stream for retrieving subject campaign metrics (Deliverability Add-On)."""
    tap_stream_id = "metrics_subject_campaign"
    key_properties = ["timestamp", "subject_campaign"]
    data_key = "results"
    path = "metrics/deliverability/subject-campaign"
    # Subject campaign supports deliverability add-on metrics only
    default_metrics = ["count_inbox_panel", "count_spam_panel"]
