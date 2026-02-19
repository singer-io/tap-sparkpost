"""Unit tests for Client class - initialization, methods, backoff, and retry logic."""
import unittest
import requests
from unittest.mock import patch
from parameterized import parameterized
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError
from tap_sparkpost.client import Client
from tap_sparkpost.exceptions import (
    SparkPostBadRequestError,
    SparkPostUnauthorizedError,
    SparkPostForbiddenError,
    SparkPostNotFoundError,
    SparkPostBackoffError,
    SparkPostInternalServerError,
    SparkPostBadGatewayError,
    SparkPostServiceUnavailableError
)


default_config = {
    "base_url": "https://api.sparkpost.com/api/v1",
    "request_timeout": 30,
    "api_key": "test_api_key",
    "start_date": "2024-01-01T00:00:00Z"
}

DEFAULT_REQUEST_TIMEOUT = 300

class MockResponse:
    """Mocked standard HTTPResponse to test error handling."""

    def __init__(
        self, status_code, resp="", content=[""], headers=None, raise_error=True, text=None
    ):
        self.json_data = resp
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.raise_error = raise_error
        self.text = text or {}
        self.reason = "error"

    def raise_for_status(self):
        """If an error occur, this method returns a HTTPError object.

        Raises:
            requests.HTTPError: Mock http error.

        Returns:
            int: Returns status code if not error occurred.
        """
        if not self.raise_error:
            return self.status_code

        raise requests.HTTPError("mock sample message")

    def json(self):
        """Returns a JSON object of the result."""
        return self.text


class TestClientInitialization(unittest.TestCase):
    """Test client initialization and configuration."""

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(default_config)

    @parameterized.expand([
        ["empty value", "", DEFAULT_REQUEST_TIMEOUT],
        ["string value", "12", 12.0],
        ["integer value", 10, 10.0],
        ["float value", 20.0, 20.0],
        ["zero value", 0, DEFAULT_REQUEST_TIMEOUT]
    ])
    @patch("tap_sparkpost.client.session")
    def test_request_timeout_values(self, test_name, input_value, expected_value, mock_session):
        """Test that request timeout is properly parsed from config."""
        config = default_config.copy()
        config["request_timeout"] = input_value
        client = Client(config)
        assert client.request_timeout == expected_value
        assert isinstance(client._session, mock_session().__class__)

    def test_base_url_default(self):
        """Test that base_url is hardcoded to SparkPost API endpoint."""
        config = default_config.copy()
        client = Client(config)
        self.assertEqual(client.base_url, "https://api.sparkpost.com/api/v1")


class TestErrorHandling(unittest.TestCase):
    """Test HTTP error handling without retry (4xx errors)."""

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(default_config)

    @parameterized.expand([
        ["400 error", 400, MockResponse(400, text={"errors": [{"message": "Bad Request"}]}), SparkPostBadRequestError],
        ["401 error", 401, MockResponse(401, text={"errors": [{"message": "Unauthorized"}]}), SparkPostUnauthorizedError],
        ["403 error", 403, MockResponse(403, text={"errors": [{"message": "Forbidden."}]}), SparkPostForbiddenError],
        ["404 error", 404, MockResponse(404, text={"errors": [{"message": "Resource could not be found"}]}), SparkPostNotFoundError],
    ])
    def test_4xx_errors_no_retry(self, test_name, error_code, mock_response, error):
        """Test that 4xx errors raise immediately without retry."""
        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.sparkpost.com/api/v1/events")

        self.assertIn(f"HTTP-error-code: {error_code}", str(e.exception))
        # Should only attempt once (no retry for 4xx errors)
        self.assertEqual(mock_request.call_count, 1)


class TestBackoffRetry(unittest.TestCase):
    """Test backoff and retry logic for retryable errors."""

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(default_config)

    @parameterized.expand([
        ["429 error", 429, MockResponse(429, text={"errors": [{"message": "Rate limit exceeded"}]}), SparkPostBackoffError],
        ["500 error", 500, MockResponse(500, text={"errors": [{"message": "Internal server error"}]}), SparkPostInternalServerError],
        ["502 error", 502, MockResponse(502, text={"errors": [{"message": "Bad gateway"}]}), SparkPostBadGatewayError],
        ["503 error", 503, MockResponse(503, text={"errors": [{"message": "Service unavailable"}]}), SparkPostServiceUnavailableError],
    ])
    @patch("time.sleep")
    def test_http_errors_with_retry(self, test_name, error_code, mock_response, error, mock_sleep):
        """Test that retryable HTTP errors (429, 5xx) trigger backoff retry."""
        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.sparkpost.com/api/v1/events")

            self.assertIn(f"HTTP-error-code: {error_code}", str(e.exception))
            # Verify 5 retry attempts
            self.assertEqual(mock_request.call_count, 5)
            # Verify sleep was called for backoff
            self.assertTrue(mock_sleep.called)

    @parameterized.expand([
        ["ConnectionResetError", ConnectionResetError],
        ["ConnectionError", ConnectionError],
        ["ChunkedEncodingError", ChunkedEncodingError],
        ["Timeout", Timeout],
    ])
    @patch("time.sleep")
    def test_connection_errors_with_retry(self, test_name, error, mock_sleep):
        """Test that connection errors trigger backoff retry."""
        with patch.object(self.client._session, "request", side_effect=error) as mock_request:
            with self.assertRaises(error):
                self.client._Client__make_request("GET", "https://api.sparkpost.com/api/v1/events")

            # Verify 5 retry attempts
            self.assertEqual(mock_request.call_count, 5)
            # Verify sleep was called for backoff
            self.assertTrue(mock_sleep.called)

    @parameterized.expand([
        ["success_on_2nd_attempt", 1, 2],
        ["success_on_3rd_attempt", 2, 3],
        ["success_on_4th_attempt", 3, 4],
    ])
    @patch("time.sleep")
    def test_successful_retry_after_failure(self, test_name, num_failures, expected_attempts, mock_sleep):
        """Test that request succeeds after initial failures."""
        responses = []
        # Add failure responses
        for _ in range(num_failures):
            responses.append(MockResponse(503, text={"errors": [{"message": "Service unavailable"}]}))
        # Add success response
        responses.append(MockResponse(200, text={"results": [{"event_id": "123"}]}, raise_error=False))

        with patch.object(self.client._session, "request", side_effect=responses) as mock_request:
            result = self.client._Client__make_request("GET", "https://api.sparkpost.com/api/v1/events")

        # Should succeed on expected attempt
        self.assertEqual(result, {"results": [{"event_id": "123"}]})
        self.assertEqual(mock_request.call_count, expected_attempts)
        self.assertEqual(mock_sleep.call_count, num_failures)


class TestAuthentication(unittest.TestCase):
    """Test authentication headers."""

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(default_config)

    def test_authenticate_sets_authorization_header(self):
        """Test that authenticate sets Authorization header."""
        headers, params = self.client.authenticate({}, {})
        self.assertEqual(headers["Authorization"], "test_api_key")
        self.assertEqual(headers["Accept"], "application/json")
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_authenticate_preserves_existing_headers(self):
        """Test that authenticate preserves existing headers."""
        existing_headers = {"X-Custom-Header": "value"}
        headers, params = self.client.authenticate(existing_headers, {})
        self.assertEqual(headers["X-Custom-Header"], "value")
        self.assertEqual(headers["Authorization"], "test_api_key")
