"""Default BI Signature template (loaded via CodeSignatureSpec)."""

from __future__ import annotations

DEFAULT_BI_SIGNATURE_CODE = '''
import dspy


class BiElementExtract(dspy.Signature):
    """Extract BI analysis elements from a natural-language query."""

    query: str = dspy.InputField(desc="Natural language BI query")
    metadata_summary: str = dspy.InputField(
        desc="Allowed metrics, dimensions, and filter enums"
    )
    metrics: str = dspy.OutputField(desc="JSON list of metric names")
    dimensions: str = dspy.OutputField(desc="JSON list of dimension names; may be empty")
    filters: str = dspy.OutputField(
        desc="JSON object of filter field -> value or list of values"
    )
'''.strip()
