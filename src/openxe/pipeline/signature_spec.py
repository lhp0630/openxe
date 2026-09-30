"""SignatureSpec protocol and shared validation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from openxe.exceptions import SignatureError


class SignatureSpec(ABC):
    """Pluggable signature source → resolved dspy.Signature class."""

    @abstractmethod
    def resolve(self) -> type:
        """Return a ``dspy.Signature`` subclass."""

    @property
    def input_fields(self) -> dict[str, Any]:
        cls = self.resolve()
        fields = getattr(cls, "input_fields", None) or {}
        return dict(fields)

    @property
    def output_fields(self) -> dict[str, Any]:
        cls = self.resolve()
        fields = getattr(cls, "output_fields", None) or {}
        return dict(fields)

    def validate(self) -> type:
        cls = self.resolve()
        if not self.input_fields:
            raise SignatureError("Signature must define at least one InputField")
        if not self.output_fields:
            raise SignatureError("Signature must define at least one OutputField")
        return cls
