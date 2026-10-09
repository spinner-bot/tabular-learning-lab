# 2026-10-10 最终自动验证重跑记录

本记录只报告自动门禁，不把自动通过扩展为人工教学、屏幕阅读器或 TabPFN 权重授权通过。

## 结果

```text
audit_lessons.py                         PASS (30 lessons, index links 30/30)
check_html_structure.py                   PASS (31 pages, 216 local links)
cross_lesson_audit.py                    PASS (30 plans linked to 30 pages)
content_depth_audit.py                   PASS (30 pages and plans)
accessibility_audit.py                   PASS (31 pages)
source_inventory.py                      PASS (30 lessons, 36 external, 157 local source links)
citation_consistency_audit.py            PASS (30 lessons, 3 manual-review warnings retained)
browser_interaction_audit.py             PASS (30 lessons)
ax_tree_course_audit.py                  PASS (30 lessons)
browser_smoke_test.py                    PASS (30 lessons, keyboard/clipboard/reduced motion/390px)
lesson_03_06_examples.py                 PASS (deterministic teaching examples)
lesson_12_13_examples.py                 PASS (MLP and multi-head attention minimal paths)
course_visual_capture.py                  PASS (60 screenshots, 0 console errors, no mobile overflow)
paper_reading_R04_tabpfn_original        PASS (course-relevant claim/evidence/boundary mapping)
cross_browser_smoke_test.py               PASS (180/180; Chromium, Firefox, WebKit; desktop/mobile)
```

新增的 01/02/03/04/06/07/08/10/22 控件均有命名或标签，并被全课程交互与 AX tree 审计纳入。

## 未由本轮自动门禁解决

- TabPFN 模型权重授权、checkpoint 预测和资源对照。
- 全课程逐句事实/教学专家终审。
- 人工视觉、真实屏幕阅读器语音输出和逐像素人工视觉复核。
- 项目级许可证选择及更广的 TabPFN 同协议实验。
