# openxe — 分层抽象设计

> 机制可插拔；产品钉死 BI。实现代码另议；本文只定边界与契约。

## 1. 一句话

| 层 | 定位 |
| --- | --- |
| **Runtime（机制）** | 可插拔 Signature 运行时：多种方式「进」Signature，统一 Predict，通用 Output dict 出 |
| **Product（产品）** | **通用 BI 要素提取**：自然语言 → 指标 / 维度 / 条件（键名与枚举由 BI 元数据约束） |

对外开源叙事与默认 API 只讲 Product；Runtime 是可复用底座，不单独包装成「任意领域抽取库」。

---

## 2. 分层图

```text
┌──────────────────────────────────────────────────────────┐
│ Product · BI 要素提取（默认对外 API）                      │
│  BiExtractor(metadata, lm, signature_spec?=默认BI模板)   │
│  text → BiResult JSON {指标, 维度, 条件, ...}              │
│  metadata：合法指标/维/条件枚举 · 空槽约定 · 归一          │
└────────────────────────────┬─────────────────────────────┘
                             │ 组装 InputField kwargs
                             │ 消费 OutputField dict → 归一
┌────────────────────────────▼─────────────────────────────┐
│ Runtime · 可插拔 Signature 运行时（领域无关）              │
│  SignatureSpec  ──resolve──►  type[dspy.Signature]         │
│  Runner(lm, state?) · Predict · OutputField-only dict    │
│  Optimize → state（可选）                                  │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Runtime：Signature 如何「进」（抽象）

### 3.1 核心抽象：`SignatureSpec`

统一「签名来源」，对 Runner 只暴露已解析的 Signature 类与字段元信息。

```text
SignatureSpec（协议 / ABC）
  resolve() -> SignatureType
  input_fields  -> 映射（名 → 字段信息）
  output_fields -> 映射（名 → 字段信息）
```

约束（对齐 `work/dspy_lfx_demo.md`）：

- 至少一个 `InputField`、至少一个 `OutputField`
- Runner **不**假设字段名；只按内省结果传参与收结果
- 返回值为 **通用** `{output_field_name: value}`，不含 BI 语义

### 3.2 适配器（可插拔进法）

| 适配器 | 进法 | 说明 |
| --- | --- | --- |
| `CodeSignatureSpec` | **Signature 代码字符串** | 主路径；`exec` 取最后一个公开 Signature 子类（同 demo） |
| `ClassSignatureSpec` | **具体 `dspy.Signature` 子类** | 库内/调用方已有类对象时直接注入，免字符串 |
| （预留） | dict / builder | 非目标；需要时再扩，不提前实现 |

Product 默认使用 **内置 BI 签名模板字符串** 经 `CodeSignatureSpec` 加载；进阶用户可替换为自定义 `SignatureSpec`（字符串或类），但 Product 层仍要求输出能被 BI 归一理解（或用户自担后处理）。

### 3.3 Runner / Optimize

| 组件 | 职责 |
| --- | --- |
| `Runner` | `dspy.Predict(spec.resolve())`；按 InputField 收 kwargs；可选 `load_state`；只返回 OutputField dict |
| `Optimize` | 编译/few-shot → 产出 state，供 Runner 恢复 |

Runtime **禁止**出现「指标 / 维度 / 条件」常量或电力等行业词。

---

## 4. Product：通用 BI 要素提取

### 4.1 目标契约（可配置键名，语义固定）

默认语义槽位：

| 槽位 | 含义 | 典型形态 |
| --- | --- | --- |
| 指标 | 度量什么 | `list[str]` |
| 维度 | 按什么切 | `list[str]`（可空） |
| 条件 | 过滤约束 | `dict[str, str \| list[str]]` |

键名可由元数据配置（如英文 `metrics` / `dimensions` / `filters`），**语义角色**不变。

### 4.2 BI 元数据

初始化注入，决定：

- 合法指标 / 维度成员、条件字段与枚举（含多值）
- 顶层键名映射
- 未提及槽位的空值约定（`[]` / `null` / `{}`）
- 别名 → 合法值的归一规则（如「居民」→ 乡村/城镇居民）

换行业 / 换数仓 = **换元数据**（± 换 Signature 描述里的提示），不改 Runtime。

### 4.3 默认 Signature（产品内置模板，仍走 Spec）

内置一段 **BI 向** Signature 代码字符串（或等价 `ClassSignatureSpec`），示意：

- Input：自然语言查询（及可选：元数据摘要字符串）
- Output：与 BI 槽位对齐的字段（或单一结构化 JSON 字段，再由 normalize 拆开——实现阶段二选一，规划保留弹性）

用户可插拔替换 Spec；默认路径保证开箱即是 BI 抽取。

### 4.4 门面

`BiExtractor`（对外也可导出为 `Extractor`）：

1. 绑定 `BiMetadata` + LM + `SignatureSpec`（默认 BI 模板）
2. `extract(text) -> BiResult`
3. 内部：拼 Input → `Runner` → 原始 dict → `normalize` → `BiResult`

---

## 5. 边界与非目标

| 做 | 不做 |
| --- | --- |
| BI 要素 JSON，喂报表 / NL2SQL / 指标平台 | 完整 SQL 生成与执行 |
| Signature 字符串或类两种进法 | 把开源定位做成「任意 NLP 任务运行时」 |
| 元数据约束下的归一 | GUI、绑定 oneboard Spec |
| state / 优化扩展点 | 在 Runtime 写死行业 Schema |

---

## 6. 与既有文档关系

| 文档 | 关系 |
| --- | --- |
| [REQUIREMENTS.md](./REQUIREMENTS.md) | 产品需求与背景；以本设计的 Product 层为准 |
| [FILE_LAYOUT.md](./FILE_LAYOUT.md) | 文件落点；Runtime / Product 分目录 |
| [README.md](./README.md) | 对外只强调 BI；机制一句带过 |
| `work/dspy_lfx_demo.md` | Runtime 中 `CodeSignatureSpec` 的参考实现 |

---

## 7. 三种接入入口

详见 [ENTRIES.md](./ENTRIES.md)。内核统一为 `OpenXE`（封装 `BiExtractor`）：

| 入口 | 说明 |
| --- | --- |
| 程序代码 | `from openxe import OpenXE` |
| MCP | `openxe.mcp`（可选依赖 `openxe[mcp]`） |
| pydantic_ai Capability | `openxe.capability`（可选依赖 `openxe[pydantic-ai]`） |

## 8. 决策摘要

1. **产品核心** = 通用 BI 要素提取（指标 / 维度 / 条件 + 元数据）。
2. **机制** = 可插拔 `SignatureSpec`（字符串进为主，类进为辅）+ 通用 Runner。
3. **接入** = 代码 / MCP / pydantic_ai Capability 三入口，共用 `OpenXE`。
4. 默认体验 = 内置 BI Signature 模板；高级用户换 Spec，但不改变「我们是 BI 抽取」的定位。
