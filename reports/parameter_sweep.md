# XGBoost / CatBoost 参数预算实验

日期：2026-10-09

## 协议

预先声明 6 个配置：XGBoost（small/regular/deeper）与 CatBoost（small/regular/deeper）。每个配置在 Breast Cancer Wisconsin Diagnostic 和 Wine 两个真实数据集上运行 3 个固定种子，使用相同的 25% 分层测试比例；不根据测试集结果再选参数。共 36 次运行。

## 运行证据

```text
python code/parameter_sweep.py
parameter sweep: PASS (36 runs, output=data\benchmark\parameter_sweep_results.json)
```

## macro-F1 均值 ± 标准差

| 数据集 | 配置 | macro-F1 | ROC-AUC 均值 | 拟合时间均值（秒） |
|---|---|---:|---:|---:|
| Breast Cancer | xgb_small | 0.957624 ± 0.017154 | 0.995528 | 0.074 |
| Breast Cancer | xgb_regular | 0.965012 ± 0.011519 | 0.996995 | 0.139 |
| Breast Cancer | xgb_deeper | 0.962489 ± 0.012942 | 0.996855 | 0.248 |
| Breast Cancer | cat_small | 0.962431 ± 0.007788 | 0.997065 | 0.200 |
| Breast Cancer | cat_regular | 0.964696 ± 0.011744 | 0.996716 | 0.447 |
| Breast Cancer | cat_deeper | 0.969715 ± 0.013246 | 0.997694 | 1.690 |
| Wine | xgb_small | 0.984762 ± 0.013197 | 0.999314 | 0.046 |
| Wine | xgb_regular | 0.984762 ± 0.013197 | 0.999314 | 0.071 |
| Wine | xgb_deeper | 0.984762 ± 0.013197 | 0.999314 | 0.103 |
| Wine | cat_small | 0.971173 ± 0.012640 | 0.999771 | 0.077 |
| Wine | cat_regular | 0.978003 ± 0.001490 | 0.999262 | 0.242 |
| Wine | cat_deeper | 0.978003 ± 0.001490 | 0.999491 | 1.235 |

原始逐次结果、参数和环境见 `data/benchmark/parameter_sweep_results.json`；脚本为 `code/parameter_sweep.py`。

## 解释边界

该实验只说明固定协议下的配置敏感性和成本差异，不是完整超参数搜索，也不支持跨数据集的最佳配置结论。3 个种子不足以替代大规模重复或置信区间分析；TabPFN 未参与。
