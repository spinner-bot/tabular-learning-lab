# 最终验收标准—证据矩阵

核验日期：2026-10-10。矩阵依据 `docs/Tabular_Learning_课程课件生成总控Prompt.md` 第十四节建立。状态只有“通过”“部分通过”“未验证”三类；“部分通过”不等同于项目完成。

## 内容

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| 30 节课件和入口存在 | `code/audit_lessons.py`、`index.html`、HTML 结构报告 | 通过 | 无结构缺口 |
| 固定教学结构和最低深度 | `code/content_depth_audit.py`、`reports/content_depth_validation.md` | 通过（结构层） | 逐句教学准确性和统一深度仍需人工核读 |
| 目标、讲解、例子、图示/交互、自测、来源 | `code/audit_lessons.py`、`reports/lesson_source_inventory_2026-10-10.md` | 通过（存在性层） | 来源是否逐条支持主张仍未全部确认 |
| 核心知识、边界和不确定性 | `research/fact_check_matrix.md`、`reports/paper_claim_verification_2026-10-10.md` | 部分通过 | F08、动态 API、逐课主张仍有缺口 |
| 课程结构、术语和公式一致 | `code/cross_lesson_audit.py`、`code/citation_consistency_audit.py` | 部分通过 | 结构一致已通过，专家级术语/公式终审未完成 |

## 研究

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| 研究核验矩阵已建立 | `research/fact_check_matrix.md` | 通过（已建立） | 多个高重要性事实仍非最终通过 |
| 重要事实有真实、相关、可访问来源 | `research/references.md`、`reports/external_link_validation.md` | 部分通过 | 链接可达不等于主张逐条核验；FT-Transformer 页面受 challenge 影响 |
| 版本/时效信息已注明 | `research/version_history.md`、`reports/tabpfn_fact_refresh.md` | 部分通过 | TabPFN 本机 API/资源实测缺失 |
| 未解决问题明确记录 | `research/open_questions.md`、`qa/final_audit.md` | 通过 | 缺口仍需后续解决或正式结案 |
| 无虚构引用/伪造实验 | 论文复核记录、TabPFN 失败记录、各 benchmark JSON | 通过（按当前证据） | 继续保持论文/本地实验/当前实现三栏分离 |

## 技术

| 要求 | 权威证据 | 状态 | 剩余缺口 |
|---|---|---|---|
| HTML 可打开、导航和本地链接有效 | `code/check_html_structure.py`、浏览器 smoke test | 通过 |
| 交互组件实际可用 | `code/browser_smoke_test.py`、`reports/lesson_05_validation.md` | 部分通过 | 深度交互只抽样验证；全课程人工操作路径未完成 |
| 代码有验证记录或明确标注未验证 | 各 lesson、`code/*_smoke_test.py`、`reports/*validation*.md` | 部分通过 | 尚未逐块执行所有课件代码 |
| 窄屏可用 | `reports/browser_full_layout_2026-10-10.json` | 通过（自动化宽度层） | 人工视觉和跨内核仍未完成 |
| 外部依赖和离线限制已说明 | `reports/tabpfn_validation.md`、课件边界说明 | 部分通过 | TabPFN 可运行环境仍缺失 |
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
