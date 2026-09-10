import streamlit as st
from pathlib import Path
from urllib.parse import urljoin
import json, math, re, html, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

LOCATOR_URL="https://www.imprimedicine.com/veterinary/meet-your-oncologists"
ELIAS_URL="https://eliasanimalhealth.com/available-locations/"

# Hospital-level additions/overrides verified from current official hospital/service pages.
# Capabilities are positive-only: an omitted service is not displayed as unavailable.
EXTRAS=[
 {"center":"Auburn University Bailey Small Animal Teaching Hospital","address":"1220 Wire Rd","city":"Auburn","region":"AL","zip":"36832","phone":"334-844-4690","website":"https://www.vetmed.auburn.edu/clinical-services/bailey-small-animal-teaching-hospital/oncology/","services":["Medical oncology","Surgical oncology","Radiation oncology","ECT","Immunotherapy","IMRT","SRT","Clinical trials"]},
 {"center":"UC Davis Veterinary Medical Teaching Hospital","address":"1 Garrod Dr","city":"Davis","region":"CA","zip":"95616","phone":"","website":"https://www.vetmed.ucdavis.edu/hospital/small-animal/oncology","services":["Medical oncology","Radiation oncology","Interventional radiology","IMRT","SRT","Clinical trials"]},
 {"center":"RISE Pet Health","address":"24721 Alicia Pkwy","city":"Laguna Hills","region":"CA","zip":"92653","phone":"949-787-7473","website":"https://risepethealth.com/oncology/","services":["Medical oncology","ECT","Immunotherapy","Gilvetmab","ELIAS ECI","ONCEPT","Intratumoral therapy","Targeted therapy","Genomic profiling"]},
 {"center":"VCA Animal Specialty Group – Los Angeles","address":"4641 Colorado Blvd","city":"Los Angeles","region":"CA","zip":"90039","phone":"818-244-7977","website":"https://vcahospitals.com/animal-specialty-group-los-angeles/departments/oncology/electrochemotherapy","services":["Medical oncology","ECT","Immunotherapy"]},
 {"center":"Animal Cancer Center of Monterey","address":"530 Ramona Ave","city":"Monterey","region":"CA","zip":"93940","phone":"831-242-0978","website":"https://www.animalcancercentermonterey.com/","services":["Medical oncology","Chemotherapy","Immunotherapy","Targeted therapy","ELIAS ECI"]},
 {"center":"Colorado Animal Specialty & Emergency (CASE)","address":"2972 Iris Ave","city":"Boulder","region":"CO","zip":"80301","phone":"303-545-2273","website":"https://www.coloradoanimalspecialty.com/services/medical-oncology","services":["Medical oncology","ECT","ELIAS ECI"]},
 {"center":"Red Rock Veterinary Health","address":"3163 W Colorado Ave","city":"Colorado Springs","region":"CO","zip":"80904","phone":"719-204-3647","website":"https://www.redrockvet.com/services","services":["Medical oncology","Chemotherapy","ECT"]},
 {"center":"BluePearl Pet Hospital – Lafayette","address":"2000 W South Boulder Rd","city":"Lafayette","region":"CO","zip":"80026","phone":"720-699-7766","website":"https://bluepearlvet.com/hospital/lafayette-co/specialties-services/oncology/","services":["Medical oncology","ECT","Immunotherapy"]},
 {"center":"Evolution Veterinary Specialists","address":"34 Van Gordon St Ste 160","city":"Lakewood","region":"CO","zip":"80228","phone":"720-510-7707","website":"https://evolutionvet.com/electrochemotherapy/","services":["Medical oncology","Surgery","ECT","Immunotherapy"]},
 {"center":"Platt Park Veterinary Hospital","address":"1900 S Broadway","city":"Denver","region":"CO","zip":"80210","phone":"303-879-1090","website":"https://ppark.vet/pet-oncology/","services":["Medical oncology","ECT","Immunotherapy","ELIAS ECI"]},
 {"center":"University of Florida Small Animal Hospital","address":"2089 SW 16th Ave","city":"Gainesville","region":"FL","zip":"32608","phone":"352-392-2235","website":"https://smallanimal.vethospital.ufl.edu/clinical-services/oncology/","services":["Medical oncology","Radiation oncology","ECT","SRT","SBRT","Immunotherapy","Clinical trials"]},
 {"center":"Veterinary Cancer Health","address":"4101 Turtle Creek Dr","city":"Coral Springs","region":"FL","zip":"33067","phone":"954-369-9688","website":"https://www.vetcancerhealth.com/services/electrochemotherapy","services":["Medical oncology","ECT","Immunotherapy","Targeted therapy","Genomic profiling"]},
 {"center":"LeadER Animal Specialty Hospital – Boca Raton","address":"19357 State Road 7","city":"Boca Raton","region":"FL","zip":"33498","phone":"561-934-5323","website":"https://leadervet.com/specialties/veterinary-oncology/electrochemotherapy","services":["Medical oncology","ECT"]},
 {"center":"Pompano Veterinary Oncology","address":"353 SW 13th Ave","city":"Pompano Beach","region":"FL","zip":"33069","phone":"754-281-8893","website":"https://pompanoveterinaryoncology.com/","services":["Medical oncology","ECT","Immunotherapy"]},
 {"center":"BluePearl Pet Hospital – Fort Myers","address":"9500 Marketplace Rd","city":"Fort Myers","region":"FL","zip":"33912","phone":"239-947-0588","website":"https://bluepearlvet.com/hospital/fort-myers-fl/specialties-services/oncology/","services":["Medical oncology","Chemotherapy","ECT","Radiation oncology","Surgery"]},
 {"center":"Dogwood Veterinary Specialty & Emergency","address":"1234 Powers Ferry Rd","city":"Marietta","region":"GA","zip":"30067","phone":"404-609-1234","website":"https://www.dogwood.vet/","services":["Medical oncology","ECT","Immunotherapy","Targeted therapy"]},
 {"center":"Coastal Veterinary Oncology – Savannah","address":"335 Stephenson Ave","city":"Savannah","region":"GA","zip":"31405","phone":"912-355-5791","website":"https://cvo.vet/oncology-services/","services":["Medical oncology","Chemotherapy","Intratumoral therapy","ECT","Immunotherapy"]},
 {"center":"BluePearl Pet Hospital – Northfield","address":"820 W Frontage Rd","city":"Northfield","region":"IL","zip":"60093","phone":"","website":"https://bluepearlvet.com/hospital/northfield-il/specialties-services/oncology/","services":["Medical oncology","Chemotherapy","ECT","Radiation oncology","Surgery"]},
 {"center":"LSU Veterinary Teaching Hospital Cancer Treatment Unit","address":"Skip Bertman Dr","city":"Baton Rouge","region":"LA","zip":"70803","phone":"","website":"https://www.lsu.edu/vetmed/veterinary_hospital/oncology.php","services":["Medical oncology","Radiation oncology","IMRT","RapidArc","SRT","Clinical trials","Intratumoral therapy"]},
 {"center":"MSPCA-Angell Animal Medical Center","address":"350 S Huntington Ave","city":"Boston","region":"MA","zip":"02130","phone":"617-541-5136","website":"https://www.mspca.org/veterinarycare/hospital-locations/oncology/","services":["Medical oncology","Surgical oncology","Radiation oncology","Immunotherapy","Targeted therapy","IMRT","VMAT","SRT"]},
 {"center":"VCA South Shore (Weymouth) Animal Hospital","address":"595 Columbian St","city":"South Weymouth","region":"MA","zip":"02190","phone":"781-337-6622","website":"https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology","services":["Medical oncology","Chemotherapy","ECT","Immunotherapy","ONCEPT"]},
 {"center":"Tufts VETS","address":"525 South St","city":"Walpole","region":"MA","zip":"02081","phone":"508-668-5454","website":"https://tuftsvets.org/services/walpole-pet-oncology-services.php","services":["Medical oncology","ECT","Immunotherapy","ONCEPT","Genomic profiling"]},
 {"center":"Animal Cancer Care Specialists","address":"531 King St Unit 6","city":"Littleton","region":"MA","zip":"01460","phone":"978-577-4848","website":"https://accsvets.com/about-us/","services":["Medical oncology"]},
 {"center":"Advanced Veterinary Specialty Center of New England","address":"2250A Boston Providence Hwy","city":"Walpole","region":"MA","zip":"02081","phone":"508-921-1018","website":"https://www.avscvets.com/","services":["Medical oncology","Radiation oncology"]},
 {"center":"Veterinary Cancer Specialists of New England","address":"50 Cohasset Ave","city":"Buzzards Bay","region":"MA","zip":"02532","phone":"508-276-0836","website":"https://www.vcsnewengland.com/","services":["Medical oncology","ECT","Immunotherapy"]},
 {"center":"Atlantic Veterinary Internal Medicine & Oncology – Hunt Valley","address":"10626 York Rd","city":"Cockeysville","region":"MD","zip":"21030","phone":"","website":"https://www.avim.us/services/oncology-and-chemotherapy","services":["Medical oncology","Chemotherapy","ECT"]},
 {"center":"BluePearl Pet Hospital – Rockville","address":"1 Taft Ct","city":"Rockville","region":"MD","zip":"20850","phone":"301-637-3228","website":"https://bluepearlvet.com/hospital/rockville-md/specialties-services/oncology/","services":["Medical oncology","Chemotherapy","Immunotherapy","ECT","Surgery"]},
 {"center":"BluePearl Pet Hospital – Auburn Hills","address":"3412 E Walton Blvd","city":"Auburn Hills","region":"MI","zip":"48326","phone":"248-371-3713","website":"https://bluepearlvet.com/hospital/auburn-hills-mi/specialties-services/oncology/electrochemotherapy/","services":["Medical oncology","ECT"]},
 {"center":"Oakland Veterinary Referral Services","address":"1400 S Telegraph Rd","city":"Bloomfield Hills","region":"MI","zip":"48302","phone":"248-334-6877","website":"https://www.ovrs.com/specialty-services/oncology.html","services":["Medical oncology","ECT"]},
 {"center":"Animal Emergency & Referral Center of Minnesota – Oakdale","address":"1160 Helmo Ave N","city":"Oakdale","region":"MN","zip":"55128","phone":"651-501-3766","website":"https://www.aercmn.com/veterinary-services/oncology.html","services":["Medical oncology","Chemotherapy","ECT"]},
 {"center":"University of Missouri Veterinary Health Center","address":"900 E Campus Dr","city":"Columbia","region":"MO","zip":"65211","phone":"573-882-7821","website":"https://vhc.missouri.edu/small-animal-hospital/oncology/cancer-treatment/","services":["Medical oncology","Radiation oncology","ECT","Immunotherapy","ELIAS ECI","Clinical trials"]},
 {"center":"Bridger Veterinary Specialists","address":"1103 Reeves Rd W Ste B1","city":"Bozeman","region":"MT","zip":"59718","phone":"","website":"https://bvspets.com/","services":["Medical oncology","ECT","Immunotherapy","Radiation oncology"]},
 {"center":"NC State Veterinary Hospital","address":"1052 William Moore Dr","city":"Raleigh","region":"NC","zip":"27607","phone":"919-513-6500","website":"https://hospital.cvm.ncsu.edu/services/small-animals/cancer-oncology/oncology/electrochemotherapy/","services":["Medical oncology","Radiation oncology","ECT"]},
 {"center":"Seacoast Emergency & Referral Veterinary Hospital (SERV)","address":"20 International Dr","city":"Stratham","region":"NH","zip":"03885","phone":"603-379-8383","website":"https://servnh.com/veterinary-cancer-care/","services":["Medical oncology","ECT","Immunotherapy","Targeted therapy"]},
 {"center":"Garden State Veterinary Specialists – Eatontown","address":"246 Industrial Way W","city":"Eatontown","region":"NJ","zip":"07724","phone":"732-922-0011","website":"https://www.gsvs.org/eatontown-nj/veterinary-oncology/","services":["Medical oncology","ECT","ELIAS ECI"]},
 {"center":"Garden State Veterinary Services – Woodbridge","address":"1200 US-9","city":"Woodbridge","region":"NJ","zip":"07095","phone":"732-283-3535","website":"https://www.gsvs.org/woodbridge-nj/veterinary-oncology/","services":["Medical oncology","ECT"]},
 {"center":"Veterinary Cancer Care","address":"2001 Vivigen Way","city":"Santa Fe","region":"NM","zip":"87505","phone":"505-982-4492","website":"https://vetcancercare.com/","services":["Medical oncology","Chemotherapy","ECT","Immunotherapy","Targeted therapy","Genomic profiling"]},
 {"center":"Veterinary Specialty Referral Center of Manhattan","address":"217 7th Ave","city":"New York","region":"NY","zip":"10011","phone":"646-632-2538","website":"https://vsrcmanhattan.com/electrochemotherapy/","services":["Medical oncology","ECT"]},
 {"center":"The Ohio State University Veterinary Medical Center","address":"601 Vernon L Tharp St","city":"Columbus","region":"OH","zip":"43210","phone":"","website":"https://vmc.vet.osu.edu/services/integrated-oncology-services","services":["Medical oncology","Surgical oncology","Radiation oncology","IMRT","SRT","SBRT","Clinical trials"]},
 {"center":"Veterinary Referral Center of Central Oregon","address":"1820 NW Monterey Pines Dr","city":"Bend","region":"OR","zip":"97703","phone":"541-209-6960","website":"https://vrcvet.com/veterinary-oncology/","services":["Medical oncology","ECT","Immunotherapy","Targeted therapy"]},
 {"center":"Veterinary Cancer & Surgery Specialists","address":"10400 SE Main St","city":"Milwaukie","region":"OR","zip":"97222","phone":"503-908-1492","website":"https://vcsspdx.com/pet-electrochemotherapy-milwaukie-or/","services":["Medical oncology","Surgical oncology","ECT"]},
 {"center":"Charleston Veterinary Referral Center","address":"3484 Shelby Ray Ct","city":"Charleston","region":"SC","zip":"29414","phone":"843-614-8387","website":"https://www.charlestonvrc.com/services/oncology","services":["Medical oncology","Radiation oncology","ECT","ELIAS ECI"]},
 {"center":"VCA Dallas Animal Specialty Hospital","address":"17727 Dallas Pkwy Suite 150","city":"Dallas","region":"TX","zip":"75287","phone":"972-267-8300","website":"https://vcahospitals.com/dallas-animal-specialty/departments/oncology","services":["Medical oncology","Surgical oncology","Radiation oncology","Chemotherapy","ECT","Immunotherapy","SRT","IMRT","IGRT","VMAT","Clinical trials","ELIAS ECI"]},
 {"center":"BRIDGE Animal Referral Center","address":"8401 Main St","city":"Edmonds","region":"WA","zip":"98026","phone":"425-697-2272","website":"https://www.barcseattle.com/electrochemotherapy","services":["Medical oncology","ECT","Immunotherapy","ELIAS ECI","Clinical trials"]},
 {"center":"Northwest Veterinary Oncology Services","address":"25228 Baker St","city":"Black Diamond","region":"WA","zip":"98010","phone":"","website":"https://www.nwvetoncology.com/","services":["Medical oncology","ECT","Targeted therapy"]},
 {"center":"BluePearl Pet Hospital – Tacoma","address":"5608 S Durango St","city":"Tacoma","region":"WA","zip":"98409","phone":"253-474-0791","website":"https://bluepearlvet.com/hospital/tacoma-wa/specialties-services/oncology/","services":["Medical oncology","ECT","ELIAS ECI","Stelfonta","Targeted therapy"]},
 {"center":"Summit Veterinary Referral Center","address":"2505 S 80th St","city":"Tacoma","region":"WA","zip":"98409","phone":"253-983-1114","website":"https://www.summitvets.com/services/oncology","services":["Medical oncology","ECT","Immunotherapy","ELIAS ECI"]},
 {"center":"Wisconsin Veterinary Referral Center – Waukesha","address":"360 Bluemound Rd","city":"Waukesha","region":"WI","zip":"53188","phone":"262-553-9223","website":"https://www.wvrcwi.com/services/oncology","services":["Medical oncology","Chemotherapy","Immunotherapy","ECT","Interventional radiology","Clinical trials"]}
]

