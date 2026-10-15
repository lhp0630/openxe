"""OpenXE — programmatic entry facade.

Usage::

    from openxe import OpenXE, BiMetadata

    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"], filters={"地市": ["南京"]}))
    result = xe.extract("南京市2026年居民售电量")
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from openxe.bi.extractor import BiExtractor
from openxe.bi.metadata import BiMetadata
from openxe.bi.result import BiResult
from openxe.knowledge_graph.base import KnowledgeGraphBase
from openxe.knowledge_graph.file_graph import load_knowledge_graph

if TYPE_CHECKING:
    from openxe.pipeline.signature_spec import SignatureSpec


class OpenXE:
    """Public BI element extraction client (entry #1: library import)."""

    def __init__(
        self,
        metadata: BiMetadata | dict[str, Any] | None = None,
        *,
        knowledge_graph: KnowledgeGraphBase | str | Path | None = None,
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

        kg: KnowledgeGraphBase | None
        if knowledge_graph is None:
            kg = None
        elif isinstance(knowledge_graph, KnowledgeGraphBase):
            kg = knowledge_graph
        else:
            kg = load_knowledge_graph(knowledge_graph)

        # BiMetadata = full catalog; KnowledgeGraph (optional) scopes model-visible names.
        if kg is not None:
            meta = kg.apply_to_metadata(meta)

        self._knowledge_graph = kg
        self._extractor = BiExtractor(
            meta,
            lm=lm,
            signature_spec=signature_spec,
            state=state,
        )

    @property
    def metadata(self) -> BiMetadata:
        """Effective metadata after optional knowledge-graph scoping."""
        return self._extractor.metadata

    @property
    def knowledge_graph(self) -> KnowledgeGraphBase | None:
        return self._knowledge_graph

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
