# 全课程浏览器交互审计

由 `python code/browser_interaction_audit.py` 生成，使用 Edge headless、390×844 viewport 和 reduced-motion 设置逐页加载 30 个 lesson。

## 结果

- 30/30 页面完成加载与交互审计。
- 150 个 `details.quiz` 自测逐个展开成功。
- 2 个范围控件完成键盘变更；1 个复制按钮完成点击路径；1 个 Canvas 具有非零布局尺寸。
- HTTP 响应错误：0；页面横向溢出：0。
- 控制台仅记录浏览器默认 `/favicon.ico` 请求的 404；审计使用带 URL 的 HTTP response 错误作为资源错误门禁，因此该现象不属于课程页面资源失败。

逐页原始记录：`reports/browser_interaction_audit_2026-10-10.json`。

## 边界

该审计覆盖现有通用交互路径和窄屏布局，不替代真实屏幕阅读器、跨浏览器人工视觉检查或 TabPFN checkpoint 运行。
