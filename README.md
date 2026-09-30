# openxe

**Open eXtract Elements** — 通用 **BI 要素**抽取（DSPy）。

自然语言 → `{指标, 维度, 条件}`；换元数据适配不同数仓/行业。底层为可插拔 Signature 运行时。

```text
南京市2026年居民售电量
        ↓  openxe(+ BI 元数据)
{ "指标": ["售电量"], "维度": [], "条件": { "地市": "南京", "年份": "2026", "分类": ["乡村居民", "城镇居民"] } }
```

## 三种入口

```python
# 1) 程序代码
from openxe import OpenXE, BiMetadata
xe = OpenXE(metadata=BiMetadata(metrics=["售电量"]))
# xe.extract("…")  # Runner 骨架未接 LM 前会 NotImplementedError
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

| | |
| --- | --- |
| 栈 | Python · uv · DSPy |
| 文档 | [需求](./REQUIREMENTS.md) · [分层设计](./DESIGN.md) · [入口](./ENTRIES.md) · [文件](./FILE_LAYOUT.md) |
| 状态 | 三入口骨架已落；Predict/归一完整实现待续 |
