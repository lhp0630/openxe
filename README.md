# openxe

**Open eXtract Elements** — 通用 **BI 要素**抽取（DSPy）。

自然语言 → `{指标, 维度, 条件}`；换元数据适配不同数仓/行业。底层为可插拔 Signature 运行时。可选 **KnowledgeGraph** 用业务规则圈定模型可见的元数据子集。

```text
南京市2026年居民售电量
        ↓  openxe(+ BiMetadata ± KnowledgeGraph)
{ "指标": ["售电量"], "维度": [], "条件": { "地市": "南京", "年份": "2026", "分类": ["乡村居民", "城镇居民"] } }
```

| | |
| --- | --- |
| **BiMetadata** | 全量合法目录（指标 / 维度 / 条件枚举） |
| **KnowledgeGraph**（可选） | 文件型业务规则图；初始化时 `apply_to_metadata` 收窄模型可选列表 |

## 三种入口

```python
# 1) 程序代码
from openxe import OpenXE, BiMetadata

xe = OpenXE(
    metadata=BiMetadata(metrics=["售电量", "电费"], dimensions=["地市"]),
    knowledge_graph="examples/testdata/knowledge_graph.xlsx",  # optional
)
# xe.extract("…")  # Runner 接 LM 前会 NotImplementedError
print(xe.metadata.summary_text())  # effective (scoped) catalog
```

```bash
# 2) MCP（可选依赖）
uv sync --extra mcp
uv run openxe-mcp
```

```python
# 3) pydantic_ai Capability（可选依赖）
from openxe.capability import build_capability
# agent = Agent(..., capabilities=[build_capability(xe)])
```

## KnowledgeGraph Excel（英文 sheet）

实体：`topics` · `vocabularies` · `measures` · `dimensions`（列：`vid` · `name` · `description`）  
关系：`synonyms` · `hyponyms` · `represents` · `topic_measures` · `topic_dimensions` · `subtopics`（列：`src_vid` · `dst_vid`）

样例：`examples/testdata/knowledge_graph.xlsx`。

| | |
| --- | --- |
| 栈 | Python · uv · DSPy · Polars |
| 文档 | [需求](./REQUIREMENTS.md) · [分层设计](./DESIGN.md) · [入口](./ENTRIES.md) · [文件](./FILE_LAYOUT.md) |
| 状态 | 三入口 + 可选 KG 已落；Predict/归一完整实现待续 |
