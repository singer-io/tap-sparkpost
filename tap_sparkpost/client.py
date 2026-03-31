"""HTTP client for SparkPost API."""
from typing import Any, Dict, Mapping, Optional, Tuple

import backoff
import requests
from requests import session
from requests.exceptions import (
    Timeout,
    ConnectionError as RequestsConnectionError,
    ChunkedEncodingError
)
from singer import get_logger, metrics

from tap_sparkpost.exceptions import (
    ERROR_CODE_EXCEPTION_MAPPING,
    SparkPostError,
    SparkPostBackoffError
)

LOGGER = get_logger()
REQUEST_TIMEOUT = 300
BASE_URL = "https://api.sparkpost.com/api/v1"

def raise_for_error(response: requests.Response) -> None:
    """Raises the associated response exception. Takes in a response object,
    checks the status code, and throws the associated exception based on the
    status code.

    :param resp: requests.Response object
    """
    try:
        response_json = response.json()
    except (ValueError, TypeError, AttributeError):
        # json() can raise ValueError for invalid JSON, TypeError/AttributeError for None
        response_json = {}
    if response.status_code not in [200, 201, 204]:
        # SparkPost returns errors in an "errors" array
        errors = response_json.get("errors", [])
        if errors:
            error = errors[0]
            message = (
                f"HTTP-error-code: {response.status_code}, "
                f"Error: {error.get('message', 'Unknown')}, "
                f"Description: {error.get('description', '')}, "
                f"Code: {error.get('code', '')}"
            )
        elif response_json.get("error"):
            message = (
                f"HTTP-error-code: {response.status_code}, "
                f"Error: {response_json.get('error')}"
            )
        else:
            error_message = ERROR_CODE_EXCEPTION_MAPPING.get(
                response.status_code, {}
            ).get("message", "Unknown Error")
            message = (
                f"HTTP-error-code: {response.status_code}, "
                f"Error: {response_json.get('message', error_message)}"
            )
        exc = ERROR_CODE_EXCEPTION_MAPPING.get(response.status_code, {}).get(
            "raise_exception", SparkPostError
        )
        raise exc(message, response) from None

class Client:
    """
    A Wrapper class.
    ~~~
    Performs:
     - Authentication
     - Response parsing
     - HTTP Error handling and retry
    """

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        self._session = session()
        self.base_url = BASE_URL
        config_request_timeout = config.get("request_timeout")
        self.request_timeout = (
            float(config_request_timeout)
            if config_request_timeout
            else REQUEST_TIMEOUT
        )

    def __enter__(self):
        self.check_api_credentials()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()

    def check_api_credentials(self) -> None:
        """
        Check if API credentials are valid.
        
        Note: This is a placeholder for future implementation.
        Currently, credentials are validated on first API call.
        """

    def authenticate(self, headers: Dict, params: Dict) -> Tuple[Dict, Dict]:
        """Authenticates the request with the API key"""
        headers = headers.copy()
        headers["Authorization"] = self.config["api_key"]
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        return headers, params

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def make_request(
        self,
        method: str,
        endpoint: Optional[str],
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        body: Optional[str] = None,
        path: Optional[str] = None
    ) -> Any:
        """
        Sends an HTTP request to the specified API endpoint.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: Full URL or path to API endpoint
            params: Query parameters
            headers: HTTP headers
            body: Request body data
            path: API path (if endpoint not provided)
        """
        params = params or {}
        headers = headers or {}
        endpoint = endpoint or f"{self.base_url}/{path}"
        headers, params = self.authenticate(headers, params)
        return self.__make_request(
            method, endpoint,
            headers=headers,
            params=params,
            data=body,
            timeout=self.request_timeout
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            ConnectionResetError,
            RequestsConnectionError,
            ChunkedEncodingError,
            Timeout,
            SparkPostBackoffError
        ),
        max_tries=5,
        factor=2,
    )
    def __make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[Mapping[Any, Any]]:
        """Performs HTTP Operations."""
        method = method.upper()
        with metrics.http_request_timer(endpoint):
            if method in ("GET", "POST"):
                if method == "GET":
                    kwargs.pop("data", None)
                response = self._session.request(method, endpoint, **kwargs)
                raise_for_error(response)
            else:
                raise ValueError(f"Unsupported method: {method}")

        # Handle responses with no content (e.g., HTTP 204) safely
        if response.status_code == 204 or not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            # Fallback for invalid or non-JSON responses on success codes
            return {}
