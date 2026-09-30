"""pydantic_ai Capability entry tests (skip if not installed)."""

from __future__ import annotations

import pytest

pytest.importorskip("pydantic_ai")

from openxe import BiMetadata, OpenXE
from openxe.capability import OpenXECapability, build_capability


def test_build_capability() -> None:
    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"]))
    cap = build_capability(xe, id="openxe")
    assert cap is not None
    holder = OpenXECapability(xe)
    assert holder.as_capability() is not None
