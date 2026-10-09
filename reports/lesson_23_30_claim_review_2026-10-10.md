# 第 23–30 节研究与交付主张级核验记录（2026-10-10）

## 核验范围

逐节阅读第 23–30 节及其 lesson plan，并对页面中的数据处理、交叉验证、比较协议、研究计划和交付声明，与 scikit-learn 官方文档、本地 benchmark/资源日志和研究资料进行对照。模板、计划和自测不被误计为已完成实验。

## 结果矩阵

| 课件 | 结论 | 已有证据 | 未闭环项 |
|---|---|---|---|
| 23 数据处理 | 部分通过 | Pipeline/ColumnTransformer、训练折拟合预处理、缺失值处理和泄漏边界与 scikit-learn 1.9.1 官方文档一致；MCAR/MAR/MNAR 已补充 Rubin (1976) 原始来源，教学规模预处理链已执行并保存 JSON/Markdown 记录，页面明确操作性边界和不可由观测数据自动证明的限制。 | 该运行不等于更广数据处理协议、生产容量或 TabPFN 实验；完整缺失数据推断方法不在本节范围。 |
| 24 可信 benchmark | 通过（协议层） | 本地重复 benchmark、真实 Breast Cancer/Wine/Diabetes 结果、预处理消融、资源和失败记录覆盖页面要求的主要字段；页面明确不只保留最佳结果。 | 更广数据集、组件消融和 TabPFN 同协议结果仍缺。 |
| 25 模型比较 | 部分通过 | 页面把 TabPFN、XGBoost、CatBoost、FT-Transformer 的比较条件化，避免绝对排名；XGBoost/CatBoost/FT-Transformer 主张和本地树模型结果已有单独记录。 | TabPFN 未完成 checkpoint 预测，四类模型尚无同协议完整比较；FT-Transformer 官方实现未在本机运行。 |
| 26 研究机会 | 通过（研究设计层） | 可证伪假设、问题—证据—实验链条与现有研究记录和开放问题一致；页面没有把方向口号写成结果。 | 研究方向的新颖性仍需逐个检索相关工作，不能由本页模板证明。 |
| 27 实验计划 | 通过（计划层） | 变量、对照、指标、资源预算、失败分支和停止规则与项目验收标准一致；示例明确标注未执行。 | 计划尚未全部转成实际 TabPFN 实验，权重授权是直接前置条件。 |
| 28 论文精读工作坊 | 部分通过（模板层） | 页面要求问题—方法—实验—结论—局限逐项映射，R04 原始论文已有核心机制核验记录。 | 本页是精读模板，不等于已完成完整论文逐表/逐图复核；仍需补充代表性论文的实际阅读记录。 |
| 29 综合项目 | 未完成（交付规范层通过） | 页面清楚区分数据许可、环境、代码、日志、真实运行、模拟示例和未执行部分。 | 课程要求的 TabPFN 与基线综合项目尚未完成，原因是 checkpoint 权重授权/下载未完成。 |
| 30 知识整合与验收 | 通过（课程框架层） | 决策题要求任务、协议、基线、版本、校准、资源和失败条件；与验收矩阵及现有门禁一致。 | 结课题能否由学习者独立完成，需真实教学试用和专家终审验证。 |

## 关键来源与本地证据

- Pipeline/预处理与泄漏：<https://scikit-learn.org/stable/modules/compose.html>、<https://scikit-learn.org/stable/modules/impute.html>。
- 交叉验证、重复和测试集边界：<https://scikit-learn.org/stable/modules/cross_validation.html>。
- 本地实验：`reports/repeated_benchmark_10seeds.md`、`reports/preprocessing_ablation_2026-10-10.md`、`reports/resource_profile_2026-10-10.md`、`reports/stress_resource_profile_2026-10-10.md`。
- 比较与模型事实：`reports/xgboost_claim_verification_2026-10-10.md`、`reports/catboost_claim_verification_2026-10-10.md`、`reports/ft_transformer_claim_verification_2026-10-10.md`。

## 处理决定

- 将“协议已设计/本地基线已运行”与“TabPFN 综合项目已完成”严格分开。
- 将第 28 节标为论文精读模板层，不把已有摘要/核心机制核验冒充逐图逐表复现。
- 保留第 23 节代码逐块执行、第 26 节新颖性检索和第 30 节真实教学试用的未闭环说明；第 23 节缺失机制的专门原始来源已补充为 R15。
- 本批完成了 23–30 节的主张边界盘点；项目整体仍不能因课程文件齐全而宣告完成。
