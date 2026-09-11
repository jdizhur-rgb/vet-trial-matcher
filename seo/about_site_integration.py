#!/usr/bin/env python3
"""Integrate the About story into the shared static site."""
from pathlib import Path
import shutil
from site_config import SITE

ABOUT_CSS = '''
.about-story{max-width:850px;margin:0 auto;font-size:1.02rem;line-height:1.72}.about-story h1{margin-bottom:26px}.about-story p{margin:0 0 19px}.story-photo{width:min(310px,42%);margin:4px 0 20px}.story-photo-right{float:right;margin-left:28px}.story-photo-left{float:left;margin-right:28px}.story-photo img{display:block;width:100%;height:auto;border-radius:16px;border:1px solid #d9e2ea}.story-photo span{display:block;text-align:center;color:#607086;font-size:.9rem;margin-top:6px}.story-close{clear:both;padding:20px 22px;background:#edf4f8;border-radius:14px;margin-top:28px!important}.founder-signoff{display:flex;align-items:center;gap:14px;margin-top:22px}.founder-signoff img{width:130px;height:130px;object-fit:cover;border-radius:14px;border:1px solid #d9e2ea}.founder-signoff strong,.founder-signoff span{display:block}.founder-signoff span{color:#607086;font-size:.92rem;margin-top:2px}@media(max-width:650px){.about-story{font-size:1rem;line-height:1.58}.about-story h1{font-size:2rem;line-height:1.1;margin-bottom:18px}.about-story p{margin-bottom:15px}.story-photo,.story-photo-right,.story-photo-left{float:none;width:55%;max-width:210px;margin:12px auto 18px}.story-photo span{font-size:.82rem;margin-top:4px}.story-close{padding:15px 16px;margin-top:20px!important}.founder-signoff{gap:12px;margin-top:18px}.founder-signoff img{width:96px;height:96px}}
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
