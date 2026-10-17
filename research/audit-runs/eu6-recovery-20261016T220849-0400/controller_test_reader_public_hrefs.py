"""Independent parent mock tests, no network or worker file writes."""
import pathlib,hashlib,json,sys,types,urllib.request,urllib.error,socket,contextlib,io,datetime
RUN=pathlib.Path(__file__).resolve().parent
WORKER=RUN/'worker-5'
SOURCE=WORKER/'read_public_branch_public_href_v3.py'
EXPECTED='5da76bf0415eaf131426fe9c24b9fa8693625e8745458a512ce1b6b8390c0c38'
raw=SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED
old=(RUN/'controller_test_reader_subset.py').read_text()
old=old.replace("SOURCE=WORKER/'checkpoints/native-explicit-subset-fix-20261017T0440/read_public_branch.py'","SOURCE=WORKER/'read_public_branch_public_href_v3.py'")
old=old.replace('0f1e1cf2f600a51be87b75bd8a274b7bc9f2ab24aec890b95082fcd47e5c622a',EXPECTED)
capture=io.StringIO()
with contextlib.redirect_stdout(capture):
    exec(compile(old,str(RUN/'controller_test_reader_subset.py'),'exec'),{'__name__':'__main__','__file__':str(RUN/'controller_test_reader_subset.py')})
prior=json.loads(capture.getvalue())
assert prior['all_pass'] and len(prior['tests'])==13
url='https://parent-mock.invalid/0'
safe=['https://parent-mock.invalid/?page=services#top','https://parent-mock.invalid/?id=12','https://parent-mock.invalid/?page=contact','https://parent-mock.invalid/#normal-section']
sensitive=['/?x='+'b'*64,'/#eyJDEMOFAKE.payload.signature','/#'+'c'*32,'/?access_token=demo','https://PARENT_DEMO_USER:PARENT_DEMO_PASS@parent-mock.invalid/secret','/?page=services&nonce=demo','/?token=demo']
external='https://PARENT_DEMO_USER:PARENT_DEMO_PASS@external-parent-mock.invalid/private'
html=('<title>Parent local only</title><p>ordinary public page</p>'+''.join('<a href="'+s+'">public test link</a>' for s in [*safe,*sensitive,external])).encode()
calls=[];saved=[];network=[]
module=types.ModuleType('recover_working');module.ROOT=WORKER;module.IDENTITY={'parent_mock':True}
gate={'metadata_only_preflight':True,'request_execution':False,'approved_URLs':[url],'permitted_urls':[url],'blocked_URLs':[]}
def read(p):
    if p=='MOCKGATE':return gate
    if p=='source-guard.json':return {'restrictions':[],'held_workflow_targets':[]}
    if p=='provider-workflow-alias-holds.json':return {'provider_workflow_aliases':[]}
    if p=='current-new-restrictions.json':return {'restrictions':[]}
    raise AssertionError(('Unexpected read',p))
module.read=read;module.save=lambda p,o:saved.append(o)
class Response:
    status=200
    def __init__(self):self.url=url
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,*args):return html
class Opener:
    def open(self,u,*a,**kw):calls.append(u);return Response()
def deny(*a,**kw):network.append(True);raise AssertionError('Real network forbidden')
previous=sys.modules.get('recover_working');argv=sys.argv[:];opener=urllib.request.build_opener;urlopen=urllib.request.urlopen;connect=socket.create_connection
try:
    sys.modules['recover_working']=module;sys.argv=['reader','UNSAVED_PARENT_MOCK','--permitted-whitelist','MOCKGATE',url]
    urllib.request.build_opener=lambda *a,**kw:Opener();urllib.request.urlopen=deny;socket.create_connection=deny
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(raw,str(SOURCE),'exec'),{'__name__':'__main__'})
finally:
    sys.argv=argv;urllib.request.build_opener=opener;urllib.request.urlopen=urlopen;socket.create_connection=connect
    if previous is None:sys.modules.pop('recover_working',None)
    else:sys.modules['recover_working']=previous
assert calls==[url] and not network
row=saved[-1]['rows'][-1]
assert row['own_public_link_metadata']==safe,row['own_public_link_metadata']
assert len(row['redacted_own_href_metadata'])==len(sensitive)
assert not any('external-parent-mock.invalid' in v for v in row['advertised_external_URL_metadata'])
out=json.dumps(saved)
assert 'PARENT_DEMO_USER' not in out and 'PARENT_DEMO_PASS' not in out
assert 'b'*64 not in out and 'c'*32 not in out and 'eyJDEMOFAKE' not in out
assert all(x['scope']=='UNKNOWN_CREDENTIAL_SHAPED_DO_NOT_REQUEST' for x in row['redacted_own_href_metadata'])
print(json.dumps({'run_id':RUN.name,'parent':'/root','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_code_sha256':EXPECTED,'inherited_independent_negative_stop_tests':prior['tests'],'public_href_test':{'actual_mock_calls':len(calls),'safe_href_count':len(safe),'sensitive_href_redacted_count':len(sensitive),'external_userinfo_omitted':True,'public_query_and_fragment_exact_preservation':True,'no_credential_sentinel_in_saved_payload':True,'pass':True},'all_pass':True,'worker_files_written':0,'real_source_requests':0,'real_source_bodies_read':0,'real_source_hashes_created':0,'network_attempts':len(network)},ensure_ascii=False,indent=2))
