# 阶段 A 研究与课程设计报告

日期：2026-10-09

## 本阶段交付

- `research/research_plan.md`
- `research/references.md`
- `research/fact_check_matrix.md`
- `research/open_questions.md`
- `research/version_history.md`
- `course_map.md`
- `lesson_plans/lesson_01_plan.md` 至 `lesson_plans/lesson_30_plan.md`
- `qa/acceptance_criteria.md`
- `DECISIONS.md` 与 `PROJECT_STATUS.md`

## 研究综述

表格学习的课程脉络从数据结构、实验协议和评估开始，进入决策树、Bagging、Boosting/GBDT，再扩展到 XGBoost 与 CatBoost 的工程和类别处理；随后介绍 MLP、Transformer 和 FT-Transformer，最后讨论以 PFN/TabPFN 为代表的预训练式表格学习、上下文推断、版本边界与研究实验。

XGBoost 的核心贡献是把正则化树提升、二阶近似、稀疏感知、近似分裂和系统优化结合起来；CatBoost 重点处理类别特征及有序提升造成的预测偏移问题；FT-Transformer 将特征编码为 token 并用 Transformer 建模特征交互，同时其比较结论必须绑定原论文实验协议；TabPFN/PFN 的核心方向是离线在任务分布上预训练一个模型，使新数据集的带标签样本作为上下文参与推断。后者不能被简化为“完全不训练”或“对所有表格任务都更强”。

## 关键风险

1. TabPFN 版本、默认模型、API 和规模限制会变化，必须以核验日期和版本记录。
2. 原始论文、官方仓库和官方文档回答的是不同问题，不能相互替代。
3. 树模型与深度模型的比较强依赖数据、预算、拆分、调参和实现。
4. ICL 在 TabPFN 中应采用操作性定义，不能把语言模型的全部机制直接迁移。
5. 任何性能数字和运行成本必须有实验记录，不能由摘要或二手资料推断。

## 质量结果

- 事实核验：部分通过；已打开并记录 XGBoost、CatBoost、FT-Transformer、PFN 和 TabPFN 官方/原始来源，TabPFN 当前默认版本和许可证已更新；逐主张上下文核对、Models 页面和实测仍待完成。
- 教学完整度：通过阶段 A 计划门槛；尚未制作课件，不能宣称课程内容通过。
- HTML 交互：未开始。
- 代码验证：未开始。
- 响应式与可访问性：未开始。
- 链接与引用：研究入口已建立，正式课件引用尚未生成。

## 尚未解决

- 当前 TabPFN Models 页面、限制、API 和解释/校准能力的逐项核验。
- 统一 benchmark 数据集、运行环境和实验预算。
- 设计系统的具体颜色、公式方案和离线依赖选择。

## 下一步

阶段 B：建立统一设计系统，制作第 05 节或第 08 节高质量样板课和课程首页原型；先完成研究核验中的阻塞事实，再开始正式 HTML。
