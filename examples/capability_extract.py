"""Entry #3 — pydantic_ai Capability (requires ``openxe[pydantic-ai]``).

Run after install::

    uv sync --extra pydantic-ai
    uv run python examples/capability_extract.py
"""

from openxe import BiMetadata, OpenXE
from openxe.capability import OpenXECapability, build_capability


def main() -> None:
    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"]))
    holder = OpenXECapability(xe, defer_loading=False)
    print("OpenXECapability holder id:", holder.id)
    # Needs pydantic-ai installed:
    # cap = build_capability(xe)
    # from pydantic_ai import Agent
    # agent = Agent("openai:gpt-4o", capabilities=[cap])
    _ = build_capability
    print("build_capability ready (call after installing pydantic-ai)")


if __name__ == "__main__":
    main()
