import concurrent.futures as cf
import datetime as dt
import hashlib,json,pathlib,re,sys,urllib.parse
import requests
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from scripts.check_evidence_keys import redact_text
OUT=pathlib.Path(__file__).parent
HOSTS='acornlakevet.com alexvet.com allcreaturevetclinic.com allpetsvetmed.com animalcarecenterbaxter.com blackdoganimalhospital.com bluffspetclinic.com carriagehousevets.com companionsweb.com cottonwoodvetclinic.net duluthvet.com fergusfallsacc.com gehrman-animal.com grandavevet.com headwatersvetcenter.com homewardboundanimalclinic.com hopevet.care housepawsmn.com kelleyanimalhospital.com lakesvet.net marshallanimalhealth.com meadowviewvetmn.com mendakotaanimalhospital.com millelacsvet.com myvetpartners.com northernveterinaryclinic.com nsvh.com pineconepethospital.com pmcwinona.com ricevetclinic.com rumrivervet.com tcvs-mn.com vetdermglobus.com willowpethospital.com aercmn.com alexandriasanimaldoctor.com alliedervet.com animalclinicofhibbing.com arrowwood.vet bemidjivethospital.com bluecrossanimal.com brainerdanimalhospitalpc.com buckinghamveterinary.com caccwinona.com clvsurgery.com detroitlakesanimalhospital.com ferguspetvet.com grvet.com heritageanimalhospital.com highlinevets.com lakelandvet.net magnificent.vet marshallanimalclinic.com mesabaanimalhospital.com mnvalleypet.com northernvalleyvet.com northlandanimalhospitalvirginia.com nurvc.com rcmvs.com rhpch.com ricecreekvet.com ricepetclinic.com south71vet.com svvetclinic.net vetclinicmn.com winonavethospital.com zimmvet.com vmc.umn.edu'.split()
def norm(u):
 p=urllib.parse.urlsplit(u);return p.netloc.lower().removeprefix('www.')+p.path.rstrip('/')+('?' + p.query if p.query else '')
denied=set()
for f in ['data/source_access_restrictions.json','research/oncology-care-queue/access-restriction-index.json']:
 for u in re.findall(r'https?://[^\s"<>]+',(ROOT/f).read_text()):denied.add(norm(u))
def get(u):
 now=dt.datetime.now(dt.timezone.utc).isoformat();key=hashlib.sha256(u.encode()).hexdigest()[:16]; dest=OUT/'pages'/f'{key}.json';dest.parent.mkdir(exist_ok=True)
 if dest.exists():return json.loads(dest.read_text())
 row={'url':u,'attempted_at':now,'method':'requests GET','key':key}
 if norm(u) in denied:row.update(result='skipped_restricted');return row
 try:
  r=requests.get(u,timeout=(8,18));row.update(status=r.status_code,final_url=r.url)
  if r.status_code!=200:row['result']='http_error'
  else:
   s=BeautifulSoup(r.text,'html.parser');links=[]
   for a in s.select('a[href]'):
    href=urllib.parse.urljoin(r.url,a['href'])
    if href.startswith(('http','tel:','mailto:')):links.append({'text':a.get_text(' ',strip=True),'url':href})
   for x in s(['script','style','noscript','svg']):x.decompose()
   txt='\n'.join(z.strip() for z in s.get_text('\n').splitlines() if z.strip())
   row.update(result='readable' if len(txt)>200 else 'thin',text=redact_text(txt),links=json.loads(redact_text(json.dumps(links))))
 except Exception as e:row.update(result='error',error=str(e)[:300])
 dest.write_text(json.dumps(row,ensure_ascii=False,indent=2));return row
urls=json.loads((OUT/'discovered-urls.json').read_text())
targets=[u for u in urls if urllib.parse.urlparse(u).netloc.removeprefix('www.') in HOSTS and not u.endswith('.pdf')]
targets += ['https://www.alliedervet.com/oncology/','https://bluepearlvet.com/hospital/golden-valley-mn/','https://bluepearlvet.com/hospital/golden-valley-mn/our-vets/','https://bluepearlvet.com/hospital/golden-valley-mn/specialties-services/surgery/','https://bluepearlvet.com/find-a-hospital/','https://vcahospitals.com/cascade/services/advanced-care/oncology','https://animalshelter.org/veterinarian/Minnesota/MN/1.html','https://vetscorecard.com/vets/mn/']
targets=sorted(set(targets))
if '--directories' in sys.argv:
 index=get('https://vetscorecard.com/vets/mn/')
 targets=sorted(set(a['url'] for a in index.get('links',[]) if re.match(r'https://vetscorecard.com/vets/mn/[^/]+/$',a['url'])))
 targets += [f'https://animalshelter.org/veterinarian/Minnesota/MN/{i}.html' for i in range(2,11)]
 print('directory targets',len(targets),flush=True)
if '--extra' in sys.argv:
 targets=json.loads((OUT/'extra-targets.json').read_text())
with cf.ThreadPoolExecutor(max_workers=12) as pool: rows=list(pool.map(get,targets))
print('first',len(rows),flush=True)
if '--follow' in sys.argv:
 more=set()
 for row in rows:
  host=urllib.parse.urlparse(row['url']).netloc.removeprefix('www.')
  candidates=[]
  for a in row.get('links',[]):
   p=urllib.parse.urlparse(a['url'])
   if p.netloc.removeprefix('www.')!=host or p.fragment or p.query or p.path.endswith(('.jpg','.png','.pdf')):continue
   if re.search(r'cancer|oncolo|chemo|surg|team|doctor|veterinarian|contact|location|staff|about-us|services',p.path+' '+a['text'],re.I):candidates.append(a['url'])
  more.update(candidates[:18])
 more-=set(targets)
 with cf.ThreadPoolExecutor(max_workers=12) as pool:rows+=list(pool.map(get,sorted(more)))
print('total',len(rows),flush=True)
(OUT/'attempts.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['text','links']} for r in rows],indent=2))
for row in rows:
 text=row.get('text','');hits=[text[max(0,m.start()-100):m.end()+250].replace('\n',' ') for m in re.finditer(r'chemotherapy|tumor remov|tumour remov|mass remov|oncology|cancer treatment',text,re.I)]
 if hits:print(row['key'],row['url'],str(hits[:6])[:1400],flush=True)
