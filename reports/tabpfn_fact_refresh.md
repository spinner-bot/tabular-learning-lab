# TabPFN 版本事实复核记录

核验日期：2026-10-10

本次复核直接打开 Prior Labs 官方仓库和 Models 页面，结果只用于更新版本敏感事实，不替代本机运行验证。

## 已确认的官方信息

- 官方仓库当前 quick start 以 TabPFN-3.5 为默认模型，提供 `TabPFNClassifier`、`TabPFNRegressor` 和版本选择器示例。
- 官方页面要求 Python 3.10+，说明首次使用会下载 checkpoint，并给出 GPU 推荐、CPU 可行性提示和批量预测建议。
- Models 页面按版本分别列出可用性、行/列/类别边界和许可；例如 TabPFN-3.5/3.5-Fast、TabPFN-3、2.6、2.5 与 v2 的限制并不相同。
- 官方仓库明确区分 Apache 2.0 代码许可与模型权重许可；模型权重可能是非商业许可，不能把代码许可当作权重许可。

## 尚未确认的内容

- 当前 Windows 工作站仍无法导入 PyTorch `c10.dll`，没有完成 checkpoint 下载、认证、预测或资源实测。
- 官方上限不等于当前硬件上的可行性；CPU 时间、显存/内存和批量大小仍需在可运行环境中测量。

证据入口：`research/references.md` 的 R07、R13；本地运行证据：`reports/tabpfn_validation.md`。
