"""Freeze country assignments before spawning; preserve historic slot cursors."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / 'research/oncology-care-queue'
COUNTRIES = {
    1: ['Austria', 'United Kingdom', 'Sweden', 'Hungary', 'Serbia', 'Latvia', 'Moldova', 'Vatican City'],
    2: ['Czechia', 'Italy', 'Norway', 'Romania', 'Bosnia and Herzegovina', 'Lithuania', 'Kosovo', 'Turkey'],
    3: ['Poland', 'Spain', 'Finland', 'Bulgaria', 'Montenegro', 'Luxembourg', 'Andorra'],
    4: ['Germany', 'Switzerland', 'Portugal', 'Slovakia', 'North Macedonia', 'Malta', 'Liechtenstein'],
    5: ['France', 'Belgium', 'Ireland', 'Slovenia', 'Albania', 'Cyprus', 'Monaco'],
    6: ['Netherlands', 'Denmark', 'Greece', 'Croatia', 'Estonia', 'Iceland', 'San Marino'],
}
PRIOR = {
    1: ['research/audit-runs/europe-slot-1-20261015'],
    2: ['research/audit-runs/europe-slot-2-20261015'],
    3: [],
    4: ['research/audit-runs/europe-slot-4-20261016', 'research/audit-runs/care-discovery-20261014T215849-0400/DE'],
    5: ['research/audit-runs/care-discovery-20261014T215849-0400/FR'],
    6: ['research/audit-runs/europe-slot-6-20261015', 'research/audit-runs/care-discovery-20261014T215849-0400/NL'],
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    now = datetime.now(ZoneInfo('America/New_York'))
    baseline = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == baseline
    state = read(QUEUE / 'state.json')
    assert state.get('active_run') is None, 'Inspect real activity of recorded run before assigning'
    run_id = 'europe-controller-' + now.strftime('%Y%m%dT%H%M%S%z')
    run = ROOT / 'research/audit-runs' / run_id
    assert not run.exists()
    run.mkdir()
    public = read(ROOT / 'data/oncology_centers.json')['centers']
    supplemental = read(ROOT / 'data/oncology_centers_supplemental.json')['centers']
    inventory = read(ROOT / 'data/oncology_care_source_inventory.json')['sources']
    assignments = []
    for slot, countries in COUNTRIES.items():
        path = QUEUE / f'europe-slots/slot-{slot}.json'
        old = read(path) if path.exists() else None
        assert old is None or old['countries'] == countries
        history = (old or {}).get('runs', [])
        unfinished = [x for x in history if x.get('disposition') == 'INCOMPLETE' or x.get('coverage_complete') is False]
        if unfinished:
            country = unfinished[-1]['country']
            reason = 'Continue explicit incomplete country; numeric cursor is not completion proof'
        else:
            same_day = [x for x in history if x.get('local_date') == now.date().isoformat()]
            if same_day:
                country = same_day[-1]['country']
                reason = 'Same local-day assignment; do not consume another country'
            else:
                used = {x['country'] for x in history if x.get('coverage_complete') is True or x.get('disposition') == 'COMPLETE'}
                country = next((c for c in countries if c not in used), None)
                reason = 'First not demonstrably completed country in own fixed queue'
        if country is None:
            continue
        worker = run / f'worker-{slot}'
        worker.mkdir()
        own = [x for x in public if x.get('country') == country]
        own_ids = {x.get('source_id') for x in own}
        frozen = {
            'run_id': run_id, 'slot': slot, 'country': country, 'baseline_sha': baseline,
            'slot_state_before': old, 'prior_receipt_directories': PRIOR[slot],
            'existing_public_records': own,
            'existing_supplemental_records': [x for x in supplemental if x.get('country') == country],
            'existing_inventory_rows': [x for x in inventory if x.get('id') in own_ids],
            'saved_pending': [x for x in state.get('pending', []) if x.get('territory', x.get('country')) == country],
            'saved_unprocessed_leads': [x for x in state.get('unprocessed_leads', []) if x.get('territory', x.get('country')) == country],
            'all_catalog_dedupe_inputs': ['data/oncology_centers.json', 'data/oncology_centers_seed.json', 'data/oncology_centers_supplemental.json', 'data/oncology_care_source_inventory.json', 'seo/oncology_teleconsultations.py', 'data/acvim_oncology_profiles.json'],
            'publication_check': 'Previously published records are baseline, not NEW; current main supersedes old proposals',
        }
        write(worker / 'input.json', frozen)
        assignments.append({
            'run_id': run_id, 'slot': slot, 'country': country, 'baseline_sha': baseline,
            'scope': 'entire_country; no candidate, sixty-record, or old test-time cap',
            'selection_reason': reason, 'worker_directory': str(worker.relative_to(ROOT)),
            'slot_state_path': str(path.relative_to(ROOT)), 'input_path': str((worker / 'input.json').relative_to(ROOT)),
            'prior_receipt_directories': PRIOR[slot], 'existing_physical_count': len(own),
            'agent_id': None, 'spawn_requested_at': None, 'spawn_returned_at': None,
            'completed_observed_at': None, 'status': 'ASSIGNED_BEFORE_SPAWN',
        })
    write(run / 'assignments.json', {'run_id': run_id, 'baseline_sha': baseline, 'frozen_at': now.isoformat(), 'assignments': assignments})
    write(run / 'run.json', {
        'run_id': run_id, 'baseline_sha': baseline, 'started_at': now.isoformat(),
        'status': 'ASSIGNED_BEFORE_SPAWN', 'architecture': 'one_controller_six_fork_none_agents',
        'shell_git_python': 'PASS', 'fresh_remote_main': baseline,
        'activity_check': 'Queue active_run null; local collaboration inventory contains only running controller. Historic slot publications are concluded checkpoints, not claims of present activity. Process inventory unavailable (ps fatal library error). Fresh-main leases and field reconciliation remain mandatory.',
        'assignment_policy': 'Explicit owner decision 2026-10-16 supersedes old weekday directions and ten-candidate test caps',
    })
    state['active_run'] = {'run_id': run_id, 'started_at': now.isoformat(), 'status': 'ASSIGNED_BEFORE_SPAWN'}
    write(QUEUE / 'state.json', state)
    write(run / 'publication-ledger.json', {'run_id': run_id, 'packages': []})
    print(json.dumps({'run_id': run_id, 'baseline': baseline, 'assignments': [{'slot': x['slot'], 'country': x['country'], 'existing': x['existing_physical_count']} for x in assignments]}))


if __name__ == '__main__':
    main()
