# CatBoost 主张核验记录

核验日期：2026-10-10  
对象：第 10 节课件与计划  
范围：论文机制与官方实现文档；不把当前库默认参数外推为论文结论。

## 结论

第 10 节的核心表述与 CatBoost 原始论文摘要及 CatBoost 官方算法文档一致，当前未发现需要修改的事实性过度断言。课件明确说明有序统计中的“过去”来自构造的随机排列，不必然是现实时间过去；同时明确说明有序方法不使所有泄漏风险消失、也不能推出所有任务都更强。

## 主张—证据对照

| 课件主张 | 原始依据 | 判定与边界 |
|---|---|---|
| 直接用当前样本标签做目标统计会引入泄漏或 prediction shift 风险 | CatBoost 论文摘要；官方 Unbiased boosting 文档 | 通过；“风险”表述比“必然完全泄漏”更准确。 |
| Ordered Boosting 是排列驱动的经典 boosting 替代方案，用于应对 prediction shift | CatBoost 论文摘要 | 通过；论文摘要直接将 ordered boosting 与 prediction shift 联系起来。 |
| 类别统计按随机排列生成，使用当前对象之前已计算的信息并配合 prior | 官方类别特征转换文档的随机排列、CTR 说明与公式描述 | 通过；这是实现流程描述，具体 CTR 类型、组合和参数仍受版本/配置影响。 |
| CatBoost 支持 one-hot，并可通过 `one_hot_max_size` 控制适用类别基数 | 官方类别特征转换文档 | 通过；课件只将其作为对照，不声称 CatBoost 总是使用同一种编码。 |
| CatBoost 不是“支持类别的 XGBoost”，也不是无条件最强 | 课程边界表述与论文/官方文档范围 | 通过；属于合理的教学边界，不是可量化性能结论。 |

## 来源

- 原始论文摘要：<https://arxiv.org/abs/1706.09516>。
- 官方有序提升说明：<https://catboost.ai/docs/en/concepts/algorithm-main-stages_fighting-biases>。
- 官方类别特征转换说明：<https://catboost.ai/docs/en/concepts/algorithm-main-stages_cat-to-numberic>。
- 课程来源登记：`research/references.md` 的 R02、R12、R14。

## 未覆盖项

本记录不证明当前安装的 `catboost` 版本、默认 CTR 配置或所有损失函数都与论文示例完全相同；也不替代当前版本 API smoke test、类别特征实验和资源测量。性能结论仍以仓库实验协议和日志为准。
