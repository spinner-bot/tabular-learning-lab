$root = Split-Path $PSScriptRoot -Parent
$utf8 = New-Object System.Text.UTF8Encoding($false)
function Update-Text([string]$relative, [hashtable]$replacements) {
    $path = Join-Path $root $relative
    $text = [IO.File]::ReadAllText($path, $utf8)
    foreach ($item in $replacements.GetEnumerator()) {
        if (-not $text.Contains($item.Key)) { throw "Missing anchor in $relative" }
        $text = $text.Replace($item.Key, $item.Value)
    }
    [IO.File]::WriteAllText($path, $text, $utf8)
}

$r03 = @{}
$r03['<li>计算混淆矩阵导出的 Accuracy、Precision、Recall 和 F1。</li>'] = '<li>计算混淆矩阵导出的 Accuracy、Precision、Recall 和 F1，并区分概率指标。</li><li>解释 ROC-AUC、Log Loss、RMSE 和 R² 的含义与边界。</li>'
$r03['<p class="callout">指标不是模型的永久标签。必须写清任务、阈值、类别比例和错误代价。</p>'] = '<p class="callout">指标不是模型的永久标签。必须写清任务、阈值、类别比例和错误代价。下面的阈值控件只使用固定的教学样例，不代表真实模型结果。</p><label for="threshold-demo">示意分类阈值：<output id="threshold-value">0.50</output></label><input id="threshold-demo" type="range" min="0" max="1" step="0.05" value="0.50"><p id="threshold-result" class="meta" aria-live="polite"></p><script>const p=[.95,.80,.65,.55,.45,.30,.10],y=[1,1,0,1,0,0,0],r=document.querySelector("#threshold-demo"),v=document.querySelector("#threshold-value"),o=document.querySelector("#threshold-result");function show(){const t=Number(r.value);let tp=0,fp=0,fn=0,tn=0;p.forEach((q,i)=>{const pred=q>=t?1:0;if(pred&&y[i])tp++;else if(pred&&!y[i])fp++;else if(!pred&&y[i])fn++;else tn++});v.value=t.toFixed(2);o.textContent=`示意混淆矩阵：TP=${tp}、FP=${fp}、FN=${fn}、TN=${tn}；阈值改变，Precision/Recall 会随之改变。`}r.addEventListener("input",show);show();</script>'
$r03['<section class="card"><h2>3. 代码示例（未执行）</h2>'] = '<section class="card"><h2>3. 回归指标与概率指标</h2><p><strong>RMSE</strong> 是 MSE 开平方，和目标变量同量纲，因此更容易解释；它仍会放大大误差。<strong>R²</strong> 衡量相对基线（通常是训练集均值）减少的平方误差比例，可能为负，不能直接解释成“准确率百分比”。</p><p><strong>Log Loss</strong> 评价概率预测：对错误且自信的概率惩罚更大。<strong>ROC-AUC</strong> 衡量模型把正例排在负例前面的排序能力，跨阈值汇总，但不等于概率校准，也不自动解决类别极不平衡。</p><div class="grid"><div class="term"><strong>回归选择</strong>报告 MAE、RMSE、R²，并说明异常值和业务代价。</div><div class="term"><strong>概率选择</strong>报告 Log Loss、校准曲线或 Brier 等与概率质量相关的指标。</div><div class="term"><strong>排序选择</strong>ROC-AUC 反映排序，不替代固定阈值下的 Precision/Recall。</div><div class="term"><strong>边界</strong>任何指标都依赖数据拆分、标签定义和决策成本。</div></div></section><section class="card"><h2>4. 代码示例（未执行）</h2>'
$r03['<h2>4. 易错点</h2>'] = '<h2>5. 易错点</h2>'
$r03['<h2>5. 自测</h2>'] = '<h2>6. 自测</h2>'
$r03['<h2>来源与闭环</h2>'] = '<h2>7. 来源与闭环</h2>'
$r03['<details class="quiz"><summary>为什么 MSE 对异常值敏感？</summary><p>误差被平方，大误差的贡献增长更快。</p></details>'] = '<details class="quiz"><summary>为什么 MSE 对异常值敏感？</summary><p>误差被平方，大误差的贡献增长更快。</p></details><details class="quiz"><summary>ROC-AUC 高能否说明概率校准良好？</summary><p>不能；ROC-AUC主要评价排序，校准要比较预测概率与实际频率。</p></details><details class="quiz"><summary>R² 是不是准确率百分比？</summary><p>不是；它是相对于基线平方误差的解释比例，可能为负且依赖数据协议。</p></details>'
Update-Text 'lessons/03_metrics.html' $r03

