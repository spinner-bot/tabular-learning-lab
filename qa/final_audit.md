# 最终审计（未通过，持续更新）

审计日期：2026-10-10

## 已有证据

- 30 个独立 lesson HTML 已存在。
- 30 份 lesson plan 和 30 份逐节 checklist 已存在。
- index.html 已链接 30/30 个课件。
- HTML 结构/本地链接审计通过：31 个页面、207 个本地链接；30 节课件均含外部可核验来源，且已纳入审计硬门禁。
- 30 份 lesson plan 与 30 个 HTML 页面已通过跨章节对应审计。
- 30 节页面与计划已通过最低内容深度结构审计；教学准确性仍需逐句人工核验。
- 基础 sklearn、树模型、XGBoost、CatBoost、MLP 和校准 smoke test 有运行记录。
- 研究计划、事实矩阵、参考文献、版本记录和开放问题已建立。
- R05 PFN 原始论文链接已核正为 arXiv:2112.10510，并保存复核记录 `reports/core_fact_verification_2026-10-10.md`；外链审计重跑通过。
- TabPFN 官方 Models/README 的版本、行列、类别、CPU 提示和许可边界已追加日期化证据；这些页面事实仍不替代本机 checkpoint 实测。
- 已生成逐课来源清单：30 个课件、34 个外部链接引用、148 个本地来源链接；该清单明确不替代语义事实核验。

## 未通过或未验证

- 逐节事实主张还没有全部逐句核验。
- TabPFN 当前工作站导入被 PyTorch c10.dll 阻塞，真实 checkpoint 实验未完成。
- 浏览器自动化 smoke test 已通过；人工逐像素视觉审阅、屏幕阅读器审计和跨内核兼容性仍未完成，证据见 `reports/browser_validation.md`。
- 静态可访问性基础审计已通过 31 个页面；屏幕阅读器和人工可用性审查仍未完成，证据见 `reports/accessibility_validation.md`。
- Edge Accessibility tree 已核对入口页和第 05 节关键控件的角色/名称；真实屏幕阅读器端到端审查仍未完成，证据见 `reports/ax_tree_validation.md`。
- 19 个外部来源链接在本次日期核验中可达；链接可达不等于主张逐条核验，证据见 `reports/external_link_validation.md`。
- TabPFN 版本、限制和许可证页面已于 2026-10-10 重新核对；本机运行证据仍未通过，详见 `reports/tabpfn_fact_refresh.md`。
- 30 节课件仍是初版，尚未完成统一深度、引用和跨章节终审。
- 已有合成数据、两个真实数据集和 36 次预声明参数实验；更大规模重复、置信区间、消融和正式数据许可审计仍未完成。

## 审计结论

项目不能宣告完成。当前状态是“全课程初版与验证基础已建立，最终质量门禁未通过”；继续工作必须从上述未通过项开始，不得用文件数量代替验收。
