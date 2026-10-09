# 第 11–15 节主张级事实核验记录（2026-10-10）

## 核验范围与规则

本批逐节阅读 `lessons/11_tabular_challenges.html` 至 `lessons/15_fair_comparison.html`、对应 lesson plan 和页面来源链接；对可外部核验的技术主张优先使用原始论文或官方文档。代码示例标注为“未执行”的，不计入已验证实验。该记录是主张级复核，不替代逐字教学专家终审。

## 结果矩阵

| 课件 | 主张与证据 | 结论 | 未闭环项 |
|---|---|---|---|
| 11 表格学习的特殊挑战 | 异质特征、小样本、缺失、类别特征、分布偏移和模型归纳偏置的教学性概括；页面引用 FT-Transformer 研究，原论文讨论表格深度模型比较协议、强基线和“无普遍最优解”的边界。 | 部分通过 | 页面中的挑战分类是教学综合，不能全部归因于 R03；尚未为每个概念补充独立官方/教材来源。 |
| 12 MLP | MLP 由线性层与非线性构成，使用反向传播训练；页面关于数值缩放、早停、正则化和验证集边界与 scikit-learn MLP 文档及常见实践一致。 | 通过（概念层；最小路径已执行） | 页面内联示例本身未执行；独立最小 MLP 路径见 `code/lesson_12_13_examples.py`，类别 embedding 不是 scikit-learn MLP 文档的直接结论，需在后续深度学习实现批次补充框架级来源。 |
| 13 Transformer | Q/K/V 直觉、`Attention(Q,K,V)=softmax(QKᵀ/√d_k)V`、多头、残差、归一化和前馈层与 *Attention Is All You Need* 的结构和公式一致；页面明确注意力权重不等于因果解释。 | 通过（机制层；最小路径已执行） | 页面内联 PyTorch 代码未执行；独立最小多头注意力路径已记录于 `reports/lesson_12_13_examples_2026-10-10.json`；热力图为示意，不是实验输出；因果解释边界仍需在解释性专题中补充更直接来源。 |
| 14 FT-Transformer | 数值/类别特征形成 feature tokens，Transformer 建模特征关系；页面对原论文结论限定为 benchmark 条件，并保留 MLP 基线、成本和无普遍排名的边界。 | 部分通过 | 原论文主张已核对；官方实现/API 未在本仓库运行，页面代码明确为伪代码；实现版本与资源结论不能升级为本机实测。 |
| 15 公平比较 | 数据拆分、预处理、调参预算、随机种子、指标、资源和不确定性共同构成比较协议；数据泄漏和不一致协议会造成过度乐观或不可比结果。 | 通过（协议层） | 页面示例是记录格式而非运行程序；更广数据集、组件消融和 TabPFN 同协议对照仍缺。 |

## 采用的关键来源

- R03：Gorishniy et al., *Revisiting Deep Learning Models for Tabular Data*，`research/references.md`；原始论文见 <https://arxiv.org/abs/2106.11959>。
- Transformer 原始论文：Vaswani et al., *Attention Is All You Need*，<https://arxiv.org/abs/1706.03762>。
- scikit-learn 1.9.1 MLP 官方文档：<https://scikit-learn.org/stable/modules/neural_networks_supervised.html>。
- scikit-learn 常见陷阱与数据泄漏：<https://scikit-learn.org/stable/common_pitfalls.html>。
- 本仓库的重复 benchmark、资源记录和比较协议：`reports/repeated_benchmark_10seeds.md`、`reports/real_benchmark_breast_cancer.md`、`reports/real_benchmark_wine.md`、`reports/resource_profile_2026-10-10.md`。

## 处理决定

- 没有把“论文中报告过”改写成“当前实现已运行”；第 14 节继续保留实现/API 未验证边界。
- 没有把 FT-Transformer 在论文 benchmark 中的竞争力改写成普遍优于树模型；第 11、14、15 节均保留任务、数据和协议条件。
- 没有把示意图或未执行代码计入实验结果；相关页面和本报告均明确标注限制。
- 本批可减少第 11–15 节的事实不确定性，但不能关闭全课程逐句核验、官方实现运行或跨浏览器/屏幕阅读器门禁。
