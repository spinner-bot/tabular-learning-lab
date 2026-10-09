# HTML 静态验证记录

## 检查范围

使用 code/check_html_structure.py 检查课程入口和 lessons/ 下全部 HTML：

- HTML 文件能被 Python 标准库解析。
- 本地 href 目标存在。
- 课件页面包含 viewport 元信息。

## 未覆盖范围

- 浏览器视觉渲染、JavaScript 控件、键盘操作和控制台错误。
- 外部链接的可访问性。

浏览器无界面测试当前未返回可用 DOM 或截图输出，因此这些项目仍标记为未验证。
