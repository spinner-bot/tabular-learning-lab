from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing anchor in {relative}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")


replace(
    "lessons/02_ml_workflow.html",
    '<p class="warning callout"><strong>时间数据：</strong>未来预测不能随机打乱历史，否则“未来信息”可能通过相邻样本泄漏。</p></section><section class="card"><h2>4. 代码示例',
    '<p class="warning callout"><strong>时间数据：</strong>未来预测不能随机打乱历史，否则“未来信息”可能通过相邻样本泄漏。</p><label><input id="leakage-switch" type="checkbox"> 模拟“先整体计算统计量再划分”</label><p id="leakage-result" class="meta" aria-live="polite">当前流程：先划分，再只用训练数据拟合变换器。</p><script>const leakage=document.querySelector("#leakage-switch"),leakageResult=document.querySelector("#leakage-result");leakage.addEventListener("change",()=>{leakageResult.textContent=leakage.checked?"风险流程：测试集统计量已进入变换，评估可能偏乐观。":"当前流程：先划分，再只用训练数据拟合变换器。"});</script></section><section class="card"><h2>4. 代码示例',
)

replace(
    "lessons/09_xgboost.html",
    '<div class="grid"><div class="term"><strong>正则化</strong>惩罚复杂树或过大的叶权重。</div><div class="term"><strong>gamma</strong>要求分裂带来足够收益。</div><div class="term"><strong>lambda/alpha</strong>控制 L2/L1 约束。</div><div class="term"><strong>缺失值方向</strong>实现默认路径，行为以版本文档为准。</div></div></section><section class="card"><h2>2. 工程设计</h2>',
    '<div class="grid"><div class="term"><strong>正则化</strong>惩罚复杂树或过大的叶权重。</div><div class="term"><strong>gamma</strong>要求分裂带来足够收益。</div><div class="term"><strong>lambda/alpha</strong>控制 L2/L1 约束。</div><div class="term"><strong>缺失值方向</strong>实现默认路径，行为以版本文档为准。</div></div><p>采样参数（如行/列子采样）可改变每轮看到的信息和树之间的相关性；量化/近似分裂把连续特征映射到候选桶，以换取速度或内存效率。它们影响的是具体训练协议，不是无条件的效果保证。</p></section><section class="card"><h2>2. 工程设计</h2>',
)
