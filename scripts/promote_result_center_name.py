from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')

# Remove the failed post-render iframe approach. components.html runs in an iframe,
# so it is the wrong mechanism for styling Streamlit's parent DOM.
start = '# Center only the result-card "Study information" expander after Streamlit has rendered it.\n'
end = 'with _nav_top.container():\n'
if start in text:
    a = text.index(start)
    b = text.index(end, a)
    text = text[:a] + text[b:]

# Streamlit 1.62 supports `key=` on st.expander and exposes that key as a
# st-key-* CSS class. Tag only Study information expanders with unique keys.
old_layout = '_layout={"section":None,"slots":[],"extra":0,"treatment":False,"age_value":None,"weight_unit":None,"weight_value":None};_pending={"contact":None,"sites":None,"url":None};_selected_region={"value":None};_selected_cancer={"value":None};_deferred={"args":None,"kwargs":None}\n'
new_layout = '_layout={"section":None,"slots":[],"extra":0,"treatment":False,"age_value":None,"weight_unit":None,"weight_value":None};_pending={"contact":None,"sites":None,"url":None};_selected_region={"value":None};_selected_cancer={"value":None};_deferred={"args":None,"kwargs":None};_study_expander_seq={"n":0}\n'
if old_layout in text:
    text = text.replace(old_layout, new_layout, 1)
elif '_study_expander_seq={"n":0}' not in text:
    raise SystemExit('Layout state anchor not found; app.py left unchanged')

old_else = '''    else:\n        with _orig["expander"](label,*a,**k):yield\n'''
new_else = '''    else:\n        if label=="Study information":\n            _study_expander_seq["n"]+=1\n            k=dict(k);k["key"]=f"study-info-{_study_expander_seq['n']}"\n        with _orig["expander"](label,*a,**k):yield\n'''
if old_else in text:
    text = text.replace(old_else, new_else, 1)
elif 'k["key"]=f"study-info-' not in text:
    raise SystemExit('Expander wrapper anchor not found; app.py left unchanged')

# Add CSS scoped only to the Streamlit key class generated above.
css_anchor = '/* Copy/PDF pair only. Study-information centering is applied by exact label after render. */\n'
css_new = '''/* Study information only: Streamlit 1.62 maps expander key to st-key-* class. */\ndiv[class*="st-key-study-info-"] details summary{\n  display:flex!important;align-items:center!important;justify-content:center!important;\n  text-align:center!important;gap:.35rem!important;\n}\ndiv[class*="st-key-study-info-"] details summary > *{\n  flex:0 0 auto!important;width:auto!important;max-width:max-content!important;\n}\ndiv[class*="st-key-study-info-"] details summary [data-testid="stMarkdownContainer"],\ndiv[class*="st-key-study-info-"] details summary p{\n  width:auto!important;text-align:center!important;margin:0!important;\n}\n\n/* Copy/PDF pair only. */\n'''
if css_anchor in text:
    text = text.replace(css_anchor, css_new, 1)
elif 'st-key-study-info-' not in text:
    raise SystemExit('Controls CSS anchor not found; app.py left unchanged')

path.write_text(text, encoding='utf-8')
print('KEYED_STUDY_INFORMATION_CENTERING')
