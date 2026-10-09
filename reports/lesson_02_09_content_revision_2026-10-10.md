# 第 02、09 节内容与交互修订记录

核验日期：2026-10-10。

## 修订

- 第 02 节增加“先整体计算统计量再划分”的泄漏开关。开关只切换明确的教学说明，不伪造实验分数；复核时发现 checkbox 的可访问名称问题，已追加 `aria-label` 并通过静态可访问性审计。
- 第 09 节补充行/列采样与量化/近似分裂的作用边界，明确它们属于具体训练协议和工程权衡，不是效果保证。

## 验证

- `accessibility_audit.py`：31 页通过。
- `browser_interaction_audit.py`：30 页通过，覆盖新增 checkbox、已有 range/details/copy/canvas 路径。
- `check_html_structure.py`：31 页、207 个本地链接通过。

仍未把第 09 节未执行的完整 XGBoost 参数对照称为已验证；当前论文/官方文档主张证据见独立核验报告。
