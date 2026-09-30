"""openxe — metadata-driven BI element extraction.

Primary entry::

    from openxe import OpenXE
"""

from openxe.api import OpenXE
from openxe.bi.metadata import BiMetadata
from openxe.bi.result import BiResult
from openxe.exceptions import (
    ExtractError,
    MetadataError,
    OpenXEError,
    SignatureError,
)

__all__ = [
    "OpenXE",
    "BiMetadata",
    "BiResult",
    "OpenXEError",
    "MetadataError",
    "ExtractError",
    "SignatureError",
]

__version__ = "0.1.0"
