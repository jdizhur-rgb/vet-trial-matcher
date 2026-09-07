from pathlib import Path
p=Path('pages/1_Clinical_Trial_Finder.py')
s=p.read_text(encoding='utf-8')
anchor="CURRENT_STATUS_CONFIDENCE = {'current', 'confirmed_current'}\ndef is_current_trial(tr):"
helper="""CURRENT_STATUS_CONFIDENCE = {'current', 'confirmed_current'}

def species_matches(trial_species, selected_species):
    \"\"\"Normalize legacy string and newer list species fields.\"\"\"
    if isinstance(trial_species, (list, tuple, set)):
        values = {str(x).strip() for x in trial_species}
    else:
        values = {x.strip() for x in str(trial_species or '').split('/') if x.strip()}
    return selected_species in values

def is_current_trial(tr):"""
if anchor not in s:
    raise SystemExit('anchor not found')
s=s.replace(anchor,helper,1)
old="species not in str(_tr.get('species', '')).split('/')"
count=s.count(old)
if count != 1:
    raise SystemExit(f'expected 1 form species filter, found {count}')
s=s.replace(old,"not species_matches(_tr.get('species', ''), species)")
old2="species not in str(tr.get('species', '')).split('/')"
count2=s.count(old2)
if count2 != 1:
    raise SystemExit(f'expected 1 result species filter, found {count2}')
s=s.replace(old2,"not species_matches(tr.get('species', ''), species)")
p.write_text(s,encoding='utf-8')
print('patched species normalization')
