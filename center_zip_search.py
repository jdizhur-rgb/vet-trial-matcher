#!/usr/bin/env python3
"""Upgrade the static oncology-center directory with real US ZIP search."""
from pathlib import Path
import html
import re


PAGE = Path(__file__).resolve().parent / "seo" / "site" / "centers" / "index.html"


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    aliases = 0
    old_input = (
        '<input class="catalog-search" type="search" '
        'placeholder="Search hospital, city or state" '
        'aria-label="Search oncology centers" oninput="filterCenters(this.value)">'
    )
    # The current owner-friendly center generator intentionally emits a plain
    # crawlable list. Turn that list into the visual/search directory here,
    # while retaining the same links and opportunity counts.
    if old_input not in text:
        items = re.findall(
            r'<li><a href="([^"]+)">(.*?)</a> — (\d+) current opportunities</li>',
            text,
            flags=re.S,
        )
        if not items:
            raise AssertionError("Center directory links not found")
        current_slugs = {url.rstrip("/").split("/")[-1] for url, _, _ in items}

        # Keep previously published full-name center URLs working when the
        # current generator chooses a shorter canonical slug.
        for url, name, _ in items:
            current_slug = url.rstrip("/").split("/")[-1]
            legacy_slug = re.sub(
                r"[^a-z0-9]+", "-", html.unescape(name).lower()
            ).strip("-")
            if not legacy_slug or legacy_slug == current_slug or legacy_slug in current_slugs:
                continue
            current_page = PAGE.parent / current_slug / "index.html"
            alias_page = PAGE.parent / legacy_slug / "index.html"
            if not current_page.exists():
                continue
            alias_text = current_page.read_text(encoding="utf-8")
            if 'name="robots"' not in alias_text:
                alias_text = alias_text.replace(
                    "</head>", '<meta name="robots" content="noindex, follow"></head>', 1
                )
            alias_page.parent.mkdir(parents=True, exist_ok=True)
            alias_page.write_text(alias_text, encoding="utf-8")
            aliases += 1

        def page_source(url: str) -> str:
            slug = url.rstrip("/").split("/")[-1]
            page = PAGE.parent / slug / "index.html"
            return page.read_text(encoding="utf-8") if page.exists() else ""

        def first_location(url: str, name: str) -> str:
            if name == "Ethos Veterinary Health / Ethos Discovery":
                return "Multiple locations, including Port City Veterinary Referral Hospital, Portsmouth, NH"
            source = page_source(url)
            match = re.search(
                r'<div class="study-locations">.*?<li>(.*?)</li>', source, flags=re.S
            )
            if not match:
                return ""
            return " ".join(
                html.unescape(re.sub(r"<.*?>", "", match.group(1))).split()
            )

        def location_zips(url: str, name: str) -> list[str]:
            source = page_source(url)
            found = re.findall(
                r"\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+(\d{5})(?:-\d{4})?\b",
                source,
            )
            if name == "Ethos Veterinary Health / Ethos Discovery":
                found.append("03801")
            return list(dict.fromkeys(found))

        def location_states(url: str) -> list[str]:
            source = page_source(url)
            return list(dict.fromkeys(re.findall(
                r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+\d{5}\b",
                source,
            )))

        cards_html = "".join(
            f'<a class="directory-card" href="{url}" data-zips="{",".join(location_zips(url,name))}" data-states="{",".join(location_states(url))}"><strong>{name}</strong>'
            f'<span>{count} current {"opportunity" if count == "1" else "opportunities"}'
            f'{" · " + html.escape(first_location(url,name)) if first_location(url,name) else ""}</span></a>'
            for url, name, count in items
        )
        rebuilt = (
            '<main><h1>Veterinary Oncology Centers</h1>'
            '<p class="lead catalog-intro"><strong>Find hospitals and research centers that may have options beyond your local clinic.</strong> '
            'This directory includes universities, teaching hospitals, specialty oncology hospitals and other research programs with current cancer treatment opportunities. '
            'Search by hospital, city or state.</p>'
            + old_input
            + '<div class="directory-grid">' + cards_html + '</div>'
            + '<script>function filterCenters(q){q=q.toLowerCase().trim();document.querySelectorAll(".directory-card").forEach(function(x){x.style.display=!q||x.textContent.toLowerCase().includes(q)?"":"none";});}</script></main>'
        )
        text, replaced = re.subn(r'<main>.*?</main>', rebuilt, text, count=1, flags=re.S)
        if replaced != 1:
            raise AssertionError("Center directory main block not found")
    cards = 0

    def add_zip(match: re.Match[str]) -> str:
        nonlocal cards
        tag, body = match.group(1), match.group(2)
        # Only attach coordinates to US addresses. Five-digit postal codes also
        # exist in Europe and must not be mistaken for US ZIP codes.
        if 'data-zips=' in tag:
            cards += 1
            return f'{tag}>{body}</a>'
        zips = re.findall(
            r"\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+(\d{5})(?:-\d{4})?\b",
            body,
        )
        cards += 1
        return f'{tag} data-zips="{",".join(dict.fromkeys(zips))}">{body}</a>'

    text = re.sub(
        r'(<a class="directory-card"[^>]*)>(.*?)</a>', add_zip, text, flags=re.S
    )
    new_input = (
        '<input class="catalog-search" type="search" inputmode="search" '
        'placeholder="ZIP code, hospital, city or state" '
        'aria-label="Search oncology centers by ZIP code, hospital, city or state" '
        'oninput="filterCenters(this.value)">'
        '<p id="center-search-status" class="center-search-status" aria-live="polite"></p>'
    )
    if old_input not in text:
        raise AssertionError("Center search input shape changed")
    text = text.replace(old_input, new_input, 1)
    text = text.replace(
        'Search by hospital, city or state.',
        'Enter a US ZIP code to see the nearest listed centers, or search by hospital, city or state.',
        1,
    )
    old_script = '<script>function filterCenters(q){q=q.toLowerCase().trim();document.querySelectorAll(".directory-card").forEach(function(x){x.style.display=!q||x.textContent.toLowerCase().includes(q)?"":"none";});}</script>'
    new_script = r'''<script>
const centerGrid=document.querySelector('.directory-grid');
const centerCards=Array.from(document.querySelectorAll('.directory-card'));
const centerOrder=new Map(centerCards.map((card,index)=>[card,index]));
const zipCache=new Map();
let centerSearchSequence=0;
function radians(value){return value*Math.PI/180;}
function milesBetween(a,b){
  const dLat=radians(b.lat-a.lat),dLon=radians(b.lon-a.lon);
  const h=Math.sin(dLat/2)**2+Math.cos(radians(a.lat))*Math.cos(radians(b.lat))*Math.sin(dLon/2)**2;
  return 3958.8*2*Math.asin(Math.sqrt(h));
}
async function zipPoint(zip){
  if(zipCache.has(zip))return zipCache.get(zip);
  const request=fetch('https://api.zippopotam.us/us/'+encodeURIComponent(zip))
    .then(response=>{if(!response.ok)throw new Error('ZIP not found');return response.json();})
    .then(data=>({lat:Number(data.places[0].latitude),lon:Number(data.places[0].longitude),place:data.places[0]['place name'],state:data.places[0]['state abbreviation']}));
  zipCache.set(zip,request);return request;
}
function clearDistance(card){const old=card.querySelector('.center-distance');if(old)old.remove();}
function restoreCenters(){
  centerCards.sort((a,b)=>centerOrder.get(a)-centerOrder.get(b)).forEach(card=>{card.style.display='';clearDistance(card);centerGrid.appendChild(card);});
}
async function searchByZip(zip,sequence){
  const status=document.getElementById('center-search-status');
  status.textContent='Finding the nearest listed centers…';
  try{
    const origin=await zipPoint(zip);
    const located=centerCards.filter(card=>card.dataset.zips);
    const points=await Promise.all(located.map(async card=>{
      const candidates=await Promise.all(card.dataset.zips.split(',').filter(Boolean).map(async zip=>({zip,point:await zipPoint(zip)})));
      const nearest=candidates.map(x=>({...x,miles:milesBetween(origin,x.point)})).sort((a,b)=>a.miles-b.miles)[0];
      return {card,nearest};
    }));
    if(sequence!==centerSearchSequence)return;
    centerCards.forEach(card=>{card.style.display='none';clearDistance(card);});
    points.map(item=>({card:item.card,miles:item.nearest.miles,nearestZip:item.nearest.zip}))
      .sort((a,b)=>a.miles-b.miles).forEach(item=>{
        item.card.style.display='';
        const label=document.createElement('span');label.className='center-distance';
        const nearestName=item.nearestZip==='03801'?'Port City Veterinary Referral Hospital · ':'';
        label.textContent=nearestName+Math.round(item.miles)+' miles from '+zip;
        item.card.appendChild(label);centerGrid.appendChild(item.card);
      });
    status.textContent='Centers with US locations, nearest to '+origin.place+', '+origin.state+'. Distances are approximate.';
  }catch(error){
    if(sequence!==centerSearchSequence)return;
    restoreCenters();status.textContent='We could not locate that ZIP code. Check the five digits or search by city, state or hospital name.';
  }
}
const stateNames={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'};
const stateCodes=new Set(Object.values(stateNames));
function filterCenters(value){
  const sequence=++centerSearchSequence,q=value.toLowerCase().trim();
  const status=document.getElementById('center-search-status');
  if(/^\d{5}$/.test(q)){searchByZip(q,sequence);return;}
  restoreCenters();
  if(!q){status.textContent='';return;}
  const requestedState=stateNames[q]||(q.length===2&&stateCodes.has(q.toUpperCase())?q.toUpperCase():'');
  let count=0;
  centerCards.forEach(card=>{
    const states=(card.dataset.states||'').split(',');
    const show=requestedState?states.includes(requestedState):card.textContent.toLowerCase().includes(q);
    card.style.display=show?'':'none';if(show)count++;
  });
  status.textContent=count?count+' matching '+(count===1?'center':'centers')+'.':'No listed centers match that search.';
}
</script>'''
    if old_script not in text:
        raise AssertionError("Legacy center filter script not found")
    text = text.replace(old_script, new_script, 1)
    text = text.replace(
        '</style>',
        '.center-search-status{min-height:1.5em;margin:-8px 0 18px;color:#52677b;font-size:.92rem}.center-distance{color:#246b48!important;font-weight:700!important}</style>',
        1,
    )
    PAGE.write_text(text, encoding="utf-8")
    print(f"CENTER_ZIP_SEARCH_OK cards={cards} legacy_aliases={aliases}")


if __name__ == "__main__":
    main()
