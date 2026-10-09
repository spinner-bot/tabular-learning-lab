# 本次最终验证记录

验证日期：2026-10-09

本记录保留本轮收尾验证的命令与结果。验证通过不等于项目最终验收通过；最终验收仍受浏览器实测、逐条事实核验、TabPFN 可运行环境和完整 benchmark 等门禁约束。

## 静态质量门禁

```text
python code/audit_lessons.py
lesson audit: PASS (30 lessons, index links 30/30)

python code/check_html_structure.py
HTML structure check: PASS (31 pages, 207 local links)
```

## 代码烟测

```text
python code/foundation_batch_smoke_test.py
foundation batch smoke test: PASS (macro-F1=0.967)

python code/tree_models_smoke_test.py
tree models smoke test: PASS

python code/deep_tabular_smoke_test.py
deep/calibration smoke test: PASS
```

树模型烟测产生的 CatBoost 临时目录已在验证后清理。当前工作树未包含测试生成物。

## 当前结论

- 课程文件、索引链接、HTML 结构和已纳入的本地代码烟测均通过。
- 30 节课件均含至少一个外部可核验来源，且该项已纳入 `code/audit_lessons.py` 硬门禁。
- 30 份 lesson plan 与 30 个 HTML 页面已通过跨章节对应审计。
- 30 节页面与计划已通过最低内容深度结构审计。
- 不宣称浏览器交互、窄屏布局、键盘操作和完整引用门禁已经通过。
- TabPFN 的真实 checkpoint 预测实验仍受当前 Windows 环境中的 PyTorch `c10.dll` 导入错误阻塞，证据见 `reports/tabpfn_validation.md`。
- 本轮只做本地提交，不执行远程推送。
