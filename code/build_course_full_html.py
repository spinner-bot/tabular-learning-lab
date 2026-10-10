"""Build a single, self-contained reading version from the 30 lesson pages."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "lessons"
OUTPUT = ROOT / "course_full.html"

MODULES = [
    ("I", "基础概念与学习任务", "先建立表格学习的共同语言：任务、数据、泄漏与评估。", 1, 4),
    ("II", "决策树与集成方法", "从一棵树走向随机森林、梯度提升与可解释的模型选择。", 5, 10),
    ("III", "特征、评估与实验设计", "把数据准备、验证策略和实验记录连接成可靠的工作流。", 11, 15),
    ("IV", "深度表格模型与 TabPFN", "了解深度模型、预训练表格模型及其适用边界。", 16, 22),
    ("V", "预处理、缺失数据与基准", "围绕预处理、缺失值和基准实验形成可复现的判断。", 23, 27),
    ("VI", "研究实践与继续学习", "将阅读、复现、诊断和研究问题组织为下一步行动。", 28, 30),
]


def lesson_number(path: Path) -> str:
    return path.name.split("_", 1)[0]


def title_from(source: str, number: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", source, re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", match.group(1)).strip()) if match else path_title(number)
    title = re.sub(r"^Lesson\s*\d+\s*[:：-]?\s*", "", title, flags=re.I)
    title = re.sub(r"^第\s*\d+\s*[讲课节]\s*[:：-]?\s*", "", title)
    return title.strip() or path_title(number)


def path_title(number: str) -> str:
    return f"第 {int(number):02d} 课"


def rewrite_links_and_ids(main_html: str, number: str, filename_to_anchor: dict[str, str]) -> tuple[str, dict[str, str]]:
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', main_html, re.I)
    id_map = {old: f"lesson-{number}-{old}" for old in ids}

    def replace_id(match: re.Match[str]) -> str:
        quote, old = match.group(1), match.group(2)
        return f"id={quote}{id_map.get(old, old)}{quote}"

    main_html = re.sub(r'id=(["\'])([^"\']+)\1', replace_id, main_html, flags=re.I)

    for attr in ("for", "aria-controls", "aria-labelledby", "aria-describedby", "data-copy", "data-status"):
        pattern = rf'({attr}=["\'])([^"\']+)(["\'])'
        main_html = re.sub(
            pattern,
            lambda m: m.group(1) + id_map.get(m.group(2), m.group(2)) + m.group(3),
            main_html,
            flags=re.I,
        )

    def replace_href(match: re.Match[str]) -> str:
        prefix, href, suffix = match.groups()
        if href.startswith("#"):
            href = "#" + id_map.get(href[1:], href[1:])
        elif href in filename_to_anchor:
            href = "#" + filename_to_anchor[href]
        elif href == "../index.html" or href == "index.html":
            href = "#course-cover"
        elif href.startswith("../"):
            href = href[3:]
        return prefix + href + suffix

    main_html = re.sub(r'(href=["\'])([^"\']+)(["\'])', replace_href, main_html, flags=re.I)
    return main_html, id_map


def scope_script(script: str, number: str, id_map: dict[str, str]) -> str:
    # Only rewrite selector strings, avoiding canvas colour literals such as #fff.
    def selector(match: re.Match[str]) -> str:
        method, quote, old = match.groups()
        return f"{method}({quote}#{id_map.get(old, f'lesson-{number}-{old}')}{quote}"

    script = re.sub(r'(querySelector(?:All)?)\(("|\')#([A-Za-z_][\w:.-]*)\2', selector, script)
    script = re.sub(r"\bdocument\.", "rootDoc.", script)
    return (
        "<script>(function(root){"
        "const rootDoc={querySelector:(s)=>root.querySelector(s),"
        "querySelectorAll:(s)=>root.querySelectorAll(s),"
        "getElementById:(id)=>root.querySelector('#'+id)};"
        + script
        + f"}})(document.getElementById('lesson-{number}'));</script>"
    )


def extract_main(source: str) -> str:
    match = re.search(r"<main\b[^>]*>(.*?)</main\s*>", source, re.I | re.S)
    if not match:
        raise ValueError("lesson has no main element")
    main = match.group(1)
    main = re.sub(r'<nav\b[^>]*class=["\'][^"\']*\bnav\b[^"\']*["\'][^>]*>.*?</nav\s*>', "", main, flags=re.I | re.S)
    main = re.sub(r"<script\b[^>]*>.*?</script\s*>", "", main, flags=re.I | re.S)
    return main.strip()


def extract_scripts(source: str) -> list[str]:
    return re.findall(r"<script\b[^>]*>(.*?)</script\s*>", source, re.I | re.S)


def build() -> None:
    lesson_paths = sorted(LESSONS_DIR.glob("*.html"))
    if len(lesson_paths) != 30:
        raise RuntimeError(f"expected 30 lessons, found {len(lesson_paths)}")
    filename_to_anchor = {p.name: f"lesson-{lesson_number(p)}" for p in lesson_paths}
    lessons: list[dict[str, object]] = []

    for path in lesson_paths:
        number = lesson_number(path)
        source = path.read_text(encoding="utf-8")
        main, id_map = rewrite_links_and_ids(extract_main(source), number, filename_to_anchor)
        scripts = [scope_script(script, number, id_map) for script in extract_scripts(source)]
        lessons.append({"number": number, "title": title_from(source, number), "main": main, "scripts": scripts})

    common_css = (ROOT / "assets" / "lesson.css").read_text(encoding="utf-8")
    extra_css = """
    :root{scroll-behavior:smooth}
    body{margin:0;background:#f6f8fb;color:#18212b}
    .course-shell{max-width:1240px;margin:0 auto;background:#fff;box-shadow:0 0 32px rgba(20,40,60,.08)}
    .course-cover,.course-toc,.course-chapter,.course-conclusion{padding:64px 7vw}
    .course-cover{min-height:58vh;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(135deg,#17324d,#2f6f8f);color:#fff}
    .course-cover h1{font-size:clamp(2.4rem,6vw,5rem);margin:.2em 0}.course-cover p{max-width:760px;font-size:1.15rem;line-height:1.8}
    .course-meta{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem}.course-meta span{border:1px solid rgba(255,255,255,.45);border-radius:999px;padding:.45rem .8rem}
    .course-toc{background:#eef5f8}.course-toc ul{line-height:1.9}.course-toc a,.course-end-nav a{color:#12617c}
    .course-chapter{border-top:8px solid #d7e6ea;background:#f8fbfc}.course-chapter h2{margin:.2em 0}.chapter-summary{max-width:720px;line-height:1.7}
    .full-lesson{max-width:1040px;margin:0 auto;padding:42px 7vw 54px;border-top:1px solid #dfe7eb;background:#fff;scroll-margin-top:18px}
    .full-lesson-heading{display:flex;justify-content:space-between;gap:1rem;align-items:baseline;flex-wrap:wrap;margin-bottom:1.2rem}.full-lesson-heading h2{margin:0;font-size:clamp(1.5rem,3vw,2.3rem)}
    .lesson-number{color:#597583;font-weight:700;letter-spacing:.08em}.course-end-nav{display:flex;justify-content:space-between;gap:1rem;margin-top:2rem;padding-top:1rem;border-top:1px solid #dfe7eb}.course-conclusion{background:#17324d;color:#fff}.course-conclusion a{color:#c8edf5}.course-conclusion li{margin:.7rem 0}
    canvas{display:block;max-width:100%;height:auto}button,input,select{font:inherit}
    @media(max-width:700px){.course-cover,.course-toc,.course-chapter,.course-conclusion,.full-lesson{padding-left:5vw;padding-right:5vw}.course-end-nav{flex-direction:column}.course-cover{min-height:50vh}}
    """
    parts = [
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="description" content="Tabular Learning 全部 30 课的整合阅读版。">',
        "<title>Tabular Learning 全套课程｜长篇整合版</title>",
        f"<style>{common_css}\n{extra_css}</style></head><body>",
        '<div class="course-shell">',
        '<header class="course-cover" id="course-cover"><p>Tabular Learning Lab · Integrated Edition</p><h1>Tabular Learning 全套课程</h1><p>表格学习：从基础概念到研究实践。这里把 30 个独立课件组织成一份连续、可检索、可交互的长篇学习材料。</p><div class="course-meta"><span>30 课</span><span>6 个模块</span><span>本地阅读版</span><span>2026-10-10</span></div><p><a href="#course-toc" style="color:#fff">开始阅读 ↓</a></p></header>',
        '<nav class="course-toc" id="course-toc" aria-labelledby="toc-title"><h2 id="toc-title">目录</h2><p>按模块循序阅读，也可以直接跳转到任意课程。</p><ol>',
    ]
    for roman, name, summary, start, end in MODULES:
        parts.append(f'<li><a href="#chapter-{roman}">模块 {roman}：{html.escape(name)}</a><ul>')
        for item in lessons[start - 1 : end]:
            parts.append(f'<li><a href="#lesson-{item["number"]}">第 {int(item["number"]):02d} 课：{html.escape(str(item["title"]))}</a></li>')
        parts.append("</ul></li>")
    parts.append("</ol></nav>")

    for roman, name, summary, start, end in MODULES:
        parts.append(f'<section class="course-chapter" id="chapter-{roman}"><p class="lesson-number">MODULE {roman}</p><h2>模块 {roman}：{html.escape(name)}</h2><p class="chapter-summary">{html.escape(summary)}</p></section>')
        for index in range(start - 1, end):
            item = lessons[index]
            number = str(item["number"])
            previous = f"#lesson-{lessons[index - 1]['number']}" if index else "#course-toc"
            following = f"#lesson-{lessons[index + 1]['number']}" if index + 1 < len(lessons) else "#course-conclusion"
            parts.append(f'<article class="full-lesson" id="lesson-{number}" aria-labelledby="lesson-{number}-title"><div class="full-lesson-heading"><span class="lesson-number">第 {int(number):02d} 课</span><h2 id="lesson-{number}-title">{html.escape(str(item["title"]))}</h2></div>{item["main"]}<div class="course-end-nav"><a href="{previous}">← 上一节</a><a href="#course-toc">目录</a><a href="{following}">下一节 →</a></div>{''.join(item["scripts"])}</article>')

    parts.append('<footer class="course-conclusion" id="course-conclusion"><p class="lesson-number">THE END</p><h2>结语：把阅读变成判断力</h2><p>这套课程从表格学习的基本概念出发，经过树模型、集成方法、实验设计、深度表格模型与 TabPFN，再回到预处理、缺失数据、基准和研究实践。学习的终点不是记住更多模型名称，而是能在真实数据上提出清楚的问题、建立可信的比较、识别结果的边界，并留下可复现的证据。</p><ul><li>重新阅读自己最薄弱的模块，并完成课件中的自测与小实验。</li><li>结合仓库中的 reports、code 与 research 材料复现一个小结论，记录数据、指标和限制。</li><li>将“可运行”与“已验证”区分开来，把不确定性写进下一轮实验计划。</li></ul><p>本长篇文件是面向基本阅读学习用途的整合版；原始 30 个课程文件、报告和中间资料均保留，仍可独立打开和追溯。</p><p><a href="#course-cover">回到封面</a> · <a href="#course-toc">回到目录</a></p></footer></div></body></html>')
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes, {len(lessons)} lessons)")


if __name__ == "__main__":
    build()
