# 跨章节一致性验证

验证命令：

```text
python code/cross_lesson_audit.py
cross-lesson audit: PASS (30 plans linked to 30 pages)
```

该检查确认 30 份 lesson plan 与 30 个 HTML 页面一一对应；每节正文回链自身计划，计划含来源字段，正文含先修/后续元数据，并且每页恰有一个 `h1`。
