# 第 02 节计划：机器学习实验的基本流程

- 学习目标：解释训练/验证/测试；识别过拟合、欠拟合和数据泄漏。
- 核心问题：为什么测试集不能反复参与决策？
- 知识点：划分、泛化、分布偏移、管道化预处理。
- 案例：先划分再标准化与先整体标准化的差异。
- 图示/交互：数据划分流程和泄漏开关。
- 代码：scikit-learn Pipeline 与固定随机种子。
- 自测：划分策略、泄漏诊断、验证集用途、时间数据、泛化判断。
- 来源：<https://scikit-learn.org/stable/common_pitfalls.html>、<https://scikit-learn.org/stable/modules/cross_validation.html> 与 `qa/acceptance_criteria.md`。
- 难点：区分验证集调参与测试集最终评估。
