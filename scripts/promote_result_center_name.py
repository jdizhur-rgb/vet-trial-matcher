from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old = ';_orig["markdown"](f"### {confidence}");_orig["markdown"](f"**{center}**");return'
new = '''\n            if confidence == "Prescreening required":\n                _orig["markdown"]('<span style="display:inline-block;font-size:.78rem;font-weight:600;color:#6f665f;background:#f3f0ec;padding:.16rem .48rem;border-radius:999px;margin:0 0 .35rem">Prescreening required</span>',unsafe_allow_html=True)\n            else:\n                _orig["markdown"](f"### {confidence}")\n            _orig["markdown"](f'<div style="font-size:1.03rem;font-weight:700;color:#2f6f73;margin:.18rem 0 .48rem">{center}</div>',unsafe_allow_html=True)\n            return'''
if old not in text:
    raise SystemExit('Expected current result-card hook not found; app.py left unchanged')
text2 = text.replace(old, new, 1)
if text2 == text:
    raise SystemExit('No change made')
path.write_text(text2, encoding='utf-8')
print('RESULT_CARD_HIERARCHY_REFINED')
