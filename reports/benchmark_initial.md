# 初始模型比较报告

日期：2026-10-09

## 范围

这是课程 benchmark 协议的本地初始检查，不是跨数据集的模型排名，也不是最终研究结论。使用 `sklearn.make_classification` 生成 900 个样本、18 个特征的二分类数据；固定 3 个拆分种子（7、42、101），每次使用 25% 测试集和 0.5 概率阈值。比较对象为多数类基线、逻辑回归、随机森林、HistGradientBoosting、XGBoost、CatBoost 和 MLP。

TabPFN 没有被隐藏或模拟：由于当前 Windows 环境的 PyTorch `c10.dll` 导入错误，本次明确排除，证据见 `reports/tabpfn_validation.md`。

## 运行证据

```text
python code/benchmark_models.py
benchmark: PASS (21 runs, output=data\benchmark\initial_results.json)
```

环境：Python 3.13.5、NumPy 2.5.0、pandas 3.0.6、scikit-learn 1.9.1、XGBoost 3.4.1、CatBoost 1.2.10。

第一次运行使用元组形式的 `weights`，在当前 scikit-learn 1.9.1 中触发 `AttributeError: 'tuple' object has no attribute 'copy'`；已修正为列表并保留最终成功结果。这个失败记录说明环境/API 假设不能省略。

## 三次运行均值

| 模型 | macro-F1 均值 | ROC-AUC 均值 | 拟合时间均值（秒） |
|---|---:|---:|---:|
| dummy | 0.4186 | 0.5000 | 0.0003 |
| logistic_regression | 0.8406 | 0.9096 | 0.0061 |
| random_forest | 0.8545 | 0.9458 | 0.2266 |
| hist_gradient_boosting | 0.8672 | 0.9458 | 0.1628 |
| xgboost | 0.8656 | 0.9474 | 0.1229 |
| catboost | 0.8534 | 0.9476 | 0.2036 |
| mlp | 0.7130 | 0.8484 | 0.0882 |

原始逐次结果和环境信息保存在 `data/benchmark/initial_results.json`；生成脚本为 `code/benchmark_models.py`。

## 限制

- 数据是合成数据，不能支持“某模型普遍更强”的结论。
- 只有 3 个固定拆分，尚未包含数据集级重复、置信区间、调参预算、内存峰值和真实数据许可审计。
- 该报告不替代 TabPFN 在可用环境中的 checkpoint 实验。
