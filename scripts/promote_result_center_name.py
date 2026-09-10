from pathlib import Path

path = Path('app.py')
text = path.read_text(encoding='utf-8')

old_css = '''/* Study information only: Streamlit 1.62 maps expander key to st-key-* class. */
div[class*="st-key-study-info-"] details summary{
  display:flex!important;align-items:center!important;justify-content:center!important;
  text-align:center!important;gap:.35rem!important;
}
div[class*="st-key-study-info-"] details summary > *{
  flex:0 0 auto!important;width:auto!important;max-width:max-content!important;
}
div[class*="st-key-study-info-"] details summary [data-testid="stMarkdownContainer"],
div[class*="st-key-study-info-"] details summary p{
  width:auto!important;text-align:center!important;margin:0!important;
}
'''
new_css = '''/* Study information only. Streamlit 1.62 DOM is:
   summary > StyledSummaryHeading(span) > [chevron, StyledSummaryLabelWrapper(div)].
   Center the heading contents and disable the label wrapper's default flex-grow:1/width:100%. */
[class*="st-key-study-info-"] [data-testid="stExpander"] details summary > span{
  display:flex!important;align-items:center!important;justify-content:center!important;
  width:100%!important;max-width:100%!important;gap:.5rem!important;
}
[class*="st-key-study-info-"] [data-testid="stExpander"] details summary > span > div{
  width:auto!important;max-width:max-content!important;flex-grow:0!important;flex-shrink:0!important;
}
[class*="st-key-study-info-"] [data-testid="stExpander"] details summary > span > div [data-testid="stMarkdownContainer"],
[class*="st-key-study-info-"] [data-testid="stExpander"] details summary > span > div p{
  width:auto!important;margin:0!important;text-align:center!important;
}
'''
if old_css not in text:
    raise SystemExit('Expected keyed Study information CSS block not found; app.py left unchanged')
text = text.replace(old_css, new_css, 1)
path.write_text(text, encoding='utf-8')
print('CENTERED_STUDY_INFORMATION_FROM_STREAMLIT_162_DOM')
