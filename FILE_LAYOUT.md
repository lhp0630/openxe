# openxe — Python 文件命名规划

> 架构见 [DESIGN.md](./DESIGN.md)、入口见 [ENTRIES.md](./ENTRIES.md)。
> **Runtime 可插拔 Signature** + **Product = 通用 BI 要素提取** + **可选 KnowledgeGraph**；三入口骨架已落。

## 1. 约定

| 项 | 规则 |
| --- | --- |
| 包根 | `src/openxe/` |
| 分层 | `pipeline/` = Runtime；`bi/` = Product；`knowledge_graph/` = 可选业务规则图 |
| 禁止 | Runtime 内写「指标/维度/条件」常量或行业词；禁止把开源定位做成任意 NLP 运行时 |

## 2. 树形一览

```text
openxe/
├── main.py                          # [过渡] uv 脚手架
├── DESIGN.md · ENTRIES.md           # 分层设计 · 三种入口
├── src/openxe/
│   ├── __init__.py                  # from openxe import OpenXE, ...
│   ├── api.py                       # OpenXE 程序代码门面（入口一）
│   ├── lm.py · exceptions.py
│   │
│   ├── pipeline/                    # Runtime
│   │   ├── signature_spec.py · runner.py · optimize.py
│   │   └── adapters/code.py · klass.py
│   │
│   ├── bi/                          # Product：BI 要素
│   │   ├── extractor.py · metadata.py · result.py
│   │   ├── normalize.py · default_signature.py
│   │
│   ├── knowledge_graph/             # 可选：文件型业务规则图
│   │   ├── __init__.py
│   │   ├── models.py                # Topic / Vocabulary / Measure / Dimension
│   │   ├── base.py                  # KnowledgeGraphBase · InMemory · apply_to_metadata
│   │   └── file_graph.py            # FileKnowledgeGraph（Excel / Polars）
│   │
│   ├── mcp/                         # 入口二：MCP（optional extra）
│   │   ├── __init__.py · server.py · __main__.py
│   │
│   └── capability/                  # 入口三：pydantic_ai（optional extra）
│       ├── __init__.py · pydantic_ai.py
│
├── examples/
│   ├── basic_extract.py             # 入口一示例（含可选 KG）
│   ├── testdata/knowledge_graph.xlsx
│   ├── mcp_extract.py
│   └── capability_extract.py
└── tests/
    ├── test_api_openxe.py
    ├── test_knowledge_graph.py
    ├── test_mcp_server.py
    ├── test_capability_pydantic_ai.py
    └── …（既有 bi / pipeline 测试）
```

## 3. 数据流

```text
[Product]
  BiMetadata (full catalog)
       │
       ├─ optional KnowledgeGraph.apply_to_metadata → effective BiMetadata
       │
  text + effective metadata
       │
       ├─ default_signature / 自定义 SignatureSpec
       ▼
[Runtime]
  SignatureSpec.resolve() → Signature 类
  Runner(lm, state?) → {OutputField...}     ← 通用、无 BI 语义
       │
       ▼
[Product]
  normalize(+ effective BiMetadata) → BiResult JSON
```

## 4. Excel 约定（`FileKnowledgeGraph`）

实体 sheet 列：`vid` · `name` · `description`（给人读的说明）

| sheet | 含义 |
| --- | --- |
| `topics` / `vocabularies` / `measures` / `dimensions` | 四类实体 |

关系 sheet 列：`src_vid` · `dst_vid`

| sheet | 边 |
| --- | --- |
| `synonyms` · `hyponyms` · `represents` | 词表 |
| `topic_measures` · `topic_dimensions` · `subtopics` | 主题结构 |

不含 Note / BizGlossary；无中文 sheet / 标题。

## 5. Runtime ↔ demo 对应

| dspy_lfx_demo | openxe Runtime |
| --- | --- |
| `signature_code` 字符串 | `adapters/code.py` |
| 具体 Signature 类（进阶） | `adapters/klass.py` |
| `_extract_signature_from_code` / 字段内省 | `signature_spec.py` + adapters |
| `Predict` + OutputField dict | `runner.py` |
| program `state` | `runner` 消费 · `optimize` 产出 |

## 6. 模块职责对照

| 需求 | 落点 |
| --- | --- |
| 可插拔 Signature 进 | `signature_spec` + `adapters/*` |
| 通用 Predict / Output | `runner.py` |
| BI 要素提取（产品核心） | `bi/extractor` · `metadata` · `result` · `normalize` |
| 业务规则圈定可见目录 | `knowledge_graph/*` · `OpenXE(knowledge_graph=…)` |
| 开箱 BI 体验 | `bi/default_signature.py` + `examples/basic_extract.py` |
| 换行业不改 Runtime | 换 `BiMetadata`（± Spec）；换主题口径换 KG |

## 7. 明确不建

| 路径 | 原因 |
| --- | --- |
| `pipeline` 内 BI 槽位硬编码 | 破坏分层 |
| 根级「万能 Extractor」抢产品叙事 | 对外只推 `bi` / `OpenXE` |
| `server.py` / NL2SQL 执行 | 非目标 |
| KG 内 Note / BizGlossary | 产品范围外 |

## 8. `main.py`

过渡用；演示以 `examples/basic_extract.py` 为准。
