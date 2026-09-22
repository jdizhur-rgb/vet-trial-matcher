#!/usr/bin/env python3
"""Build the searchable veterinary oncology-center directory from one JSON file."""
from __future__ import annotations

import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "oncology_centers.json"
SOURCE = ROOT / "seo" / "static" / "matcher-preview" / "centers" / "index.html"
OUTPUTS = (
    (SOURCE, "https://vettrialfinder.com/matcher-preview/centers/"),
    (ROOT / "seo" / "site" / "matcher-preview" / "centers" / "index.html", "https://vettrialfinder.com/matcher-preview/centers/"),
    (ROOT / "seo" / "site" / "matcher" / "centers" / "index.html", "https://vettrialfinder.com/matcher/centers/"),
)

STATE_NAMES = {
    "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
    "CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho",
    "IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana",
    "ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota",
    "MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada",
    "NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina",
    "ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania",
    "RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas",
    "UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia",
    "WI":"Wisconsin","WY":"Wyoming","ON":"Ontario","QC":"Quebec",
    "DC":"District of Columbia","PR":"Puerto Rico",
}

FILTER_GROUPS = {
    "Medical oncology": {"Medical oncology"},
    "Local oncology care": {"Local oncology care"},
    "Chemotherapy": {"Chemotherapy", "Chemotherapy administration and monitoring"},
    "Radiation oncology": {
        "Radiation oncology", "Radiation consultation", "Radiation therapy",
        "SRT", "SBRT", "IMRT", "VMAT", "IGRT", "RapidArc",
        "Stereotactic radiation therapy",
    },
    "Cancer surgery": {"Surgery", "Surgical oncology"},
    "Electrochemotherapy": {"ECT", "Electrochemotherapy"},
    "Immunotherapy": {"Immunotherapy", "ELIAS ECI", "ONCEPT", "T-cell therapy"},
    "Targeted therapy": {"Targeted therapy"},
    "Interventional radiology": {"Interventional radiology"},
    "Clinical trials": {"Clinical trials"},
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value).split())


def card(center: dict) -> str:
    state_name = STATE_NAMES.get(center["region"], center["region"])
    search = normalized(" ".join((center["name"], center["street"], center["city"], center["region"], state_name, center["postal_code"], center["country"])))
    service_names = set(center["services"])
    filter_groups = [
        normalized(label)
        for label, aliases in FILTER_GROUPS.items()
        if service_names & aliases
    ]
    attrs = {
        "data-country": center["country"],
        "data-search": search,
        "data-services": "|".join(normalized(x) for x in center["services"]),
        "data-filters": "|".join(filter_groups),
        "data-lat": center["latitude"],
        "data-lon": center["longitude"],
    }
    attr_text = " ".join(f'{key}="{esc(value)}"' for key, value in attrs.items())
    street = f'{esc(center["street"])}<br>' if center.get("street") else ""
    phone = f'<p>☎️ {esc(center["phone"])}</p>' if center.get("phone") else ""
    availability = (
        f'<p><strong>Availability:</strong> {esc(center["availability_note"])}. Contact the hospital before making plans.</p>'
        if center.get("availability_note") else ""
    )
    tags = "".join(f"<span>{esc(x)}</span>" for x in center["services"])
    link_label = "ACVIM specialist listing →" if "vetspecialists.com/vet-detail" in center["website"] else "Official website →"
    return (
        f'<article class="p-card" {attr_text}><h2>{esc(center["name"])}</h2>'
        f'<p>{street}{esc(center["city"])}, {esc(center["region"])} {esc(center["postal_code"])} · {esc(center["country"])}</p>'
        f'<p class="distance" hidden></p>{phone}{availability}<div class="tags">{tags}</div>'
        f'<p><a href="{esc(center["website"])}" target="_blank" rel="noopener">{link_label}</a></p></article>'
    )


