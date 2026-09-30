"""CodeSignatureSpec — Signature from Python source string (dspy_lfx_demo)."""

from __future__ import annotations

from typing import Any

import dspy

from openxe.exceptions import SignatureError
from openxe.pipeline.signature_spec import SignatureSpec


class CodeSignatureSpec(SignatureSpec):
    def __init__(self, code: str) -> None:
        if not code or not code.strip():
            raise SignatureError("signature code must be non-empty")
        self._code = code
        self._cached: type | None = None

    def resolve(self) -> type:
        if self._cached is not None:
            return self._cached
        self._cached = _extract_signature_from_code(self._code)
        return self._cached


def _extract_signature_from_code(signature_code: str) -> type:
    namespace: dict[str, Any] = {"dspy": dspy}
    exec(compile(signature_code, "<openxe_signature>", "exec"), namespace)

    candidates: list[type] = []
    for name, obj in namespace.items():
        if name.startswith("_"):
            continue
        if isinstance(obj, type) and issubclass(obj, dspy.Signature):
            if obj is not dspy.Signature:
                candidates.append(obj)
    if not candidates:
        raise SignatureError("No dspy.Signature subclass found in signature code")
    return candidates[-1]
