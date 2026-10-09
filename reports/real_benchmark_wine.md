# 第二个真实数据集 benchmark

日期：2026-10-09

本次沿用 Breast Cancer benchmark 的模型集合、3 个随机种子、25% 分层测试集和固定小预算，改用 UCI Wine 数据集（178 个样本、13 个特征、3 个类别）。UCI 官方页面标注该数据集为 CC BY 4.0，并给出 DOI [10.24432/C5PC7J](https://doi.org/10.24432/C5PC7J)；来源与变量信息见 [UCI 数据集页面](https://archive.ics.uci.edu/dataset/109/wine)。仓库不保存原始数据。

## 运行证据

```text
python code/real_benchmark_suite.py
real wine benchmark: PASS (21 runs, output=data\benchmark\real_wine_results.json)
```

## 三次运行均值

| 模型 | macro-F1 均值 | ROC-AUC（OvR）均值 | 拟合时间均值（秒） |
|---|---:|---:|---:|
| dummy | 0.1905 | 0.5000 | 0.0003 |
| logistic_regression | 0.9769 | 0.9993 | 0.0097 |
| random_forest | 0.9848 | 0.9998 | 0.1299 |
| hist_gradient_boosting | 0.9854 | 0.9993 | 0.1666 |
| xgboost | 0.9848 | 0.9993 | 0.0752 |
| catboost | 0.9780 | 0.9993 | 0.1914 |
| mlp | 0.6540 | 0.8318 | 0.0406 |

逐次结果与环境保存在 `data/benchmark/real_wine_results.json`。

## 限制

Wine 数据集页面本身提示该数据集结构良好、并不很具挑战性；因此本结果不能证明模型在困难任务上的表现，也不能与 Breast Cancer 结果直接合并成排名。TabPFN 未参与，原因见 `reports/tabpfn_validation.md`。
