"""
Structured exception hierarchy for the API.
All business exceptions inherit from AstraBlockError so they can be caught
by the global error handler and serialised into a consistent envelope.
"""
from typing import Any, Optional


class AstraBlockError(Exception):
    """Base exception — every domain error inherits from this."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AstraBlockError):
    def __init__(self, resource: str = "resource", identifier: str = ""):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=404,
            error_code="NOT_FOUND",
        )


class ValidationError(AstraBlockError):
    def __init__(self, message: str = "Validation failed", details: Any = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class AuthenticationError(AstraBlockError):
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
        )


class AuthorizationError(AstraBlockError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
        )


class RateLimitError(AstraBlockError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class ExternalServiceError(AstraBlockError):
    def __init__(self, service: str = "external service", message: str = ""):
        super().__init__(
            message=f"{service} error: {message}",
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
        )
