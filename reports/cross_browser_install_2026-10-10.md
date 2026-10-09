# Playwright 跨浏览器运行包安装记录（2026-10-10）

## 操作

在项目 Python 环境执行：

```text
python -m playwright install firefox webkit
```

安装结果：

- Firefox 155.0（Playwright firefox v1543）安装成功。
- WebKit 26.6（Playwright webkit v2359）安装成功。
- 运行包存放于用户级 Playwright 缓存，不写入仓库，不改变课程数据。

## 安装后验证

使用 `code/cross_browser_smoke_test.py` 重跑 30 节课件的桌面与移动视口：

- Chromium：60/60
- Firefox：60/60
- WebKit：60/60
- 合计：180/180，状态 PASS

该记录只证明自动化页面路径在三个浏览器引擎中可运行；真实屏幕阅读器语音输出、逐像素人工视觉复核和独立 axe/pa11y 规则引擎仍属于未完成项。
