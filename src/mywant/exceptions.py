class MyWantError(Exception):
    """Base exception for all MyWant SDK errors."""


class APIError(MyWantError):
    """Raised when the server returns a non-2xx response."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class NotFoundError(APIError):
    """Raised on HTTP 404."""


class ConflictError(APIError):
    """Raised on HTTP 409 (e.g. want is running, recipe already exists)."""


class ValidationError(APIError):
    """Raised on HTTP 400."""
