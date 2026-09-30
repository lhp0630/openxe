"""BI metadata: legal metrics / dimensions / filter enums and key aliases."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator

from openxe.exceptions import MetadataError


class BiMetadata(BaseModel):
    """Schema constraints for BI element extraction."""

    metrics: list[str] = Field(default_factory=list, description="Legal metric names")
    dimensions: list[str] = Field(
        default_factory=list, description="Legal dimension names"
    )
    filters: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Filter field -> legal values (multi-value allowed)",
    )
    key_names: dict[str, str] = Field(
        default_factory=lambda: {
            "metrics": "指标",
            "dimensions": "维度",
            "filters": "条件",
        },
        description="Semantic role -> output JSON key",
    )
    aliases: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Surface form -> legal value(s) for normalize",
    )

    @model_validator(mode="after")
    def _require_key_roles(self) -> BiMetadata:
        for role in ("metrics", "dimensions", "filters"):
            if role not in self.key_names:
                raise MetadataError(f"key_names missing role: {role}")
        return self

    def summary_text(self) -> str:
        """Compact metadata blurb for Signature InputField."""
        return (
            f"metrics={self.metrics!r}; dimensions={self.dimensions!r}; "
            f"filters={self.filters!r}"
        )
