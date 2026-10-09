# 第 10 节计划：CatBoost

- 学习目标：解释类别特征处理、Ordered Target Statistics 和 Ordered Boosting。
- 核心问题：类别目标统计为何会产生泄漏/预测偏移？
- 知识点：one-hot、目标统计、排列、ordered boosting、prediction shift。
- 案例：同一类别在不同前缀上的统计量。
- 图示/交互：排列前缀与统计量更新。
- 代码：CatBoost 原生类别输入与 one-hot 对照，记录协议。
- 自测：目标泄漏、排列、one-hot 边界、与 XGBoost 比较、绝对排名辨析。
- 来源：R02、CatBoost 官方算法文档 R12。
- 难点：不能把 CatBoost 宣称为无条件最强。
