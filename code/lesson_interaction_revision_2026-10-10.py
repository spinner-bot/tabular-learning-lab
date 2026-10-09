from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing anchor in {relative}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")


replace(
    "lessons/03_metrics.html",
    '<div class="grid"><div class="term"><strong>回归选择</strong>报告 MAE、RMSE、R²，并说明异常值和业务代价。</div>',
    '<svg viewBox="0 0 680 150" role="img" aria-label="回归预测与残差示意图" style="max-width:100%;background:#fbfcfa;border:1px solid #dce2e7;border-radius:10px"><path d="M55 125 H635 M55 20 V125" stroke="#17212b" stroke-width="2"/><path d="M75 110 L600 35" stroke="#3155d4" stroke-width="3"/><circle cx="100" cy="102" r="5" fill="#c77700"/><circle cx="180" cy="92" r="5" fill="#c77700"/><circle cx="265" cy="82" r="5" fill="#c77700"/><circle cx="355" cy="68" r="5" fill="#c77700"/><circle cx="450" cy="58" r="5" fill="#c77700"/><circle cx="555" cy="42" r="5" fill="#c77700"/><text x="275" y="145">预测值</text><text x="8" y="90" transform="rotate(-90 8 90)">真实值</text><text x="460" y="25" fill="#3155d4">理想拟合参考</text></svg><div class="grid"><div class="term"><strong>回归选择</strong>报告 MAE、RMSE、R²，并说明异常值和业务代价。</div>',
)

replace(
    "lessons/06_tree_splits.html",
    '<div class="grid"><div class="term"><strong>分类</strong>比较 Gini、熵或信息增益等类别目标。</div><div class="term"><strong>回归</strong>比较平方误差、绝对误差等回归目标，取决于实现。</div></div></section><section class="card"><h2>4. 代码示例',
    '<div class="grid"><div class="term"><strong>分类</strong>比较 Gini、熵或信息增益等类别目标。</div><div class="term"><strong>回归</strong>比较平方误差、绝对误差等回归目标，取决于实现。</div></div><label for="split-demo">候选切点：<output id="split-value">1.5</output></label><input id="split-demo" type="range" min="0" max="2" step="1" value="0"><p id="split-result" class="meta" aria-live="polite"></p><script>const splitCandidates=["1.5","2.5","3.5"],splitGini=[0,0.5,0],splitRange=document.querySelector("#split-demo"),splitValue=document.querySelector("#split-value"),splitResult=document.querySelector("#split-result");function showSplit(){const i=Number(splitRange.value);splitValue.value=splitCandidates[i];splitResult.textContent=`固定玩具数据 x=[1,2,3,4]、y=[0,0,1,1] 的示意加权 Gini：${splitGini[i].toFixed(2)}；这里只比较候选，不代表模型泛化结果。`}splitRange.addEventListener("input",showSplit);showSplit();</script></section><section class="card"><h2>4. 代码示例',
)

print("Updated residual and split demonstrations.")
