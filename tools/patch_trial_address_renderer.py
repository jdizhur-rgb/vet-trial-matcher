from pathlib import Path

p = Path('pages/1_Clinical_Trial_Finder.py')
text = p.read_text(encoding='utf-8')

old_import = "import streamlit.components.v1 as components\n"
new_import = old_import + "from seo.trial_site_directory import active_trial_addresses\n"
if new_import not in text:
    if old_import not in text:
        raise SystemExit('import anchor not found')
    text = text.replace(old_import, new_import, 1)

old_pdf = '''        if tr.get("sites"):\n            lines.append("Participating sites: " + "; ".join(f"{x['hospital']} — {x['city']}, {x['state']}" for x in tr["sites"]))\n'''
new_pdf = '''        if tr.get("sites"):\n            lines.append("Participating sites: " + "; ".join(str(x.get('name') or x.get('hospital') or x.get('label') or '').strip() for x in tr["sites"] if str(x.get('name') or x.get('hospital') or x.get('label') or '').strip()))\n        _addresses = active_trial_addresses(tr)\n        if _addresses:\n            lines.append("Address: " + "; ".join(_addresses))\n'''
if new_pdf not in text:
    if old_pdf not in text:
        raise SystemExit('pdf anchor not found')
    text = text.replace(old_pdf, new_pdf, 1)

old_card = '''                if tr.get('sites'):\n                    site_text = '; '.join(\n                        f"{x['hospital']} — {x['city']}, {x['state']}" for x in tr['sites']\n                    )\n                    st.write('**Participating sites:** ' + site_text)\n'''
new_card = '''                if tr.get('sites'):\n                    site_text = '; '.join(\n                        str(x.get('name') or x.get('hospital') or x.get('label') or '').strip()\n                        for x in tr['sites']\n                        if str(x.get('name') or x.get('hospital') or x.get('label') or '').strip()\n                    )\n                    if site_text:\n                        st.write('**Participating sites:** ' + site_text)\n                _addresses = active_trial_addresses(tr)\n                if _addresses:\n                    st.write('**Address:** ' + '; '.join(_addresses))\n'''
if new_card not in text:
    if old_card not in text:
        raise SystemExit('card anchor not found')
    text = text.replace(old_card, new_card, 1)

p.write_text(text, encoding='utf-8')
print('PATCHED', p)
