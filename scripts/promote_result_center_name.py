from pathlib import Path

app_path = Path('app.py')
text = app_path.read_text(encoding='utf-8')

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
if old_css in text:
    text = text.replace(old_css, new_css, 1)
elif new_css not in text:
    raise SystemExit('Expected Study information CSS block not found; app.py left unchanged')
app_path.write_text(text, encoding='utf-8')

finder_path = Path('pages/1_Clinical_Trial_Finder.py')
finder = finder_path.read_text(encoding='utf-8')
old_footer = 'Verified treatment trials and experimental treatment programs • U.S. + Europe/UK • Last deep audit: September 5, 2026'
new_footer = 'Verified treatment trials and experimental treatment programs • U.S. + Europe/UK • Updated daily'
if old_footer in finder:
    finder = finder.replace(old_footer, new_footer, 1)
elif new_footer not in finder:
    raise SystemExit('Expected footer text not found; Finder left unchanged')
finder_path.write_text(finder, encoding='utf-8')
print('UPDATED_DAILY_FOOTER')
