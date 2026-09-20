"""Small, diagnosis-specific blocks for clinically accessible off-label treatment evidence."""

from __future__ import annotations

import html


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
