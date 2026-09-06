from pathlib import Path
p=Path('pages/2_Additional_Oncology_Options.py')
s=p.read_text(encoding='utf-8')
start=s.index('st.markdown("""<style>')
end=s.index('</style>""",unsafe_allow_html=True)',start)+len('</style>""",unsafe_allow_html=True)')
css='''st.markdown("""<style>
/* Route buttons: target Streamlit key classes so mobile stacking keeps distinct shades. */
.st-key-route_ect button {background-color:#e7f2fa !important;border-color:#bfd8e9 !important;color:#285b7a !important;}
.st-key-route_advanced button {background-color:#d6e9f6 !important;border-color:#a9cce3 !important;color:#245674 !important;}
.st-key-route_compassionate button {background-color:#c5dfef !important;border-color:#91bdd8 !important;color:#1f4f6c !important;}
.st-key-route_ect button,.st-key-route_advanced button,.st-key-route_compassionate button {border-radius:12px !important;min-height:3.25rem !important;font-weight:500 !important;}
.st-key-route_ect button:hover,.st-key-route_advanced button:hover,.st-key-route_compassionate button:hover {filter:brightness(.97);}
</style>""",unsafe_allow_html=True)'''
s=s[:start]+css+s[end:]
p.write_text(s,encoding='utf-8')
