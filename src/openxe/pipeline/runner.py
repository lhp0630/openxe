"""Generic Predict runner — OutputField-only dict (no BI semantics)."""

from __future__ import annotations

from typing import Any

from openxe.pipeline.signature_spec import SignatureSpec


def run_predict(
    spec: SignatureSpec,
    inputs: dict[str, Any],
    *,
    lm: Any = None,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute ``dspy.Predict`` for ``spec`` and return OutputField values.

    Skeleton: validates spec + input keys; LM call not wired yet.
    """
    signature_cls = spec.validate()
    input_names = set(spec.input_fields.keys())
    missing = input_names - set(inputs.keys())
    if missing:
        raise ValueError(f"missing InputField values: {sorted(missing)}")

    _ = signature_cls
    _ = lm
    _ = state
    raise NotImplementedError(
        "run_predict LM/Predict path not implemented yet "
        "(spec validated; wire dspy.Predict next)."
    )
