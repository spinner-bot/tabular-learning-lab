# Tabular Learning Lab

这是一个面向机器学习基础较浅学习者的表格学习课程与实验项目。

## 当前状态

30 节 HTML 课件和逐节计划已建立初版。研究核验、代码实验、浏览器测试和最终审计仍需继续；不能把“文件存在”视为项目完成。

## 如何阅读

1. 直接打开 index.html 查看课程地图。
2. 选择 lessons/ 下的课件。
3. 课件正文尽量不依赖外部 CDN；外部来源链接用于研究核验。
4. 若浏览器对本地文件限制资源访问，可从项目根目录启动本地静态服务器。

## 目录

- docs/：项目总控规范。
- research/：研究计划、事实矩阵、参考文献、版本和开放问题。
- course_map.md：30 节课程地图。
- lesson_plans/：逐节教学计划。
- lessons/：独立 HTML 课件。
- code/：代码、依赖和验证脚本。
- data/：数据说明与许可。
- qa/：验收标准、逐节清单和测试报告。
- reports/：阶段报告和中间验证记录。
- assets/：设计系统、共享样式和脚本。

## 代码

基础课 smoke test：

    python code/foundation_batch_smoke_test.py

HTML 结构和链接：

    python code/check_html_structure.py
    python code/audit_lessons.py

基础依赖版本记录在 code/requirements.txt。TabPFN 不放入基础依赖，因为其 checkpoint、许可证、硬件和版本需要单独核验。

## 研究核验

关键事实必须绑定原始论文或官方文档、适用版本和核验日期。当前动态 TabPFN 资料以 research/version_history.md 和 research/open_questions.md 为准。

## Git 工作方式

遵守 specs/git_SPEC.md：合并和拉取使用 --no-ff；工作中密集创建本地提交、阶段性稀疏推送，不使用强制推送。
