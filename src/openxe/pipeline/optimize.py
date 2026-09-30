"""Optional compile / few-shot optimize → program state."""

from __future__ import annotations

from typing import Any


def optimize(
    program: Any,
    trainset: list[Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """Return serializable program state for ``run_predict(..., state=...)``."""
    _ = program
    _ = trainset
    _ = kwargs
    raise NotImplementedError("optimize not implemented yet")
