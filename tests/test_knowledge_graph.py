"""FileKnowledgeGraph + metadata scoping tests (offline Excel fixture)."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest
from openpyxl import Workbook

from openxe import BiMetadata, OpenXE
from openxe.knowledge_graph import FileKnowledgeGraph, load_knowledge_graph


def _write_workbook(path: Path, sheets: dict[str, pl.DataFrame]) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    for name, df in sheets.items():
        ws = wb.create_sheet(name)
        cols = list(df.columns)
        ws.append(cols)
        for row in df.iter_rows(named=True):
            ws.append([row[c] for c in cols])
    wb.save(path)
    return path


@pytest.fixture
def sample_xlsx(tmp_path: Path) -> Path:
    path = tmp_path / "kg.xlsx"
    sheets = {
        "topics": pl.DataFrame(
            {
                "vid": ["Topic|billing", "Topic|energy"],
                "name": ["抄核收", "电量"],
                "description": ["billing domain", "energy subtopic"],
            }
        ),
        "vocabularies": pl.DataFrame(
            {
                "vid": ["Vocabulary|用电量", "Vocabulary|售电量"],
                "name": ["用电量", "售电量"],
                "description": ["alias", "canonical measure word"],
            }
        ),
        "measures": pl.DataFrame(
            {
                "vid": ["Measure|售电量"],
                "name": ["售电量"],
                "description": ["energy sold"],
            }
        ),
        "dimensions": pl.DataFrame(
            {
                "vid": ["Dimension|地市"],
                "name": ["地市"],
                "description": ["city company"],
            }
        ),
        "synonyms": pl.DataFrame(
            {
                "src_vid": ["Vocabulary|用电量"],
                "dst_vid": ["Vocabulary|售电量"],
            }
        ),
        "hyponyms": pl.DataFrame(
            {
                "src_vid": pl.Series([], dtype=pl.Utf8),
                "dst_vid": pl.Series([], dtype=pl.Utf8),
            }
        ),
        "represents": pl.DataFrame(
            {
                "src_vid": ["Vocabulary|售电量"],
                "dst_vid": ["Measure|售电量"],
            }
        ),
        "topic_measures": pl.DataFrame(
            {
                "src_vid": ["Topic|energy"],
                "dst_vid": ["Measure|售电量"],
            }
        ),
        "topic_dimensions": pl.DataFrame(
            {
                "src_vid": ["Topic|energy"],
                "dst_vid": ["Dimension|地市"],
            }
        ),
        "subtopics": pl.DataFrame(
            {
                "src_vid": ["Topic|billing"],
                "dst_vid": ["Topic|energy"],
            }
        ),
    }
    return _write_workbook(path, sheets)


def test_file_kg_loads_entities_and_edges(sample_xlsx: Path) -> None:
    kg = load_knowledge_graph(sample_xlsx)
    assert isinstance(kg, FileKnowledgeGraph)
    assert {t.name for t in kg.topics} == {"抄核收", "电量"}
    assert kg.find_measure("售电量") is not None
    assert kg.find_dimension("地市") is not None
    vocab = kg.search_vocab("用电量")
    assert vocab is not None
    assert vocab.standard().name == "售电量"
    parent = kg.search_topic("抄核收")
    assert parent is not None
    assert any(st.name == "电量" for st in parent.subtopics)


def test_apply_to_metadata_intersects_catalog(sample_xlsx: Path) -> None:
    kg = FileKnowledgeGraph(sample_xlsx)
    full = BiMetadata(
        metrics=["售电量", "电费", "负荷"],
        dimensions=["地市", "行业"],
        filters={"地市": ["南京"], "行业": ["工业"]},
    )
    scoped = kg.apply_to_metadata(full)
    assert scoped.metrics == ["售电量"]
    assert scoped.dimensions == ["地市"]
    assert list(scoped.filters.keys()) == ["地市"]


def test_openxe_optional_knowledge_graph_scopes_metadata(sample_xlsx: Path) -> None:
    xe = OpenXE(
        metadata=BiMetadata(
            metrics=["售电量", "电费"],
            dimensions=["地市", "行业"],
            filters={"地市": ["南京"], "行业": ["工业"]},
        ),
        knowledge_graph=sample_xlsx,
    )
    assert xe.knowledge_graph is not None
    assert xe.metadata.metrics == ["售电量"]
    assert xe.metadata.dimensions == ["地市"]
