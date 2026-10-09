# 最终审计（未通过，持续更新）

审计日期：2026-10-10

## 已有证据

- 30 个独立 lesson HTML 已存在。
- 30 份 lesson plan 和 30 份逐节 checklist 已存在。
- index.html 已链接 30/30 个课件。
- HTML 结构/本地链接审计通过：31 个页面、216 个本地链接；30 节课件均含外部可核验来源，且已纳入审计硬门禁。最新完整自动重跑见 `reports/final_validation_run_2026-10-10.md`。
- 30 份 lesson plan 与 30 个 HTML 页面已通过跨章节对应审计。
- 30 节页面与计划已通过最低内容深度结构审计；教学准确性仍需逐句人工核验。
- 基础 sklearn、树模型、XGBoost、CatBoost、MLP 和校准 smoke test 有运行记录。
- 研究计划、事实矩阵、参考文献、版本记录和开放问题已建立。
- R05 PFN 原始论文链接已核正为 arXiv:2112.10510，并保存复核记录 `reports/core_fact_verification_2026-10-10.md`；外链审计重跑通过。
- TabPFN 官方 Models/README 的版本、行列、类别、CPU 提示和许可边界已追加日期化证据；这些页面事实仍不替代本机 checkpoint 实测。
- 已生成逐课来源清单：30 个课件、35 个外部链接引用、157 个本地来源链接；该清单明确不替代语义事实核验。
- 已保存 `reports/paper_claim_verification_2026-10-10.md` 及 XGBoost、CatBoost、FT-Transformer 补充核验报告：主要论文机制已到章节/官方文档级，当前库行为、官方实现运行和逐课事实终审仍单独保留为缺口。
- 已完成全课程桌面/移动截图捕获与缩略图复核，并保留入口页与第 05 节人工视觉记录；全课程截图证据仍不扩展为逐像素、屏幕阅读器或跨内核视觉认证。
- 已让 Edge smoke test 保存 30 个课件的 390px 布局测量记录；该记录只证明自动化页面宽度断言，不替代人工逐页视觉和屏幕阅读器审查。
- 全课程引用一致性结构审计已通过，保存 3 个人工复核提示；R ID 与页面 URL 的表达差异和语义支持仍不被自动脚本误判为通过。
- 3 条引用格式提示已逐条记录人工处置：`reports/citation_manual_review_2026-10-10.md`；自动审计警告继续保留，逐句事实终审仍未完成。
- 已完成课件过度断言风险筛查并保留处置记录：`reports/claim_risk_review_2026-10-10.md`；命中项均处于误区/边界/不可推出语境，不能替代逐句事实核验。
- 已补充 FT-Transformer 原始论文 HTML 主张核验：`reports/ft_transformer_claim_verification_2026-10-10.md`；F08 的架构/边界证据增强，但官方实现运行和逐节事实终审仍未完成。
- 已补充 XGBoost 与 CatBoost 主张级核验：`reports/xgboost_claim_verification_2026-10-10.md`、`reports/catboost_claim_verification_2026-10-10.md`；第 09、10 节核心算法表述与原始论文/官方文档一致，当前库版本行为仍与论文证据分开标记。
- 已建立总控 Prompt 第十四节的最终验收矩阵：`reports/final_acceptance_matrix_2026-10-10.md`，逐项区分通过、部分通过和未验证。

## 未通过或未验证

- 逐节事实主张还没有全部逐句核验。
- TabPFN 基础环境曾被 PyTorch c10.dll 阻塞；2026-10-10 隔离环境已通过代码导入，但真实 checkpoint/预测仍因模型权重授权未完成。
- 隔离探针已成功导入 PyTorch 2.7.1+cpu 与 TabPFN 9.1.0；最小 fit 进入官方权重授权流程但未取得授权，未下载权重，详见 `reports/tabpfn_probe_2026-10-10.md`。
- 浏览器自动化 smoke test 已通过；Chromium、Firefox、WebKit 三引擎自动路径已完成，人工逐像素视觉审阅和屏幕阅读器审计仍未完成，证据见 `reports/cross_browser_smoke_2026-10-10.md`。
- 静态可访问性基础审计已通过 31 个页面；屏幕阅读器和人工可用性审查仍未完成，证据见 `reports/accessibility_validation.md`。
- Edge Accessibility tree 已核对入口页和第 05 节关键控件的角色/名称；真实屏幕阅读器端到端审查仍未完成，证据见 `reports/ax_tree_validation.md`。
- 20 个外部来源链接在本次日期核验中可达；链接可达不等于主张逐条核验，证据见 `reports/external_link_validation.md`。
- TabPFN 版本、限制和许可证页面已于 2026-10-10 重新核对；本机运行证据仍未通过，详见 `reports/tabpfn_fact_refresh.md`。
- 30 节课件仍是初版，尚未完成统一深度、引用和跨章节终审。
- 已有合成数据、两个真实数据集和 36 次预声明参数实验；更广数据集、消融、内存峰值和正式数据许可审计仍未完成。
- 已新增两个真实数据集上的 10 种子、140 次重复实验及描述性 95% t 近似区间；更广数据集、消融、内存峰值、正式许可审计和 TabPFN 对照仍未完成。
- 已新增预处理消融：2 个数据集、3 个模型、5 个种子、60 次运行，并保留 9 次收敛警告；更广消融、内存峰值、正式许可审计和 TabPFN 对照仍未完成。
- 已新增代表性资源剖析：14 次拟合记录拟合时间与 RSS 峰值；更大规模压力测试、正式许可审计和 TabPFN 对照仍未完成。
- 已新增更大规模资源压力剖析：5,000×50 与 15,000×50 两档合成数据、6 个模型、12 次拟合；TabPFN 资源对照和生产容量测试仍未完成。
- 已新增全课程浏览器交互审计：30/30 页面、150 个自测展开、范围控件/复制/Canvas 路径通过，HTTP 资源错误为 0；该证据不替代真实屏幕阅读器和跨浏览器人工复核。
- Edge Accessibility tree 已扩展为 30/30 页面逐页检查命名 heading 和交互角色；工作站缺少 NVDA，真实屏幕阅读器语音与人工视觉复核仍未完成；三引擎自动复核已由 `reports/cross_browser_smoke_2026-10-10.md` 覆盖。
- 已新增 Diabetes 回归扩展：70 次固定协议运行，保留逐次 JSON、汇总报告和无告警结果；该实验不替代更广数据集覆盖或 TabPFN 对照。
- 已建立许可证与来源审计：`data/license_manifest.json` 与 `reports/license_audit_2026-10-10.md`，明确项目许可证未声明、依赖许可证、UCI 数据集来源边界、TabPFN 代码/模型权重分离和论文仅引用边界。

## 审计结论

项目不能宣告完成。当前状态是“全课程初版与验证基础已建立，最终质量门禁未通过”；继续工作必须从上述未通过项开始，不得用文件数量代替验收。
