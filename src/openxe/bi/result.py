"""BiResult: stable BI slot serialization."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BiResult(BaseModel):
    """Extracted BI elements. Field names follow metadata ``key_names`` when dumped
    via :meth:`to_dict`; the model itself keeps English role attributes.
    """

    metrics: list[str] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)
    filters: dict[str, str | list[str]] = Field(default_factory=dict)

    def to_dict(
        self,
        *,
        key_names: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Serialize using optional role→key mapping (default Chinese keys)."""
        names = key_names or {
            "metrics": "指标",
            "dimensions": "维度",
            "filters": "条件",
        }
        return {
            names["metrics"]: list(self.metrics),
            names["dimensions"]: list(self.dimensions),
            names["filters"]: dict(self.filters),
        }
