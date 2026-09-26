#!/usr/bin/env python3
"""Add search to the grouped clinical-trial center directory."""
from pathlib import Path
import re

PAGE = Path(__file__).resolve().parent / "seo" / "site" / "centers" / "index.html"

def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    cards = 0
    def add_data(match: re.Match[str]) -> str:
        nonlocal cards
        tag, body = match.group(1), match.group(2)
        zips = re.findall(r"\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+(\d{5})(?:-\d{4})?\b", body)
        states = re.findall(r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+\d{5}\b", body)
        cards += 1
        return f'{tag} data-zips="{",".join(dict.fromkeys(zips))}" data-states="{",".join(dict.fromkeys(states))}">{body}</a>'
    text = re.sub(r'(<a class="center-directory-card"[^>]*)>(.*?)</a>', add_data, text, flags=re.S)
    if not cards:
        raise AssertionError("Grouped center directory cards not found")
    search = ('<div class="center-directory-search"><label for="center-search"><strong>Find a center in this directory</strong></label>'
        '<input id="center-search" class="catalog-search" type="search" inputmode="search" placeholder="Hospital, university, city or state" '
        'aria-label="Search clinical trial centers" oninput="filterCenters(this.value)"><p id="center-search-status" aria-live="polite"></p></div>')
    if '</nav>' not in text:
        raise AssertionError("Center directory navigation not found")
    text = text.replace('</nav>', '</nav>'+search, 1)
    script = r'''<script>
const centerCards=Array.from(document.querySelectorAll('.center-directory-card'));
const stateNames={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'};
const stateCodes=new Set(Object.values(stateNames));
function filterCenters(value){const q=value.toLowerCase().trim();const requestedState=stateNames[q]||(q.length===2&&stateCodes.has(q.toUpperCase())?q.toUpperCase():'');let count=0;centerCards.forEach(card=>{const states=(card.dataset.states||'').split(',');const show=!q||(requestedState?states.includes(requestedState):card.textContent.toLowerCase().includes(q));card.hidden=!show;if(show)count++;});document.querySelectorAll('.center-region').forEach(x=>{x.hidden=!x.querySelector('.center-directory-card:not([hidden])');});document.querySelectorAll('.center-directory-section').forEach(x=>{x.hidden=!x.querySelector('.center-directory-card:not([hidden])');});document.getElementById('center-search-status').textContent=q?(count?count+' matching '+(count===1?'center.':'centers.'):'No listed centers match that search.'):'';}
</script>'''
    text = text.replace('</main>', script+'</main>', 1)
    text = text.replace('</style>', '.center-directory-search{max-width:620px;margin:0 0 30px}.center-directory-search label{display:block;margin-bottom:7px}.center-directory-search input{width:100%;box-sizing:border-box}.center-directory-search p{min-height:1.4em;margin:6px 0 0;color:#607086;font-size:.9rem}.center-directory-card[hidden],.center-region[hidden],.center-directory-section[hidden]{display:none!important}</style>', 1)
    PAGE.write_text(text, encoding="utf-8")
    print(f"CENTER_DIRECTORY_SEARCH_OK cards={cards}")

if __name__ == "__main__":
    main()
