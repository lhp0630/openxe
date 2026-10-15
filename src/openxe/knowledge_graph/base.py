"""In-memory knowledge graph API (eager maps)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from openxe.bi.metadata import BiMetadata
from openxe.knowledge_graph.models import Dimension, Measure, Topic, Vocabulary


class KnowledgeGraphBase(ABC):
    """Business-rule graph that can constrain which metadata the model may see."""

    @property
    @abstractmethod
    def topics(self) -> list[Topic]: ...

    @property
    @abstractmethod
    def vocab(self) -> list[Vocabulary]: ...

    @property
    @abstractmethod
    def measures(self) -> list[Measure]: ...

    @property
    @abstractmethod
    def dimensions(self) -> list[Dimension]: ...

    @abstractmethod
    def search_topic(self, topic: str) -> Topic | None: ...

    @abstractmethod
    def search_vocab(self, vocab: str) -> Vocabulary | None: ...

    @abstractmethod
    def find_measure(self, name: str) -> Measure | None: ...

    @abstractmethod
    def find_dimension(self, name: str) -> Dimension | None: ...

    @abstractmethod
    def apply_to_metadata(self, metadata: BiMetadata) -> BiMetadata:
        """Intersect full catalog with names declared in this graph."""


class InMemoryKnowledgeGraph(KnowledgeGraphBase):
    """Map-backed KG; subclasses populate maps then call ``_commit_maps``."""

    def __init__(self) -> None:
        self._topic_map: dict[str, Topic] = {}
        self._vocab_map: dict[str, Vocabulary] = {}
        self._measure_map: dict[str, Measure] = {}
        self._dimension_map: dict[str, Dimension] = {}
        self._node_map: dict[str, Topic | Vocabulary | Measure | Dimension] = {}

    @property
    def topics(self) -> list[Topic]:
        return list(self._topic_map.values())

    @property
    def vocab(self) -> list[Vocabulary]:
        return list(self._vocab_map.values())

    @property
    def measures(self) -> list[Measure]:
        return list(self._measure_map.values())

    @property
    def dimensions(self) -> list[Dimension]:
        return list(self._dimension_map.values())

    def search_topic(self, topic: str) -> Topic | None:
        vocab = self.search_vocab(topic)
        if vocab is not None:
            std = vocab.standard()
            if isinstance(std.represent, Topic):
                return std.represent
        return self._topic_map.get(topic)

    def search_vocab(self, vocab: str) -> Vocabulary | None:
        return self._vocab_map.get(vocab)

    def find_measure(self, name: str) -> Measure | None:
        return self._measure_map.get(name)

    def find_dimension(self, name: str) -> Dimension | None:
        return self._dimension_map.get(name)

    def apply_to_metadata(self, metadata: BiMetadata) -> BiMetadata:
        """Keep only BiMetadata entries whose names appear in this graph.

        Empty graph maps leave that role unconstrained (pass-through).
        """
        measure_names = set(self._measure_map)
        dim_names = set(self._dimension_map)

        metrics = (
            [m for m in metadata.metrics if m in measure_names]
            if measure_names
            else list(metadata.metrics)
        )
        dimensions = (
            [d for d in metadata.dimensions if d in dim_names]
            if dim_names
            else list(metadata.dimensions)
        )
        filters = (
            {k: v for k, v in metadata.filters.items() if k in dim_names}
            if dim_names
            else dict(metadata.filters)
        )
        return metadata.model_copy(
            update={
                "metrics": metrics,
                "dimensions": dimensions,
                "filters": filters,
            }
        )

    def _commit_maps(
        self,
        topics: dict[str, Topic],
        vocabularies: dict[str, Vocabulary],
        nodes: dict[str, Topic | Vocabulary | Measure | Dimension],
        measures: dict[str, Measure],
        dimensions: dict[str, Dimension],
    ) -> None:
        for topic in sorted(topics.values(), key=lambda t: t.level, reverse=True):
            if topic.subtopics:
                topic.subtopics = sorted(topic.subtopics, key=lambda x: x.priority)
            if topic.measures:
                topic.measures = sorted(topic.measures, key=lambda x: x.priority)
            if topic.dimensions:
                topic.dimensions = sorted(topic.dimensions, key=lambda x: x.priority)

        self._topic_map = topics
        self._vocab_map = vocabularies
        self._node_map = nodes
        self._measure_map = measures
        self._dimension_map = dimensions


def wire_edge(
    edge_type: str,
    s_node: Topic | Vocabulary | Measure | Dimension,
    d_node: Topic | Vocabulary | Measure | Dimension,
    properties: dict[str, Any] | None = None,
) -> None:
    """Apply one directed edge onto in-memory graph objects."""
    properties = properties or {}
    match edge_type:
        case "synonym" | "synonyms":
            if isinstance(s_node, Vocabulary) and isinstance(d_node, Vocabulary):
                s_node.synonym = d_node
                return
        case "hyponym" | "hyponyms":
            if isinstance(s_node, Vocabulary) and isinstance(d_node, Vocabulary):
                s_node.hyponyms.append(d_node)
                return
        case "represents":
            if isinstance(s_node, Vocabulary) and isinstance(d_node, (Topic, Measure)):
                s_node.represent = d_node
                return
        case "subtopic" | "subtopics":
            if isinstance(s_node, Topic) and isinstance(d_node, Topic):
                if properties:
                    d_node = d_node.model_copy(update=properties)
                s_node.subtopics.append(d_node)
                return
        case "measure" | "topic_measures":
            if isinstance(s_node, Topic) and isinstance(d_node, Measure):
                if properties:
                    d_node = d_node.model_copy(update=properties)
                s_node.measures.append(d_node)
                return
        case "dimension" | "topic_dimensions":
            if isinstance(s_node, Topic) and isinstance(d_node, Dimension):
                if properties:
                    d_node = d_node.model_copy(update=properties)
                s_node.dimensions.append(d_node)
                return
        case _:
            return
