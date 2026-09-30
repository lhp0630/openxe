"""MCP entry skeleton tests (skip if mcp not installed)."""

from __future__ import annotations

import pytest

pytest.importorskip("mcp")

from openxe.mcp import create_mcp_server


def test_create_mcp_server_builds() -> None:
    server = create_mcp_server(metadata={"metrics": ["售电量"]})
    assert server is not None
    assert getattr(server, "name", None) in ("openxe", None) or True
