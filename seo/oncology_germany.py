#!/usr/bin/env python3
"""Bilingual Germany guide generated from the canonical oncology directory."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import generate_seo as g
from oncology_state_pages import GUIDE_CSS, esc
from site_shell import wrap_html

DIRECTORY_CSS = '''.germany-directory details{border-bottom:1px solid #d9e2ea}
.germany-directory summary{cursor:pointer;padding:10px 0;font-weight:650}
.germany-directory li{margin:8px 0;overflow-wrap:anywhere}
.germany-directory li time{color:#607086;font-size:.88em}'''

ROOT = Path(__file__).resolve().parents[1]
PATH = 'veterinary-oncology/germany'
URLS = {'en': f'{g.SITE}/{PATH}/', 'de': f'{g.SITE}/{PATH}/de/'}
REGIONS = {
    'Bavaria': 'Bayern', 'Hesse': 'Hessen', 'Lower Saxony': 'Niedersachsen',
    'Mecklenburg-Western Pomerania': 'Mecklenburg-Vorpommern',
    'North Rhine-Westphalia': 'Nordrhein-Westfalen', 'Rhineland-Palatinate': 'Rheinland-Pfalz',
    'Saxony': 'Sachsen', 'Saxony-Anhalt': 'Sachsen-Anhalt', 'Thuringia': 'Thüringen',
}
SERVICES = {
    'Chemotherapy': ('Chemotherapy', 'Chemotherapie'),
    'Electrochemotherapy': ('Electrochemotherapy', 'Elektrochemotherapie'),
    'Local oncology care': ('Local oncology care', 'Onkologische Versorgung vor Ort'),
    'Medical oncology': ('Medical oncology', 'Medikamentöse Onkologie'),
    'Radiation oncology': ('Radiation therapy', 'Strahlentherapie'),
    'Surgery': ('Tumor removal', 'Tumorentfernung'),
    'Surgical oncology': ('Oncologic surgery', 'Onkologische Chirurgie'),
    'Targeted therapy': ('Targeted therapy', 'Zielgerichtete Therapie'),
}
MOBILE_AREAS = {
    'de-callavet-mobile-rhein-main': ('Wiesbaden, Frankfurt, Mainz and surrounding areas', 'Wiesbaden, Frankfurt, Mainz und Umgebung'),
    'de-vetmed-service-witschel-mobile': ('Munich area, through participating practices', 'Raum München, über kooperierende Tierarztpraxen'),
    'de-rollender-tierarzt-bredenbroeker-mobile': ('Parts of Berlin and northern Brandenburg', 'Teile Berlins und des nördlichen Brandenburgs'),
    'de-imke-bartels-mobile-hamburg': ('Northeastern Hamburg', 'Hamburger Nordosten'),
    'de-dirk-joergens-mobile': ('Marburg and Kirchhain area', 'Raum Marburg und Kirchhain'),
    'de-laura-oelker-mobile-hemmingen': ('Hemmingen, Pattensen, Springe, Wennigsen, Gehrden, Ronnenberg', 'Hemmingen, Pattensen, Springe, Wennigsen, Gehrden, Ronnenberg'),
    'de-tierarzt-bus-jessica-schulz-mobile': ('Titz, Bedburg, Elsdorf, Bergheim, Erkelenz, Linnich, Heinsberg, Jülich, Aldenhoven', 'Titz, Bedburg, Elsdorf, Bergheim, Erkelenz, Linnich, Heinsberg, Jülich, Aldenhoven'),
}
RADIATION = {
    'de-tierklinik-hofheim': (
        'Conventional and stereotactic radiation with a linear accelerator. Stereotactic treatment usually takes three to five sessions when appropriate for the tumor.',
        'Konventionelle und stereotaktische Bestrahlung am Linearbeschleuniger. Wenn die Stereotaxie für den Tumor geeignet ist, sind in der Regel drei bis fünf Sitzungen vorgesehen.',
        'https://www.tierklinik-hofheim.de/die-klinik/fachbereiche/onkologie/strahlentherapi-stereotaxie.html',
    ),
    'de-equinox-healthcare-linsengericht': (
        'Linear-accelerator radiation. The center describes IMRT and VMAT, as well as electron treatment in selected cases.',
        'Bestrahlung am Linearbeschleuniger. Das Zentrum beschreibt IMRT und VMAT sowie in ausgewählten Fällen die Bestrahlung mit Elektronen.',
        'https://www.equinox.vet/',
    ),
    'de-grussendorf-bramsche': (
        'Linear-accelerator radiation and IMRT. The center lists brain, nasal and oral tumors among the cases it treats.',
        'Bestrahlung am Linearbeschleuniger und IMRT. Das Zentrum nennt unter anderem Hirntumoren sowie Tumoren der Nase und der Maulhöhle.',
        'https://www.tiergesundheitszentrum.com/leistungen/tumortherapiezentrum/',
    ),
    'de-vetspezial-lehrte': (
        'RapidArc radiation. The clinic describes treatment of nasal tumors and radiation after tumor surgery.',
        'Bestrahlung mit RapidArc. Die Klinik beschreibt unter anderem die Behandlung von Nasentumoren und die Bestrahlung nach einer Tumoroperation.',
        'https://zentrum-kleintiermedizin.de/fachgebiete/strahlentherapie/',
    ),
    'de-lmu-kleintierklinik-muenchen': (
        'Selected superficial tumors, surgical sites and some tumors at the front of the mouth. The current service also lists palliative radiation for selected limb bone tumors. Ask the clinic about referral for deep tumors.',
        'Ausgewählte oberflächliche Tumoren, Operationsgebiete und einige Tumoren im vorderen Maulbereich. Bei bestimmten Knochentumoren an den Gliedmaßen bietet die Klinik auch palliative Bestrahlung an. Bei tief liegenden Tumoren kann die Klinik zur Überweisung beraten.',
        'https://www.vetmed.lmu.de/kleintierklinik/de/fachgebiete/onkologie/leistungen-onkologie/bestrahlung.html',
    ),
    'de-schulze-lammers-witten': (
        'Superficial radiation for selected tumors of the skin, underlying tissue and other accessible sites.',
        'Oberflächenbestrahlung für ausgewählte Tumoren der Haut, der Unterhaut und anderer oberflächlich zugänglicher Bereiche.',
        'https://die-tierarzt-praxis.de/leistungen/strahlentherapie/',
    ),
}
COPY = {
    'en': {
        'title': 'Veterinary cancer treatment in Germany',
        'description': 'Find cancer care for dogs and cats in Germany, including radiation, electrochemotherapy, chemotherapy and tumor surgery. Browse clinics and official contacts by federal state.',
        'lead': 'Where to find cancer treatment for dogs and cats in Germany, from chemotherapy and tumor surgery near home to radiation and electrochemotherapy at dedicated centers.',
        'finder': 'Oncology care finder',
        'language': 'Deutsch',
        'on_page': 'On this page',
        'counts': '{physical} clinic locations · {chemo} listings with chemotherapy · {radiation} radiation locations · {ect} electrochemotherapy locations',
        'radiation': 'Where to find radiation therapy',
        'radiation_intro': 'Start with where the tumor is. Some clinics can treat deep tumors with a linear accelerator. Others offer radiation for selected superficial tumors and surgical sites. The notes below describe what each center publishes.',
        'ect': 'Electrochemotherapy and other local treatments',
        'ect_intro': 'Electrochemotherapy (ECT) treats a specific tumor or surgical site. When contacting a clinic, give the diagnosis and exact location and ask whether it treats cases like yours.',
        'ahlen': 'AniCura Ahlen lists ECT for selected urinary or reproductive tract tumors.',
        'pdt': 'LMU Munich also lists photodynamic therapy (PDT).',
        'potsdam': 'NIICE Potsdam lists tumor surgery. Its clinic page describes chemotherapy and ECT as coming soon.',
        'directory': 'Clinics and services by federal state',
        'directory_intro': 'Expand a group to see locations, services, phone numbers and source dates. The directory includes general practices that remove tumors, clinics that administer chemotherapy and dedicated oncology centers. For chemotherapy, ask who will plan the protocol and monitor bloodwork. For surgery, ask whether the clinic can handle the tumor’s location and whether a surgical referral would help.',
        'network': 'Network contacts',
        'mobile': 'Mobile veterinary services',
        'unknown': 'Federal state missing from the directory record',
        'source': 'Official source',
        'branches': 'Branch information',
        'restricted': 'Published intake notice: existing clients only.',
        'online': 'Online second opinions',
        'online_text': 'Owners can request an oncology second opinion through VetOnkologie or Krebs beim Hund. Vetonc advises the treating veterinarian. Check whether the service accepts cases from your country, which records to send and what the review costs.',
        'online_link': 'Browse online oncology consultations',
        'trials': 'Cancer clinical trials',
        'trials_text': 'In the November 7, 2026 review, we found no publicly confirmed German site enrolling dogs or cats in a new study offering treatment directed at the cancer. The trial finder can check other countries by species and diagnosis.',
        'trial_link': 'Search for cancer clinical trials',
        'coverage': 'The November 7, 2026 review covered public sources across all 16 federal states. Individual source dates are shown where recorded. Confirm the service, referral requirements, costs and appointment availability directly with the provider.',
    },
    'de': {
        'title': 'Krebsbehandlung für Hunde und Katzen in Deutschland',
        'description': 'Tieronkologie in Deutschland. Finden Sie Tierkliniken und Praxen für Bestrahlung, Elektrochemotherapie, Chemotherapie und Tumoroperationen nach Bundesland.',
        'lead': 'Hier finden Sie Tierkliniken und Praxen, die Hunde und Katzen mit Krebs behandeln. Die Übersicht reicht von Chemotherapie und Tumoroperationen in Wohnortnähe bis zu Bestrahlung und Elektrochemotherapie in spezialisierten Einrichtungen.',
        'finder': 'Kliniksuche für Tieronkologie',
        'language': 'English',
        'on_page': 'Auf dieser Seite',
        'counts': '{physical} Klinik- und Praxisstandorte · {chemo} Einträge mit Chemotherapie · {radiation} Standorte mit Strahlentherapie · {ect} Standorte mit Elektrochemotherapie',
        'radiation': 'Wo Tumoren bestrahlt werden',
        'radiation_intro': 'Bei der Wahl der Klinik kommt es darauf an, wo der Tumor liegt. Einige Zentren können tiefer liegende Tumoren mit einem Linearbeschleuniger bestrahlen. Andere bieten eine Bestrahlung für ausgewählte oberflächliche Tumoren und Operationsgebiete an.',
        'ect': 'Elektrochemotherapie und weitere lokale Behandlungen',
        'ect_intro': 'Bei der Elektrochemotherapie (ECT) wird ein bestimmter Tumor oder ein Operationsgebiet behandelt. Nennen Sie bei der Anfrage die Diagnose und die genaue Lage des Tumors und fragen Sie, ob die Klinik solche Fälle behandelt.',
        'ahlen': 'AniCura Ahlen nennt ECT für ausgewählte Tumoren der Harn- oder Geschlechtsorgane.',
        'pdt': 'Die LMU München führt auch die photodynamische Therapie (PDT) auf.',
        'potsdam': 'Die NIICE-Tagesklinik in Potsdam bietet Tumoroperationen an. Chemotherapie und ECT werden auf der Klinikseite für die nähere Zukunft angekündigt.',
        'directory': 'Kliniken, Praxen und Leistungen nach Bundesland',
        'directory_intro': 'Öffnen Sie die Gruppe für Ihre Region. Dort finden Sie Standorte, Leistungen, Telefonnummern und das Datum der Quellenprüfung. Die Liste enthält Praxen, die Tumoren entfernen, Einrichtungen mit Chemotherapie und spezialisierte Onkologiezentren. Fragen Sie bei einer Chemotherapie, wer das Behandlungsschema festlegt und die Blutwerte kontrolliert. Fragen Sie vor einer Operation, ob die Praxis Tumoren an dieser Stelle operiert und wann sie an eine spezialisierte Chirurgie überweist.',
        'network': 'Kontakte für Praxis- und Klinikverbünde',
        'mobile': 'Mobile tierärztliche Dienste',
        'unknown': 'Standorte ohne Bundeslandangabe im Verzeichnis',
        'source': 'Offizielle Quelle',
        'branches': 'Standorte und Kontakt',
        'restricted': 'Laut Praxis derzeit nur für bestehende Kundschaft.',
        'online': 'Onkologische Zweitmeinung online',
        'online_text': 'Tierhalterinnen und Tierhalter können bei VetOnkologie und Krebs beim Hund eine onkologische Zweitmeinung einholen. Vetonc berät die behandelnde Tierarztpraxis. Fragen Sie vor der Buchung, ob eine Beratung aus Ihrem Land möglich ist, welche Befunde benötigt werden und was die Beratung kostet.',
        'online_link': 'Online-Beratungen im Verzeichnis ansehen',
        'trials': 'Klinische Krebsstudien',
        'trials_text': 'Bei der Recherche vom 7. November 2026 fanden wir keinen öffentlich bestätigten Studienstandort in Deutschland, der Hunde oder Katzen für eine neue Studie mit einer gegen den Tumor gerichteten Behandlung aufnahm. In der Studiensuche können Sie nach Tierart und Diagnose auch in anderen Ländern suchen.',
        'trial_link': 'Nach klinischen Krebsstudien suchen',
        'coverage': 'Für die Recherche vom 7. November 2026 wurden öffentliche Quellen aus allen 16 Bundesländern ausgewertet. Das Datum der Quellenprüfung steht beim jeweiligen Eintrag. Fragen Sie vor der Buchung direkt bei der Einrichtung nach Leistungen, Überweisung, Kosten und freien Terminen.',
    },
}


def card(row, copy, description='', source=None):
    name = esc(row['name'])
    url = esc(source or row.get('verification_url') or row['website'])
    address = ' · '.join(esc(row[key]) for key in ('city', 'street', 'postal_code') if row.get(key))
    phone = row.get('phone') or ''
    dial = ''.join(c for c in phone if c.isdigit() or c == '+')
    phone_link = f' · <a href="tel:{esc(dial)}">{esc(phone)}</a>' if dial else ''
    detail = f'<p>{esc(description)}</p>' if description else ''
    return (
        f'<article class="ri-listing"><h3>{name}</h3><p class="ri-address">{address}</p>'
        f'{detail}<p><a href="{url}">{copy["source"]}</a>{phone_link}</p></article>'
    )


def directory(rows, copy, locale):
    groups = defaultdict(list)
    for row in rows:
        kind = row.get('location_type', 'physical')
        region = row.get('region') or ''
        group = copy[kind] if kind in ('mobile', 'network') else REGIONS.get(region, region) or copy['unknown']
        groups[group].append(row)

    sections = []
    for group in sorted(groups, key=lambda name: (name in (copy['unknown'], copy['mobile'], copy['network']), name.casefold())):
        records = sorted(groups[group], key=lambda row: (row.get('city', ''), row['name']))
        items = []
        for row in records:
            identity = esc(row['source_id'])
            name = esc(row['name'])
            url = esc(row.get('verification_url') or row['website'])
            place = ', '.join(esc(row[key]) for key in ('street', 'postal_code', 'city') if row.get(key))
            if row['source_id'] in MOBILE_AREAS:
                place = esc(MOBILE_AREAS[row['source_id']][locale])
            elif row.get('location_type') == 'mobile':
                place = esc(REGIONS.get(row.get('region'), row.get('region')))
            services = ' · '.join(esc(SERVICES[service][locale]) for service in row['services'])
            checked = esc(row.get('last_verified'))
            phone = row.get('phone') or ''
            dial = ''.join(c for c in phone if c.isdigit() or c == '+')
            contact = f' · <a href="tel:{esc(dial)}">{esc(phone)}</a>' if dial else ''
            email = esc(row.get('email'))
            if email:
                contact += f' · <a href="mailto:{email}">{email}</a>'
            branches = esc(row.get('branch_finder_url'))
            if branches:
                contact += f' · <a href="{branches}">{copy["branches"]}</a>'
            address = f' · {place}' if place else ''
            date = f' · <time datetime="{checked}">{checked}</time>' if checked else ''
            restricted = (
                f'<br>{copy["restricted"]}'
                if 'no new clients can be accepted' in row.get('availability_note', '').lower() else ''
            )
            items.append(f'<li id="{identity}"><a href="{url}">{name}</a>{address}{contact}<br>{services}{date}{restricted}</li>')
        sections.append(f'<details><summary>{esc(group)} ({len(records)})</summary><ul>{"".join(items)}</ul></details>')
    return ''.join(sections)


def generate(root):
    rows = [row for row in json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
            if row['country'] == 'Germany']
    assert len({row['source_id'] for row in rows}) == len(rows), 'Duplicate German care identities'
    counts = Counter(service for row in rows for service in row['services'])
    for locale, (language, copy) in enumerate(COPY.items()):
        other = 'de' if language == 'en' else 'en'
        title = copy['title']
        summary = copy['counts'].format(
            physical=sum(row.get('location_type', 'physical') == 'physical' for row in rows),
            chemo=counts['Chemotherapy'], radiation=counts['Radiation oncology'], ect=counts['Electrochemotherapy'],
        )
        radiation = ''.join(card(row, copy, *(
            (RADIATION[row['source_id']][locale], RADIATION[row['source_id']][2])
            if row['source_id'] in RADIATION else ('', None)
        )) for row in sorted(rows, key=lambda row: row['city']) if 'Radiation oncology' in row['services'])
        ect = ''.join(card(row, copy, copy['ahlen'] if row['source_id'] == 'de-anicura-ahlen' else '')
                      for row in sorted(rows, key=lambda row: (row['city'], row['name']))
                      if 'Electrochemotherapy' in row['services'])
        sections = ('radiation', 'ect', 'directory', 'online', 'trials')
        navigation = ''.join(f'<a href="#{section}">{copy[section]}</a>' for section in sections)
        body = f'''<div class="ri-care-guide"><style>{GUIDE_CSS}{DIRECTORY_CSS}</style>
<p><a href="/matcher/centers/">{copy['finder']}</a> · <a href="{URLS[other]}" hreflang="{other}" lang="{other}">{copy['language']}</a></p>
<h1>{title}</h1>
<p class="lead">{copy['lead']}</p>
<div class="ri-summary"><p>{summary}</p><nav aria-label="{copy['on_page']}">{navigation}</nav></div>
<section id="radiation"><h2>{copy['radiation']}</h2><p>{copy['radiation_intro']}</p><div class="ri-listings">{radiation}</div></section>
<section id="ect"><h2>{copy['ect']}</h2><p>{copy['ect_intro']}</p><div class="ri-listings">{ect}</div>
<p>{copy['pdt']} <a href="https://www.vetmed.lmu.de/kleintierklinik/de/fachgebiete/onkologie/leistungen-onkologie/elektrochemotherapie-photodynamische-therapie.html">{copy['source']} · LMU</a></p>
<p>{copy['potsdam']} <a href="https://niice-tieraerzte-potsdam.de/fachgebiete/">{copy['source']} · NIICE</a></p></section>
<section id="directory" class="germany-directory"><h2>{copy['directory']}</h2><p>{copy['directory_intro']}</p>{directory(rows, copy, locale)}</section>
<section id="online"><h2>{copy['online']}</h2><p>{copy['online_text']}</p><p><a href="/online-oncology-consultations/">{copy['online_link']}</a></p></section>
<section id="trials"><h2>{copy['trials']}</h2><p>{copy['trials_text']}</p><p><a href="/matcher/">{copy['trial_link']}</a></p></section>
<div class="ri-notice"><p>{copy['coverage']}</p></div></div>'''
        url = URLS[language]
        text = g.page(title, copy['description'], body, url, lang=language, alternates=URLS)
        social = (f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}">'
                  f'<meta property="og:description" content="{esc(copy["description"])}"><meta property="og:url" content="{url}">')
        text = wrap_html(text.replace('</head>', social + '</head>', 1))
        if language == 'de':
            text = text.replace('<header class="site-header">', '<header class="site-header" lang="en">')
            text = text.replace('<footer class="site-footer">', '<footer class="site-footer" lang="en">')
        dest = root / url.removeprefix(f'{g.SITE}/') / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
    print(f'GERMANY_CARE_GUIDES_OK languages={len(COPY)} directory_rows={len(rows)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
