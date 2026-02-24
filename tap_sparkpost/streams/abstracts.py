"""Base stream classes for SparkPost tap."""
from abc import ABC, abstractmethod
import json
from datetime import datetime
from typing import Any, Dict, Tuple, List, Iterator
from singer import (
    Transformer,
    get_bookmark,
    get_logger,
    metrics,
    write_bookmark,
    write_record,
    write_schema,
    metadata
)

LOGGER = get_logger()


class BaseStream(ABC):  # pylint: disable=too-many-instance-attributes
    """
    A Base Class providing structure and boilerplate for generic streams
    and required attributes for any kind of stream
    ~~~
    Provides:
     - Basic Attributes (stream_name,replication_method,key_properties)
     - Helper methods for catalog generation
     - `sync` and `get_records` method for performing sync
    """

    url_endpoint = ""
    path = ""
    page_size = 1000  # SparkPost default per_page value
    next_page_key = "links"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    children = []
    parent = ""
    data_key = "results"
    parent_bookmark_key = ""
    http_method = "GET"

    def __init__(self, client=None, catalog=None, config=None) -> None:
        self.client = client
        self.catalog = catalog
        self.config = config or {}
        self.schema = catalog.schema.to_dict()
        self.metadata = metadata.to_map(catalog.metadata)
        self.child_to_sync = []
        self.params = {}
        self.data_payload = {}

    @property
    @abstractmethod
    def tap_stream_id(self) -> str:
        """Unique identifier for the stream.

        This is allowed to be different from the name of the stream, in
        order to allow for sources that have duplicate stream names.
        """

    @property
    @abstractmethod
    def replication_method(self) -> str:
        """Defines the sync mode of a stream."""

    @property
    @abstractmethod
    def replication_keys(self) -> List:
        """Defines the replication key for incremental sync mode of a
        stream."""

    @property
    @abstractmethod
    def key_properties(self) -> Tuple[str, str]:
        """List of key properties for stream."""

    def is_selected(self):
        """Check if stream is selected in catalog."""
        return metadata.get(self.metadata, (), "selected")

    @abstractmethod
    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """
        Performs a replication sync for the stream.
        ~~~
        Args:
         - state (dict): represents the state file for the tap.
         - transformer (object): A Object of the singer.transformer class.
         - parent_obj (dict): The parent object for the stream.

        Returns:
         - bool: The return value. True for success, False otherwise.

        Docs:
         - https://github.com/singer-io/getting-started/blob/master/docs/SYNC_MODE.md
        """


    def get_records(self) -> Iterator:
        """Interacts with api client interaction and pagination.

        Uses cursor-based pagination as per SparkPost API documentation:
        - Start with cursor=initial for first page
        - Use links array from response for subsequent pages
        - per_page parameter controls page size (max 10,000)
        """
        self.params["per_page"] = self.page_size
        self.params["cursor"] = "initial"

        max_pages = 10000  # Safety limit for pagination
        current_page = 0

        while current_page < max_pages:
            response = self.client.make_request(
                self.http_method,
                self.url_endpoint,
                self.params,
                self.headers,
                body=json.dumps(self.data_payload) if self.data_payload else None,
                path=self.path
            )
            raw_records = response.get(self.data_key, [])

            # Yield records
            yield from raw_records

            # Check for next page in links array
            links = response.get(self.next_page_key, [])
            next_url = None

            # links is an array of objects with rel and href properties
            if isinstance(links, list):
                for link in links:
                    if link.get("rel") == "next":
                        next_url = link.get("href")
                        break

            if not next_url or "cursor=" not in next_url:
                break

            # Extract cursor from next URL
            # SparkPost returns full URL like:
            # /api/v1/events/message?events=delivery&per_page=1000&cursor=...
            cursor_param = next_url.split("cursor=")[1].split("&")[0]
            self.params["cursor"] = cursor_param
            current_page += 1

    def write_schema(self) -> None:
        """
        Write a schema message.
        """
        try:
            write_schema(self.tap_stream_id, self.schema, self.key_properties)
        except OSError as err:
            LOGGER.error(
                "OS Error while writing schema for: %s", self.tap_stream_id
            )
            raise err

    def update_params(self, **kwargs) -> None:
        """
        Update params for the stream
        """
        self.params.update(kwargs)

    def update_data_payload(self, **kwargs) -> None:
        """
        Update JSON body for the stream
        """
        self.data_payload.update(kwargs)

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        _ = parent_record  # Unused but kept for interface consistency
        return record

    def get_url_endpoint(self, parent_obj: Dict = None) -> str:
        """
        Get the URL endpoint for the stream
        """
        _ = parent_obj  # Unused but kept for interface consistency
        return self.url_endpoint or f"{self.client.base_url}/{self.path}"


