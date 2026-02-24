# Flux-RX Exceptions Module
from __future__ import annotations


class FluxError(Exception):
    """Base exception for all Flux-RX errors."""

    pass


class FluxDataError(FluxError):
    """Raised when there is an issue fetching, parsing, or caching data."""

    pass


class FluxComputeError(FluxError):
    """Raised when an error occurs during analytics or metrics computation."""

    pass


class FluxThemeError(FluxError):
    """Raised when an invalid theme is requested or a theme configuration is malformed."""

    pass


class FluxConfigError(FluxError):
    """Raised when there is an invalid configuration setting."""

    pass
