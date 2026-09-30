"""Agent framework capabilities.

Import concrete builders from submodules so core install stays light::

    from openxe.capability.pydantic_ai import build_capability
"""

from __future__ import annotations

from typing import Any


def __getattr__(name: str) -> Any:
    if name in {"OpenXECapability", "build_capability"}:
        from openxe.capability import pydantic_ai as _pai

        return getattr(_pai, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["OpenXECapability", "build_capability"]
