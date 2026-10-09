# 第 13 节计划：Transformer 与注意力

- 学习目标：解释 token、embedding、Q/K/V、多头注意力、残差和归一化。
- 核心问题：模型如何让一个特征参考其他特征？
- 知识点：scaled dot-product attention、位置/特征 token、FFN。
- 案例：三特征注意力矩阵手算。
- 图示/交互：注意力热力图和逐步计算。
- 代码：小型 attention 实现与 PyTorch 对照。
- 自测：QKV、缩放、头、残差、注意力不等于因果解释。
- 来源：Vaswani et al. 原始论文和 PyTorch 文档。
- 难点：表格 token 化与序列 token 化的语义不同。
