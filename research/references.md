# 参考文献与官方资料

核验日期：2026-10-10。以下链接为研究入口；实际课件使用时仍需确认具体主张与版本。

| ID | 来源 | 年份/版本 | 类型 | URL | 支撑内容 | 局限 |
|---|---|---:|---|---|---|---|
| R01 | Chen & Guestrin, *XGBoost: A Scalable Tree Boosting System* | 2016 | 原始论文 | https://doi.org/10.1145/2939672.2939785 | XGBoost 目标、正则化、稀疏感知、加权分位数和系统设计 | 论文结论不能代表所有当前实现 |
| R02 | Prokhorenkova et al., *CatBoost: unbiased boosting with categorical features* | 2018 | 原始论文 | https://openreview.net/forum?id=PmLty7tODm | Ordered Boosting、类别特征处理、prediction shift | 实验版本与当前库可能不同 |
| R03 | Gorishniy et al., *Revisiting Deep Learning Models for Tabular Data* | 2021 | 原始论文 | https://arxiv.org/abs/2106.11959 | ResNet/FT-Transformer 架构与标准化比较 | 原文 HTML 已于 2026-10-10 核验；结论受数据集、预算和实现影响 |
| R04 | Hollmann et al., *TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second* | 2022 | 原始论文 | https://arxiv.org/abs/2207.01848 | 原始 TabPFN 动机、PFN 架构和小样本分类实验 | 旧版本限制不能直接用于当前版本 |
| R05 | Müller et al., *Transformers Can Do Bayesian Inference* | 2022 | 原始论文 | https://arxiv.org/abs/2112.10510 | Prior-Data Fitted Networks（PFN）范式、先验拟合与单次前向预测 | 需要结合具体 PFN/TabPFN 任务解释；不把 PFN 通用结论等同于当前 TabPFN 版本 |
| R06 | *Statistical Foundations of Prior-Data Fitted Networks* | 2023 | 理论论文 | https://arxiv.org/abs/2305.11097 | PFN 的统计视角与合成任务先验 | 不等于 TabPFN 当前工程 API |
| R07 | Prior Labs, TabPFN 官方仓库 | 2026-10-10 页面显示 3.5 | 官方仓库 | https://github.com/PriorLabs/TabPFN | 安装、分类/回归 API、模型版本、资源、许可证和限制 | README 会随版本变化 |
| R08 | TabPFN 官方文档 | 当前版本需复核 | 官方文档 | https://tabpfn.github.io/site/ | API、使用方式、限制和示例 | 旧页面与新仓库可能存在差异 |
| R13 | Prior Labs TabPFN Models 页面 | 2026-10-10 页面 | 官方模型页面 | https://docs.priorlabs.ai/models | 各 checkpoint 的版本限制、模型和许可 | 动态页面，必须记录访问日期 |
| R09 | Hollmann et al., *Accurate predictions on small data with a tabular foundation model* | 2025 | 后续研究/开放版本 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11711098/ | TabPFN 后续能力与小数据任务证据 | 需核对对应实现和版本 |
| R10 | *Scaling TabPFN: Sketching and Feature Selection for Tabular Prior-Data Fitted Networks* | 2023 | 后续论文 | https://arxiv.org/abs/2311.10609 | 样本/特征规模扩展思路 | 不是所有扩展都属于默认 TabPFN |
| R11 | XGBoost 官方文档 | 当前版本需复核 | 官方文档 | https://xgboost.readthedocs.io/ | 当前 API、参数和实现行为 | 文档不是原始算法论文 |
| R12 | CatBoost 官方算法文档 | 当前版本需复核 | 官方文档 | https://catboost.ai/docs/en/concepts/algorithm-main-stages_fighting-biases | Ordered Boosting 与偏差说明 | 需与原始论文交叉核对 |
| R14 | CatBoost 类别特征转数值官方文档 | 2026-10-10 页面 | 官方实现文档 | https://catboost.ai/docs/en/concepts/algorithm-main-stages_cat-to-numberic | 随机排列、前缀目标统计、prior、类别组合和 one-hot 分支 | 实现文档不等于原始论文；参数行为仍受版本影响 |

## 使用规则

- 课件正文使用 `[Rxx]` 标记，并在课件末尾列出实际使用来源。
- 每个性能数字必须记录数据集、任务、协议、版本和核验日期。
- 未能由来源直接支持的结论不得写成事实。
