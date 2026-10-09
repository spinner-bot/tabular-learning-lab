from pathlib import Path

path = Path(__file__).resolve().parents[1] / "lessons/01_tabular_learning_intro.html"
text = path.read_text(encoding="utf-8")
old = '<p class="meta">图 1：同样的特征到模型框架可以产生不同类型的标签输出。</p></section><section class="card"><h2>3. 端到端小例子</h2>'
new = '<p class="meta">图 1：同样的特征到模型框架可以产生不同类型的标签输出。</p><label for="task-demo">任务类型：</label><select id="task-demo" aria-label="分类或回归任务类型"><option value="classification">分类：输出离散类别或概率</option><option value="regression">回归：输出数值</option></select><p id="task-result" class="meta" aria-live="polite">当前选择：分类；先明确标签语义，再选择指标和模型协议。</p><script>const task=document.querySelector("#task-demo"),taskResult=document.querySelector("#task-result");task.addEventListener("change",()=>{taskResult.textContent=task.value==="classification"?"当前选择：分类；先明确标签语义，再选择指标和模型协议。":"当前选择：回归；先明确标签语义，再选择误差指标和模型协议。"});</script></section><section class="card"><h2>3. 端到端小例子</h2>'
if old not in text:
    raise RuntimeError("lesson 01 task switch anchor not found")
path.write_text(text.replace(old, new), encoding="utf-8", newline="")
print("Updated lesson 01 task switch.")
