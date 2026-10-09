# 初始模型比较数据

`initial_results.json` 是由 `code/benchmark_models.py` 生成的本地协议检查结果。

它使用固定的合成二分类数据、3 个随机种子、统一的 25% 测试集比例、统一的 0.5 概率阈值，并记录 accuracy、balanced accuracy、macro-F1、ROC-AUC 和拟合时间。

该结果用于验证课程中的 benchmark 记录流程，不代表跨数据集的模型排名；当前环境无法导入 PyTorch，因此不包含 TabPFN。任何正式结论仍需使用有许可的数据集、预注册协议和可运行的 TabPFN 环境复核。
