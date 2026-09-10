from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old_css = '''/* Unified study/action controls. */
div[data-testid="stExpander"] details summary{justify-content:center!important;text-align:center!important;gap:.35rem!important}
div[data-testid="stExpander"] details summary p{text-align:center!important}
div[data-testid="stDownloadButton"] button{width:100%!important;min-height:3rem!important;font-size:1rem!important;font-weight:600!important;border-radius:.8rem!important}
@media(max-width:900px){div[data-testid="stHorizontalBlock"]{row-gap:.35rem!important}div[data-testid="stDownloadButton"]{margin-top:0!important;margin-bottom:0!important}}
'''
new_css = '''/* Result-card study controls + Copy/PDF pair only. Do not affect form/layout columns. */
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary{
  justify-content:center!important;text-align:center!important;gap:.35rem!important;
}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary p{
  text-align:center!important;
}
#copy-results-native{
  width:100%!important;height:48px!important;padding:0 12px!important;
  border:1px solid #d8d3cf!important;border-radius:.8rem!important;background:#fff!important;
  font-size:1rem!important;font-weight:600!important;color:#4b4642!important;
}
#copy-msg:empty{display:none!important}
#copy-msg:not(:empty){margin:.2rem 0 0!important;min-height:0!important}
div[data-testid="stHorizontalBlock"]:has(#copy-results-native) div[data-testid="stDownloadButton"] button{
  width:100%!important;height:48px!important;min-height:48px!important;
  font-size:1rem!important;font-weight:600!important;border-radius:.8rem!important;
}
@media(max-width:900px){
  div[data-testid="stHorizontalBlock"]:has(#copy-results-native){
    display:flex!important;flex-direction:column!important;gap:.45rem!important;
  }
  div[data-testid="stHorizontalBlock"]:has(#copy-results-native) > div[data-testid="stColumn"]{
    width:100%!important;min-width:100%!important;flex:1 1 auto!important;
  }
}
'''
if old_css in text:
    text = text.replace(old_css, new_css, 1)
elif '/* Result-card study controls + Copy/PDF pair only.' not in text:
    raise SystemExit('Expected existing study/save CSS block not found; app.py left unchanged')
path.write_text(text, encoding='utf-8')
print('SCOPED_STUDY_AND_SAVE_LAYOUT')
