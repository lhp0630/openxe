# openxe — Python 文件命名规划

> 架构见 [DESIGN.md](./DESIGN.md)、入口见 [ENTRIES.md](./ENTRIES.md)。
> **Runtime 可插拔 Signature** + **Product = 通用 BI 要素提取**；三入口骨架已落。

## 1. 约定

| 项 | 规则 |
| --- | --- |
| 包根 | `src/openxe/` |
| 两层 | `pipeline/` = Runtime（领域无关）；`bi/` = Product（BI 要素） |
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
│   ├── mcp/                         # 入口二：MCP（optional extra）
│   │   ├── __init__.py · server.py · __main__.py
│   │
│   └── capability/                  # 入口三：pydantic_ai（optional extra）
│       ├── __init__.py · pydantic_ai.py
│
├── examples/
│   ├── basic_extract.py             # 入口一示例
│   ├── mcp_extract.py               # 入口二说明/占位
│   └── capability_extract.py        # 入口三说明/占位
└── tests/
    ├── test_api_openxe.py
    ├── test_mcp_server.py
    ├── test_capability_pydantic_ai.py
    └── …（既有 bi / pipeline 测试）
```

已移除/不再使用的旧占位（若仓库中仍有则视为废弃）：

- 根级 `extractor.py` / `metadata.py` / `result.py` / `normalize.py` → 迁入 `bi/`
- `pipeline/signature_code.py` → 并入 `pipeline/adapters/code.py`

## 3. 数据流

```text
[Product]
  text + BiMetadata
       │
       ├─ default_signature / 自定义 SignatureSpec
       ▼
[Runtime]
  SignatureSpec.resolve() → Signature 类
  Runner(lm, state?) → {OutputField...}     ← 通用、无 BI 语义
       │
       ▼
[Product]
  normalize(+ BiMetadata) → BiResult JSON   ← 指标 / 维度 / 条件
```

## 4. Runtime ↔ demo 对应

| dspy_lfx_demo | openxe Runtime |
| --- | --- |
| `signature_code` 字符串 | `adapters/code.py` |
| 具体 Signature 类（进阶） | `adapters/klass.py` |
| `_extract_signature_from_code` / 字段内省 | `signature_spec.py` + adapters |
| `Predict` + OutputField dict | `runner.py` |
| program `state` | `runner` 消费 · `optimize` 产出 |

## 5. 模块职责对照

| 需求 | 落点 |
| --- | --- |
| 可插拔 Signature 进 | `signature_spec` + `adapters/*` |
| 通用 Predict / Output | `runner.py` |
| BI 要素提取（产品核心） | `bi/extractor` · `metadata` · `result` · `normalize` |
| 开箱 BI 体验 | `bi/default_signature.py` + `examples/basic_extract.py` |
| 换行业不改 Runtime | 换 `BiMetadata`（± 换 Spec / 模板描述） |

## 6. 明确不建

| 路径 | 原因 |
| --- | --- |
| `pipeline` 内 BI 槽位硬编码 | 破坏分层 |
| 根级「万能 Extractor」抢产品叙事 | 对外只推 `bi` |
| `server.py` / NL2SQL 执行 | 非目标 |

## 7. `main.py`

过渡用；演示以 `examples/basic_extract.py` 为准。
