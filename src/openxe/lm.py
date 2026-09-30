"""LM / DSPy backend configuration (vendor-agnostic)."""

from __future__ import annotations

from typing import Any


def configure_lm(
    model: str | None = None,
    *,
    api_base: str | None = None,
    api_key: str | None = None,
    **kwargs: Any,
) -> Any:
    """Build or configure a DSPy LM instance.

    Skeleton: full wiring deferred. Callers may pass a ready-made LM into ``OpenXE``.
    """
    raise NotImplementedError(
        "configure_lm is not implemented yet; pass an LM instance to OpenXE(lm=...)."
    )
