# openxe — 需求与背景

## 1. 命名

| 项 | 说明 |
| --- | --- |
| 全称意向 | **Open eXtract Elements** |
| 仓库/包名 | `openxe` |
| 含义 | 面向开源的 **BI 要素**抽取：从自然语言中抽出指标、维度、条件等结构化要素 |

`xe` = e**X**tract **E**lements。架构分层见 [DESIGN.md](./DESIGN.md)。

---

## 2. 背景

业务侧常见短查询或指标描述，例如：

> 南京市2026年居民售电量

下游（报表、NL2SQL、指标平台、检索编排）需要稳定 JSON，典型 BI 要素：

- **指标**：度量什么（如售电量）
- **维度**：按什么切（可空）
- **条件**：过滤约束（地市、年份、分类等）

行业词表与 Schema 差异大，需要 **BI 元数据驱动**；抽取内核通过可插拔 Signature 运行时实现，避免绑死单一提示结构。

---

## 3. 目标

基于 **Python + uv + DSPy** 的开源库 `openxe`：

| 层 | 目标 |
| --- | --- |
| **Product（核心）** | 通用 BI 要素提取：文本 + BI 元数据 → `{指标, 维度, 条件}` 类 JSON |
| **Runtime（机制）** | 可插拔 `SignatureSpec`（代码字符串进为主，Signature 类进为辅）→ 通用 Predict → Output dict |

1. **输入**：自然语言查询 / 指标口径描述  
2. **配置**：BI 元数据（合法值、键名、空槽约定）+ 可选自定义 `SignatureSpec`（默认用内置 BI 模板）  
3. **输出**：符合该元数据约定的 BI JSON  

### 3.1 示例（示意）

```text
南京市2026年居民售电量
```

```json
{
  "指标": ["售电量"],
  "维度": [],
  "条件": {
    "地市": "南京",
    "年份": "2026",
    "分类": ["乡村居民", "城镇居民"]
  }
}
```

「居民」→ 分类枚举由 **元数据** 约束，不在库内硬编码。

---

## 4. 需求清单

### 4.1 功能需求

| ID | 需求 | 优先级 |
| --- | --- | --- |
| F1 | 短文本 BI 要素抽取，输出 JSON | P0 |
| F2 | 初始化注入 BI 元数据，决定合法值与槽位形态 | P0 |
| F3 | 换元数据适配不同行业/数仓，不改 Runtime | P0 |
| F4 | 可插拔 Signature：字符串代码 / 具体类 → 统一 Runner；支持 state / 优化扩展 | P0 |
| F5 | 默认内置 BI Signature 模板；顶层键名可配置 | P1 |
| F6 | 条件单值/多值；未提及槽位置空 | P1 |
| F7 | 最小 BI 示例 + 样例元数据，开箱可试 | P1 |

### 4.2 非功能需求

| ID | 需求 | 说明 |
| --- | --- | --- |
| N1 | 技术栈 | Python；**uv** |
| N2 | 开源友好 | BI 定位清晰；Runtime 可扩展但不抢产品叙事 |
| N3 | 可替换模型 | LM 配置外置 |
| N4 | 可测试 | Runtime 与 BI 层可分层测 |

### 4.3 非目标

- 规划阶段不写实现代码（仅设计与注释占位）
- 不做完整 NL2SQL / 查询执行 / GUI
- 不把项目定位为「任意领域通用元素抽取运行时」
- 不绑定 oneboard 等内部 Spec

---

## 5. 差异化定位

| 对比 | openxe |
| --- | --- |
| 固定 Schema NER | BI 元数据 + 默认可换 Signature 模板 |
| 纯 DSPy/LFX Signature 组件 | **产品钉死 BI 要素**；Runtime 只是底座 |
| OpenIE | 输出直接服务分析/查询编排 |

一句话：**可插拔 Signature 运行时 + 通用 BI 要素提取产品。**

---

## 6. 后续实现阶段（备忘）

1. 按 [DESIGN.md](./DESIGN.md) / [FILE_LAYOUT.md](./FILE_LAYOUT.md) 实现 Runtime（Spec + adapters + runner）
2. 实现 `bi/*`（metadata / default_signature / normalize / BiExtractor）
3. 示例与分层测试
4. 可选 `optimize` + state

---

## 7. 交付物

- [x] 命名：`openxe`
- [x] 需求与背景（本文）
- [x] README（BI 产品叙事）
- [x] 分层抽象设计：[DESIGN.md](./DESIGN.md)
- [x] 文件命名与注释占位：[FILE_LAYOUT.md](./FILE_LAYOUT.md)
- [ ] 实现代码
