from __future__ import annotations

import json
from pathlib import Path

from seo.trial_site_directory import build_directory, trial_site_records

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_trials():
    with (DATA / "trials_base.json").open(encoding="utf-8") as fh:
        base = json.load(fh)
    by_id = {t["id"]: t for t in base}
    paths = [DATA / "trial_updates.json"] + sorted(DATA.glob("catalog_patch_*.json"))
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as fh:
            doc = json.load(fh)
        for trial_id in doc.get("delete", []):
            by_id.pop(trial_id, None)
        for patch in doc.get("upsert", []):
            trial_id = patch["id"]
            if trial_id in by_id:
                merged = dict(by_id[trial_id])
                for key, value in patch.items():
                    if key in {"requires", "excludes"} and isinstance(value, dict):
                        nested = dict(merged.get(key, {}))
                        nested.update(value)
                        merged[key] = nested
                    else:
                        merged[key] = value
                by_id[trial_id] = merged
            else:
                by_id[trial_id] = patch
    return list(by_id.values())


def main():
    trials = load_trials()
    directory = build_directory(trials)
    out = DATA / "trial_site_directory.json"
    out.write_text(json.dumps(directory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    active = 0
    inactive = 0
    unresolved_active = []
    for trial in trials:
        for rec in trial_site_records(trial):
            if rec["status"] == "active":
                active += 1
                if not rec["addresses"]:
                    unresolved_active.append((trial.get("id", ""), rec["site_name"], trial.get("center", "")))
            else:
                inactive += 1

    print("TRIALS", len(trials))
    print("ORGANIZATIONS", len(directory["organizations"]))
    print("ACTIVE_SITE_RECORDS", active)
    print("INACTIVE_SITE_RECORDS", inactive)
    print("UNRESOLVED_ACTIVE", len(unresolved_active))
    for row in unresolved_active[:100]:
        print("UNRESOLVED", *row, sep=" | ")


if __name__ == "__main__":
    main()
