from pathlib import Path

p = Path('pages/1_Clinical_Trial_Finder.py')
s = p.read_text(encoding='utf-8')
s = s.replace("st.set_page_config(page_title='Vet Cancer Trial Finder — Beta', page_icon='🐾', layout='centered')", "st.set_page_config(page_title='Vet Cancer Treatment Finder', page_icon='🐾', layout='centered')")
s = s.replace("st.markdown('**Beta prototype.** Answer what you know. It is completely fine to choose **I don’t know**.')", "st.markdown('Answer what you know. It is completely fine to choose **I don’t know**.')")
s = s.replace("st.info('This tool screens for clinical trials that may be worth contacting. It does not determine eligibility and does not replace your veterinarian or oncologist.')", "st.info('This finder identifies potentially relevant cancer treatment options. It does not determine eligibility. Final eligibility and treatment decisions are determined by the treating or research team. It is not a substitute for veterinary advice.')")
s = s.replace('Trial information can change. ', '')
p.write_text(s, encoding='utf-8')

p = Path('app.py')
s = p.read_text(encoding='utf-8')
s = s.replace('.beta-corner{text-align:right;font-size:.72rem;color:#8a8580;margin:.05rem .15rem .15rem}', '.beta-corner{display:none}')
s = s.replace('if body.startswith("**Beta prototype.**"):\n            rest=body.replace("**Beta prototype.**","",1).strip();_orig["markdown"](\'<div class="beta-corner">Beta prototype</div>\',unsafe_allow_html=True);_orig["markdown"](f\'<div class="intro-answer">{rest}</div>\',unsafe_allow_html=True);return', 'if body.startswith("Answer what you know."):\n            _orig["markdown"](f\'<div class="intro-answer">{body}</div>\',unsafe_allow_html=True);return')
s = s.replace('Trial information can change. ', '')
p.write_text(s, encoding='utf-8')
