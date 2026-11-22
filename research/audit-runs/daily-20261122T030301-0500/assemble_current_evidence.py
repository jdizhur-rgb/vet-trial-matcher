#!/usr/bin/env python3
"""Assemble only this run's saved Web responses into route-level evidence."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
RUN_ID = HERE.name


def write(name: str, value: object) -> None:
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def split_result(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n-{40,}\n", text) if part.strip()]


def assemble(kind: str) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(HERE.glob(f"web-{kind}-open-*.json")):
        payload = json.loads(path.read_text())
        text = "\n".join(
            item.get("text", "")
            for item in payload.get("result", {}).get("content", [])
            if item.get("type") == "text"
        )
        segments = split_result(text)
        urls = payload.get("retrieved_urls", [])
        if len(segments) != len(urls):
            raise SystemExit(f"{path.name}: {len(urls)} URLs but {len(segments)} result segments")
        completed = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        evidence_ref = str(path.relative_to(HERE.parents[2]))
        for url, segment in zip(urls, segments):
            internal_error = segment.startswith("Internal Error")
            crawl = re.search(r"Crawled: ([^;\n]+)", segment)
            title = segment.splitlines()[0].strip() if segment else ""
            rows.append({
                "url": url,
                "batch": payload.get("batch"),
                "completed_at": completed,
                "method": "web_open",
                "result": "web_error" if internal_error else "success",
                "opened": not internal_error,
                "crawled_label": crawl.group(1).strip() if crawl else None,
                "crawled_today": bool(crawl and crawl.group(1).strip() == "today"),
                "title": title,
                "text_sha256": hashlib.sha256(segment.encode()).hexdigest(),
                "excerpt": segment[:1400],
                "evidence_file": evidence_ref,
            })
    return rows


for kind in ("source", "protocol"):
    rows = assemble(kind)
    write(f"current-{kind}-web-summary.json", {
        "schema_version": 1,
        "run_id": RUN_ID,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "method": "web_open_same_official_urls_after_shell_transport_failure",
        "routes": rows,
        "summary": {
            "routes": len(rows),
            "success": sum(r["result"] == "success" for r in rows),
            "web_error": sum(r["result"] == "web_error" for r in rows),
            "crawled_today": sum(r["crawled_today"] for r in rows),
        },
    })


searches = []
for path in sorted(HERE.glob("discovery-search-*.json")):
    payload = json.loads(path.read_text())
    searches.append({
        "file": str(path.relative_to(HERE.parents[2])),
        "specs": payload.get("specs", []),
        "is_error": bool(payload.get("result", {}).get("isError")),
        "content_sha256": hashlib.sha256(
            json.dumps(payload.get("result", {}), sort_keys=True).encode()
        ).hexdigest(),
    })
write("global-discovery-evidence.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "search_batches": searches,
    "query_total": sum(len(x["specs"]) for x in searches),
    "note": "Raw result text remains in the referenced per-batch files; this index does not claim exhaustive global discovery.",
})

write("lead-protocol-current-findings.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "findings": [
        {
            "url": "https://www.paccalvet.com/cat-cancer-study",
            "current_result": "401 Unauthorized in direct Web open; discovery result exposed a trial page and up to four Paccal Vet doses but did not establish exact cancer cohort, active sites, or current intake.",
            "decision": "PENDING_EVIDENCE",
        },
        {
            "url": "https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/",
            "current_result": "Official UF page (Web crawl labelled yesterday) says the college is currently recruiting but its protocol field says Enrollment Paused. It names oral carcinoma, radiation backbone, daily oral LSD1 inhibitor, costs, interest form, and PI Marillia Takada.",
            "decision": "PENDING_EVIDENCE because current access labels conflict; distinct from the CSU LSD1 record by institution, PI, and radiation-linked protocol.",
        },
        {
            "url": "https://www.gamgee.io/trial/",
            "current_result": "Official page crawled today says trial now recruiting in Australia for dogs with mast-cell cancer and a personalized mRNA therapeutic vaccine.",
            "decision": "VERIFIED_EXISTING au-gamgee-personalized-mrna-vaccine",
        },
        {
            "url": "https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien/",
            "current_result": "Official Oniris page crawled today says recruitment is open for large/giant dogs with appendicular osteosarcoma for percutaneous BIOCERA-VET cement; the intervention is palliative stabilization and pain relief.",
            "decision": "VERIFIED_EXISTING fr-oniris-osa-biocera-vet-cement; remains outside treatment matching.",
        },
    ],
    "provenance": "Direct Web opens performed after run initialization; raw tool response is summarized factually here. Search batch files preserve the independent discovery result text.",
})
