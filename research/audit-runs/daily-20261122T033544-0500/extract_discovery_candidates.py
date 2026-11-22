#!/usr/bin/env python3
import glob, json, re
from pathlib import Path

run = Path(__file__).resolve().parent
rows = []
pattern = re.compile(r'(?m)^(.+?) \((https?://[^\s)]+(?:\)[^\s]*)?)\)\s*$')
for path in sorted(glob.glob(str(run / 'discovery-search-*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    text = '\n'.join(
        block.get('text', '') for block in data.get('result', {}).get('content', [])
        if block.get('type') == 'text'
    )
    for title, url in pattern.findall(text):
        rows.append({'batch': data['batch'], 'title': title.strip(), 'url': url.strip()})

unique = []
seen = set()
for row in rows:
    key = row['url'].rstrip('/')
    if key in seen:
        continue
    seen.add(key)
    unique.append(row)

(run / 'discovery-candidates-raw.json').write_text(
    json.dumps({'count': len(unique), 'candidates': unique}, indent=2, ensure_ascii=False) + '\n',
    encoding='utf-8'
)
print(json.dumps({'count': len(unique), 'candidates': unique}, indent=2, ensure_ascii=False))
