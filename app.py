from pathlib import Path

# Emergency-stable single-page entrypoint.
# Streamlit Cloud was corrupting the delta tree when the app shell rendered
# navigation elements and then executed a page through st.navigation/page.run.
# Run the finder directly so the frontend receives one stable element tree.

finder = Path(__file__).parent / "pages" / "_Clinical_Trial_Finder_legacy.py"
source = finder.read_text(encoding="utf-8")
source = source.replace("tr['notes']", "tr.get('notes', 'See the official study page for current study details.')")
source = source.replace("tr['status']", "tr.get('status', 'Status not recorded')")
source = source.replace("tr['center']", "tr.get('center', 'Study center')")
source = source.replace("tr['title']", "tr.get('title', 'Clinical study')")
exec(compile(source, str(finder), "exec"), globals(), globals())
