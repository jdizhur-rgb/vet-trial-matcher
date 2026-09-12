from pathlib import Path

path = Path('pages/1_Clinical_Trial_Finder.py')
text = path.read_text(encoding='utf-8')
text = text.replace(
    'from seo.trial_site_directory import active_trial_addresses\n',
    'from seo.trial_site_directory import active_trial_addresses, trial_site_records\n',
    1,
)
old = '''                if tr.get('sites'):\n                    site_text = '; '.join(\n                        str(x.get('name') or x.get('hospital') or x.get('label') or '').strip()\n                        for x in tr['sites']\n                        if str(x.get('name') or x.get('hospital') or x.get('label') or '').strip()\n                    )\n                    if site_text:\n                        st.write('**Participating sites:** ' + site_text)\n                _addresses = active_trial_addresses(tr)\n                if _addresses:\n                    st.write('**Address:** ' + '; '.join(_addresses))\n'''
new = '''                _location_rows = []\n                for _rec in trial_site_records(tr):\n                    if _rec.get('status') != 'active':\n                        continue\n                    _site_name = str(_rec.get('site_name') or '').strip()\n                    _site_addresses = [str(x).strip() for x in _rec.get('addresses', []) if str(x).strip()]\n                    if _site_addresses:\n                        for _address in _site_addresses:\n                            _row = _address\n                            if _site_name and _site_name.lower() not in _address.lower():\n                                _row = f'{_site_name} — {_address}'\n                            if _row not in _location_rows:\n                                _location_rows.append(_row)\n                    elif _site_name and _site_name not in _location_rows:\n                        _location_rows.append(_site_name)\n                if _location_rows:\n                    st.write('**Location:** ' + '; '.join(_location_rows))\n'''
if old not in text:
    raise SystemExit('target card location block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print('PATCHED', path)
