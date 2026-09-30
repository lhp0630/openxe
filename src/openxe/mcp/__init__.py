"""MCP entry: expose OpenXE as MCP tools (optional extra ``openxe[mcp]``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from openxe.api import OpenXE


def create_mcp_server(
    openxe: OpenXE | None = None,
    *,
    metadata: dict[str, Any] | None = None,
    name: str = "openxe",
) -> Any:
    """Build an MCP server instance with BI extract tool.

    Requires ``pip install openxe[mcp]`` (or ``mcp`` package).
    """
    from openxe.mcp.server import build_server

    return build_server(openxe=openxe, metadata=metadata, name=name)


__all__ = ["create_mcp_server"]
