# 浏览器实测报告

日期：2026-10-09

## 环境

- Microsoft Edge：使用本机已安装的 Edge 可执行文件。
- Playwright：1.63.0，本地验证依赖，不加入课程运行时依赖。
- 桌面视口：1440×900。
- 窄屏视口：390×844。
- 两种上下文均启用 `prefers-reduced-motion: reduce`。

## 结果

```text
python code/browser_smoke_test.py
browser smoke test: PASS (30 lessons, keyboard interaction, reduced motion, 390px overflow check)
```

已验证：

- 课程入口页面加载成功，30 个课程链接均可见。
- 30 个 lesson 页面逐页加载成功，每页有一个 `h1`。
- 第 05 节 Canvas 交互可加载；滑块改变深度后文本同步更新。
- 使用键盘方向键操作滑块成功。
- 390px 视口下 30 个课件均无横向溢出。
- 自测题数量和入口页面结构保持通过。
- 已保存桌面入口和窄屏第 05 节截图：`reports/browser_artifacts/index_desktop.png`、`reports/browser_artifacts/lesson_05_mobile.png`。

## 边界

这是自动化 smoke test，不等同于人工逐像素视觉审阅、屏幕阅读器审计或所有浏览器内核的兼容性认证。复制按钮的系统剪贴板权限也未作为硬门禁；页面在权限拒绝时会显示手动复制提示。
