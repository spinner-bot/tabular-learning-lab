# 树模型批次代码验证记录

日期：2026-10-09  
环境：Python 3.13.5、scikit-learn 1.9.1、xgboost 3.4.1、catboost 1.2.10。

运行：

    python code/tree_models_smoke_test.py

结果：tree models smoke test: PASS

覆盖：决策树、随机森林、GBDT 回归、XGBoost 多分类和 CatBoost 原生类别特征输入。

限制：这是最小 smoke test，不等于第 09/10 节的完整参数对照实验或公平 benchmark。
