from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old = '''            if confidence == "Prescreening required":
                _orig["markdown"]('<span style="display:inline-block;font-size:.78rem;font-weight:600;color:#6f665f;background:#f3f0ec;padding:.16rem .48rem;border-radius:999px;margin:0 0 .35rem">Prescreening required</span>',unsafe_allow_html=True)
            else:
                _orig["markdown"](f"### {confidence}")
            _orig["markdown"](f'<div style="font-size:1.03rem;font-weight:700;color:#2f6f73;margin:.18rem 0 .48rem">{center}</div>',unsafe_allow_html=True)
            return'''
new = '''            if confidence == "Prescreening required":
                _orig["markdown"]('<span style="display:inline-block;font-size:.76rem;font-weight:600;color:#6f665f;background:#f3f0ec;padding:.12rem .44rem;border-radius:999px;margin:0 0 .18rem">Prescreening required</span>',unsafe_allow_html=True)
            else:
                _orig["markdown"](f"### {confidence}")
            _orig["markdown"](f'<div style="font-size:1.03rem;line-height:1.18;font-weight:700;color:#2f6f73;margin:.08rem 0 .24rem">{center}</div>',unsafe_allow_html=True)
            return'''
if old not in text:
    raise SystemExit('Expected current result-card hierarchy hook not found; app.py left unchanged')
text = text.replace(old, new, 1)
css_anchor = '.intro-answer{font-size:.94rem;color:#45414a;margin:.35rem 0 .65rem}'
css_extra = css_anchor + '''\n/* Compact result cards: tighten vertical rhythm without changing controls. */\ndiv[data-testid="stMainBlockContainer"] h3{line-height:1.18!important;margin:.22rem 0 .12rem!important}\ndiv[data-testid="stMainBlockContainer"] p{line-height:1.38!important;margin-top:.18rem!important;margin-bottom:.32rem!important}\ndiv[data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"]{margin-bottom:0!important}\ndiv[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"]{gap:.48rem!important}\n'''
if '/* Compact result cards:' not in text:
    if css_anchor not in text:
        raise SystemExit('CSS anchor not found; app.py left unchanged')
    text = text.replace(css_anchor, css_extra, 1)
path.write_text(text, encoding='utf-8')
print('RESULT_CARDS_COMPACTED')
