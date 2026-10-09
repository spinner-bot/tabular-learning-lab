# 第 03、06、22 节指标与树分裂主张来源复核

核验日期：2026-10-10。

## 复核结论

- 第 03 节新增的 Log Loss、Brier、ROC-AUC、RMSE、R² 与阈值评价边界可由 scikit-learn 1.9.1 官方模型评估文档支持。文档明确区分预测概率与阈值决策，也将 log loss/Brier、ROC-AUC、RMSE 和 R² 列为不同评价接口；课件没有把 ROC-AUC 写成校准保证。
- 第 06 节的 Gini/Entropy/信息增益与回归误差下降属于决策树准则的教学化表达；scikit-learn 官方决策树文档作为实现交叉来源。课件同时保留“局部训练目标不保证泛化”的边界。
- 第 22 节的 Brier/ECE、可靠性图和分箱敏感性与 scikit-learn 官方概率校准文档一致；TabPFN 特定版本功能仍单独标记为需核验。

## 来源

- <https://scikit-learn.org/stable/modules/model_evaluation.html>
- <https://scikit-learn.org/stable/modules/tree.html>
- <https://scikit-learn.org/stable/modules/calibration.html>

## 范围限制

这是来源与教学表述复核，不是对所有 sklearn 版本 API 的永久承诺，也不替代本仓库实际代码和浏览器测试。
