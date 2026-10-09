# 课件陈旧环境主张复核

核验日期：2026-10-10  
范围：30 节课件中与本地依赖、运行状态直接相关的陈述。

## 已修正

- 第 01–04 节原先写成“当前环境未安装 pandas/scikit-learn”。仓库已在 `code/requirements.txt` 固定 `pandas==3.0.6` 与 `scikit-learn==1.9.1`，且本次导入检查通过；课件改为“示例尚未单独执行，依赖版本以 requirements 为准”。
- 第 17 节原先把历史 PyTorch `c10.dll` 导入错误写成当前阻塞。课件已改为引用 `reports/tabpfn_probe_2026-10-10.md`：隔离环境导入通过，但 checkpoint 预测在官方模型授权/权重获取阶段尚未完成。

## 保留的边界

- 第 09–10 节仍标注 XGBoost/CatBoost 代码为未执行、且不属于基础依赖文件；这与 `code/requirements_phase_c.txt` 的分层依赖设计一致，不等同于当前 Python 进程中绝对不可导入。
- “代码示例未执行”不被改写成“代码已验证”；实际运行证据继续放在 `code/`、`data/benchmark/` 和 `reports/` 中。

## 复核结果

`audit_lessons.py`、`check_html_structure.py`、`accessibility_audit.py` 和 `citation_consistency_audit.py` 均通过；引用一致性脚本仍保留 3 条已登记的人工复核提示。
