# 第 07 节计划：Bagging、随机森林与集成

- 学习目标：解释 bootstrap、样本/特征随机性和方差降低。
- 核心问题：多个不完美模型为何可能更稳定？
- 知识点：Bagging、随机森林、相关性与集成收益、OOB 评估。
- 案例：单树与森林在不同 bootstrap 样本上的预测波动。
- 图示/交互：树数量与方差曲线。
- 代码：RandomForest 与 OOB score。
- 自测：bootstrap、随机子特征、OOB、偏差方差、与 boosting 区别。
- 来源：Breiman 随机森林论文、sklearn ensemble 文档。
- 难点：集成降低方差但不自动消除偏差。
