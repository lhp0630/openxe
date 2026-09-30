"""BiExtractor — product core (wrapped by OpenXE)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from openxe.bi.default_signature import DEFAULT_BI_SIGNATURE_CODE
from openxe.bi.metadata import BiMetadata
from openxe.bi.normalize import normalize
from openxe.bi.result import BiResult
from openxe.exceptions import ExtractError

if TYPE_CHECKING:
    from openxe.pipeline.signature_spec import SignatureSpec


class BiExtractor:
    """Bind metadata + LM + SignatureSpec; extract text → BiResult."""

    def __init__(
        self,
        metadata: BiMetadata,
        *,
        lm: Any = None,
        signature_spec: SignatureSpec | None = None,
        state: dict[str, Any] | None = None,
    ) -> None:
        self.metadata = metadata
        self.lm = lm
        self.state = state
        self.signature_spec = signature_spec or self._default_spec()

    def _default_spec(self) -> SignatureSpec:
        from openxe.pipeline.adapters.code import CodeSignatureSpec

        return CodeSignatureSpec(DEFAULT_BI_SIGNATURE_CODE)

    def extract(self, text: str) -> BiResult:
        """Run pipeline then normalize. Skeleton raises until Runner is implemented."""
        if not text or not str(text).strip():
            raise ExtractError("query text must be non-empty")

        from openxe.pipeline.runner import run_predict

        raw = run_predict(
            self.signature_spec,
            {
                "query": text.strip(),
                "metadata_summary": self.metadata.summary_text(),
            },
            lm=self.lm,
            state=self.state,
        )
        return normalize(raw, self.metadata)

    async def aextract(self, text: str) -> BiResult:
        """Async facade; skeleton delegates to sync extract."""
        return self.extract(text)
