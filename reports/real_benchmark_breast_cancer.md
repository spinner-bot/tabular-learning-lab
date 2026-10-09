# 真实数据初始 benchmark

日期：2026-10-09

## 数据与许可边界

使用 scikit-learn 内置的 Breast Cancer Wisconsin Diagnostic 数据加载器；运行时不联网、不把原始数据复制进仓库。UCI 官方页面标注该数据集为 CC BY 4.0，并给出 DOI [10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B)；来源与变量信息见 [UCI 数据集页面](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)。本报告只保存运行结果和元数据。

数据规模为 569 个样本、30 个特征。每个模型使用相同的 25% 分层测试集比例和 3 个随机种子（7、42、101）；指标为 accuracy、balanced accuracy、macro-F1、ROC-AUC 和拟合时间。模型配置沿用初始 benchmark 的固定小预算，不进行针对测试集的调参。

## 运行证据

```text
python code/real_benchmark.py
real benchmark: PASS (21 runs, output=data\benchmark\real_breast_cancer_results.json)
```

## 三次运行均值

| 模型 | macro-F1 均值 | ROC-AUC 均值 | 拟合时间均值（秒） |
|---|---:|---:|---:|
| dummy | 0.3863 | 0.5000 | 0.0003 |
| logistic_regression | 0.9800 | 0.9969 | 0.0089 |
| random_forest | 0.9496 | 0.9953 | 0.1754 |
| hist_gradient_boosting | 0.9675 | 0.9957 | 0.1600 |
| xgboost | 0.9649 | 0.9969 | 0.1286 |
| catboost | 0.9674 | 0.9966 | 0.3028 |
| mlp | 0.9228 | 0.9802 | 0.0616 |

原始逐次结果、环境和协议保存在 `data/benchmark/real_breast_cancer_results.json`；生成脚本为 `code/real_benchmark.py`。

## 不可外推项

- 单一数据集、固定小预算和 3 个拆分不能支持普遍模型排名或临床决策结论。
- 尚未完成跨数据集重复、置信区间、完整参数预算、内存峰值、数据版本锁定和消融实验。
- TabPFN 未参与，原因和证据见 `reports/tabpfn_validation.md`；不能将本报告结果解释为 TabPFN 对照结果。
