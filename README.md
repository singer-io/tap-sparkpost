# tap-sparkpost

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This tap:

- Pulls raw data from the [Sparkpost API](https://developers.sparkpost.com/api/).
- Extracts the following resources:
    - [Events](https://developers.sparkpost.com/api/events/)

    - [Webhooks](https://developers.sparkpost.com/api/webhooks/)

    - [Templates](https://developers.sparkpost.com/api/templates/)

    - [SendingDomains](https://developers.sparkpost.com/api/sending-domains/)

    - [TrackingDomains](https://developers.sparkpost.com/api/tracking-domains/)

    - [SuppressionList](https://developers.sparkpost.com/api/suppression-list/)

    - [RecipientLists](https://developers.sparkpost.com/api/recipient-lists/)

    - [Account](https://developers.sparkpost.com/api/account/)

    - [Usage](https://developers.sparkpost.com/api/usage/)

    - [Subaccounts](https://developers.sparkpost.com/api/subaccounts/)

    - [IpPools](https://developers.sparkpost.com/api/ip-pools/)

    - [MetricsRecipientDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-recipient-domain)

    - [MetricsSendingIp](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-sending-ip)

    - [MetricsIpPool](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-ip-pool)

    - [MetricsSendingDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-sending-domain)

    - [MetricsSubaccount](https://developers.sparkpost.com/api/metrics/)

    - [MetricsCampaign](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-campaign)

    - [MetricsTemplate](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-template)

    - [MetricsSubjectCampaign](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-subject-campaign)

    - [MetricsWatchedDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-watched-domain)

    - [MetricsMailboxProvider](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-mailbox-provider)

    - [MetricsMailboxProviderRegion](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-mailbox-provider-region)

    - [MetricsTimeSeries](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics)

    - [MetricsBounceReason](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-reason-metrics)

    - [MetricsBounceReasonByDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-reason-metrics-by-domain)

    - [MetricsBounceClassification](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-classification-metrics)

    - [MetricsRejectionReason](https://developers.sparkpost.com/api/metrics/#metrics-get-rejection-reason-metrics)

    - [MetricsRejectionReasonByDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-rejection-reason-metrics-by-domain)

    - [MetricsDelayReason](https://developers.sparkpost.com/api/metrics/#metrics-get-delay-reason-metrics)

    - [MetricsDelayReasonByDomain](https://developers.sparkpost.com/api/metrics/#metrics-get-delay-reason-metrics-by-domain)

    - [MetricsEngagementDetails](https://developers.sparkpost.com/api/metrics/#metrics-get-engagement-details)

    - [MetricsDeliveriesByAttempt](https://developers.sparkpost.com/api/metrics/#metrics-get-deliveries-by-attempt)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams


**[events](https://developers.sparkpost.com/api/events/)**
- Data Key = results
- Primary keys: ['event_id']
- Replication strategy: INCREMENTAL

**[webhooks](https://developers.sparkpost.com/api/webhooks/)**
- Data Key = results
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[templates](https://developers.sparkpost.com/api/templates/)**
- Data Key = results
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[sending_domains](https://developers.sparkpost.com/api/sending-domains/)**
- Data Key = results
- Primary keys: ['domain']
- Replication strategy: FULL_TABLE

**[tracking_domains](https://developers.sparkpost.com/api/tracking-domains/)**
- Data Key = results
- Primary keys: ['domain']
- Replication strategy: FULL_TABLE

**[suppression_list](https://developers.sparkpost.com/api/suppression-list/)**
- Data Key = results
- Primary keys: ['recipient']
- Replication strategy: FULL_TABLE

**[recipient_lists](https://developers.sparkpost.com/api/recipient-lists/)**
- Data Key = results
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[account](https://developers.sparkpost.com/api/account/)**
- Data Key = results
- Primary keys: ['customer_id']
- Replication strategy: FULL_TABLE

**[usage](https://developers.sparkpost.com/api/usage/)**
- Data Key = results
- Primary keys: ['timestamp']
- Replication strategy: FULL_TABLE

**[subaccounts](https://developers.sparkpost.com/api/subaccounts/)**
- Data Key = results
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[ip_pools](https://developers.sparkpost.com/api/ip-pools/)**
- Data Key = results
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[metrics_recipient_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-recipient-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'domain']
- Replication strategy: INCREMENTAL

**[metrics_sending_ip](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-sending-ip)**
- Data Key = results
- Primary keys: ['timestamp', 'sending_ip']
- Replication strategy: INCREMENTAL

**[metrics_ip_pool](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-ip-pool)**
- Data Key = results
- Primary keys: ['timestamp', 'ip_pool']
- Replication strategy: INCREMENTAL

**[metrics_sending_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-sending-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'sending_domain']
- Replication strategy: INCREMENTAL

**[metrics_subaccount](https://developers.sparkpost.com/api/metrics/)**
- Data Key = results
- Primary keys: ['timestamp', 'subaccount_id']
- Replication strategy: INCREMENTAL

**[metrics_campaign](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-campaign)**
- Data Key = results
- Primary keys: ['timestamp', 'campaign_id']
- Replication strategy: INCREMENTAL

**[metrics_template](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-template)**
- Data Key = results
- Primary keys: ['timestamp', 'template_id']
- Replication strategy: INCREMENTAL

**[metrics_subject_campaign](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-subject-campaign)**
- Data Key = results
- Primary keys: ['timestamp', 'subject_campaign']
- Replication strategy: INCREMENTAL

**[metrics_watched_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-watched-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'watched_domain']
- Replication strategy: INCREMENTAL

**[metrics_mailbox_provider](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-mailbox-provider)**
- Data Key = results
- Primary keys: ['timestamp', 'mailbox_provider']
- Replication strategy: INCREMENTAL

**[metrics_mailbox_provider_region](https://developers.sparkpost.com/api/metrics/#metrics-get-metrics-by-mailbox-provider-region)**
- Data Key = results
- Primary keys: ['timestamp', 'mailbox_provider_region']
- Replication strategy: INCREMENTAL

**[metrics_time_series](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics)**
- Data Key = results
- Primary keys: ['timestamp']
- Replication strategy: INCREMENTAL
- **Supports precision parameter**: Controls aggregation level (1min, 5min, 15min, hour, 12hr, day, week, month)

**[metrics_bounce_reason](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-reason-metrics)**
- Data Key = results
- Primary keys: ['timestamp', 'reason', 'classification_id']
- Replication strategy: INCREMENTAL

**[metrics_bounce_reason_by_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-reason-metrics-by-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'reason', 'domain', 'classification_id']
- Replication strategy: INCREMENTAL

**[metrics_bounce_classification](https://developers.sparkpost.com/api/metrics/#metrics-get-bounce-classification-metrics)**
- Data Key = results
- Primary keys: ['timestamp', 'classification_id']
- Replication strategy: INCREMENTAL

**[metrics_rejection_reason](https://developers.sparkpost.com/api/metrics/#metrics-get-rejection-reason-metrics)**
- Data Key = results
- Primary keys: ['timestamp', 'reason', 'rejection_category_id']
- Replication strategy: INCREMENTAL

**[metrics_rejection_reason_by_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-rejection-reason-metrics-by-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'reason', 'domain', 'rejection_category_id']
- Replication strategy: INCREMENTAL

**[metrics_delay_reason](https://developers.sparkpost.com/api/metrics/#metrics-get-delay-reason-metrics)**
- Data Key = results
- Primary keys: ['timestamp', 'reason']
- Replication strategy: INCREMENTAL

**[metrics_delay_reason_by_domain](https://developers.sparkpost.com/api/metrics/#metrics-get-delay-reason-metrics-by-domain)**
- Data Key = results
- Primary keys: ['timestamp', 'reason', 'domain']
- Replication strategy: INCREMENTAL

**[metrics_engagement_details](https://developers.sparkpost.com/api/metrics/#metrics-get-engagement-details)**
- Data Key = results
- Primary keys: ['timestamp', 'link_name']
- Replication strategy: INCREMENTAL

**[metrics_deliveries_by_attempt](https://developers.sparkpost.com/api/metrics/#metrics-get-deliveries-by-attempt)**
- Data Key = results
- Primary keys: ['timestamp', 'attempt']
- Replication strategy: INCREMENTAL



## Authentication

## Quick Start

1. Install

    Clone this repository, and then install using setup.py. We recommend using a virtualenv:

    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > python setup.py install
    OR
    > cd .../tap-sparkpost
    > pip install -e .
    ```
2. Dependent libraries. The following dependent libraries were installed.
    ```bash
    > pip install singer-python
    > pip install target-stitch
    > pip install target-json

    ```
    - [singer-tools](https://github.com/singer-io/singer-tools)
    - [target-stitch](https://github.com/singer-io/target-stitch)

3. Create your tap's `config.json` file.  The tap config file for this tap should include these entries:
   - `api_key` (string, required): Your SparkPost API key
   - `start_date` (string, required): The default value to use if no bookmark exists for an endpoint (rfc3339 date string). Example: `"2019-01-01T00:00:00Z"`
   - `request_timeout` (integer, optional): Max time in seconds for request to wait for response. Default: `300`
   - `precision` (string, optional): **Time-series metrics only**. Controls aggregation level for [metrics_time_series](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics) endpoint. Default: `"day"`

    **Precision Parameter Values:**

    The `precision` parameter is **only applicable to the metrics_time_series stream**. It controls how data is aggregated across time:

    - `"1min"`: 1-minute aggregation - Returns metrics aggregated in 1-minute intervals
    - `"5min"`: 5-minute aggregation - Returns metrics aggregated in 5-minute intervals
    - `"15min"`: 15-minute aggregation - Returns metrics aggregated  in 15-minute intervals
    - `"hour"`: Hourly aggregation - Returns metrics aggregated in 1-hour intervals
    - `"12hr"`: 12-hour aggregation - Returns metrics aggregated in 12-hour intervals
    - `"day"`: Daily aggregation (default) - Returns metrics aggregated per day
    - `"week"`: Weekly aggregation - Returns metrics aggregated per week
    - `"month"`: Monthly aggregation - Returns metrics aggregated per month

    **Important Notes:**
    - Precision parameter is **NOT supported** by other metrics endpoints (metrics_recipient_domain, metrics_sending_ip, etc.)
    - Once a sync begins with a specific precision, do not change it during the sync to avoid mixed aggregation levels
    - Smaller precision values (1min, 5min) will return more granular data but may impact API performance
    - Reference: [SparkPost Time-Series Metrics API](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics)

    **Example config.json:**

    ```json
    {
        "api_key": "your_sparkpost_api_key_here",
        "start_date": "2019-01-01T00:00:00Z",
        "request_timeout": 300,
        "precision": "day"
    }

    ```
    Optionally, also create a `state.json` file. `currently_syncing` is an optional attribute used for identifying the last object to be synced in case the job is interrupted mid-stream. The next run would begin where the last job left off.

    ```json
    {
        "currently_syncing": "dummy_stream1",
        "bookmarks": {
            "dummy_stream1": "2019-09-27T22:34:39.000000Z",
            "dummy_stream2": "2019-09-28T15:30:26.000000Z",
            "dummy_stream3": "2019-09-28T18:23:53Z"
        }
    }
    ```

4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-sparkpost --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-sparkpost --config tap_config.json --catalog catalog.json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To load to json files to verify outputs:
    ```bash
    > tap-sparkpost --config tap_config.json --catalog catalog.json | target-json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To pseudo-load to [Stitch Import API](https://github.com/singer-io/target-stitch) with dry run:
    ```bash
    > tap-sparkpost --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json --dry-run > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

6. Test the Tap
    While developing the sparkpost tap, the following utilities were run in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_sparkpost -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.67/10
    ```

    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap_sparkpost --config tap_config.json --catalog catalog.json | singer-check-tap > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

    #### Unit Tests

    Unit tests may be run with the following.

    ```
    python -m pytest --verbose
    ```

    Note, you may need to install test dependencies.

    ```
    pip install -e .'[dev]'
    ```
---

Copyright &copy; 2019 Stitch
