# 质量验证环境能力核查（2026-10-10）

## 检查方式

使用只读命令检查当前工作站的可执行程序和项目可用工具；为完成跨内核自动验证，本轮额外安装了 Playwright Firefox/WebKit 浏览器运行包，未改变仓库数据或系统配置。

## 结果

| 能力 | 当前状态 | 影响 |
|---|---|---|
| Microsoft Edge | 已由项目脚本定位并使用其安装路径运行 | 已完成 Edge 浏览器、窄屏、交互、AX tree 和全课程截图证据 |
| Windows Narrator | `C:\Windows\System32\Narrator.exe` 存在 | 仅存在程序不等于已完成语音端到端审计；本项目没有自动化语音输出记录 |
| NVDA | 未找到 | 无法完成 NVDA 复核 |
| Firefox | 系统命令未找到；Playwright Firefox 运行包已安装并可运行 | 已完成 Firefox 30 节桌面/移动自动 smoke test |
| Chrome/Chromium 命令 | 系统命令未找到，但 Playwright bundled Chromium 可运行 | 已完成 Chromium 30 节桌面/移动自动 smoke test；不等同于系统 Chrome |
| Playwright Firefox/WebKit | Firefox 1543、WebKit 2359 运行包已安装并可启动 | 已完成 Firefox/WebKit 各 30 节桌面/移动自动 smoke test |
| axe/pa11y CLI | 未找到 | 当前无第二套独立规则引擎证据；保留静态可访问性、Edge AX tree 和浏览器交互审计 |

## 结论

当前环境已完成 Edge 与 Playwright Chromium/Firefox/WebKit 自动门禁；三引擎共 180/180 页面路径通过。环境仍不足以证明真实屏幕阅读器语音输出、逐像素人工视觉复核或独立 axe/pa11y 规则引擎通过。该限制不改变现有自动测试结果，也不应被描述为最终无障碍验收通过。
