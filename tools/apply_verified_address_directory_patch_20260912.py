from pathlib import Path
import json

p = Path('seo/center_directory.py')
text = p.read_text(encoding='utf-8')

locations = {
    'Royal Veterinary College Queen Mother Hospital for Animals': 'Queen Mother Hospital for Animals, The Royal Veterinary College, Hawkshead Lane, North Mymms, Hatfield AL9 7TA, UK',
    'Charleston Veterinary Referral Center': 'Charleston Veterinary Referral Center, 3484 Shelby Ray Ct, Charleston, SC 29414',
    'Boston West Veterinary Emergency & Specialty': 'Boston West Veterinary Emergency & Specialty, 5 Strathmore Rd, Natick, MA 01760',
    'Pacific Northwest Pet ER & Specialty Center': 'Pacific Northwest Pet ER & Specialty Center, 815 SE 160th Ave, Vancouver, WA 98683',
    'Upstate Vet Emergency + Specialty Care': 'Upstate Vet Emergency & Specialty Care, 393 Woods Lake Rd, Greenville, SC 29607',
    'Animal Medical Center of Plainfield': 'Animal Medical Center of Plainfield, 13813 S Route 59, Plainfield, IL 60544',
    'Eastern Carolina Veterinary Medical Center': 'Eastern Carolina Veterinary Medical Center, 50 Greenville Ave, Wilmington, NC 28403',
    'Spanaway Veterinary Clinic': 'Spanaway Veterinary Clinic, 16920 Pacific Ave S, Spanaway, WA 98387',
    'Nashville Veterinary Specialists': 'Nashville Veterinary Specialists, 2971 Sidco Dr, Nashville, TN 37204',
    'Veterinary Cancer Care': 'Veterinary Cancer Care, 2001 Vivigen Way #B, Santa Fe, NM 87505',
    'Animal Cancer Care and Research Center': 'Animal Cancer Care and Research Center, 4 Riverside Cir, Roanoke, VA 24016',
    'Animal Emergency Hospital': 'Animal Emergency Hospital, 722 Baltimore Pike, Bel Air, MD 21014',
    'Premier Veterinary Group - Chicago': 'Premier Veterinary Group, 3927 W Belmont Ave, Chicago, IL 60618',
    'McAbee Veterinary Hospital': 'McAbee Veterinary Hospital, 4586 N Palmetto Ave, Winter Park, FL 32792',
    'Sumner Veterinary Hospital': 'Sumner Veterinary Hospital, 16024 60th St E, Sumner, WA 98390',
}

aliases = {
    'Cornell University Hospital for Animals': 'Cornell University College of Veterinary Medicine',
    'Lloyd Veterinary Medical Center, Iowa State University': 'Iowa State University College of Veterinary Medicine',
    'University of Tennessee Veterinary Medical Center': 'University of Tennessee College of Veterinary Medicine',
    'Auburn University Bailey Small Animal Teaching Hospital': 'Auburn University College of Veterinary Medicine',
    'Care Center': 'CARE Center Cincinnati',
    'CARE Center': 'CARE Center Cincinnati',
    'Boston West Veterinary Emergency and Specialty': 'Boston West Veterinary Emergency & Specialty',
    'Pacific Northwest Pet Emergency & Specialty Center': 'Pacific Northwest Pet ER & Specialty Center',
    'Premier Vet Group': 'Premier Veterinary Group - Chicago',
    'Bridge Animal Referral Center, 8401 Main St': 'Bridge Animal Referral Center (BARC)',
    'Bridge Animal Referral Center': 'Bridge Animal Referral Center (BARC)',
}

loc_anchor = '    # MedVet study locations\n'
if 'Royal Veterinary College Queen Mother Hospital for Animals' not in text:
    block = '    # Verified participating hospitals — 2026-09-12\n' + ''.join(
        f'    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n' for k, v in locations.items()
    ) + '\n'
    text = text.replace(loc_anchor, block + loc_anchor)

alias_anchor = '    "Massachusetts Veterinary Referral Hospital (MVRH)": "Massachusetts Veterinary Referral Hospital",\n'
if '"Cornell University Hospital for Animals"' not in text:
    block = ''.join(
        f'    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n' for k, v in aliases.items()
    )
    text = text.replace(alias_anchor, block + alias_anchor)

p.write_text(text, encoding='utf-8')

sources = {
    'Royal Veterinary College Queen Mother Hospital for Animals': {'url':'https://www.rvc.ac.uk/act/contact','verified':'2026-09-12'},
    'Charleston Veterinary Referral Center': {'url':'https://www.charlestonvrc.com/contact-us','verified':'2026-09-12'},
    'Boston West Veterinary Emergency & Specialty': {'url':'https://www.bostonwestvet.com/about-us','verified':'2026-09-12'},
    'Pacific Northwest Pet ER & Specialty Center': {'url':'https://www.pacificnwvets.com/','verified':'2026-09-12'},
    'Upstate Vet Emergency + Specialty Care': {'url':'https://www.upstatevet.com/contact-us','verified':'2026-09-12'},
    'Animal Medical Center of Plainfield': {'url':'https://www.animalmedicalcenterplainfield.com/about-us','verified':'2026-09-12'},
    'Eastern Carolina Veterinary Medical Center': {'url':'https://www.easterncarolinavet.com/contact-us','verified':'2026-09-12'},
    'Spanaway Veterinary Clinic': {'url':'https://www.spanawayvet.com/contact-us','verified':'2026-09-12'},
    'Nashville Veterinary Specialists': {'url':'https://www.nashvillevetspecialists.com/contact-us','verified':'2026-09-12'},
    'Veterinary Cancer Care': {'url':'https://vetcancercare.com/contact/','verified':'2026-09-12'},
    'Animal Cancer Care and Research Center': {'url':'https://cancercare.vetmed.vt.edu/directions.html','verified':'2026-09-12'},
    'Animal Emergency Hospital': {'url':'https://www.marylandpetemergency.com/directions.html','verified':'2026-09-12'},
    'Premier Veterinary Group - Chicago': {'url':'https://www.premiervets.net/locations/chicago','verified':'2026-09-12'},
    'McAbee Veterinary Hospital': {'url':'https://www.mcabeeveterinary.com/','verified':'2026-09-12'},
    'Sumner Veterinary Hospital': {'url':'https://sumnervet.com/contact/','verified':'2026-09-12'},
    'Cornell University Hospital for Animals': {'url':'https://www.vet.cornell.edu/hospitals/pharmacy/pharmacy-faq','verified':'2026-09-12'},
    'Lloyd Veterinary Medical Center, Iowa State University': {'url':'https://vetmed.iastate.edu/vmc/veterinarians/contact-us/','verified':'2026-09-12'},
    'University of Tennessee Veterinary Medical Center': {'url':'https://vetmed.tennessee.edu/vmc/about/about-the-center/','verified':'2026-09-12'},
    'Auburn University Bailey Small Animal Teaching Hospital': {'url':'https://www.vetmed.auburn.edu/clinical-services/bailey-small-animal-teaching-hospital/','verified':'2026-09-12'},
    'Care Center': {'url':'https://carecentervets.com/contact-locations/cincinnati/','verified':'2026-09-12'},
    'Bridge Animal Referral Center': {'url':'https://www.barcseattle.com/','verified':'2026-09-12'},
}
Path('data/address_sources_verified_20260912.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('PATCHED_VERIFIED_DIRECTORY', len(locations), 'locations', len(aliases), 'aliases')
