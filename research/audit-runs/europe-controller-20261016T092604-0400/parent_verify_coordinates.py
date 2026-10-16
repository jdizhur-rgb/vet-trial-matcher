"""Re-read only approved exact-address geo schemas and destination markers."""
import concurrent.futures
import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent


def verify(changes):
    sample = changes[0]
    values = {x['field']: x['new_value'] for x in changes}
    out = {'source_id': sample['source_id'], 'url': sample['official_url'], 'attempted_at': datetime.now(timezone.utc).isoformat(), 'proposed_latitude': values['latitude'], 'proposed_longitude': values['longitude']}
    try:
        with urllib.request.urlopen(out['url'], timeout=18) as response:
            raw = response.read(3000000).decode('utf-8', errors='replace')
            out['http_status'] = response.status
        out['address_geo_objects'] = []
        def walk(obj):
            if isinstance(obj, list):
                for child in obj:
                    walk(child)
            if isinstance(obj, dict):
                geo = obj.get('geo') or (obj if 'latitude' in obj and 'longitude' in obj else None)
                if isinstance(geo, dict) and isinstance(obj.get('address'), dict):
                    try:
                        if abs(float(geo.get('latitude')) - values['latitude']) < 0.000001 and abs(float(geo.get('longitude')) - values['longitude']) < 0.000001:
                            out['address_geo_objects'].append({k: obj[k] for k in ('@type', 'name', 'address', 'geo', 'latitude', 'longitude') if k in obj})
                    except (TypeError, ValueError):
                        pass
                for child in obj.values():
                    if isinstance(child, (dict, list)):
                        walk(child)
        for script in re.findall(r'<script\b[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', raw, re.I | re.S):
            try:
                walk(json.loads(script))
            except json.JSONDecodeError:
                pass
        out['destination_markers'] = []
        for lat, lon in re.findall(r'!3d(-?[0-9.]+)!4d(-?[0-9.]+)', html.unescape(raw)):
            if abs(float(lat)-values['latitude']) < 0.000001 and abs(float(lon)-values['longitude']) < 0.000001:
                out['destination_markers'].append({'latitude': float(lat), 'longitude': float(lon), 'kind': '!3d/!4d actual destination, not viewport'})
        out['machine_correspondence'] = bool(out['address_geo_objects'] or out['destination_markers'])
    except Exception as error:
        out['error'] = type(error).__name__ + ': ' + str(error)
    return out


def main():
    groups = {}
    for change in json.loads((RUN / 'worker-1/checkpoint-02/proposed_changes.json').read_text())['changes']:
        if change['operation'] == 'UPDATE':
            groups.setdefault(change['source_id'], []).append(change)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        rows = list(executor.map(verify, groups.values()))
    result = {'run_id': RUN.name, 'kind': 'independent_parent_official_address_geo_readback', 'sources': rows}
    (RUN / 'parent-coordinate-readback-02.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'sources': len(rows), 'correspondence': sum(x.get('machine_correspondence', False) for x in rows), 'not_corresponding': [x for x in rows if not x.get('machine_correspondence')]}))


if __name__ == '__main__':
    main()
