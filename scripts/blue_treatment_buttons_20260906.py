from pathlib import Path
p=Path('pages/2_Additional_Oncology_Options.py')
s=p.read_text(encoding='utf-8')
old='''div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {background:#f2f6f8;border:1px solid #d7e0e6;color:#334155;border-radius:12px;min-height:3.25rem;font-weight:500;}\ndiv[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {border-color:#9fb6c5;background:#eaf1f5;color:#243746;}'''
new='''div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(1) div[data-testid="stButton"] button {background:#eaf4fb;border:1px solid #c7ddeb;color:#315f7d;border-radius:12px;min-height:3.25rem;font-weight:500;}\ndiv[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button {background:#dcecf7;border:1px solid #b8d3e5;color:#285875;border-radius:12px;min-height:3.25rem;font-weight:500;}\ndiv[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] button {background:#cfe4f2;border:1px solid #a9cadf;color:#214f6d;border-radius:12px;min-height:3.25rem;font-weight:500;}\ndiv[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {filter:brightness(.97);border-color:#8fb8d1;}'''
if old not in s: raise SystemExit('style block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
