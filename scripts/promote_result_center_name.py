from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old = ';_orig["markdown"](f"### {confidence}");st.caption(center);return'
new = ';_orig["markdown"](f"### {confidence}");_orig["markdown"](f"**{center}**");return'
if old not in text:
    raise SystemExit('Expected result-center rendering hook not found; app.py left unchanged')
text2 = text.replace(old, new, 1)
if text2 == text:
    raise SystemExit('No change made')
path.write_text(text2, encoding='utf-8')
print('RESULT_CENTER_PROMOTED')
