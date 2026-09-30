"""Entry #2 — MCP server (requires ``openxe[mcp]``).

Run::

    uv sync --extra mcp
    uv run openxe-mcp
    # or: uv run python -m openxe.mcp

Optional::

    export OPENXE_METADATA_JSON='{"metrics":["售电量"],"filters":{"地市":["南京"]}}'
"""

from openxe.mcp import create_mcp_server


def main() -> None:
    server = create_mcp_server(
        metadata={"metrics": ["售电量"], "filters": {"地市": ["南京"]}},
    )
    print("MCP server built:", type(server).__name__)
    # server.run()  # stdio; use openxe-mcp for production launch


if __name__ == "__main__":
    main()