CANADA=[
 {"center":"Toronto Animal Cancer Centre","address":"","city":"Toronto","region":"ON","zip":"","country":"Canada","phone":"416-627-8222","website":"https://www.torontoacc.com/services","services":["Medical oncology","ECT"]},
 {"center":"Centre Vétérinaire Rive-Sud","address":"","city":"Brossard","region":"QC","zip":"","country":"Canada","phone":"450-656-3660","website":"https://www.vetetnous.com/centres/centre-veterinaire-rive-sud/","services":["Medical oncology","ECT"]}
]

# New ECT locations found in the hospital-first audit and not present in the former 33-U.S.-center file.
ECT_NEW={
 ("Dallas","TX"), ("Edmonds","WA"), ("Denver","CO"), ("Pompano Beach","FL"),
 ("New York","NY"), ("Columbia","MO"), ("Black Diamond","WA"), ("Cockeysville","MD"),
 ("Fort Myers","FL"), ("Northfield","IL"), ("Charleston","SC"), ("Bozeman","MT")
}

def _norm(s):
 return re.sub(r"[^a-z0-9]","",(s or "").lower().replace("veterinary","").replace("animal","").replace("pet hospital","").replace("pet","").replace("hospital",""))

def _fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 VetCancerTreatmentFinder/1.0"})
 with urllib.request.urlopen(req,timeout=12) as r:return r.read().decode("utf-8","ignore")