class IncrementalStream(BaseStream):
    """Base Class for Incremental Stream."""


    def get_bookmark(self, state: dict, stream: str, key: Any = None) -> int:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""
        return get_bookmark(
            state,
            stream,
            key or self.replication_keys[0],
            self.client.config["start_date"],
        )

    def write_bookmark(
        self, state: dict, stream: str, key: Any = None, value: Any = None
    ) -> Dict:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""
        if not (key or self.replication_keys):
            return state

        bookmark_key = key or self.replication_keys[0]
        current_bookmark = get_bookmark(
            state, stream, bookmark_key, self.client.config["start_date"]
        )
        value = max(current_bookmark, value)
        return write_bookmark(state, stream, bookmark_key, value)

    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """Implementation for `type: Incremental` stream."""
        bookmark_date = self.get_bookmark(state, self.tap_stream_id)
        current_max_bookmark_date = bookmark_date
        # SparkPost API uses 'from' and 'to' parameters for date filtering
        # Format: YYYY-MM-DDTHH:MM:ssZ (UTC)
        # Use dict expansion since 'from' is a Python keyword
        self.update_params(**{"from": bookmark_date})
        self.update_data_payload(parent_obj=parent_obj)
        self.url_endpoint = self.get_url_endpoint(parent_obj)

        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in self.get_records():
                record = self.modify_object(record, parent_obj)
                transformed_record = transformer.transform(
                    record, self.schema, self.metadata
                )

                record_bookmark = transformed_record[self.replication_keys[0]]
                if record_bookmark >= bookmark_date:
                    if self.is_selected():
                        write_record(self.tap_stream_id, transformed_record)
                        counter.increment()

                    current_max_bookmark_date = max(
                        current_max_bookmark_date, record_bookmark
                    )

                    for child in self.child_to_sync:
                        child.sync(state=state, transformer=transformer, parent_obj=record)

            state = self.write_bookmark(state, self.tap_stream_id, value=current_max_bookmark_date)
            return counter.value


class FullTableStream(BaseStream):
    """Base Class for Full Table Stream."""

    replication_keys = []

    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """Abstract implementation for `type: Fulltable` stream."""
        self.url_endpoint = self.get_url_endpoint(parent_obj)
        self.update_data_payload(parent_obj=parent_obj)
        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in self.get_records():
                transformed_record = transformer.transform(
                    record, self.schema, self.metadata
                )
                if self.is_selected():
                    write_record(self.tap_stream_id, transformed_record)
                    counter.increment()

                for child in self.child_to_sync:
                    child.sync(state=state, transformer=transformer, parent_obj=record)

            return counter.value


class ParentBaseStream(IncrementalStream):
    """Base Class for Parent Stream."""

    def get_bookmark(self, state: Dict, stream: str, key: Any = None) -> int:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""

        min_parent_bookmark = (
            super().get_bookmark(state, stream) if self.is_selected() else None
        )
        for child in self.child_to_sync:
            bookmark_key = f"{self.tap_stream_id}_{self.replication_keys[0]}"
            child_bookmark = super().get_bookmark(
                state, child.tap_stream_id, key=bookmark_key
            )
            min_parent_bookmark = (
                min(min_parent_bookmark, child_bookmark)
                if min_parent_bookmark
                else child_bookmark
            )

        return min_parent_bookmark

    def write_bookmark(
        self, state: Dict, stream: str, key: Any = None, value: Any = None
    ) -> Dict:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""
        if self.is_selected():
            super().write_bookmark(state, stream, value=value)

        for child in self.child_to_sync:
            bookmark_key = f"{self.tap_stream_id}_{self.replication_keys[0]}"
            super().write_bookmark(
                state, child.tap_stream_id, key=bookmark_key, value=value
            )

        return state


# Shared metrics constants for subclasses to avoid duplicate-code
BOUNCE_METRICS = [
    "count_bounce",
    "count_inband_bounce",
    "count_outofband_bounce",
    "count_admin_bounce",
]


