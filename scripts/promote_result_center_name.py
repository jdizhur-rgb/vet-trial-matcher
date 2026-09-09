from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old = '''            if confidence == "Prescreening required":
                _orig["markdown"]('<span style="display:inline-block;font-size:.76rem;font-weight:600;color:#6f665f;background:#f3f0ec;padding:.12rem .44rem;border-radius:999px;margin:0 0 .18rem">Prescreening required</span>',unsafe_allow_html=True)
            else:
                _orig["markdown"](f"### {confidence}")
            _orig["markdown"](f'<div style="font-size:1.03rem;line-height:1.18;font-weight:700;color:#2f6f73;margin:.08rem 0 .24rem">{center}</div>',unsafe_allow_html=True)
            return'''
new = '''            if confidence == "Prescreening required":
                _orig["markdown"]('<span style="display:inline-block;font-size:.76rem;font-weight:600;color:#6f665f;background:#f3f0ec;padding:.12rem .44rem;border-radius:999px;margin:0 0 .12rem">Prescreening required</span>',unsafe_allow_html=True)
            else:
                _orig["markdown"](f'<div style="font-size:.82rem;line-height:1.1;font-weight:650;color:#6f665f;margin:0 0 .12rem">{confidence}</div>',unsafe_allow_html=True)
            _orig["markdown"](f'<div style="font-size:1.03rem;line-height:1.16;font-weight:700;color:#2f6f73;margin:.04rem 0 .18rem">{center}</div>',unsafe_allow_html=True)
            return'''
if old not in text:
    raise SystemExit('Expected compact result-card hook not found; app.py left unchanged')
text = text.replace(old, new, 1)
css_anchor = 'div[data-testid="stMainBlockContainer"] h3{line-height:1.18!important;margin:.22rem 0 .12rem!important}'
css_new = 'div[data-testid="stMainBlockContainer"] h3{font-size:1rem!important;line-height:1.16!important;margin:.12rem 0 .08rem!important}'
if css_anchor in text:
    text = text.replace(css_anchor, css_new, 1)
path.write_text(text, encoding='utf-8')
print('MATCH_LABEL_SHRUNK')
