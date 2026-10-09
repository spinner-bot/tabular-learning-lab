# 最终验收标准—证据矩阵

核验日期：2026-10-10。矩阵依据 `docs/Tabular_Learning_课程课件生成总控Prompt.md` 第十四节建立。状态只有“通过”“部分通过”“未验证”三类；“部分通过”不等同于项目完成。

## 内容

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| 第 11–30 节主张级批次核验 | `reports/lesson_11_15_claim_review_2026-10-10.md`、`reports/lesson_16_22_claim_review_2026-10-10.md`、`reports/lesson_23_30_claim_review_2026-10-10.md` | 部分通过 | 已完成分批主张边界盘点；逐句专家终审、TabPFN 权重实验、完整论文精读和真实教学试用仍未完成 |
| 30 节课件和入口存在 | `code/audit_lessons.py`、`index.html`、HTML 结构报告 | 通过 | 无结构缺口 |
| 固定教学结构和最低深度 | `code/content_depth_audit.py`、`reports/content_depth_validation.md`、`reports/lesson_03_06_content_revision_2026-10-10.md` | 通过（结构与已发现缺口修订层） | 逐句教学准确性和统一深度仍需人工核读 |
| 目标、讲解、例子、图示/交互、自测、来源 | `code/audit_lessons.py`、`reports/lesson_source_inventory_2026-10-10.md` | 通过（存在性层） | 来源是否逐条支持主张仍未全部确认 |
| 核心知识、边界和不确定性 | `research/fact_check_matrix.md`、`reports/paper_claim_verification_2026-10-10.md`、`reports/xgboost_claim_verification_2026-10-10.md`、`reports/catboost_claim_verification_2026-10-10.md`、`reports/ft_transformer_claim_verification_2026-10-10.md` | 部分通过 | 主要论文机制已补充核验；动态 API、逐课主张和官方实现运行仍有缺口 |
| 课程结构、术语和公式一致 | `code/cross_lesson_audit.py`、`code/citation_consistency_audit.py` | 部分通过 | 结构一致已通过，专家级术语/公式终审未完成 |

## 研究

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| 研究核验矩阵已建立 | `research/fact_check_matrix.md` | 通过（已建立） | 多个高重要性事实仍非最终通过 |
| 重要事实有真实、相关、可访问来源 | `research/references.md`、`reports/external_link_validation.md`、各主张核验报告 | 部分通过 | 链接可达不等于主张逐条核验；FT-Transformer 原始 HTML 已核验，但官方实现和逐课映射仍未完成 |
| 版本/时效信息已注明 | `research/version_history.md`、`reports/tabpfn_fact_refresh.md` | 部分通过 | TabPFN 本机 API/资源实测缺失 |
| 未解决问题明确记录 | `research/open_questions.md`、`qa/final_audit.md` | 通过 | 缺口仍需后续解决或正式结案 |
| 无虚构引用/伪造实验 | 论文复核记录、TabPFN 失败记录、各 benchmark JSON | 通过（按当前证据） | 继续保持论文/本地实验/当前实现三栏分离 |
| 实验重复、区间和消融证据 | `reports/repeated_benchmark_10seeds.md`、`reports/preprocessing_ablation_2026-10-10.md`、对应 JSON | 部分通过 | 更广数据集、组件消融、大规模内存压力和 TabPFN 同协议对照仍缺失 |
| 资源记录 | `reports/resource_profile_2026-10-10.md`、`reports/stress_resource_profile_2026-10-10.md`、对应 JSON | 部分通过 | 已补充两档较大合成规模压力测试；仍缺 TabPFN 资源对照和生产容量测试 |
| 许可证与数据来源边界 | `data/license_manifest.json`、`reports/license_audit_2026-10-10.md` | 部分通过 | 依赖和数据来源已列明；项目级许可证尚未决定，TabPFN 模型权重仍需按版本接受条款 |
| 回归与更广数据集证据 | `code/regression_benchmark.py`、`reports/repeated_benchmark_diabetes_regression_2026-10-10.md`、对应 JSON | 部分通过 | 已补充 1 个回归数据集和 70 次重复运行；仍需更广任务/数据集与组件级消融 |
| 全课程交互路径 | `code/browser_interaction_audit.py`、`reports/browser_interaction_audit_2026-10-10.md`、`reports/course_visual_review_2026-10-10.md`、`reports/cross_browser_smoke_2026-10-10.md`、对应 JSON | 部分通过 | 30 页通用交互路径、三引擎 180 条桌面/移动路径与 60 张截图已自动核验；真实屏幕阅读器和逐像素人工视觉复核仍缺 |
| 全课程 AX tree 命名 | `code/ax_tree_course_audit.py`、`reports/ax_tree_course_audit_2026-10-10.md`、对应 JSON | 部分通过 | 30 页 Edge AX tree 已核验；屏幕阅读器语音输出仍缺 |

