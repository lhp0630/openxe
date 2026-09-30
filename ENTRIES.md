# openxe — 三种入口规划

> 产品核心仍是 BI 要素提取；三种入口共用同一 `OpenXE` / `BiExtractor` 内核。

## 1. 总览

```text
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐
│ 1. 程序代码接入  │  │ 2. MCP 接入       │  │ 3. pydantic_ai Capability │
│ from openxe     │  │ openxe-mcp /      │  │ Agent(capabilities=[…]) │
│   import OpenXE │  │ python -m …mcp   │  │                         │
└────────┬────────┘  └────────┬─────────┘  └────────────┬────────────┘
         │                    │                         │
         └────────────────────┼─────────────────────────┘
                              ▼
                     OpenXE / BiExtractor
                              ▼
                     pipeline Runtime + BI normalize
```

| 入口 | 包路径 | 典型用法 |
| --- | --- | --- |
| 程序代码 | `openxe.api.OpenXE`（根再导出） | `from openxe import OpenXE` |
| MCP | `openxe.mcp` | `uv run openxe-mcp` / stdio |
| pydantic_ai | `openxe.capability.pydantic_ai` | `Agent(..., capabilities=[...])` |

MCP / Capability 为 **可选依赖**（`openxe[mcp]`、`openxe[pydantic-ai]`），核心库不强制安装。

## 2. 入口一：程序代码

```python
from openxe import OpenXE, BiMetadata

xe = OpenXE(metadata=BiMetadata(...))
result = xe.extract("南京市2026年居民售电量")
print(result.to_dict())
```

- `OpenXE`：稳定对外门面（薄封装 `BiExtractor`）
- 进阶仍可深入 `openxe.bi` / `openxe.pipeline`

## 3. 入口二：MCP

- 暴露 tool：`extract_bi_elements(query: str) -> JSON`
- 可选 resource：当前元数据摘要（骨架预留）
- 进程入口：`python -m openxe.mcp` / 脚本 `openxe-mcp`

## 4. 入口三：pydantic_ai Capability

- `OpenXECapability`：基于 `pydantic_ai.capabilities.Capability`（或 `AbstractCapability`）
- 向 Agent 注入 tool（如 `extract_bi_elements`），内部调 `OpenXE.extract`
- 可选 `defer_loading=True` 作 on-demand capability（骨架字段预留）

## 5. 依赖边界

| extra | 包 |
| --- | --- |
| （默认） | `dspy` · `pydantic` |
| `mcp` | `mcp` |
| `pydantic-ai` | `pydantic-ai` |
| `all` | 上述全部 |
