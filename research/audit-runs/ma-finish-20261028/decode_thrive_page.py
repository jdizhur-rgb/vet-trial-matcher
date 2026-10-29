"""Decode public inline page content, without running JS or using backend APIs.

Input is a locally saved, ordinarily retrieved public HTML page. Output stays in
scratch; save only concise reviewed clinical facts in the research repository.
Flight text chunks may contain literal newlines and need not end before the
next JSON row, so splitting the payload by lines loses valid clinic content.
"""
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def clinic_props(html):
    chunks = []
    for script in BeautifulSoup(html, 'html.parser').find_all('script'):
        text = script.string or ''
        if 'self.__next_f.push(' not in text:
            continue
        row, _ = json.JSONDecoder().raw_decode(text.split('self.__next_f.push(', 1)[1])
        if row[0] == 1:
            chunks.append(row[1])
    payload = ''.join(chunks)
    for match in re.finditer(r'[0-9a-f]+:(?=\["\$",)', payload):
        try:
            row, _ = json.JSONDecoder(strict=False).raw_decode(payload[match.end():])
        except ValueError:
            continue
        if (isinstance(row, list) and len(row) > 3 and isinstance(row[3], dict)
                and row[3].get('props', {}).get('contentTypeId') == 'pageClinic'):
            return row[3]['props']
    raise ValueError('No complete public clinic page props found')


if __name__ == '__main__':
    print(json.dumps(clinic_props(Path(sys.argv[1]).read_text()), ensure_ascii=False, indent=2))
