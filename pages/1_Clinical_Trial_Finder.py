from pathlib import Path

_legacy = Path(__file__).with_name('_Clinical_Trial_Finder_legacy.py')
_source = _legacy.read_text(encoding='utf-8')
_source = _source.replace("tr['notes']", "tr.get('notes', 'See the official study page for current study details.')")
_source = _source.replace("tr['status']", "tr.get('status', 'Status not recorded')")
_source = _source.replace("tr['center']", "tr.get('center', 'Study center')")
_source = _source.replace("tr['title']", "tr.get('title', 'Clinical study')")
exec(compile(_source, str(_legacy), 'exec'), globals(), globals())
