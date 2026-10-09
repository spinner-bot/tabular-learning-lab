# 静态可访问性验证

验证命令：

```text
python code/accessibility_audit.py
accessibility audit: PASS (31 pages, labels/media/names checked)
```

该检查覆盖 30 节课件和课程入口，验证页面语言、表单控件关联标签、Canvas/SVG 的 `aria-label`、图片 `alt`、按钮名称和链接文本。

它是静态基础门禁，不替代屏幕阅读器、键盘全路径测试、对比度工具和人工可用性审查。

补充的 Edge Accessibility tree 检查见 `reports/ax_tree_validation.md`；它验证了入口标题/课程链接，以及第 05 节滑块、复制按钮和 Canvas 的角色与名称。
