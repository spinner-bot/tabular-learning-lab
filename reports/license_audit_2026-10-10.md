# 许可证与数据来源审计

审计日期：2026-10-10

本报告只核对仓库声明的来源、许可证字段和文件边界，不替代法律意见。代码库许可证、第三方依赖许可证、数据集许可、模型权重条款和论文引用权利分别处理。

| 名称 | 类型 | 许可证/条款 | 状态 | 官方来源 |
|---|---|---|---|---|
| tabular-learning-lab | repository | UNDECLARED | decision_required | Repository root |
| Python / standard library | runtime | Python Software Foundation License | documented | [Python documentation](https://docs.python.org/3/license.html) |
| NumPy | dependency | BSD-3-Clause | documented | [NumPy repository](https://github.com/numpy/numpy/blob/main/LICENSE.txt) |
| pandas | dependency | BSD-3-Clause | documented | [pandas repository](https://github.com/pandas-dev/pandas/blob/main/LICENSE) |
| scikit-learn | dependency | BSD-3-Clause | documented | [scikit-learn repository](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING) |
| XGBoost | dependency | Apache-2.0 | documented | [XGBoost repository](https://github.com/dmlc/xgboost/blob/master/LICENSE) |
| CatBoost | dependency | Apache-2.0 | documented | [CatBoost repository](https://github.com/catboost/catboost/blob/master/LICENSE) |
| psutil | dependency | BSD-3-Clause | documented | [psutil repository](https://github.com/giampaolo/psutil/blob/master/LICENSE) |
| Breast Cancer Wisconsin Diagnostic | dataset | CC BY 4.0 | source_only | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic) |
| Wine | dataset | CC BY 4.0 | source_only | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/109/wine) |
| TabPFN source code | optional_dependency | Apache-2.0 | documented | [PriorLabs/TabPFN repository](https://github.com/PriorLabs/TabPFN/blob/main/LICENSE) |
| TabPFN model weights | model_weights | Version-dependent; verify the selected model card | separate_acceptance_required | [Prior Labs model documentation](https://docs.priorlabs.ai/models) |
| Research papers and documentation | citation | Not assumed | citation_only | research/references.md |

## 边界与行动

- 仓库当前没有项目级许可证；在项目负责人选定前，不宣称仓库整体可按某个开源许可证再分发。
- UCI 两个数据集只作为运行时来源，不把原始数据复制进仓库；发布结果时保留 DOI、来源和 CC BY 4.0 归因要求。
- TabPFN 代码和模型权重分开记录；模型权重必须按所选版本的模型页面单独接受条款，不能由 Apache-2.0 代码许可推导权重许可。
- 论文和官方文档按引用使用，不把引用权利扩展解释为复制或再分发权利。

## 机器检查

- 条目数：13
- 检查结果：PASS
