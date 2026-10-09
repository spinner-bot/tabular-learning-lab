# 全课程视觉捕获与复核记录（2026-10-10）

## 范围

- 使用 `code/course_visual_capture.py` 在 Microsoft Edge 中捕获 30 个课件的桌面版（1440×1000）和移动版（390×844），共 60 张全页截图。
- 使用 `code/course_visual_contact_sheet.py` 生成 6 张分批缩略图，便于按课程顺序检查整体布局。
- 机器可读记录：`reports/course_visual_capture_2026-10-10.json`。
- 截图原件：`reports/browser_artifacts/course_visual_2026-10-10/`；缩略图位于其 `contact_sheets/` 子目录。

## 结果

- 60/60 页面捕获成功。
- 捕获期间控制台错误为 0。
- 移动视口的 `document.documentElement.scrollWidth` 均不超过 390px，未发现横向溢出。
- 对 6 张缩略图进行全课程顺序检查，并对第 03、06、17、30 节的完整截图进行抽样复核：未发现明显的卡片重叠、标题截断、控件越界或导航断裂；移动版均保持单列布局。

## 证据边界

本记录补充了全课程截图和自动布局测量，但缩略图检查不是逐像素人工审查，也不等同于真实屏幕阅读器语音输出或跨浏览器复核。逐句教学准确性、屏幕阅读器、跨内核人工检查，以及 TabPFN 权重授权后的运行仍保留在最终验收矩阵的未完成项中。