@st.cache_data(ttl=86400,show_spinner=False)
def _locator_centers():
 """Use the current ImpriMed oncologist-hospital locator as a broad hospital backbone."""
 try: raw=_fetch(LOCATOR_URL)
 except Exception:return []
 # Restrict to the hospital list, then capture linked hospital name + following US postal address.
 start=raw.lower().find("alaska")
 end=raw.lower().find("oncology teleconsulting option")
 if start>=0:raw=raw[start:end if end>start else None]
 pat=re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>\s*([^<]{0,260}?\b[A-Z]{2}\s+\d{5}(?:-\d{4})?)',re.I|re.S)
 out=[]
 for href,label,tail in pat.findall(raw):
  name=re.sub(r'<[^>]+>',' ',label);name=html.unescape(re.sub(r'\s+',' ',name)).strip()
  addr=html.unescape(re.sub(r'\s+',' ',tail)).strip(' \n\r\t-–—')
  m=re.search(r'^(.*?),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5})(?:-\d{4})?$',addr)
  if not m or len(name)<3:continue
  street,city,state,z=m.groups()
  href=urljoin(LOCATOR_URL,html.unescape(href))
  out.append({"center":name,"address":street.strip(),"city":city.strip(),"region":state,"zip":z,"country":"USA","phone":"","website":href,"services":["Medical oncology"],"source":LOCATOR_URL})
 return out

