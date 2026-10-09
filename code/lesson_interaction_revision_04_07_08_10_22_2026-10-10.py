from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing anchor in {relative}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")


replace(
    "lessons/04_bias_variance.html",
    '<text x="270" y="145">模型复杂度 →</text></svg></section><section class="card"><h2>3. 公平比较协议</h2>',
    '<text x="270" y="145">模型复杂度 →</text></svg><label for="complexity-demo">示意复杂度：<output id="complexity-value">3</output></label><input id="complexity-demo" aria-label="示意模型复杂度" type="range" min="1" max="9" step="1" value="3"><p id="complexity-result" class="meta" aria-live="polite">低复杂度可能偏差较高；高复杂度可能增加方差。此处为概念示意。</p><script>const complexity=document.querySelector("#complexity-demo"),complexityValue=document.querySelector("#complexity-value"),complexityResult=document.querySelector("#complexity-result");complexity.addEventListener("input",()=>{const n=Number(complexity.value);complexityValue.value=n;complexityResult.textContent=n<=3?"低复杂度示意：偏差风险较高，训练/验证都可能欠拟合。":n>=7?"高复杂度示意：训练误差可能更低，但方差/过拟合风险上升。":"中等复杂度示意：需要结合验证曲线和预算判断。"});</script></section><section class="card"><h2>3. 公平比较协议</h2>',
)

replace(
    "lessons/07_random_forest.html",
    '<text x="280" y="145">树数量 →</text></svg></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
    '<text x="280" y="145">树数量 →</text></svg><label for="forest-demo">示意树数量：<output id="forest-value">10</output></label><input id="forest-demo" aria-label="示意随机森林树数量" type="range" min="1" max="100" step="1" value="10"><p id="forest-result" class="meta" aria-live="polite"></p><script>const forest=document.querySelector("#forest-demo"),forestValue=document.querySelector("#forest-value"),forestResult=document.querySelector("#forest-result");forest.addEventListener("input",()=>{const n=Number(forest.value);forestValue.value=n;forestResult.textContent=`示意解释：增加到 ${n} 棵树通常能稳定聚合，但不保证所有误差下降；计算和内存也会增加。`});forest.dispatchEvent(new Event("input"));</script></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
)

replace(
    "lessons/08_gbdt.html",
    '<text x="595" y="80">…</text></svg></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
    '<text x="595" y="80">…</text></svg><label for="round-demo">示意提升轮数：<output id="round-value">1</output></label><input id="round-demo" aria-label="示意梯度提升轮数" type="range" min="1" max="10" step="1" value="1"><p id="round-result" class="meta" aria-live="polite"></p><script>const round=document.querySelector("#round-demo"),roundValue=document.querySelector("#round-value"),roundResult=document.querySelector("#round-result");round.addEventListener("input",()=>{const n=Number(round.value);roundValue.value=n;roundResult.textContent=`示意状态：F${n}=F0+η·f1+…+η·f${n}；每轮依赖前一轮方向，训练下降不等于验证泛化一定改善。`});round.dispatchEvent(new Event("input"));</script></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
)

replace(
    "lessons/10_catboost.html",
    '<text x="425" y="120">当前样本之后不可用</text></svg></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
    '<text x="425" y="120">当前样本之后不可用</text></svg><label for="prefix-demo">处理排列中的第几个位置：<output id="prefix-value">4</output></label><input id="prefix-demo" aria-label="有序统计排列前缀位置" type="range" min="1" max="4" step="1" value="4"><p id="prefix-result" class="meta" aria-live="polite"></p><script>const prefix=document.querySelector("#prefix-demo"),prefixValue=document.querySelector("#prefix-value"),prefixResult=document.querySelector("#prefix-result");prefix.addEventListener("input",()=>{const n=Number(prefix.value);prefixValue.value=n;prefixResult.textContent=n===1?"前缀为空：只能使用先验，不能使用当前标签。":`当前位置 ${n}：只使用排列中更早位置的样本统计，当前样本及其之后的信息不可用。`});prefix.dispatchEvent(new Event("input"));</script></section><section class="card"><h2>3. 代码示例（未执行）</h2>',
)

replace(
    "lessons/22_calibration.html",
    '<p class="meta">图中数据为示意；分箱数量和样本量会影响读图。</p></section><section class="card"><h2>3. 解释边界</h2>',
    '<p class="meta">图中数据为示意；分箱数量和样本量会影响读图。</p><label for="bin-demo">示意分箱数：<output id="bin-value">5</output></label><input id="bin-demo" aria-label="示意校准分箱数" type="range" min="2" max="10" step="1" value="5"><p id="bin-result" class="meta" aria-live="polite">分箱越细不一定越好：样本量不足时估计会更不稳定。</p><script>const bins=document.querySelector("#bin-demo"),binValue=document.querySelector("#bin-value"),binResult=document.querySelector("#bin-result");bins.addEventListener("input",()=>{const n=Number(bins.value);binValue.value=n;binResult.textContent=`当前示意分箱数：${n}；ECE 和可靠性图必须同时报告分箱定义与每箱样本量。`});</script></section><section class="card"><h2>3. 解释边界</h2>',
)

print("Updated five planned interactions.")
