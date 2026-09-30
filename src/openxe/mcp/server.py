"""MCP server skeleton — tool ``extract_bi_elements`` → OpenXE."""

from __future__ import annotations

from typing import Any

from openxe.api import OpenXE
from openxe.bi.metadata import BiMetadata


def _require_mcp() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "MCP entry requires the 'mcp' package. Install with: pip install 'openxe[mcp]'"
        ) from exc
    return FastMCP


def build_server(
    *,
    openxe: OpenXE | None = None,
    metadata: dict[str, Any] | BiMetadata | None = None,
    name: str = "openxe",
) -> Any:
    """Create FastMCP app. ``openxe`` or ``metadata`` configures the extractor."""
    FastMCP = _require_mcp()
    xe = openxe or OpenXE(metadata=metadata)

    mcp = FastMCP(
        name,
        instructions=(
            "openxe: extract BI elements (metrics, dimensions, filters) "
            "from natural-language queries."
        ),
    )

    @mcp.tool()
    def extract_bi_elements(query: str) -> dict[str, Any]:
        """Extract BI elements (指标/维度/条件) from a natural language query.

        Args:
            query: Natural language BI query, e.g. 南京市2026年居民售电量.
        """
        return xe.extract_dict(query)

    @mcp.resource("openxe://metadata")
    def metadata_resource() -> str:
        """Current BI metadata summary bound to this server."""
        return xe.metadata.summary_text()

    return mcp


def run_stdio(
    *,
    openxe: OpenXE | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Run MCP over stdio (default host transport)."""
    server = build_server(openxe=openxe, metadata=metadata)
    server.run()
