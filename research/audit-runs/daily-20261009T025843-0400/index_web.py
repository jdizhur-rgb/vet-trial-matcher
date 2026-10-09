import json,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).parent
pages=[]
for file in sorted(ROOT.glob('web-*.json')):
    data=json.loads(file.read_text())
    if not isinstance(data,dict) or 'result' not in data:continue
    ts=data.get('started_at') or data.get('recorded_at')
    if ts and ts.endswith(' UTC'): ts=datetime.strptime(ts,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
    for block in data.get('result',{}).get('content',[]):
        if block.get('type')!='text':continue
        for part in re.split(r'\n-+\n',block['text']):
            match=re.search(r'Source: (?:open|click|find)\(\{"ref_id":"([^"\n]+)"',part)
            if not match:continue
            url=match.group(1);ref=re.search(r'【(turn\w+)】',part)
            m=re.search(r'\((https?://[^\n)]+)\)',part.splitlines()[0]);url=m.group(1) if m else url
            failed_url=re.search(r'Failed to fetch (https?://\S+?): (?:\(|HTTP)',part)
            if not url.startswith('http') and failed_url: url=failed_url.group(1)
            lines=[re.sub(r'^L\d+(?:@P[\d-]+)?: ?', '', l) for l in part.splitlines() if re.match(r'^L\d+(?:@P[\d-]+)?:',l)]
            body='\n'.join(lines)
            total=int((re.search(r'Total lines: (\d+)',part) or [None,0])[1]); nums=[int(x) for x in re.findall(r'^L(\d+)(?:@P[\d-]+)?:',part,re.M)]
            pages.append({'url':url,'attempted_at':ts,'method':'Web_open','file':file.name,'reference':ref.group(1) if ref else None,'crawl_label':(re.search(r'Crawled: ([^;]+)',part) or [None,None])[1],'body':body,'reader_sha256':hashlib.sha256(body.encode()).hexdigest(),'retrieved':bool(body) and not any(x in body[:400] for x in ['Failed to fetch','not accessible via this tool','Forbidden','Internal Server Error']), 'total_lines':total,'last_line':max(nums) if nums else -1,'first_line':min(nums) if nums else -1,'full_text_available':bool(nums) and min(nums)==0 and max(nums)>=total-1})
(ROOT/'web-page-index.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    import sys
    inv=json.loads((ROOT/'inventory-before.json').read_text())['sources']
    lo=int(sys.argv[1]) if len(sys.argv)>1 else 0;hi=int(sys.argv[2]) if len(sys.argv)>2 else len(inv)
    for i,s in enumerate(inv[lo:hi],lo):
        matches=[p for p in pages if p['url'].rstrip('/')==s['master_url'].rstrip('/')]
        p=max(matches,key=lambda x:len(x['body']),default=None)
        print('\nSOURCE',i,s['id'], 'ref',p['reference'] if p else None,'crawl',p['crawl_label'] if p else None)
        if not p: print('MISSING RESPONSE');continue
        body=p['body'];wanted=[l for l in body.splitlines() if re.search(r'clinical|trial|studies|recruit|enroll|lymphom|cancer|tumou?r|sarcom|carcinom|glioma|melanom|oncolog|腫瘍|がん|臨床|治験|募集|研究|肿瘤|癌|临床|试验|入组|종양|임상|모집|tumori|neoplas|ensai|estud|essai|étud|klinisch|studie',l,re.I)]
        print('\n'.join(wanted)[:2200])
