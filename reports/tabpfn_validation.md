# TabPFN 环境验证记录

日期：2026-10-09

## 安装结果

- tabpfn 9.1.0 已安装。
- PyTorch 2.14.1 默认 wheel 导入失败：Windows WinError 1114，c10.dll 初始化失败。
- 按官方 CPU-only 路径重装 torch 2.14.1+cpu，仍失败。
- 进一步尝试 torch 2.9.1+cpu，仍在 c10.dll 初始化失败。

## 结论

当前 Windows/Python 3.13 工作站无法完成 TabPFN 导入，因此没有执行 checkpoint 下载、认证或预测；不能声称 TabPFN 实验通过。

这不是 TabPFN API 结果，而是底层 PyTorch DLL 环境阻塞。后续可在支持的 Python/Windows 运行环境、Linux/WSL 或具备正确运行库的机器上重试。
