"""Generate the standalone browser matcher tables from shared reviewed data."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    taxonomy = json.loads((ROOT / 'data/diagnosis_taxonomy.json').read_text())
    rules = json.loads((ROOT / 'data/matcher_protocol_rules.json').read_text())
    text = '\n'.join([
        '  // BEGIN SHARED MATCHER TABLES (generated; edit data/*.json)',
        '  const ALIASES = ' + json.dumps(taxonomy['aliases'], ensure_ascii=False) + ';',
        '  const FAMILIES = ' + json.dumps(taxonomy['families'], ensure_ascii=False) + ';',
        '  const PROTOCOL_RULES = ' + json.dumps(rules, ensure_ascii=False) + ';',
        '  // END SHARED MATCHER TABLES',
    ])
    path = ROOT / 'seo/static/matcher/matcher.js'
    source = path.read_text()
    source, count = re.subn(r'  // BEGIN SHARED MATCHER TABLES.*?  // END SHARED MATCHER TABLES', lambda _: text, source, flags=re.S)
    if count != 1:
        raise ValueError('Missing or duplicate generated matcher table block')
    path.write_text(source)
    print('MATCHER_TAXONOMY_SYNC_OK')


if __name__ == '__main__':
    main()
