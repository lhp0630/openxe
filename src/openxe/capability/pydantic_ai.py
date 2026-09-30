"""pydantic_ai Capability entry — bundle OpenXE as agent tools.

Usage (after ``pip install 'openxe[pydantic-ai]'``)::

    from openxe import OpenXE, BiMetadata
    from openxe.capability import build_capability
    from pydantic_ai import Agent

    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"]))
    agent = Agent("openai:gpt-4o", capabilities=[build_capability(xe)])
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from openxe.api import OpenXE


def _require_capability_cls() -> type:
    try:
        from pydantic_ai.capabilities import Capability
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "pydantic_ai Capability entry requires 'pydantic-ai'. "
            "Install with: pip install 'openxe[pydantic-ai]'"
        ) from exc
    return Capability


def build_capability(
    openxe: OpenXE,
    *,
    id: str = "openxe",
    description: str | None = None,
    defer_loading: bool = False,
) -> Any:
    """Build a ``pydantic_ai.capabilities.Capability`` wrapping ``OpenXE``."""
    Capability = _require_capability_cls()
    desc = description or (
        "Extract BI elements (metrics / dimensions / filters) "
        "from natural-language analysis queries."
    )
    cap = Capability(
        id=id,
        description=desc,
        defer_loading=defer_loading,
    )

    @cap.tool_plain
    def extract_bi_elements(query: str) -> dict[str, Any]:
        """Extract BI elements (指标/维度/条件) from a natural language query."""
        return openxe.extract_dict(query)

    return cap


class OpenXECapability:
    """Thin factory/holder so callers can ``from openxe.capability import OpenXECapability``.

    Prefer :func:`build_capability` for the actual pydantic_ai object. This class
    stores the bound :class:`~openxe.api.OpenXE` and builds on :meth:`as_capability`.
    """

    def __init__(
        self,
        openxe: OpenXE,
        *,
        id: str = "openxe",
        description: str | None = None,
        defer_loading: bool = False,
    ) -> None:
        self.openxe = openxe
        self.id = id
        self.description = description
        self.defer_loading = defer_loading

    def as_capability(self) -> Any:
        return build_capability(
            self.openxe,
            id=self.id,
            description=self.description,
            defer_loading=self.defer_loading,
        )
