"""File-backed KnowledgeGraph (Excel via Polars).

Sheet / column names are English snake_case. Entity columns:
``vid``, ``name``, ``description`` (human-readable prose).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import polars as pl

from openxe.knowledge_graph.base import InMemoryKnowledgeGraph, wire_edge
from openxe.knowledge_graph.models import Dimension, Measure, Topic, Vocabulary

_ENTITY_MODELS: dict[str, type[Topic | Vocabulary | Measure | Dimension]] = {
    "topics": Topic,
    "vocabularies": Vocabulary,
    "measures": Measure,
    "dimensions": Dimension,
}

# Relation sheets after entities; subtopics last so measure/dimension copies carry children.
_EDGE_TYPES: dict[str, str] = {
    "synonyms": "synonyms",
    "hyponyms": "hyponyms",
    "represents": "represents",
    "topic_measures": "topic_measures",
    "topic_dimensions": "topic_dimensions",
    "subtopics": "subtopics",
}

_GraphNode = Topic | Vocabulary | Measure | Dimension


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    props: dict[str, Any] = {}
    for key, value in row.items():
        if value is None:
            continue
        name = str(key).strip().lower()
        if name in {"descriptions", "description"}:
            name = "description"
        props[name] = value
    return props


def _edge_endpoints(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]] | None:
    props = _normalize_row(row)
    sid = props.pop("src_vid", None) or props.pop("src_id", None)
    did = props.pop("dst_vid", None) or props.pop("dst_id", None)
    if not sid or not did:
        return None
    return str(sid), str(did), props


class FileKnowledgeGraph(InMemoryKnowledgeGraph):
    """In-memory KG loaded from an Excel workbook of entity/relation sheets."""

    def __init__(self, path: str | Path, **_: Any) -> None:
        super().__init__()
        self.path = Path(path)
        self.load()

    def load(self) -> None:
        topics: dict[str, Topic] = {}
        vocabularies: dict[str, Vocabulary] = {}
        measures: dict[str, Measure] = {}
        dimensions: dict[str, Dimension] = {}
        nodes: dict[str, _GraphNode] = {}

        for sheet_name, model_cls in _ENTITY_MODELS.items():
            df = pl.read_excel(self.path, sheet_name=sheet_name)
            for row in df.to_dicts():
                props = _normalize_row(row)
                vid = props.get("vid")
                if not vid:
                    continue
                node = model_cls.model_validate(props)
                nodes[str(vid)] = node
                match node:
                    case Topic():
                        topics[node.name] = node
                    case Vocabulary():
                        vocabularies[node.name] = node
                    case Measure():
                        measures[node.name] = node
                    case Dimension():
                        dimensions[node.name] = node

        for sheet_name, edge_type in _EDGE_TYPES.items():
            df = pl.read_excel(self.path, sheet_name=sheet_name)
            for row in df.to_dicts():
                endpoints = _edge_endpoints(row)
                if endpoints is None:
                    continue
                sid, did, properties = endpoints
                s_node = nodes.get(sid)
                d_node = nodes.get(did)
                if s_node is None or d_node is None or s_node == d_node:
                    continue
                wire_edge(edge_type, s_node, d_node, properties)

        self._commit_maps(topics, vocabularies, nodes, measures, dimensions)


def load_knowledge_graph(path: str | Path) -> FileKnowledgeGraph:
    """Load a file-backed knowledge graph (currently Excel only)."""
    return FileKnowledgeGraph(path)
