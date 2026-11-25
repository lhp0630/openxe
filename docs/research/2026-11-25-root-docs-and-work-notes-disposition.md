# 根目录 Markdown 与 work/ 随手笔记：文档落点清查

- **角色：** `docs/research/` 下**当前研究结论主入口**（扁平 + 日期文件名；索引见 [`README.md`](./README.md)）
- **日期：** 2026-11-25
- **范围：** `work/` 全部笔记、仓库根目录 Markdown；对照 smtgit 文档治理中的 **Research / RFC / living docs** 三分法（**不**引入 Agent Rules）
- **性质：** 调研报告。**不构成**维护者批准、RFC 接受或授权删除/搬迁根目录文档。
- **相关提案（Draft，待维护者裁定）：**
  - [`RFCs/RFC-DOC-001-documentation-governance-bootstrap.md`](../../RFCs/RFC-DOC-001-documentation-governance-bootstrap.md)
  - [`RFCs/RFC-ARCH-001-runtime-product-kg-layering.md`](../../RFCs/RFC-ARCH-001-runtime-product-kg-layering.md)

## 1. 问题

openxe 根目录同时存在多份「规划/设计」Markdown（`REQUIREMENTS.md`、`DESIGN.md`、`ENTRIES.md`、`FILE_LAYOUT.md`），与产品向 `README.md` 交叉引用；本地 `work/` 另有未入库笔记。缺少统一落点规则时会出现：

1. **决策与现状混写** — 设计意图与「已实现骨架」难以区分。
2. **角色重叠** — 同一内容既像需求、又像架构决策、又像文件清单。
3. **随手笔记无法进仓** — `work/.gitignore` 为 `*`，有价值证据需提炼后才能纳入 Git。

本报告回答：**哪些应进调研报告、哪些应进 RFC、哪些应保留为活文档、哪些应丢弃或不入库。**

## 2. 方法与证据边界

| 类别 | 本报告如何处理 |
|------|----------------|
| **Verified facts** | 路径存在性、代码行为（如 `run_predict` 仍 `NotImplementedError`）、`work/.gitignore` |
| **Survey findings** | 各文档主题、与三分法的匹配度 |
| **Design proposals** | 落点建议；需 RFC 承载的决策单独成文 |
| **Open assumptions** | 维护者是否接受「根目录设计文逐步迁出」 |

**未做：** 改写应用源码；接受任何 RFC；把 `/home/lma/smtgit` 的 Agent Rules 拷入本仓。

## 3. 仓库文档盘点（Verified）

### 3.1 根目录 Markdown

| 文件 | 主题摘要 | 篇幅角色（现状） |
|------|----------|------------------|
| [`README.md`](../../README.md) | 产品定位、三入口、KG 一句话、文档链接 | 对外总览（活文档） |
| [`REQUIREMENTS.md`](../../REQUIREMENTS.md) | 命名、背景、目标、F/N 需求、非目标、阶段备忘 | 需求 + 部分进度勾选 |
| [`DESIGN.md`](../../DESIGN.md) | Runtime / Product / KG 分层契约与边界 | 架构决策叙述 |
| [`ENTRIES.md`](../../ENTRIES.md) | 代码 / MCP / pydantic_ai 三入口与依赖边界 | 接入面设计 |
| [`FILE_LAYOUT.md`](../../FILE_LAYOUT.md) | `src/openxe` 树、数据流、Excel sheet、与 demo 对照 | 实现落点规划 |

### 3.2 `work/`（本地，默认不入库）

| 文件 | 主题摘要 | 信息价值 |
|------|----------|----------|
| `work/todo.md` | 已完成骨架项 + 待办（Predict 路径、E2E、MCP/Capability 注入 KG） | 进度便签；**无独立长期证据价值** |
| `work/dspy_lfx_demo.md` | LFX 组件内 DSPy Signature 解析 / Predict / state 参考实现 | **Runtime 设计证据**；已在 `FILE_LAYOUT` / `DESIGN` 中引用 |

### 3.3 实现状态抽查（Verified，支撑「规划≠完成」）

| 断言 | 证据 |
|------|------|
| 三入口 + 可选 KG 骨架已落 | `src/openxe/api.py`、`mcp/`、`capability/`、`knowledge_graph/` |
| Runner Predict 未接 LM | `src/openxe/pipeline/runner.py` 在校验后 `raise NotImplementedError` |
| `work/` 整体被忽略 | `work/.gitignore` 内容为 `*` |

## 4. 三分法对照

| 问题 | 落点 |
|------|------|
| 我们学到了什么、有哪些选项？ | `docs/research/` |
| 我们应该做什么、为何如此？ | `RFCs/`（Status 仅维护者可接受） |
| 用户现在如何用、契约是什么？ | `README.md` +（治理接受后）`docs/` 活文档 |

