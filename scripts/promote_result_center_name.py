from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')
old_css = '''/* Result-card study controls + Copy/PDF pair only. Do not affect form/layout columns. */
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary{
  display:flex!important;align-items:center!important;justify-content:center!important;
  text-align:center!important;gap:.35rem!important;
}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary > *{
  flex:0 0 auto!important;width:auto!important;max-width:max-content!important;
}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary [data-testid="stMarkdownContainer"],
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stExpander"] details summary p{
  width:auto!important;text-align:center!important;margin:0!important;
}
#copy-results-native{
  width:100%!important;height:48px!important;padding:0 12px!important;
  border:1px solid #d8d3cf!important;border-radius:.8rem!important;background:#fff!important;
  font-size:1rem!important;font-weight:600!important;color:#4b4642!important;
  text-align:center!important;
}
#copy-msg:empty{display:none!important}
#copy-msg:not(:empty){margin:.2rem 0 0!important;min-height:0!important}
div[data-testid="stHorizontalBlock"]:has(#copy-results-native) div[data-testid="stDownloadButton"] button{
  width:100%!important;height:48px!important;min-height:48px!important;padding:0 12px!important;
  border:1px solid #d8d3cf!important;border-radius:.8rem!important;background:#fff!important;
  color:#4b4642!important;justify-content:center!important;box-shadow:none!important;
}
div[data-testid="stHorizontalBlock"]:has(#copy-results-native) div[data-testid="stDownloadButton"] button p{
  margin:0!important;font-size:1rem!important;font-weight:600!important;color:#4b4642!important;
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
new_css = '''/* Copy/PDF pair only. Study-information centering is applied by exact label after render. */
#copy-results-native{
  width:100%!important;height:48px!important;padding:0 12px!important;
  border:1px solid #d8d3cf!important;border-radius:.8rem!important;background:#fff!important;
  font-size:1rem!important;font-weight:600!important;color:#4b4642!important;
  text-align:center!important;
}
#copy-msg:empty{display:none!important}
#copy-msg:not(:empty){margin:.2rem 0 0!important;min-height:0!important}
div[data-testid="stHorizontalBlock"]:has(#copy-results-native) div[data-testid="stDownloadButton"] button{
  width:100%!important;height:48px!important;min-height:48px!important;padding:0 12px!important;
  border:1px solid #d8d3cf!important;border-radius:.8rem!important;background:#fff!important;
  color:#4b4642!important;justify-content:center!important;box-shadow:none!important;
}
div[data-testid="stHorizontalBlock"]:has(#copy-results-native) div[data-testid="stDownloadButton"] button p{
  margin:0!important;font-size:1rem!important;font-weight:600!important;color:#4b4642!important;
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
if old_css not in text:
    raise SystemExit('Expected existing controls CSS block not found; app.py left unchanged')
text = text.replace(old_css, new_css, 1)

anchor = '''with _nav_top.container():\n'''
js = '''# Center only the result-card "Study information" expander after Streamlit has rendered it.\ncomponents.html("""<script>\n(()=>{\n  const d=window.parent.document;\n  const apply=()=>{\n    d.querySelectorAll('div[data-testid="stExpander"] summary').forEach(s=>{\n      if((s.innerText||'').trim()!=='Study information') return;\n      s.style.setProperty('display','flex','important');\n      s.style.setProperty('align-items','center','important');\n      s.style.setProperty('justify-content','center','important');\n      s.style.setProperty('gap','.35rem','important');\n      s.style.setProperty('text-align','center','important');\n      Array.from(s.children).forEach(c=>{\n        c.style.setProperty('flex','0 0 auto','important');\n        c.style.setProperty('width','auto','important');\n        c.style.setProperty('max-width','max-content','important');\n      });\n      s.querySelectorAll('[data-testid="stMarkdownContainer"],p').forEach(c=>{\n        c.style.setProperty('width','auto','important');\n        c.style.setProperty('margin','0','important');\n        c.style.setProperty('text-align','center','important');\n      });\n    });\n  };\n  apply();\n  const o=new MutationObserver(apply);\n  o.observe(d.body,{childList:true,subtree:true});\n  setTimeout(()=>o.disconnect(),5000);\n})();\n</script>""",height=0)\n\n'''
if 'Center only the result-card "Study information" expander' not in text:
    if anchor not in text:
        raise SystemExit('Post-render anchor not found; app.py left unchanged')
    text = text.replace(anchor, js + anchor, 1)

path.write_text(text, encoding='utf-8')
print('EXACT_STUDY_INFORMATION_CENTERING')
