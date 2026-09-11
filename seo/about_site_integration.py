#!/usr/bin/env python3
"""Integrate the About story into the shared static site."""
from pathlib import Path
import shutil
from site_config import SITE

MOBILE_CSS = '''
@media(max-width:650px){
.site-header{position:static;margin:0 -15px 14px;padding:0 15px}.site-nav{display:block;min-height:0;padding:10px 0}.brand{display:block;font-size:1rem;margin-bottom:7px}.site-nav nav{justify-content:flex-start;gap:7px 12px;margin-top:0}.site-nav nav a{font-size:.82rem;line-height:1.25}
.home-hero{display:grid;grid-template-columns:minmax(0,1fr) 116px;grid-template-areas:"eyebrow eyebrow" "title title" "lead lead" "actions pets";gap:10px 14px;padding:16px 0 12px;align-items:end}.home-hero>div:first-child{display:contents}.home-hero .eyebrow{grid-area:eyebrow;font-size:.84rem;line-height:1.3;margin:0}.home-hero h1{grid-area:title;font-size:1.72rem;line-height:1.08;margin:0}.home-hero .lead{grid-area:lead;font-size:.96rem;line-height:1.45;margin:0}.hero-actions{grid-area:actions;gap:8px;margin:4px 0 0;align-self:center}.hero-actions .cta,.secondary-cta{padding:9px 12px;font-size:.9rem}.pet-panel{grid-area:pets;display:grid;grid-template-columns:1fr 1fr;gap:6px;max-width:none;width:116px;align-self:center}.pet-tile{min-height:54px;border-radius:11px}.pet-tile span{font-size:2rem}
main>h1{font-size:2rem;line-height:1.08}.lead{font-size:1rem;line-height:1.5}.site-grid{grid-template-columns:1fr;gap:10px;margin:12px 0 24px}.site-card{padding:14px 16px;border-radius:12px}.site-card h3{font-size:1.05rem;margin-bottom:5px}.site-card p{font-size:.92rem;line-height:1.45}.how{grid-template-columns:1fr;gap:9px}.how div{padding:13px 15px}.how strong{font-size:.95rem}.how span{font-size:.9rem;line-height:1.45}.site-footer{margin-top:30px;padding-top:18px}.section-index{columns:1}
}
'''

ABOUT_CSS = '''
.about-story{max-width:850px;margin:0 auto;font-size:1.02rem;line-height:1.72}.about-story h1{margin-bottom:26px}.about-story p{margin:0 0 19px}.story-photo{width:min(310px,42%);margin:4px 0 20px}.story-photo-right{float:right;margin-left:28px}.story-photo-left{float:left;margin-right:28px}.story-photo img{display:block;width:100%;height:auto;border-radius:16px;border:1px solid #d9e2ea}.story-photo span{display:block;text-align:center;color:#607086;font-size:.9rem;margin-top:6px}.story-close{clear:both;padding:20px 22px;background:#edf4f8;border-radius:14px;margin-top:28px!important}.founder-signoff{display:flex;align-items:center;gap:14px;margin-top:22px}.founder-signoff img{width:130px;height:130px;object-fit:cover;border-radius:14px;border:1px solid #d9e2ea}.founder-signoff strong,.founder-signoff span{display:block}.founder-signoff span{color:#607086;font-size:.92rem;margin-top:2px}@media(max-width:650px){.about-story{font-size:1rem;line-height:1.55}.about-story h1{font-size:1.65rem;line-height:1.08;margin-bottom:14px}.about-story p{margin-bottom:12px}.story-photo,.story-photo-right,.story-photo-left{float:none;width:48%;max-width:180px;margin:8px auto 14px}.story-photo span{font-size:.78rem;margin-top:3px}.story-close{padding:13px 14px;margin-top:16px!important}.founder-signoff{gap:10px;margin-top:15px}.founder-signoff img{width:82px;height:82px}.founder-signoff span{font-size:.84rem}}
'''


def integrate_about(root: Path) -> None:
    assets = root / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / 'assets'
    for name in ('senya-about.jpg', 'yasha-about.jpg', 'yuliia-senya-about.jpg'):
        if (source / name).exists():
            shutil.copy2(source / name, assets / name)

    for page in root.rglob('index.html'):
        text = page.read_text(encoding='utf-8')
        if f'{SITE}/about/' not in text:
            text = text.replace(f'<a href="{SITE}/help/">Help</a>', f'<a href="{SITE}/about/">About</a><a href="{SITE}/help/">Help</a>', 1)
        text = text.replace('</style>', MOBILE_CSS + '</style>', 1)
        if page.parent.name == 'about':
            text = text.replace('</style>', ABOUT_CSS + '</style>', 1)
        page.write_text(text, encoding='utf-8')

    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        text = sitemap.read_text(encoding='utf-8')
        url = f'{SITE}/about/'
        if url not in text:
            text = text.replace('</urlset>', f'<url><loc>{url}</loc></url>\n</urlset>')
            sitemap.write_text(text, encoding='utf-8')
    print('ABOUT_PAGE_OK')
