# DSPy / LFX demo → openxe Runtime 参考提炼

- **角色：** `docs/research/supplementary/` 专项证据（独立价值；非当前主结论入口）
- **日期：** 2026-11-25
- **来源：** 本地 `work/dspy_lfx_demo.md`（被 `work/.gitignore` 忽略，不入库）
- **性质：** 调研补充。**不构成**维护者批准或 Runtime API 冻结。
- **消费方：** [`RFC-ARCH-001`](../../../RFCs/RFC-ARCH-001-runtime-product-kg-layering.md)（Draft）；主报告 [`../2026-11-25-root-docs-and-work-notes-disposition.md`](../2026-11-25-root-docs-and-work-notes-disposition.md)

## 1. 为何单独保留

`DESIGN.md` / `FILE_LAYOUT.md` 已声明 Runtime 对齐 demo，但原始文件是完整 LFX `Component` 草稿（含未完成的 `_make_lfx_input`），不适合作为仓库活文档。本报告只保留 **对 openxe Runtime 仍有约束力的行为观察**。

## 2. Verified：demo 中的可迁移行为

| Demo 行为 | 对 Runtime 的含义 | openxe 落点（规划/骨架） |
|-----------|-------------------|---------------------------|
| 用户提供 Signature **代码字符串**，`exec` 后取最后一个公开 `dspy.Signature` 子类 | 字符串进为主路径 | `pipeline/adapters/code.py` → `CodeSignatureSpec` |
| 要求至少一个 InputField、至少一个 OutputField | Spec 校验契约 | `signature_spec.py` `validate()` |
| `dspy.Predict(signature)` + 按 InputField 名取 kwargs | Runner 领域无关 | `pipeline/runner.py` `run_predict`（LM 路径待接） |
| 结果只取 OutputField 键 | 返回通用 dict，无 BI 语义 | Runner 契约；BI 在 `normalize` |
| 可选 program `state` / `load_state` | 优化产物可恢复 | `runner` 参数 + `optimize.py`（未实现） |
| LM 参数从宿主模型对象抽取（demo 绑 ChatOpenAI） | openxe 应 **外置 LM**，不绑 LFX | `lm.py` / 调用方注入 |

## 3. Survey：刻意不迁入的部分

| Demo 内容 | 不迁入理由 |
|-----------|------------|
| LFX `Component` / `CodeInput` / `HandleInput` / 动态 `update_build_config` | 产品入口是库 / MCP / Capability，不是 LFX 节点 |
| 情感分析等示例 Signature | 开源叙事钉死 **BI 要素**；示例属 Product 默认模板 |
| `_make_lfx_input` 未完成桩 | 无信息价值 |
| 在组件内硬编码 OpenAI 模型名改写 | 与「可替换模型」非功能需求冲突 |

## 4. Design proposal（供 RFC，非已接受）

1. Runtime **禁止**出现「指标 / 维度 / 条件」或行业词常量（与 demo「通用 Signature 组件」一致，但产品层反向钉死 BI）。
2. `CodeSignatureSpec` 的解析规则与 demo 对齐：最后一个公开 Signature 子类；空代码 / 无子类 → 明确错误。
3. `ClassSignatureSpec` 为辅路径（demo 无此形态，属 openxe 扩展），避免库内已有类再经字符串 round-trip。
4. 完整 Predict 接线应以本表 §2 为验收清单，而不是回贴 demo 源码。

## 5. Open assumptions

- Demo 是否仍会更新：若更新，应再出 dated supplementary，而不是改写本文件沉默漂移。
- LFX 是否成为第四入口：当前根文档与代码均未规划；若需要，另开 RFC，不在本报告范围。

## 6. References

- 本地源：`work/dspy_lfx_demo.md`
- 代码：`src/openxe/pipeline/adapters/code.py`、`signature_spec.py`、`runner.py`
- 根规划：`DESIGN.md` §3、`FILE_LAYOUT.md` §5
