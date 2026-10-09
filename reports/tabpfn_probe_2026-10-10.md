# TabPFN 隔离环境探针

日期：2026-10-10。

## 环境

- 隔离目录：`.tabpfn_probe`（仅本机临时环境，不纳入仓库）。
- Python：3.13，Windows AMD64。
- PyTorch：2.7.1+cpu，官方 CPU wheel。
- TabPFN：9.1.0。

## 结果

1. `import torch` 成功，`torch.tensor([1, 2])` 成功；原工作环境的 `c10.dll` 导入错误可通过隔离环境绕开。
2. `import tabpfn` 成功。
3. 最小 `TabPFNClassifier.fit/predict` 首次初始化进入官方一次性许可证接受/登录流程，要求浏览器登录、接受模型权重条款或提供 API key；当前未代用户接受条款或提供凭据，因此测试终止。
4. 未下载、未保存或提交模型权重；未将临时环境或缓存纳入仓库。

## 结论

TabPFN 代码导入门禁已通过，checkpoint/预测门禁仍为“未验证”。当前剩余条件是项目负责人完成官方账户登录并接受所选权重版本条款；授权后应复跑最小分类、真实数据基线对照、时间/RSS 记录，并锁定 checkpoint 版本和许可。
