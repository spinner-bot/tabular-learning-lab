"""Check external lesson source URLs and preserve dated results."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "external_link_validation.json"
URL_RE = re.compile(r'href="(https?://[^"#]+)"')


def check(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "tabular-learning-lab-link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return {"url": url, "status": response.status, "final_url": response.geturl()}
    except urllib.error.HTTPError as error:
        if error.code in {403, 405}:
            try:
                request = urllib.request.Request(url, method="GET", headers={"Range": "bytes=0-512", "User-Agent": "tabular-learning-lab-link-check/1.0"})
                with urllib.request.urlopen(request, timeout=15) as response:
                    return {"url": url, "status": response.status, "final_url": response.geturl(), "method": "GET-fallback"}
            except Exception as fallback:  # pragma: no cover - network-specific
                return {"url": url, "error": f"{type(fallback).__name__}: {fallback}"}
        return {"url": url, "status": error.code, "error": str(error)}
    except Exception as error:  # pragma: no cover - network-specific
        return {"url": url, "error": f"{type(error).__name__}: {error}"}


def main() -> None:
    urls = sorted({url for page in (ROOT / "lessons").glob("*.html") for url in URL_RE.findall(page.read_text(encoding="utf-8"))})
    results = [check(url) for url in urls]
    OUTPUT.write_text(json.dumps({"date": str(date.today()), "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    failures = [result for result in results if result.get("status", 0) < 200 or result.get("status", 0) >= 400 or "error" in result]
    for result in results:
        print(result)
    if failures:
        raise SystemExit(f"external link check: FAIL ({len(failures)}/{len(results)} failures)")
    print(f"external link check: PASS ({len(results)} URLs)")


if __name__ == "__main__":
    main()
