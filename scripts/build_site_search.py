#!/usr/bin/env python3
"""Build a local, static search across public site pages."""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seo" / "site"
sys.path.insert(0, str(ROOT / "seo"))
import generate_seo as g  # noqa: E402
import site_shell  # noqa: E402


class MainText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.skip = 0
        self.heading = 0
        self.title: list[str] = []
        self.content: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.inside = True
        elif self.inside and tag in {"script", "style", "nav"}:
            self.skip += 1
        elif self.inside and not self.skip and tag == "h1":
            self.heading += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "main":
            self.inside = False
        elif self.inside and tag in {"script", "style", "nav"} and self.skip:
            self.skip -= 1
        elif self.inside and tag == "h1" and self.heading:
            self.heading -= 1

    def handle_data(self, data: str) -> None:
        if self.inside and not self.skip:
            self.content.append(data)
            if self.heading:
                self.title.append(data)


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main() -> None:
    sitemap = ElementTree.parse(SITE / "sitemap.xml")
    entries: list[dict[str, str]] = []
    urls = sorted({node.text.strip() for node in sitemap.iter() if node.tag.endswith("loc") and node.text})
    for url in urls:
        if not url.startswith(site_shell.SITE + "/") or url.endswith("/search/"):
            continue
        relative = url.removeprefix(site_shell.SITE).strip("/")
        page = SITE / relative / "index.html" if relative else SITE / "index.html"
        if not page.exists():
            continue
        source = page.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="[^"]*noindex', source, re.I):
            continue
        parser = MainText()
        parser.feed(source)
        match = re.search(r'<meta name="description" content="([^"]*)"', source)
        title = compact(" ".join(parser.title)) or compact(re.search(r"<title>(.*?)</title>", source, re.S).group(1))
        body = compact(" ".join(parser.content))
        entries.append({"title": title, "url": url, "description": compact(match.group(1)) if match else "", "body": body[:5000]})
    if not any("UC Davis" in entry["title"] and "/centers/" in entry["url"] for entry in entries):
        raise AssertionError("UC Davis clinical trial center missing from site search")
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    body = '''<h1>Search the site</h1><p class="lead">Find clinical trials, trial centers, oncology care and articles by name or topic.</p>
<label for="site-query" class="search-label">Search the site</label><input id="site-query" class="catalog-search" type="search" placeholder="Try UC Davis, lymphoma or electrochemotherapy" autocomplete="off">
<p id="site-search-status" role="status" aria-live="polite">Enter a name or topic to search.</p><div id="site-search-results" class="site-search-results"></div>
<style>.search-label{display:block;font-weight:700;margin:22px 0 0}.site-search-results{max-width:860px}.site-search-result{border-top:1px solid #d9e2ea;padding:15px 0}.site-search-result h2{font-size:1.15rem;margin:0 0 5px}.site-search-result p{color:#42536a;margin:0}.site-search-result small{color:#607086}</style>
<script type="application/json" id="site-search-index">__INDEX__</script>
<script>(function(){
const rows=JSON.parse(document.getElementById('site-search-index').textContent);
const input=document.getElementById('site-query'),results=document.getElementById('site-search-results'),status=document.getElementById('site-search-status');
const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
const prepared=rows.map(row=>({...row,name:norm(row.title),descriptionNorm:norm(row.description),bodyNorm:norm(row.body)}));
function render(){const words=norm(input.value).split(' ').filter(Boolean);results.replaceChildren();if(!words.length){status.textContent='Enter a name or topic to search.';return;}
const matches=prepared.map(row=>{const all=row.name+' '+row.descriptionNorm+' '+row.bodyNorm;if(!words.every(word=>all.includes(word)))return null;let score=0;for(const word of words){if(row.name.includes(word))score+=12;if(row.descriptionNorm.includes(word))score+=4;if(row.bodyNorm.includes(word))score+=1;}if(row.name.includes(words.join(' ')))score+=25;return{row,score};}).filter(Boolean).sort((a,b)=>b.score-a.score||a.row.title.localeCompare(b.row.title));
status.textContent=matches.length?matches.length+' matching '+(matches.length===1?'page.':'pages.'):'No pages match that search.';
for(const {row} of matches.slice(0,30)){const item=document.createElement('article');item.className='site-search-result';const heading=document.createElement('h2'),link=document.createElement('a');link.href=row.url;link.textContent=row.title;heading.append(link);const summary=document.createElement('p');summary.textContent=row.description||row.body.slice(0,180);item.append(heading,summary);results.append(item);}
}
input.addEventListener('input',render);let stored='';try{stored=sessionStorage.getItem('siteSearchQuery')||'';sessionStorage.removeItem('siteSearchQuery')}catch{}const initial=stored||new URLSearchParams(location.search).get('q');if(initial){input.value=initial;render();}
})();</script>'''.replace("__INDEX__", payload)
    target = SITE / "search"
    target.mkdir(exist_ok=True)
    page = g.page("Search the site | Vet Trial Finder", "Search clinical trials, trial centers, oncology care and articles on Vet Trial Finder.", body, site_shell.SITE + "/search/")
    (target / "index.html").write_text(site_shell.wrap_html(page), encoding="utf-8")
    site_shell.add_to_sitemap(SITE, [site_shell.SITE + "/search/"])
    print(f"SITE_SEARCH_OK pages={len(entries)}")


if __name__ == "__main__":
    main()