def portal(centers: list[dict]) -> str:
    options = '<option value="">All services</option>' + "".join(
        f'<option value="{esc(normalized(x))}">{esc(x)}</option>' for x in FILTER_GROUPS
    )
    cards = "".join(card(x) for x in centers)
    return f'''<section class="portal"><nav class="portal-nav"><a href="../">🐾 Clinical trials</a><a href="../centers/">🏥 Oncology centers</a><a href="../advanced/">🧬 Other treatment options</a><a href="../expanded-access/">🧪 Expanded access</a></nav><h1>Find a veterinary oncologist near you</h1><p class="lead">Search veterinary oncology hospitals, board-certified specialists and local clinics offering cancer care by ZIP code, city, state or available service.</p><div class="controls"><input id="q" type="search" placeholder="Hospital, city or state" aria-label="Search by hospital, city or state"><input id="zip" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" placeholder="ZIP code for nearest centers" aria-label="ZIP code for nearest centers"><select id="svc" aria-label="Filter by service">{options}</select></div><p class="note">Listings are not all the same: some are specialist oncology services, while others provide local cancer care or chemotherapy. Use the service filter and confirm current availability with the hospital before making plans.</p><p id="status" class="count" aria-live="polite"></p><p class="count"><span id="n">{len(centers)}</span> oncology locations shown</p><div class="grid" id="cards">{cards}</div><details id="international" hidden><summary><span id="intl-n">0</span> international centers — distance not calculated</summary><div class="grid" id="intl-cards"></div></details><script>
const q=document.querySelector('#q'),zip=document.querySelector('#zip'),svc=document.querySelector('#svc'),cards=[...document.querySelectorAll('.p-card')],grid=document.querySelector('#cards'),n=document.querySelector('#n'),status=document.querySelector('#status'),intl=document.querySelector('#international'),intlGrid=document.querySelector('#intl-cards'),intlN=document.querySelector('#intl-n'),original=new Map(cards.map((c,i)=>[c,i]));
const norm=v=>v.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
const rad=v=>v*Math.PI/180, miles=(a,b)=>{{const x=rad(b.lat-a.lat),y=rad(b.lon-a.lon),h=Math.sin(x/2)**2+Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.sin(y/2)**2;return 3958.8*2*Math.asin(Math.sqrt(h))}};
let seq=0;const cache=new Map();async function zipPoint(z){{if(!cache.has(z))cache.set(z,fetch('https://api.zippopotam.us/us/'+z).then(r=>{{if(!r.ok)throw Error();return r.json()}}).then(d=>({{lat:+d.places[0].latitude,lon:+d.places[0].longitude,place:d.places[0]['place name'],state:d.places[0]['state abbreviation']}})));return cache.get(z)}}
function reset(){{cards.sort((a,b)=>original.get(a)-original.get(b)).forEach(c=>{{c.hidden=false;c.querySelector('.distance').hidden=true;grid.appendChild(c)}});intl.hidden=true;status.textContent=''}}
const hasService=(c,service)=>!service||c.dataset.filters.split('|').includes(service);
function textFilter(){{const needle=norm(q.value),service=svc.value;let count=0;cards.forEach(c=>{{const show=(!needle||c.dataset.search.includes(needle))&&hasService(c,service);c.hidden=!show;if(show)count++}});n.textContent=count;status.textContent=needle||service?(count?count+' matching '+(count===1?'center.':'centers.'):'No listed centers match that search.'):''}}
async function zipFilter(z,mySeq){{status.textContent='Finding the nearest listed centers…';try{{const origin=await zipPoint(z);if(mySeq!==seq)return;const service=svc.value,eligible=cards.filter(c=>hasService(c,service)),us=eligible.filter(c=>c.dataset.country==='USA'),other=eligible.filter(c=>c.dataset.country!=='USA');cards.forEach(c=>c.hidden=true);us.map(c=>({{c,d:miles(origin,{{lat:+c.dataset.lat,lon:+c.dataset.lon}})}})).sort((a,b)=>a.d-b.d).forEach(x=>{{x.c.hidden=false;const p=x.c.querySelector('.distance');p.textContent='Approximately '+Math.round(x.d)+' miles';p.hidden=false;grid.appendChild(x.c)}});other.forEach(c=>{{c.hidden=false;intlGrid.appendChild(c)}});intlN.textContent=other.length;intl.hidden=!other.length;n.textContent=us.length;status.textContent=us.length?'Nearest matching US centers first from '+origin.place+', '+origin.state+'. Straight-line distance.':'No listed US centers match that service filter.'}}catch{{if(mySeq!==seq)return;reset();textFilter();status.textContent='We could not locate that ZIP code. Check the five digits or search by city, state or hospital name.'}}}}
function run(){{const mySeq=++seq,z=zip.value.trim();if(/^\\d{{5}}$/.test(z)){{q.value='';zipFilter(z,mySeq)}}else{{reset();textFilter()}}}}
q.addEventListener('input',()=>{{zip.value='';run()}});zip.addEventListener('input',run);svc.addEventListener('change',run);
</script></section>'''


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    centers = data["centers"]
    assert centers and all(x.get("name") and x.get("website") for x in centers)
    portal_html = portal(centers)
    for path, canonical in OUTPUTS:
        template_path = path if path.exists() else SOURCE
        rendered = template_path.read_text(encoding="utf-8")
        rendered = re.sub(r'<title>.*?</title>', '<title>Find veterinary oncology centers near you | Vet Trial Finder</title>', rendered, count=1)
        rendered = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Search veterinary oncology hospitals and cancer treatment centers by ZIP code, city, state or available service.">', rendered, count=1)
        rendered, changed = re.subn(r'<section class="portal">.*?</section>', lambda _: portal_html, rendered, count=1, flags=re.S)
        assert changed == 1, path
        rendered = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{canonical}">', rendered, count=1)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    print(f"ONCOLOGY_CENTER_FINDER_OK centers={len(centers)}")


if __name__ == "__main__":
    main()
