# 逐课来源清单（2026-10-10）

本清单由 `code/source_inventory.py` 生成。它只记录课件链接结构，不判断链接内容是否逐句支持主张；可达性见 `reports/external_link_validation.md`，事实核验见 `research/fact_check_matrix.md`。

| 课件 | 外部来源数 | 本地来源数 | 外部来源 |
|---|---:|---:|---|
| `01_tabular_learning_intro.html` | 1 | 4 | `https://scikit-learn.org/stable/supervised_learning.html` |
| `02_ml_workflow.html` | 1 | 4 | `https://scikit-learn.org/stable/common_pitfalls.html` |
| `03_metrics.html` | 1 | 6 | `https://scikit-learn.org/stable/modules/model_evaluation.html` |
| `04_bias_variance.html` | 1 | 4 | `https://scikit-learn.org/stable/modules/cross_validation.html` |
| `05_decision_trees.html` | 1 | 6 | `https://scikit-learn.org/stable/modules/tree.html` |
| `06_tree_splits.html` | 1 | 6 | `https://scikit-learn.org/stable/modules/tree.html` |
| `07_random_forest.html` | 1 | 4 | `https://scikit-learn.org/stable/modules/ensemble.html` |
| `08_gbdt.html` | 1 | 4 | `https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting` |
| `09_xgboost.html` | 1 | 5 | `https://xgboost.readthedocs.io/` |
| `10_catboost.html` | 2 | 5 | `https://catboost.ai/docs/en/concepts/algorithm-main-stages_fighting-biases`<br>`https://catboost.ai/docs/en/concepts/algorithm-main-stages_cat-to-numberic` |
| `11_tabular_challenges.html` | 1 | 5 | `https://openreview.net/forum?id=i_Q1yrOegLY` |
| `12_mlp.html` | 1 | 6 | `https://scikit-learn.org/stable/modules/neural_networks_supervised.html` |
| `13_transformer.html` | 1 | 6 | `https://arxiv.org/abs/1706.03762` |
| `14_ft_transformer.html` | 1 | 5 | `https://openreview.net/forum?id=i_Q1yrOegLY` |
| `15_fair_comparison.html` | 1 | 5 | `https://scikit-learn.org/stable/modules/cross_validation.html` |
| `16_tabpfn_motivation.html` | 1 | 6 | `https://arxiv.org/abs/2207.01848` |
| `17_tabpfn_inference.html` | 1 | 6 | `https://github.com/PriorLabs/TabPFN` |
| `18_icl.html` | 1 | 5 | `https://arxiv.org/abs/2112.10510` |
| `19_tabpfn_prior.html` | 1 | 6 | `https://arxiv.org/abs/2305.11097` |
| `20_tabpfn_versions.html` | 3 | 5 | `https://github.com/PriorLabs/TabPFN`<br>`https://github.com/PriorLabs/TabPFN`<br>`https://docs.priorlabs.ai/models` |
| `21_tabpfn_experiment.html` | 1 | 4 | `https://github.com/PriorLabs/TabPFN` |
| `22_calibration.html` | 2 | 5 | `https://scikit-learn.org/stable/modules/calibration.html`<br>`https://github.com/PriorLabs/TabPFN` |
| `23_data_processing.html` | 3 | 5 | `https://dash.harvard.edu/entities/publication/73120378-8764-6bd4-e053-0100007fdf3b`<br>`https://scikit-learn.org/stable/modules/preprocessing.html`<br>`https://scikit-learn.org/stable/modules/impute.html` |
| `24_reproducible_benchmark.html` | 1 | 5 | `https://scikit-learn.org/stable/modules/cross_validation.html` |
| `25_model_comparison.html` | 1 | 5 | `https://scikit-learn.org/stable/modules/model_evaluation.html` |
| `26_research_opportunities.html` | 1 | 7 | `https://arxiv.org/abs/2207.01848` |
| `27_experiment_plan.html` | 1 | 5 | `https://scikit-learn.org/stable/modules/cross_validation.html` |
| `28_paper_workshop.html` | 1 | 6 | `https://arxiv.org/abs/2207.01848` |
| `29_capstone.html` | 1 | 6 | `https://github.com/PriorLabs/TabPFN` |
| `30_synthesis.html` | 1 | 7 | `https://scikit-learn.org/stable/modules/model_evaluation.html` |

合计：30 个课件，36 个外部链接，158 个本地链接。

## 判定

- 结构门禁：每个课件至少含一个外部来源：通过。
- 语义事实、链接可达性、版本日期和运行实测不由本脚本代替。
