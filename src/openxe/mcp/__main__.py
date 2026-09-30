"""``python -m openxe.mcp`` — stdio MCP server entry."""

from __future__ import annotations

import json
import os


def main() -> None:
    """Launch openxe MCP server.

    Optional env ``OPENXE_METADATA_JSON``: JSON object for BiMetadata.
    """
    from openxe.mcp.server import run_stdio

    raw = os.environ.get("OPENXE_METADATA_JSON")
    metadata = json.loads(raw) if raw else None
    run_stdio(metadata=metadata)


if __name__ == "__main__":
    main()