def _same(a,b):
 if a.get("region")!=b.get("region"):return False
 if a.get("zip") and b.get("zip") and a.get("zip")!=b.get("zip"):return False
 na,nb=_norm(a.get("center")),_norm(b.get("center"))
 return bool(na and nb and (na in nb or nb in na))

@st.cache_data(ttl=86400,show_spinner=False)
def load_centers():
 rows=_locator_centers()
 # Curated records override locator records and add centers missed by that locator.
 for x0 in EXTRAS:
  x=dict(x0);x["country"]="USA";x["verified"]="2026-09-10"
  hit=next((r for r in rows if _same(r,x)),None)
  if hit:
   hit.update({k:v for k,v in x.items() if v not in ("",None,[])})
  else:rows.append(x)
 # Preserve every previously verified ECT center as a capability when it matches the broad hospital set.
 try:
  old=json.loads((Path(__file__).resolve().parents[1]/"data"/"ect_centers_usa_canada.json").read_text()).get("centers",[])
  for e in old:
   if e.get("country")!="USA":continue
   hit=next((r for r in rows if r.get("region")==e.get("region") and r.get("city","").lower()==e.get("city","").lower() and (_norm(e.get("center")) in _norm(r.get("center")) or _norm(r.get("center")) in _norm(e.get("center")))),None)
   if hit:
    if "ECT" not in hit["services"]:hit["services"].append("ECT")
    if not hit.get("phone"):hit["phone"]=e.get("phone","")
    if not hit.get("website"):hit["website"]=e.get("website","")
 # Add the two verified Canadian ECT oncology centers separately.
 except Exception:pass
 # Exact-address/name dedupe after overrides.
 clean=[]
 for r in rows+CANADA:
  dup=next((x for x in clean if _same(x,r) or (x.get("country")==r.get("country") and x.get("region")==r.get("region") and x.get("zip") and x.get("zip")==r.get("zip") and x.get("address") and x.get("address").lower()==r.get("address","").lower() and _norm(x.get("center"))==_norm(r.get("center")))),None)
  if dup:
   for s in r.get("services",[]):
    if s not in dup.setdefault("services",[]):dup["services"].append(s)
   for k in ("address","zip","phone","website"):
    if not dup.get(k) and r.get(k):dup[k]=r[k]
  else:clean.append(r)
 return clean

