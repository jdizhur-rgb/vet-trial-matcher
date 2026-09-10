from pathlib import Path

p = Path('app.py')
s = p.read_text(encoding='utf-8')
old = '''            _orig["markdown"](f'<div style="font-size:1.03rem;line-height:1.16;font-weight:700;color:#2f6f73;margin:.04rem 0 .18rem">{center}</div>',unsafe_allow_html=True);return
'''
new = '''            _orig["markdown"](f'<div style="font-size:1.03rem;line-height:1.16;font-weight:700;color:#2f6f73;margin:.04rem 0 .18rem">{center}</div>',unsafe_allow_html=True)
            try:
                from seo.center_directory import addresses_for as _addresses_for
                _addresses = _addresses_for(center)
            except Exception:
                _addresses = []
            for _address in _addresses:
                _orig["markdown"](f"📍 {_address}")
            return
'''
if 'from seo.center_directory import addresses_for as _addresses_for' in s:
    raise SystemExit('Address renderer already exists; refusing duplicate patch')
if old not in s:
    raise SystemExit('Expected center renderer not found; refusing unsafe patch')
s = s.replace(old, new, 1)
for label in ('🐾︎ Clinical Trials', '🏥 Oncology Centers', '🧬 Advanced Treatments', '🧪 Expanded Access'):
    if label not in s:
        raise SystemExit(f'Navigation guard failed: {label}')
p.write_text(s, encoding='utf-8')
print('ADDRESS_RENDERER_RESTORED_NAVIGATION_PRESERVED')
