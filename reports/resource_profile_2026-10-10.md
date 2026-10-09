# 代表性资源剖析

日期：2026-10-10

脚本 `code/resource_profile.py` 在两个真实数据集上用固定 seed=42 和现有 7 个模型记录拟合时间与进程 RSS 峰值，共 14 次拟合。采样间隔为 0.01 秒；RSS 包含解释器和已加载库，不是与硬件无关的模型复杂度指标。

原始结果：`data/benchmark/resource_profile.json`。

| 数据集 | 模型 | 拟合时间（秒） | 峰值 RSS（MB） |
|---|---|---:|---:|
| Breast Cancer | dummy | 0.001626 | 163.984 |
| Breast Cancer | logistic_regression | 0.010733 | 164.664 |
| Breast Cancer | random_forest | 0.178703 | 165.078 |
| Breast Cancer | hist_gradient_boosting | 0.181804 | 168.340 |
| Breast Cancer | xgboost | 0.158881 | 177.293 |
| Breast Cancer | catboost | 0.470861 | 189.309 |
| Breast Cancer | mlp | 0.063130 | 185.934 |
| Wine | dummy | 0.001199 | 185.695 |
| Wine | logistic_regression | 0.011001 | 185.703 |
| Wine | random_forest | 0.130986 | 185.730 |
| Wine | hist_gradient_boosting | 0.162203 | 186.246 |
| Wine | xgboost | 0.064546 | 186.117 |
| Wine | catboost | 0.186151 | 187.809 |
| Wine | mlp | 0.039163 | 187.008 |

## 边界

这是单进程、单种子、两个小数据集的代表性资源记录，不是硬件无关的复杂度结论，也不替代多规模内存压力测试。TabPFN 未参与，原因见 `reports/tabpfn_validation.md`。
