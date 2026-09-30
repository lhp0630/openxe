"""openxe.pipeline — pluggable Signature runtime."""

from openxe.pipeline.runner import run_predict
from openxe.pipeline.signature_spec import SignatureSpec

__all__ = ["SignatureSpec", "run_predict"]
