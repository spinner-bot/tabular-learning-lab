# TabPFN 环境复核（2026-10-10）

## 检查

在当前默认 Python 环境中执行了只读导入检查：

```text
import tabpfn, torch
```

包发现结果为 `tabpfn` 位于 `D:\Lib\site-packages\tabpfn`，但导入过程中 PyTorch 抛出：

```text
OSError: [WinError 1114] Error loading "D:\Lib\site-packages\torch\lib\c10.dll" or one of its dependencies.
```

## 结论

- “默认环境中能发现 tabpfn 包”不等于“TabPFN 可运行”。
- 本次复核没有下载权重、接受许可、修改系统 DLL 或生成预测结果。
- 历史隔离探针记录仍单独保留：隔离环境曾通过 PyTorch/TabPFN 导入，但最小 `fit` 进入模型权重授权流程后未完成授权，见 `reports/tabpfn_probe_2026-10-10.md`。
- 当前项目不得把全局环境的包安装状态或本次失败误写成 TabPFN 实验结果。