**本仓刻意不做：** `.agents/rules/`、`AGENTS.md` 体系迁入（维护者另议）。

## 5. 逐文档处置建议

| 文档 | 建议角色 | 动作 | 理由 |
|------|----------|------|------|
| `README.md` | **Living** | **保留**；治理 RFC 接受后可把文档链改到 `docs/research` / `RFCs` | 产品总览，不属于决策记录 |
| `REQUIREMENTS.md` | **过渡 Living → 动机并入 RFC** | **暂留根目录**；问题/目标/非目标已写入 `RFC-ARCH-001`；接受后可缩为 `docs/` 需求摘要或只保留 RFC + README | 「需求清单」有活文档价值，但「阶段勾选」应随代码更新，不宜永久当决策源 |
| `DESIGN.md` | **RFC 候选（已提炼）** | 内容提炼为 **`RFC-ARCH-001` Draft**；接受前根文件可作对照副本，接受后勿双源维护 | 明确回答 *what should we do*（分层、契约、非目标） |
| `ENTRIES.md` | **并入架构 RFC** | 并入 `RFC-ARCH-001` §接入入口；不必单独 RFC | 与内核分层同一决策面 |
| `FILE_LAYOUT.md` | **并入架构 RFC** | 并入 `RFC-ARCH-001` §文件布局；以 `src/` 为最终真相 | 规划树易漂移；决策在 RFC，现状以代码为准 |
| `work/todo.md` | **Ephemeral** | **不入库**；开放项写入本报告 §7 | 无审计价值的便签 |
| `work/dspy_lfx_demo.md` | **Research supplementary** | 已提炼为 [`supplementary/2026-11-25-dspy-lfx-runtime-reference.md`](./supplementary/2026-11-25-dspy-lfx-runtime-reference.md)；原始 demo **不必**进仓 | 证据进 research；完整组件代码属参考草稿 |

### 5.1 是否「整篇转换成」调研报告或 RFC？

| 文档 | 整篇改名搬迁？ | 说明 |
|------|----------------|------|
| `README.md` | **否** | 保持 README |
| `REQUIREMENTS.md` | **否（整篇）** | 问题陈述进 RFC 动机；不必整份改成 research |
| `DESIGN.md` + `ENTRIES.md` + `FILE_LAYOUT.md` | **否（机械搬迁）**；**是（决策提炼）** | 用一份架构 RFC 吸收决策，避免三份并行「准 RFC」 |
| `work/*` | **否** | 只提炼有信息增量的结论 |

**结论（Survey）：** 根目录多份 Markdown **需要纳入治理**，但正确做法是 **按角色拆分/提炼**，而不是把每份文件一对一改名为 research 或 RFC。

## 6. 已产出的仓库文档（本轮）

| 产出 | 路径 | 状态 |
|------|------|------|
| 本主报告 | `docs/research/2026-11-25-root-docs-and-work-notes-disposition.md` | 调研结论 |
| Runtime 参考专项 | `docs/research/supplementary/2026-11-25-dspy-lfx-runtime-reference.md` | 调研补充 |
| 文档治理 RFC | `RFCs/RFC-DOC-001-…` | **Draft** |
| 分层架构 RFC | `RFCs/RFC-ARCH-001-…` | **Draft** |
| RFC 过程与模板 | `RFCs/README.md`、`process.md`、`TEMPLATE.md` | 过程基础设施 |

## 7. 从 `work/todo.md` 摘出的开放实现项（非 RFC 接受）

以下为进度备忘，供实现跟踪；**不**表示架构未定：

- [ ] Runner `Predict` + BI `normalize` 完整路径（接 LM）
- [ ] 示例端到端可跑通（需 LM）
- [ ] MCP / Capability 启动参数支持注入 KG 路径

## 8. 给维护者的裁定点

1. 是否接受 **仅 Research + RFC**（暂不引入 Agent Rules）作为本仓文档治理最小集？（见 `RFC-DOC-001`）
2. 是否接受将 Runtime / Product / KG / 三入口 / 文件布局 **合并为一份** `RFC-ARCH-001`？
3. `RFC-ARCH-001` 接受后，根目录 `DESIGN.md` / `ENTRIES.md` / `FILE_LAYOUT.md` / `REQUIREMENTS.md` 是 **归档删除、迁入 `docs/archive/`、还是保留为非规范导读**？

## 9. References

- smtgit 治理入口（外部参照，非本仓规范）：`/home/lma/smtgit/AGENTS.md` — Documentation governance 表
- smtgit research 布局：`/home/lma/smtgit/docs/research/README.md`
- 本仓源文件：§3 所列路径；`src/openxe/pipeline/runner.py`
