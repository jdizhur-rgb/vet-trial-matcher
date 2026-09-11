from pathlib import Path

# Stable single-page entrypoint for Streamlit Cloud.
# Running the finder directly avoids delta-tree corruption from rendering a
# shell and then executing a page through st.navigation/page.run.

_app_file = Path(__file__).resolve()
finder = _app_file.parent / "pages" / "_Clinical_Trial_Finder_legacy.py"
source = finder.read_text(encoding="utf-8")
source = source.replace("tr['notes']", "tr.get('notes', 'See the official study page for current study details.')")
source = source.replace("tr['status']", "tr.get('status', 'Status not recorded')")
source = source.replace("tr['center']", "tr.get('center', 'Study center')")
source = source.replace("tr['title']", "tr.get('title', 'Clinical study')")

_original_file = globals().get("__file__")
globals()["__file__"] = str(finder)
try:
    exec(compile(source, str(finder), "exec"), globals(), globals())
finally:
    if _original_file is not None:
        globals()["__file__"] = _original_file
