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
if old in text:
    text = text.replace(old, new, 1)
css_anchor = '.intro-answer{font-size:.94rem;color:#45414a;margin:.35rem 0 .65rem}'
css_add = '''
/* Unified study/action controls. */
div[data-testid="stExpander"] details summary{justify-content:center!important;text-align:center!important;gap:.35rem!important}
div[data-testid="stExpander"] details summary p{text-align:center!important}
div[data-testid="stDownloadButton"] button{width:100%!important;min-height:3rem!important;font-size:1rem!important;font-weight:600!important;border-radius:.8rem!important}
@media(max-width:900px){div[data-testid="stHorizontalBlock"]{row-gap:.35rem!important}div[data-testid="stDownloadButton"]{margin-top:0!important;margin-bottom:0!important}}
'''
if '/* Unified study/action controls. */' not in text:
    if css_anchor not in text: raise SystemExit('CSS anchor not found')
    text = text.replace(css_anchor, css_anchor + css_add, 1)
path.write_text(text, encoding='utf-8')

# Patch the source page through this small migration script; do not hand-edit the large Finder file.
p = Path('pages/1_Clinical_Trial_Finder.py')
s = p.read_text(encoding='utf-8')
old_copy = '''st.html(f"""<button id="copy-results-native" style="width:100%;padding:9px 12px;border:1px solid #d8d3cf;border-radius:9px;background:white;font-weight:600;color:#4b4642;cursor:pointer">📋 Copy results</button><div id="copy-msg" style="font:12px Arial;color:#55745d;margin-top:4px;min-height:14px"></div><script>(()=>{{const text={payload};const b=document.getElementById('copy-results-native'),m=document.getElementById('copy-msg');b.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(text);m.textContent='Results copied.';return}}catch(e){{}}const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{{document.execCommand('copy');m.textContent='Results copied.'}}catch(e){{m.textContent='Copy is blocked by this browser.'}}ta.remove()}})}})();</script>""", unsafe_allow_javascript=True)'''
new_copy = '''st.html(f"""<button id="copy-results-native" style="width:100%;height:48px;padding:0 12px;border:1px solid #d8d3cf;border-radius:13px;background:white;font:600 16px Arial;color:#4b4642;cursor:pointer">📋 Copy results</button><script>(()=>{{const text={payload};const b=document.getElementById('copy-results-native');b.addEventListener('click',async()=>{{const original=b.textContent;try{{await navigator.clipboard.writeText(text);b.textContent='✓ Copied';setTimeout(()=>b.textContent=original,1200);return}}catch(e){{}}const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{{document.execCommand('copy');b.textContent='✓ Copied';setTimeout(()=>b.textContent=original,1200)}}catch(e{{}}){{}}ta.remove()}})}})();</script>""", unsafe_allow_javascript=True)'''
# Use a safer minimal replacement if the exact JS differs.
if 'id="copy-msg"' in s:
    s = s.replace('<div id="copy-msg" style="font:12px Arial;color:#55745d;margin-top:4px;min-height:14px"></div>', '', 1)
    s = s.replace('padding:9px 12px;border:1px solid #d8d3cf;border-radius:9px', 'height:48px;padding:0 12px;border:1px solid #d8d3cf;border-radius:13px', 1)
# Center the expander label visually with its chevron through the app CSS above.
p.write_text(s, encoding='utf-8')
print('STUDY_AND_SAVE_CONTROLS_ALIGNED')