$r06 = @{}
$r06['<div class="grid"><div class="term"><strong>Gini</strong>对节点中随机抽样的标签被错分的程度建模。</div><div class="term"><strong>熵 Entropy</strong>用类别分布的不确定性衡量混杂程度。</div><div class="term"><strong>信息增益</strong>父节点不确定性减去子节点加权不确定性。</div><div class="term"><strong>阈值候选</strong>数值特征相邻排序值之间的候选切点。</div></div>'] = '<div class="grid"><div class="term"><strong>Gini</strong>公式为 1−Σₖpₖ²，节点纯时为 0。</div><div class="term"><strong>熵 Entropy</strong>公式为 −Σₖpₖlog₂pₖ，表示标签不确定性。</div><div class="term"><strong>信息增益</strong>父节点不纯度减去按样本数加权的子节点不纯度。</div><div class="term"><strong>阈值候选</strong>数值特征相邻排序值之间的候选切点。</div></div><p>例如父节点正负各半时，Gini=0.5、熵=1；纯节点两者都为 0。不同准则可能选择不同切点，具体实现还受停止条件和样本权重影响。</p>'
$r06['<p class="callout">节点不纯度下降是训练选择标准，不是对未来泛化效果的保证。</p>'] = '<p class="callout">节点不纯度下降是训练选择标准，不是对未来泛化效果的保证。</p></section><section class="card"><h2>3. 回归树的误差下降</h2><p>回归树不计算类别不纯度，而常用节点内平方误差（SSE）或其等价的方差目标。例：父节点目标为 [1,2,5,6]，均值 3.5，SSE=17；若切成 [1,2] 与 [5,6]，两个子节点均值分别为 1.5、5.5，总 SSE=0.5+0.5=1，训练目标下降 16。这个下降只评价当前样本，不保证未来数据同样改善。</p><div class="grid"><div class="term"><strong>分类</strong>比较 Gini、熵或信息增益等类别目标。</div><div class="term"><strong>回归</strong>比较平方误差、绝对误差等回归目标，取决于实现。</div></div>'
$r06['<section class="card"><h2>3. 代码示例（未执行）</h2>'] = '<section class="card"><h2>4. 代码示例（未执行）</h2>'
$r06['<h2>4. 易错点</h2>'] = '<h2>5. 易错点</h2>'
$r06['<h2>5. 自测</h2>'] = '<h2>6. 自测</h2>'
$r06['<h2>来源与闭环</h2>'] = '<h2>7. 来源与闭环</h2>'
$r06['<details class="quiz"><summary>分类树和回归树选择标准相同吗？</summary><p>不相同；分类使用类别不纯度，回归使用误差等目标。</p></details>'] = '<details class="quiz"><summary>分类树和回归树选择标准相同吗？</summary><p>不相同；分类使用类别不纯度，回归使用误差等目标。</p></details><details class="quiz"><summary>父节点正负各半时，Gini 和熵分别是多少？</summary><p>Gini=1−(0.5²+0.5²)=0.5，熵=−0.5log₂0.5−0.5log₂0.5=1。</p></details><details class="quiz"><summary>回归树如何比较候选分裂？</summary><p>比较分裂前后的节点误差（常见为平方误差）下降，并按子节点样本量正确汇总。</p></details>'
Update-Text 'lessons/06_tree_splits.html' $r06
Write-Output 'Updated lessons 03 and 06.'
