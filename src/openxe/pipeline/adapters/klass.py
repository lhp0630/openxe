"""ClassSignatureSpec — wrap an existing dspy.Signature subclass."""

from __future__ import annotations

import dspy

from openxe.exceptions import SignatureError
from openxe.pipeline.signature_spec import SignatureSpec


class ClassSignatureSpec(SignatureSpec):
    def __init__(self, signature_cls: type) -> None:
        if not isinstance(signature_cls, type) or not issubclass(
            signature_cls, dspy.Signature
        ):
            raise SignatureError("signature_cls must be a dspy.Signature subclass")
        if signature_cls is dspy.Signature:
            raise SignatureError("signature_cls must not be the base Signature")
        self._cls = signature_cls

    def resolve(self) -> type:
        return self._cls
