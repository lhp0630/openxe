"""Skeleton tests for OpenXE programmatic entry."""

from __future__ import annotations

import pytest

from openxe import BiMetadata, BiResult, OpenXE
from openxe.pipeline.adapters.code import CodeSignatureSpec
from openxe.bi.default_signature import DEFAULT_BI_SIGNATURE_CODE


def test_openxe_construct_and_metadata() -> None:
    xe = OpenXE(
        metadata={
            "metrics": ["售电量"],
            "filters": {"地市": ["南京"]},
        }
    )
    assert isinstance(xe.metadata, BiMetadata)
    assert xe.metadata.metrics == ["售电量"]
    assert "地市" in xe.metadata.filters


def test_bi_result_to_dict_default_keys() -> None:
    r = BiResult(metrics=["售电量"], dimensions=[], filters={"年份": "2026"})
    d = r.to_dict()
    assert d["指标"] == ["售电量"]
    assert d["条件"]["年份"] == "2026"


def test_default_signature_code_loads() -> None:
    spec = CodeSignatureSpec(DEFAULT_BI_SIGNATURE_CODE)
    cls = spec.validate()
    assert "query" in spec.input_fields
    assert "metrics" in spec.output_fields
    assert cls.__name__ == "BiElementExtract"


def test_extract_raises_until_runner_wired() -> None:
    xe = OpenXE(metadata=BiMetadata(metrics=["售电量"]))
    with pytest.raises(NotImplementedError):
        xe.extract("南京市2026年居民售电量")
