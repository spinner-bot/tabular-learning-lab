"""Validate the repository's manually curated license and provenance manifest."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "license_manifest.json"
REPORT = ROOT / "reports" / "license_audit_2026-10-10.md"


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    errors: list[str] = []
    for item in items:
        for key in ("name", "kind", "license", "status", "notes"):
            if not item.get(key):
                errors.append(f"{item.get('name', '<unnamed>')}: missing {key}")
        url = item.get("url")
        if url is not None and urlparse(url).scheme not in {"http", "https"}:
            errors.append(f"{item['name']}: URL is not http(s): {url}")

    names = [item["name"] for item in items]
    if len(names) != len(set(names)):
        errors.append("duplicate item names")

    required = {
        "tabular-learning-lab",
        "Breast Cancer Wisconsin Diagnostic",
        "Wine",
        "TabPFN model weights",
        "XGBoost",
        "CatBoost",
        "scikit-learn",
    }
    missing = sorted(required - set(names))
    errors.extend(f"required item missing: {name}" for name in missing)

    lines = [
        "# 许可证与数据来源审计",
        "",
        f"审计日期：{payload.get('audit_date', '未记录')}",
        "",
        "本报告只核对仓库声明的来源、许可证字段和文件边界，不替代法律意见。代码库许可证、第三方依赖许可证、数据集许可、模型权重条款和论文引用权利分别处理。",
        "",
        "| 名称 | 类型 | 许可证/条款 | 状态 | 官方来源 |",
        "|---|---|---|---|---|",
    ]
    for item in items:
        url = item.get("url")
        source = f"[{item['source']}]({url})" if url else item["source"]
        lines.append(
            f"| {item['name']} | {item['kind']} | {item['license']} | {item['status']} | {source} |"
        )
    lines.extend(
        [
            "",
            "## 边界与行动",
            "",
            "- 仓库当前没有项目级许可证；在项目负责人选定前，不宣称仓库整体可按某个开源许可证再分发。",
            "- UCI 两个数据集只作为运行时来源，不把原始数据复制进仓库；发布结果时保留 DOI、来源和 CC BY 4.0 归因要求。",
            "- TabPFN 代码和模型权重分开记录；模型权重必须按所选版本的模型页面单独接受条款，不能由 Apache-2.0 代码许可推导权重许可。",
            "- 论文和官方文档按引用使用，不把引用权利扩展解释为复制或再分发权利。",
            "",
            "## 机器检查",
            "",
            f"- 条目数：{len(items)}",
            f"- 检查结果：{'PASS' if not errors else 'FAIL'}",
        ]
    )
    if errors:
        lines.extend(["", "错误：", *[f"- {error}" for error in errors]])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if errors:
        print("license audit: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"license audit: PASS ({len(items)} items, output={REPORT.relative_to(ROOT)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