def miles(a,b,c,d):
 r=3958.8;p1=math.radians(a);p2=math.radians(c);dp=math.radians(c-a);dl=math.radians(d-b)
 q=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
 return 2*r*math.asin(math.sqrt(q))

@st.cache_data(ttl=2592000,show_spinner=False)
def postal_coords(country,z):
 cc="us" if country=="USA" else "ca";z=(z or "").strip().replace(" ","")
 if not z:return None
 try:
  req=urllib.request.Request(f"https://api.zippopotam.us/{cc}/{z}",headers={"User-Agent":"VetCancerTreatmentFinder/1.0"})
  with urllib.request.urlopen(req,timeout=5) as resp:data=json.load(resp)
  p=data["places"][0];return float(p["latitude"]),float(p["longitude"]),p.get("place name",""),p.get("state abbreviation",p.get("state",""))
 except Exception:return None

@st.cache_data(ttl=2592000,show_spinner=False)
def center_coords(country,z):
 v=postal_coords(country,z);return (v[0],v[1]) if v else None

def geocode_many(rows):
 out={};jobs={}
 with ThreadPoolExecutor(max_workers=18) as ex:
  for i,x in enumerate(rows):
   if x.get("zip"):jobs[ex.submit(center_coords,x.get("country","USA"),x["zip"])]=i
  for f in as_completed(jobs):
   try:
    p=f.result()
    if p:out[jobs[f]]=p
   except Exception:pass
 return out

