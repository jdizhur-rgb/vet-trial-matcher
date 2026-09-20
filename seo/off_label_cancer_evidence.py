"""Small, diagnosis-specific blocks for clinically accessible off-label treatment evidence."""

from __future__ import annotations

import html
import re
from pathlib import Path


CANINE = {
    "urothelial carcinoma": {
        "title": "Off-label targeted therapy: sorafenib + piroxicam",
        "body": (
            "Sorafenib is a human multi-kinase inhibitor that a veterinary oncologist may be able to prescribe off-label. "
            "A 2026 prospective phase II study treated 43 dogs with muscle-invasive urothelial carcinoma using sorafenib plus piroxicam as first-line therapy. "
            "Twenty-seven dogs (62.8%) had a partial response, 11 (25.6%) had stable disease and five (11.6%) had progressive disease. "
            "Median progression-free survival was 175 days and median overall survival was 407 days."
        ),
        "when": (
            "This may be worth discussing for a dog with active muscle-invasive bladder or urethral urothelial carcinoma, including selected dogs with metastatic disease, "
            "when urine flow and kidney function are adequate. The study excluded dogs with tumor-related hydronephrosis, complete urethral obstruction, end-stage disease or end-stage kidney disease. "
            "It did not establish benefit for cats or superficial urothelial tumors."
        ),
        "limits": (
            "This was a single-arm study performed at one Japanese center and used a historical piroxicam-only comparison, so it does not prove that the combination is better than current standard treatments. "
            "Sorafenib is not approved for canine urothelial carcinoma, and access and cost vary. Blood pressure, kidney values and liver enzymes need close monitoring. "
            "Hypertension occurred in 49% of dogs; one dog developed grade 3 acute kidney injury. The regimen should be considered and supervised by a veterinary oncologist, not started independently."
        ),
        "source_url": "https://www.nature.com/articles/s41598-026-64955-1",
        "source_label": "2026 prospective phase II study (Scientific Reports)",
    }
}


def render(key: str, pet: str) -> str:
    item = CANINE.get(key) if pet == "dog" else None
    if not item:
        return ""
    e = html.escape
    return (
        '<aside class="off-label-evidence">'
        f'<h2>{e(item["title"])}</h2>'
        f'<p>{e(item["body"])}</p>'
        f'<p><strong>When it may be considered:</strong> {e(item["when"])}</p>'
        f'<p><strong>Important limitations and monitoring:</strong> {e(item["limits"])}</p>'
        f'<p class="evidence-source"><a href="{e(item["source_url"], quote=True)}" rel="noopener">{e(item["source_label"])} →</a></p>'
        '</aside>'
    )


def move_blocks_to_treatment_options(root: Path) -> int:
    """Place off-label evidence with current treatment listings, not in the guide flow."""
    root = Path(root)
    changed = 0
    for path in root.glob("*/dogs/urothelial-carcinoma/index.html"):
        text = path.read_text(encoding="utf-8")
        block_match = re.search(r'<aside class="off-label-evidence">.*?</aside>', text, re.S)
        if not block_match:
            raise AssertionError(f"Missing off-label evidence block in {path}")
        block = block_match.group(0)
        revised = text[:block_match.start()] + text[block_match.end():]
        transition = re.search(r'<section class="options-transition">.*?</section>', revised, re.S)
        if not transition:
            raise AssertionError(f"Missing treatment-options transition in {path}")
        revised = revised[:transition.end()] + block + revised[transition.end():]
        revised = re.sub(
            r'<p class="option-count">(\d+) options? currently in our catalog\.</p>',
            r'<p class="option-count">\1 clinical trial listings currently in our catalog.</p>',
            revised,
            count=1,
        )
        path.write_text(revised, encoding="utf-8")
        changed += 1
    if not changed:
        raise AssertionError("No canine urothelial-carcinoma page found for off-label evidence")
    return changed
