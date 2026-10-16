"""Independent controller readback: concise facts, never raw embedded payloads."""
import concurrent.futures
import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from scripts.check_evidence_keys import redact_text

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PACKAGES = [(1, 2), (2, 3), (3, 5), (4, 3), (5, 3)]


def read(url):
    at = datetime.now(timezone.utc).isoformat()
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'VetTrialFinder official-source verification'})
        with urllib.request.urlopen(request, timeout=18) as response:
            body = response.read(3000000).decode('utf-8', errors='replace')
            code = response.status
            body = re.sub(r'<!--.*?-->', ' ', body, flags=re.S)
            body = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', body, flags=re.S | re.I)
        plain = html.unescape(re.sub('<[^>]+>', ' ', body))
        plain = re.sub(r'\s+', ' ', plain).strip()
        return {'url': url, 'attempted_at': at, 'status': code, 'text': redact_text(plain)}
    except Exception as error:
        return {'url': url, 'attempted_at': at, 'error': type(error).__name__ + ': ' + str(error)}


def main():
    existing = {x.get('source_id') for x in json.loads((ROOT / 'data/oncology_centers_supplemental.json').read_text())['centers']}
    changes = []
    for slot, checkpoint in PACKAGES:
        package = RUN / f'worker-{slot}/checkpoint-{checkpoint:02}'
        for change in json.loads((package / 'proposed_changes.json').read_text())['changes']:
            if change['operation'] == 'NEW' and change['source_id'] not in existing:
                changes.append((slot, change))
    urls = {u for _, c in changes for u in [c['official_url'], *c['new_value'].get('supporting_urls', [])]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        responses = dict(zip(sorted(urls), executor.map(read, sorted(urls))))
    result = []
    for slot, change in changes:
        evidence = []
        for url in [change['official_url'], *change['new_value'].get('supporting_urls', [])]:
            response = dict(responses[url]); plain = response.pop('text', '')
            snippets = []
            for match in re.finditer(r'(tumor|tumour|tumeur|nádor|novotvar|onkolog|oncolog|chimioth|chemioter|chemoter|imunoter|immunoth|elektrochem|chirurg)', plain, re.I):
                start, end = max(0, match.start()-70), min(len(plain), match.end()+180)
                if not snippets or start > snippets[-1][0]+130:
                    snippets.append((start, plain[start:end]))
                if len(snippets) >= 8:
                    break
            # Persist one brief excerpt, not a collection of page passages.
            response['short_review_excerpt'] = ' '.join(snippets[-1][1].split()[:20]) if snippets else ''
            for field in ('street', 'phone'):
                value = change['new_value'].get(field, '')
                i = plain.casefold().find(value.casefold()) if value else -1
                response[field+'_literal_found'] = i >= 0
                if i >= 0:
                    response[field+'_context'] = plain[max(0,i-40):i+len(value)+60]
            evidence.append(response)
        result.append({'slot': slot, 'source_id': change['source_id'], 'proposed_services': change['new_value']['services'], 'reads': evidence})
    output = {'run_id': RUN.name, 'kind': 'independent_parent_transport_and_concise_primary_readback_not_automatic_approval', 'records': result}
    (RUN / 'parent-readback-02.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'records': len(result), 'urls': len(urls), 'success':sum(x.get('status') == 200 for x in responses.values()), 'errors':[{'url':x['url'],'error':x['error']} for x in responses.values() if 'error' in x]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
