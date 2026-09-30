"""Normalize runner raw Output dict into BiResult under BiMetadata."""

from __future__ import annotations

from typing import Any

from openxe.bi.metadata import BiMetadata
from openxe.bi.result import BiResult


def normalize(raw: dict[str, Any], metadata: BiMetadata) -> BiResult:
    """Align raw model output to metadata enums / empty slots.

    Skeleton: returns empty BiResult shaped by metadata key roles.
    Full enum alignment deferred.
    """
    _ = raw
    _ = metadata
    return BiResult()
