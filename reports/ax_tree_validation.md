# 浏览器 Accessibility Tree 验证

验证命令：

```text
python code/ax_tree_audit.py
AX tree audit: PASS (entry and sample lesson named controls verified)
```

该检查使用 Edge DevTools Accessibility tree，核对入口页标题/课程链接，以及第 05 节两个滑块、复制按钮和 Canvas 图示的角色与可访问名称。完整快照保存在 `reports/accessibility_ax_tree.json`。

这不是屏幕阅读器端到端认证；屏幕阅读器语音输出、用户设置和跨平台差异仍需人工验证。