## 技术

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| HTML 可打开、导航和本地链接有效 | `code/check_html_structure.py`、浏览器 smoke test、`reports/cross_browser_smoke_2026-10-10.md` | 通过 |
| 交互组件实际可用 | `code/browser_smoke_test.py`、`code/browser_interaction_audit.py`、`reports/lesson_03_06_content_revision_2026-10-10.md`、`reports/cross_browser_smoke_2026-10-10.md` | 部分通过 | 自动路径已覆盖阈值滑块、details、复制和 canvas；真实屏幕阅读器和人工操作路径未完成 |
| 代码有验证记录或明确标注未验证 | 各 lesson、`code/*_smoke_test.py`、`code/lesson_23_preprocessing_example.py`、`reports/*validation*.md` | 部分通过 | 已补充第 23 节教学规模预处理链；尚未逐块执行所有课件代码 |
| 窄屏可用 | `reports/browser_full_layout_2026-10-10.json`、`reports/cross_browser_smoke_2026-10-10.md` | 通过（自动化宽度层） | 人工视觉仍未完成 |
| 外部依赖和离线限制已说明 | `reports/tabpfn_validation.md`、`reports/tabpfn_probe_2026-10-10.md`、课件边界说明 | 部分通过 | TabPFN 代码导入已在隔离环境通过；模型权重授权、checkpoint/预测和资源对照仍未完成 |
| TabPFN 隔离环境导入与授权门禁 | `reports/tabpfn_probe_2026-10-10.md` | 部分通过 | PyTorch 2.7.1+cpu 与 TabPFN 9.1.0 导入已通过；模型权重授权、checkpoint/预测和资源对照仍未完成 |
| 无明显控制台/排版问题 | 截图、Edge smoke test、`reports/manual_visual_review_2026-10-10.md` | 部分通过 | 仅人工查看入口和第 05 节，未覆盖全课程/多内核 |

## 教学与交付

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| 面向基础较浅学习者，直觉—定义—实例 | 30 份 lesson plan、30 个页面、内容深度审计 | 部分通过 | 统一教学质量尚未人工终审 |
| 公式/代码有解释，自测有诊断价值，误区有纠正 | 结构审计和页面内容 | 部分通过 | 结构存在性通过，教学专家终审未完成 |
| 目录、README、地图、研究资料、状态和测试报告齐全 | 仓库目录、`README.md`、`PROJECT_STATUS.md`、`reports/` | 通过（交付物层） | 不以文件存在代替质量验收 |
| 最终审计区分通过/未通过/未验证 | 本文件、`qa/final_audit.md` | 通过 | 项目整体仍不能宣告完成 |

## 结论

当前项目是“初版课程与验证基础已建立，若干技术/研究门禁通过，最终人工和环境门禁未完成”。在 TabPFN checkpoint、本课程逐句事实、屏幕阅读器端到端、全课程人工视觉/跨内核和更广实验缺口关闭前，不得标记 goal 为 complete。
