"""Custom exceptions for SparkPost tap."""


class SparkPostError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class SparkPostBackoffError(SparkPostError):
    """class representing backoff error handling."""

class SparkPostBadRequestError(SparkPostError):
    """class representing 400 status code."""

class SparkPostUnauthorizedError(SparkPostError):
    """class representing 401 status code."""


class SparkPostForbiddenError(SparkPostError):
    """class representing 403 status code."""

class SparkPostNotFoundError(SparkPostError):
    """class representing 404 status code."""

class SparkPostConflictError(SparkPostError):
    """class representing 409 status code."""

class SparkPostUnprocessableEntityError(SparkPostError):
    """class representing 422 status code."""

class SparkPostRateLimitError(SparkPostBackoffError):
    """class representing 429 status code."""

class SparkPostInternalServerError(SparkPostBackoffError):
    """class representing 500 status code."""

class SparkPostNotImplementedError(SparkPostBackoffError):
    """class representing 501 status code."""

class SparkPostBadGatewayError(SparkPostBackoffError):
    """class representing 502 status code."""

class SparkPostServiceUnavailableError(SparkPostBackoffError):
    """class representing 503 status code."""

ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": SparkPostBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": SparkPostUnauthorizedError,
        "message": (
            "The access token provided is expired, revoked, "
            "malformed or invalid for other reasons."
        )
    },
    403: {
        "raise_exception": SparkPostForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": SparkPostNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": SparkPostConflictError,
        "message": (
            "The API request cannot be completed because the requested "
            "operation would conflict with an existing item."
        )
    },
    422: {
        "raise_exception": SparkPostUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": SparkPostRateLimitError,
        "message": (
            "The API rate limit for your organisation/application "
            "pairing has been exceeded."
        ),
    },
    500: {
        "raise_exception": SparkPostInternalServerError,
        "message": (
            "The server encountered an unexpected condition which prevented"
            " it from fulfilling the request."
        )
    },
    501: {
        "raise_exception": SparkPostNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": SparkPostBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": SparkPostServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}
