#!/usr/bin/env python3
import json
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent


class Extractor(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.text = []
        self.links = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(urljoin(self.base, href))
    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


ev = json.loads((RUN / "current-source-evidence.json").read_text())
by_source = defaultdict(list)
fallback_needed = []
for row in ev["attempts"]:
    if row["result"] == "http_response" and row.get("artifact"):
        artifact_path = ROOT / row["artifact"]
        raw = artifact_path.read_bytes() if artifact_path.exists() else b""
        sample = raw[:200].lower()
        is_pdf = raw.startswith(b"%PDF")
        if is_pdf:
            text = ""
            links = []
        else:
            decoded = raw.decode("utf-8", "replace")
            parser = Extractor(row["url"])
            try:
                parser.feed(decoded)
                text = re.sub(r"\s+", " ", " ".join(parser.text)).strip()
                links = list(dict.fromkeys(parser.links))
            except Exception:
                text, links = "", []
        relevant_links = [u for u in links if re.search(r"trial|study|studies|research|oncolog|cancer|protocol|clinical", u, re.I)]
        summary = {**row, "is_pdf": is_pdf, "visible_text_chars": len(text),
                   "text_excerpt": text[:1800], "link_count": len(links),
                   "relevant_links": relevant_links[:100]}
        thin = row.get("status") != 200 or is_pdf or len(text) < 400
        if thin:
            fallback_needed.append({"source_id": row["source_id"], "url": row["url"],
                                    "reason": "pdf_requires_text_extraction" if is_pdf else
                                              f"http_{row.get('status')}_or_thin_text_{len(text)}"})
    else:
        summary = dict(row)
        if row["result"] == "transport_error" or (row.get("status") and row["status"] >= 400):
            fallback_needed.append({"source_id": row["source_id"], "url": row["url"],
                                    "reason": row["result"]})
    by_source[row["source_id"]].append(summary)

out = {"run_id": RUN.name, "sources": [{"source_id": k, "routes": v} for k, v in by_source.items()],
       "web_fallback_needed": list({(x["source_id"], x["url"]): x for x in fallback_needed}.values())}
(RUN / "source-body-review.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
(RUN / "web-fallback-targets.json").write_text(json.dumps(out["web_fallback_needed"], indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"sources": len(by_source), "web_fallback_targets": len(out["web_fallback_needed"]),
                  "thin_source_ids": len({x['source_id'] for x in out['web_fallback_needed']})}, indent=2))
