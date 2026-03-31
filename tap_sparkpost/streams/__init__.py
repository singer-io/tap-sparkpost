"""Stream definitions for SparkPost tap."""
from tap_sparkpost.streams.events import Events
from tap_sparkpost.streams.webhooks import Webhooks
from tap_sparkpost.streams.templates import Templates
from tap_sparkpost.streams.sending_domains import SendingDomains
from tap_sparkpost.streams.tracking_domains import TrackingDomains
from tap_sparkpost.streams.suppression_list import SuppressionList
from tap_sparkpost.streams.recipient_lists import RecipientLists
from tap_sparkpost.streams.account import Account
from tap_sparkpost.streams.usage import Usage
from tap_sparkpost.streams.subaccounts import Subaccounts
from tap_sparkpost.streams.ip_pools import IpPools
from tap_sparkpost.streams.metrics_recipient_domain import MetricsRecipientDomain
from tap_sparkpost.streams.metrics_sending_ip import MetricsSendingIp
from tap_sparkpost.streams.metrics_ip_pool import MetricsIpPool
from tap_sparkpost.streams.metrics_sending_domain import MetricsSendingDomain
from tap_sparkpost.streams.metrics_subaccount import MetricsSubaccount
from tap_sparkpost.streams.metrics_campaign import MetricsCampaign
from tap_sparkpost.streams.metrics_template import MetricsTemplate
from tap_sparkpost.streams.metrics_subject_campaign import MetricsSubjectCampaign
from tap_sparkpost.streams.metrics_watched_domain import MetricsWatchedDomain
from tap_sparkpost.streams.metrics_mailbox_provider import MetricsMailboxProvider
from tap_sparkpost.streams.metrics_mailbox_provider_region import MetricsMailboxProviderRegion
from tap_sparkpost.streams.metrics_time_series import MetricsTimeSeries
from tap_sparkpost.streams.metrics_bounce_reason import MetricsBounceReason
from tap_sparkpost.streams.metrics_bounce_reason_by_domain import MetricsBounceReasonByDomain
from tap_sparkpost.streams.metrics_bounce_classification import MetricsBounceClassification
from tap_sparkpost.streams.metrics_rejection_reason import MetricsRejectionReason
from tap_sparkpost.streams.metrics_rejection_reason_by_domain import MetricsRejectionReasonByDomain
from tap_sparkpost.streams.metrics_delay_reason import MetricsDelayReason
from tap_sparkpost.streams.metrics_delay_reason_by_domain import MetricsDelayReasonByDomain
from tap_sparkpost.streams.metrics_engagement_details import MetricsEngagementDetails
from tap_sparkpost.streams.metrics_deliveries_by_attempt import MetricsDeliveriesByAttempt

STREAMS = {
    "events": Events,
    "webhooks": Webhooks,
    "templates": Templates,
    "sending_domains": SendingDomains,
    "tracking_domains": TrackingDomains,
    "suppression_list": SuppressionList,
    "recipient_lists": RecipientLists,
    "account": Account,
    "usage": Usage,
    "subaccounts": Subaccounts,
    "ip_pools": IpPools,
    "metrics_recipient_domain": MetricsRecipientDomain,
    "metrics_sending_ip": MetricsSendingIp,
    "metrics_ip_pool": MetricsIpPool,
    "metrics_sending_domain": MetricsSendingDomain,
    "metrics_subaccount": MetricsSubaccount,
    "metrics_campaign": MetricsCampaign,
    "metrics_template": MetricsTemplate,
    "metrics_subject_campaign": MetricsSubjectCampaign,
    "metrics_watched_domain": MetricsWatchedDomain,
    "metrics_mailbox_provider": MetricsMailboxProvider,
    "metrics_mailbox_provider_region": MetricsMailboxProviderRegion,
    "metrics_time_series": MetricsTimeSeries,
    "metrics_bounce_reason": MetricsBounceReason,
    "metrics_bounce_reason_by_domain": MetricsBounceReasonByDomain,
    "metrics_bounce_classification": MetricsBounceClassification,
    "metrics_rejection_reason": MetricsRejectionReason,
    "metrics_rejection_reason_by_domain": MetricsRejectionReasonByDomain,
    "metrics_delay_reason": MetricsDelayReason,
    "metrics_delay_reason_by_domain": MetricsDelayReasonByDomain,
    "metrics_engagement_details": MetricsEngagementDetails,
    "metrics_deliveries_by_attempt": MetricsDeliveriesByAttempt,
}
