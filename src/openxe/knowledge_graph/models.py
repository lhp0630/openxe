"""Graph entity models used by file-backed KnowledgeGraph.

Only Topic / Vocabulary / Measure / Dimension — no notes or glossary.
Excel entity columns are ``vid``, ``name``, ``description`` (human-readable prose).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Vocabulary(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vid: str
    name: str
    description: str | None = None
    synonym: Vocabulary | None = None
    hyponyms: list[Vocabulary] = Field(default_factory=list)
    represent: Topic | Measure | None = None
    entity_type: Literal["Vocabulary"] = "Vocabulary"

    def standard(self) -> Vocabulary:
        if self.synonym is not None:
            return self.synonym.standard()
        return self


class Topic(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vid: str
    name: str
    description: str | None = None
    level: int = 1
    priority: float = 1
    subtopics: list[Topic] = Field(default_factory=list)
    measures: list[Measure] = Field(default_factory=list)
    dimensions: list[Dimension] = Field(default_factory=list)
    entity_type: Literal["Topic"] = "Topic"

    def __contains__(self, item: Topic) -> bool:
        return any(x == item for x in self.subtopics)

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Topic) and self.vid == value.vid

    def __ne__(self, value: object) -> bool:
        return not (self == value)


class Measure(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vid: str
    name: str
    description: str | None = None
    priority: float = 1
    entity_type: Literal["Measure"] = "Measure"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Measure) and self.vid == value.vid

    def __ne__(self, value: object) -> bool:
        return not (self == value)


class Dimension(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vid: str
    name: str
    description: str | None = None
    priority: float = 1
    entity_type: Literal["Dimension"] = "Dimension"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Dimension):
            return self.vid == value.vid
        if isinstance(value, str):
            return self.name == value
        return False

    def __ne__(self, value: object) -> bool:
        return not (self == value)


# Forward refs for Vocabulary.represent / nested Topic lists
Vocabulary.model_rebuild()
Topic.model_rebuild()
