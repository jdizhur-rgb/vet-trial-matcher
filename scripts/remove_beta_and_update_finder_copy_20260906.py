from pathlib import Path

root = Path(__file__).resolve().parents[1]
page = root / "pages" / "1_Clinical_Trial_Finder.py"
app = root / "app.py"

p = page.read_text(encoding="utf-8")
p = p.replace("page_title='Vet Cancer Trial Finder — Beta'", "page_title='Vet Cancer Trial Finder'")
p = p.replace("st.markdown('**Beta prototype.** Answer what you know. It is completely fine to choose **I don’t know**.')", "st.markdown('Answer what you know. It is completely fine to choose **I don’t know**.')")
p = p.replace("This tool screens for clinical trials that may be worth contacting. It does not determine eligibility and does not replace your veterinarian or oncologist.", "This finder identifies potentially relevant cancer treatment options. It does not determine eligibility and does not replace your veterinarian or oncologist.")
p = p.replace("Beta: trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research team.", "Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research or treatment team.")
p = p.replace("This finder identifies potentially relevant clinical trials; it does not determine eligibility. Final eligibility is determined by the study investigators. It is not a substitute for veterinary advice.", "This finder identifies potentially relevant cancer treatment options. It does not determine eligibility. Final eligibility and treatment decisions are determined by the treating or research team. It is not a substitute for veterinary advice.")
page.write_text(p, encoding="utf-8")

a = app.read_text(encoding="utf-8")
a = a.replace(".beta-corner{text-align:right;font-size:.72rem;color:#8a8580;margin:.05rem .15rem .15rem}", ".beta-corner{text-align:right;font-size:.72rem;color:#8a8580;margin:.05rem .15rem .15rem}")
a = a.replace('''        if body.startswith("**Beta prototype.**"):\n            rest=body.replace("**Beta prototype.**","",1).strip();_orig["markdown"]('<div class="beta-corner">Beta prototype</div>',unsafe_allow_html=True);_orig["markdown"](f'<div class="intro-answer">{rest}</div>',unsafe_allow_html=True);return''', '''        if body.startswith("Answer what you know."):\n            _orig["markdown"](f'<div class="intro-answer">{body}</div>',unsafe_allow_html=True);return''')
app.write_text(a, encoding="utf-8")

print("Removed beta labeling and updated finder/disclaimer copy.")