def render():
 st.markdown("<div style='height:1.0rem'></div>",unsafe_allow_html=True)
 st.markdown("<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>🏥 Find an Oncology Center</div>",unsafe_allow_html=True)
 st.write("Find veterinary oncology hospitals near you and filter by verified treatment capabilities.")
 rows=load_centers()
 st.markdown("""<style>.onc-badges{display:flex;flex-wrap:wrap;gap:.32rem;margin:.35rem 0 .45rem}.onc-badge{display:inline-block;background:#eef5f7;border:1px solid #d5e5e9;color:#315b63;padding:.17rem .46rem;border-radius:999px;font-size:.78rem;font-weight:600}.onc-address{color:#5f5a56;font-size:.92rem;margin:.1rem 0 .28rem}</style>""",unsafe_allow_html=True)
 country=st.selectbox("Country",["USA","Canada"],key="onc_country")
 zip_code=st.text_input("ZIP / postal code",placeholder="e.g. 01095 or M5V 3L9",key="onc_zip")
 available=sorted({s for x in rows if x.get("country")==country for s in x.get("services",[]) if s not in {"Medical oncology","Chemotherapy","Surgery","Surgical oncology"}})
 preferred=["ECT","Immunotherapy","ELIAS ECI","Stelfonta","Gilvetmab","ONCEPT","Radiation oncology","SRT","SBRT","IMRT","VMAT","Interventional radiology","Genomic profiling","Targeted therapy","Clinical trials"]
 options=[s for s in preferred if s in available]+[s for s in available if s not in preferred]
 selected=st.multiselect("Treatment / service (optional)",options,placeholder="Show all oncology centers",key="onc_services")
 if st.button("Find oncology centers",use_container_width=True,type="primary",key="onc_find"):
  loc=postal_coords(country,zip_code)
  if not loc:st.error("ZIP / postal code not found.");return
  lat,lon,place,region=loc
  candidates=[x for x in rows if x.get("country")==country and (not selected or all(s in x.get("services",[]) for s in selected))]
  if not candidates:st.warning("No verified centers in the database match those filters.");return
  with st.spinner("Finding the nearest centers…"):coords=geocode_many(candidates)
  ranked=[]
  for i,x in enumerate(candidates):
   p=coords.get(i)
   if p:ranked.append((miles(lat,lon,p[0],p[1]),x))
  ranked.sort(key=lambda v:v[0])
  if not ranked:st.warning("Matching centers were found, but distance data could not be calculated right now.");return
  st.success(f"Nearest oncology centers to {place}{', '+region if region else ''}")
  for dist,x in ranked[:15]:
   with st.container(border=True):
    st.subheader(x["center"])
    locparts=[x.get("address","").strip(),x.get("city","").strip(),(x.get("region","")+" "+x.get("zip","")).strip()]
    addr=", ".join(v for v in locparts if v)
    st.markdown(f"<div class='onc-address'>{addr} · approximately {dist:.0f} miles away</div>",unsafe_allow_html=True)
    svcs=x.get("services",[])
    if svcs:st.markdown("<div class='onc-badges'>"+"".join(f"<span class='onc-badge'>{html.escape(s)}</span>" for s in svcs)+"</div>",unsafe_allow_html=True)
    if x.get("phone"):
     digits="".join(c for c in x["phone"] if c.isdigit());st.markdown(f"☎️ [{x['phone']}](tel:{digits})")
    if x.get("website"):st.link_button("Hospital / oncology page",x["website"],use_container_width=True)
  st.caption("Only positively verified capabilities are shown. Distances are approximate straight-line distances from postal-code centroids.")
