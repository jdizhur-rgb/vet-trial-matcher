from pathlib import Path

# Top navigation: rename the old catch-all button and use a treatment icon.
p=Path('app.py')
s=p.read_text(encoding='utf-8')
s=s.replace('title="Additional Oncology Options",icon="🧬"','title="More Treatment Options",icon="💊"')
s=s.replace('st.button("🧬 Other Options",key="nav_options"','st.button("💊 More Treatment Options",key="nav_options"')
p.write_text(s,encoding='utf-8')

# Additional-options landing page: make the three treatment routes explicit.
p=Path('pages/2_Additional_Oncology_Options.py')
s=p.read_text(encoding='utf-8')
s=s.replace("<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>🧬 Other Options</div>","<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>💊 More Treatment Options</div>")
s=s.replace('st.write("A short list of non-routine treatment options with current access and enough evidence or clinical relevance to be worth discussing with a veterinary oncologist.")','st.write("Explore treatment access beyond standard clinical trials.")\n\nroute=st.radio("Choose an option",["⚡ Electrochemotherapy (ECT)","🧬 Advanced / Novel Treatments","🧪 Compassionate / Expanded Access"],horizontal=True,label_visibility="collapsed",key="treatment_option_route")')
# Existing ECT finder only opens on the ECT route; existing option matcher is the Advanced route.
s=s.replace('with st.expander("⚡ Find ECT Centers near you"):', 'if route=="⚡ Electrochemotherapy (ECT)":\n with st.expander("⚡ Find ECT Centers near you",expanded=True):')
# Indent the existing ECT expander body until the next top-level expander.
start=s.index('if route=="⚡ Electrochemotherapy (ECT)":')
end=s.index('\nwith st.expander("How options qualify"):',start)
block=s[start:end]
lines=block.splitlines()
# first two lines already have correct nesting; body after `with` needs one additional space relative to original.
for i in range(2,len(lines)):
    lines[i]=' '+lines[i]
s=s[:start]+'\n'.join(lines)+s[end:]
# Gate the advanced-treatment form; compassionate route gets a clear dedicated landing state for the access catalog being populated.
marker='\nwith st.expander("How options qualify"):'
idx=s.index(marker)
tail=s[idx+1:]
# Keep qualifying explainer + existing form under advanced route by indenting the remainder.
indented='\n'.join(' '+ln if ln else ln for ln in tail.splitlines())
comp='''\nelif route=="🧪 Compassionate / Expanded Access":\n st.subheader("Compassionate / Expanded Access")\n st.write("Investigational anticancer treatments that may be available outside a conventional recruiting clinical trial. Availability is verified program by program; contact and eligibility details are shown only when there is a real current access pathway.")\n st.info("Verified compassionate and special-access programs are being added here separately from clinical trials so they are not confused with ordinary trial enrollment.")\nelse:\n'''
s=s[:idx]+comp+indented
p.write_text(s,encoding='utf-8')
print('Updated treatment-options navigation')
