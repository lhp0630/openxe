"""OpenXE — programmatic entry facade.

Usage::

    from openxe import OpenXE, BiMetadata

    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"], filters={"地市": ["南京"]}))
    result = xe.extract("南京市2026年居民售电量")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from openxe.bi.extractor import BiExtractor
from openxe.bi.metadata import BiMetadata
from openxe.bi.result import BiResult

if TYPE_CHECKING:
    from openxe.pipeline.signature_spec import SignatureSpec


class OpenXE:
    """Public BI element extraction client (entry #1: library import)."""

    def __init__(
        self,
        metadata: BiMetadata | dict[str, Any] | None = None,
        *,
        lm: Any = None,
        signature_spec: SignatureSpec | None = None,
        state: dict[str, Any] | None = None,
    ) -> None:
        if metadata is None:
            meta = BiMetadata()
        elif isinstance(metadata, BiMetadata):
            meta = metadata
        else:
            meta = BiMetadata.model_validate(metadata)
        self._extractor = BiExtractor(
            meta,
            lm=lm,
            signature_spec=signature_spec,
            state=state,
        )

    @property
    def metadata(self) -> BiMetadata:
        return self._extractor.metadata

    def extract(self, text: str) -> BiResult:
        """Extract BI elements from natural language."""
        return self._extractor.extract(text)

    async def aextract(self, text: str) -> BiResult:
        """Async extract (skeleton: sync under the hood)."""
        return await self._extractor.aextract(text)

    def extract_dict(self, text: str) -> dict[str, Any]:
        """Extract and serialize with metadata key_names."""
        result = self.extract(text)
        return result.to_dict(key_names=self.metadata.key_names)
