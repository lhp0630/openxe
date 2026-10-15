# openxe — 三种入口规划

> 产品核心仍是 BI 要素提取；三种入口共用同一 `OpenXE` / `BiExtractor` 内核。
> 可选 `knowledge_graph` 在初始化时圈定模型可见元数据（见 [DESIGN.md](./DESIGN.md) §4.2）。

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
              OpenXE(metadata, knowledge_graph?=None)
                              ▼
                     BiExtractor(effective metadata)
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

xe = OpenXE(
    metadata=BiMetadata(...),                 # 全量目录
    knowledge_graph="path/to/knowledge_graph.xlsx",  # 可选：业务规则圈定
)
result = xe.extract("南京市2026年居民售电量")
print(result.to_dict())
```

- `OpenXE`：稳定对外门面（薄封装 `BiExtractor`）
- `knowledge_graph`：`KnowledgeGraphBase` 实例、或 Excel 路径；省略则不圈定
- 进阶仍可深入 `openxe.bi` / `openxe.knowledge_graph` / `openxe.pipeline`

## 3. 入口二：MCP

- 暴露 tool：`extract_bi_elements(query: str) -> JSON`
- 可选 resource：当前（有效）元数据摘要（骨架预留）
- 进程入口：`python -m openxe.mcp` / 脚本 `openxe-mcp`
- 元数据 / KG：进程启动时注入（环境变量或配置；KG 为后续扩展点）

## 4. 入口三：pydantic_ai Capability

- `OpenXECapability`：基于 `pydantic_ai.capabilities.Capability`（或 `AbstractCapability`）
- 向 Agent 注入 tool（如 `extract_bi_elements`），内部调 `OpenXE.extract`
- 构造时传入已配置好 `metadata` / 可选 `knowledge_graph` 的 `OpenXE` 实例
- 可选 `defer_loading=True` 作 on-demand capability（骨架字段预留）

## 5. 依赖边界

| extra | 包 |
| --- | --- |
| （默认） | `dspy` · `pydantic` · `polars` · `fastexcel` |
| `mcp` | `mcp` |
| `pydantic-ai` | `pydantic-ai` |
| `all` | 上述全部 |
