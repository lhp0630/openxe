"""openxe public errors."""

from __future__ import annotations


class OpenXEError(Exception):
    """Base error for openxe."""


class MetadataError(OpenXEError):
    """Invalid or inconsistent BI metadata."""


class ExtractError(OpenXEError):
    """BI element extraction failed."""


class SignatureError(OpenXEError):
    """SignatureSpec resolve / validate failed."""