class MetricsBaseStream(IncrementalStream):
    """Base class for metrics streams with date-based incremental syncing.
    
    All SparkPost metrics endpoints require date parameters:
    - from: Required datetime parameter (YYYY-MM-DDTHH:MM)
    - to: Optional datetime parameter (defaults to now)
    - metrics: Required list of metrics to return

    Reference: https://developers.sparkpost.com/api/metrics/#header-metrics-api

    Note: The 'precision' parameter is ONLY supported by the time-series endpoint.
    Other metrics endpoints do not accept this parameter.
    See: https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics

    Uses start_date from config for initial sync, then bookmarks last sync date.
    """

    replication_keys = ["timestamp"]  # Timestamp field for metrics data
    replication_method = "INCREMENTAL"

    # Default metrics to fetch - can be overridden by subclasses
    default_metrics = ["count_targeted", "count_sent", "count_delivered"]

    def get_precision_params(self) -> Dict:
        """Get precision parameter for API request.

        Returns:
            Dict: Empty dict for most metrics endpoints.
                  Only time-series endpoint overrides this to return precision.

        Note:
            Precision parameter is ONLY valid for time-series metrics endpoint.
            Reference:
            https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics
        """
        return {}

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """Rename 'ts' field to 'timestamp' for metrics streams.

        The SparkPost API returns 'ts' field for time-series metrics,
        but schemas use 'timestamp' for consistency with Singer conventions.

        Reference:
        https://developers.sparkpost.com/api/metrics/#header-metrics-api

        Args:
            record: API response record
            parent_record: Unused, kept for interface consistency

        Returns:
            Dict: Record with 'ts' renamed to 'timestamp' if present
        """
        _ = parent_record  # Unused but kept for interface consistency

        # If record has 'ts' field, rename it to 'timestamp'
        if 'ts' in record:
            record['timestamp'] = record.pop('ts')

        return record

    def get_records(self) -> Iterator:
        """Fetch metrics records with date range parameters."""
        # SparkPost metrics API doesn't use pagination
        # It returns all results for the date range specified
        response = self.client.make_request(
            self.http_method,
            self.url_endpoint,
            self.params,
            self.headers,
            body=json.dumps(self.data_payload) if self.data_payload else None,
            path=self.path
        )

        raw_records = response.get(self.data_key, [])
        yield from raw_records

    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """Implementation for metrics incremental stream with date parameters."""
        bookmark_date = self.get_bookmark(state, self.tap_stream_id)
        current_max_bookmark_date = bookmark_date

        params = {
            "from": bookmark_date,
            "metrics": ",".join(self.default_metrics)
        }
        params.update(self.get_precision_params())
        self.update_params(**params)
        self.update_data_payload(parent_obj=parent_obj)
        self.url_endpoint = self.get_url_endpoint(parent_obj)

        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in self.get_records():
                record = self.modify_object(record, parent_obj)
                transformed_record = transformer.transform(
                    record, self.schema, self.metadata
                )

                record_bookmark = transformed_record.get(self.replication_keys[0], bookmark_date)

                # Ensure string type for comparison
                if not isinstance(record_bookmark, str):
                    record_bookmark = str(record_bookmark)

                # Normalize timestamp format: remove microseconds and standardize timezone
                record_bookmark_normalized = record_bookmark.replace(
                    ".000000Z", "Z"
                ).replace("+00:00", "Z")

                # Update record with normalized timestamp
                if record_bookmark != record_bookmark_normalized:
                    transformed_record[self.replication_keys[0]] = record_bookmark_normalized
                    record_bookmark = record_bookmark_normalized

                if record_bookmark_normalized >= bookmark_date:
                    if self.is_selected():
                        write_record(self.tap_stream_id, transformed_record)
                        counter.increment()

                    current_max_bookmark_date = max(
                        current_max_bookmark_date, record_bookmark
                    )

                    for child in self.child_to_sync:
                        child.sync(state=state, transformer=transformer, parent_obj=record)

            # Normalize bookmark format before writing
            if current_max_bookmark_date != bookmark_date:
                current_max_bookmark_str = str(current_max_bookmark_date)
                current_max_bookmark_str = (
                    current_max_bookmark_str.replace("+00:00", "Z")
                    .replace(".000000Z", "Z")
                )

                # Parse and reformat to remove microseconds
                try:
                    parsed_date = datetime.strptime(
                        current_max_bookmark_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    current_max_bookmark_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    try:
                        parsed_date = datetime.strptime(
                            current_max_bookmark_str, "%Y-%m-%dT%H:%M:%SZ"
                        )
                        current_max_bookmark_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        current_max_bookmark_date = current_max_bookmark_str

            state = self.write_bookmark(state, self.tap_stream_id, value=current_max_bookmark_date)
            return counter.value


class EmptyStream(FullTableStream):
    """Base class for streams that are unavailable or unsupported.
    
    Returns empty data to allow tap to continue processing other streams.
    Use for endpoints that:
    - Don't exist in the API version
    - Require parameters not available in free tier
    - Are write-only (e.g., transmissions)
    """

    def get_records(self):
        """Return empty generator for unavailable endpoint."""
        return []


class ChildBaseStream(IncrementalStream):
    """Base Class for Child Stream."""

    def __init__(self, client=None, catalog=None, config=None) -> None:
        """Initialize ChildBaseStream."""
        super().__init__(client, catalog, config)
        self.bookmark_value = None

    def get_url_endpoint(self, parent_obj=None):
        """Prepare URL endpoint for child streams."""
        return f"{self.client.base_url}/{self.path.format(parent_obj['id'])}"

    def get_bookmark(self, state: Dict, stream: str, key: Any = None) -> int:
        """Singleton bookmark value for child streams."""
        if self.bookmark_value is None:
            self.bookmark_value = super().get_bookmark(state, stream)

        return self.bookmark_value
