# 预处理消融实验

日期：2026-10-10

本实验比较“原始特征”与“在训练流程内拟合 StandardScaler”两种条件。两个真实数据集、3 个模型（LogisticRegression、RandomForest、MLP）、5 个固定种子（7、42、101、131、197）和相同的 25% 分层测试拆分，共 60 次运行。TabPFN 未参与。

原始逐次结果和警告保存在 `data/benchmark/preprocessing_ablation.json`，脚本为 `code/preprocessing_ablation.py`。

## 主要结果（macro-F1 均值 ± 标准差）

| 数据集 | 模型 | 原始特征 | StandardScaler |
|---|---|---:|---:|
| Breast Cancer | LogisticRegression | 0.953529 ± 0.016849 | 0.980519 ± 0.008556 |
| Breast Cancer | RandomForest | 0.945663 ± 0.012488 | 0.944195 ± 0.011561 |
| Breast Cancer | MLP | 0.431444 ± 0.160708 | 0.929893 ± 0.023630 |
| Wine | LogisticRegression | 0.946345 ± 0.018931 | 0.976910 ± 0.023149 |
| Wine | RandomForest | 0.981714 ± 0.010222 | 0.981714 ± 0.010222 |
| Wine | MLP | 0.313004 ± 0.121856 | 0.573858 ± 0.138643 |

## 警告与边界

- 9 次原始 LogisticRegression 运行记录了收敛警告；这些警告已写入逐次 JSON，原始条件结果不能解释为“已充分收敛的无缩放基线”。
- 结果只支持本协议下的条件性观察：树模型对缩放相对不敏感，而线性/MLP 对特征尺度更敏感；不构成所有数据集或所有模型的普遍规律。
- 这项消融补充了“是否缩放”的一个受控问题，仍不替代模型组件消融、更多数据集、内存峰值和公平调参预算审计。
