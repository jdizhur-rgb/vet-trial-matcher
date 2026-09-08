from pathlib import Path
p=Path('pages/1_Clinical_Trial_Finder.py')
s=p.read_text(encoding='utf-8')
s=s.replace("with st.expander('Help us improve this beta'):", "with st.expander('Help us improve this finder'):")
s=s.replace("st.caption('Beta: trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research team.')", "st.caption('Trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research or treatment team.')")
s=s.replace('st.caption("This finder identifies potentially relevant clinical trials; it does not determine eligibility. Final eligibility is determined by the study investigators. It is not a substitute for veterinary advice.")', 'st.caption("This finder identifies potentially relevant cancer treatment options. It does not determine eligibility. Final eligibility and treatment decisions are determined by the treating or research team. It is not a substitute for veterinary advice.")')
p.write_text(s, encoding='utf-8')
