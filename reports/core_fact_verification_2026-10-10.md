# 核心模型事实复核记录

核验日期：2026-10-10。以下记录只确认来源中明确支持的范围；没有把论文结论、当前实现和本机运行结果混写。

## 已核对

- PFN 原始来源已更正为 Müller 等人的 *Transformers Can Do Bayesian Inference*（[arXiv:2112.10510](https://arxiv.org/abs/2112.10510)）。论文摘要支持：从先验采样任务，训练网络近似后验预测，并在推断时以集合/上下文输入进行一次前向预测；这属于 PFN 通用机制，不自动等同于当前 TabPFN 版本。
- TabPFN 原始论文为 Hollmann 等人的 *TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second*（[arXiv:2207.01848](https://arxiv.org/abs/2207.01848)）。课程中的原始模型动机、早期小表格分类范围和当前实现说明已分开标注。
- XGBoost 的算法事实引用其原始论文（[arXiv:1603.02754](https://arxiv.org/abs/1603.02754)）；CatBoost 的 Ordered Boosting、类别特征处理和 prediction shift 引用其原始论文（[arXiv:1706.09516](https://arxiv.org/abs/1706.09516)）。课程不把论文实验版本直接当作当前库行为。
- FT-Transformer 的入口仍记录为 OpenReview 原始页面，但当前自动访问被 challenge 重定向；因此保留为“已定位、未完成逐段核验”，不升级为最终通过。
- 当前 TabPFN 安装、版本限制和许可证事实以 [官方仓库](https://github.com/PriorLabs/TabPFN) 与 [官方 Models 页面](https://docs.priorlabs.ai/models) 为准；本机 Windows PyTorch 动态库错误仍单独记录，不以官方页面替代本机实测。

## 尚未通过的边界

- 尚未完成所有原始论文逐段核验、当前库逐参数核验和人工视觉/屏幕阅读器复核。
- TabPFN 当前 checkpoint 的本机端到端预测仍受 Windows `c10.dll` 导入错误阻塞；没有伪造运行成功或性能数字。
- 论文性能、课程 benchmark 和当前版本性能必须继续保持三种证据分栏。
