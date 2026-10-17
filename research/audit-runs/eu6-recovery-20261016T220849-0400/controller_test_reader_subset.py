"""Parent independent mock-only review; no worker writes or network access."""
import pathlib,hashlib,json,sys,types,urllib.request,urllib.error,socket,contextlib,io,datetime
RUN=pathlib.Path(__file__).resolve().parent
WORKER=RUN/'worker-5'
SOURCE=WORKER/'checkpoints/native-explicit-subset-fix-20261017T0440/read_public_branch.py'
raw=SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='0f1e1cf2f600a51be87b75bd8a274b7bc9f2ab24aec890b95082fcd47e5c622a'
urls=['https://parent-mock.invalid/'+str(i) for i in range(4)]
gate={'metadata_only_preflight':True,'request_execution':False,'approved_URLs':urls,'permitted_urls':urls,'blocked_URLs':[]}
tests=[('missing-subset',[],0,403),('only-second',[urls[1]],1,403),('unknown',['https://parent-mock.invalid/unknown'],0,403),('unexpected-flag',['--ignored'],0,403),('no-whitelist',[urls[0]],0,403),('duplicate',[urls[0],urls[0]],0,403),('new-hold',[urls[1]],0,403)]
tests += [('stop-'+str(s),urls,1,s) for s in (401,403,429,302,'auth','challenge')]
results=[]
for name,subset,expected,status in tests:
    calls=[];saved=[];network_attempts=[];reads=[0]
    module=types.ModuleType('recover_working');module.ROOT=WORKER;module.IDENTITY={'parent_mock':True}
    def read(path):
        if path=='MOCKGATE':return gate
        if path=='source-guard.json':return {'restrictions':[],'held_workflow_targets':[]}
        if path=='provider-workflow-alias-holds.json':return {'provider_workflow_aliases':[]}
        if path=='current-new-restrictions.json':
            reads[0]+=1
            return {'restrictions':[{'url':urls[1]}] if name=='new-hold' and reads[0]>1 else []}
        raise AssertionError(('Unexpected file read',path))
    module.read=read;module.save=lambda p,obj:saved.append(obj)
    class Response:
        status=200;url=urls[0]
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def read(self,*args):return b'<title>Connexion</title>' if status=='auth' else b'<title>Just a moment</title>'
    class FakeOpener:
        def open(self,url,*args,**kwargs):
            calls.append(url)
            if status in ('auth','challenge'):return Response()
            raise urllib.error.HTTPError(url,status,'PARENT_LOCAL_MOCK',{'Location':'https://held-parent-mock.invalid/private'} if status==302 else {},None)
    def deny_network(*args,**kwargs):
        network_attempts.append(True);raise AssertionError('Real network forbidden in parent test')
    old_module=sys.modules.get('recover_working');old_argv=sys.argv[:];old_opener=urllib.request.build_opener;old_urlopen=urllib.request.urlopen;old_connect=socket.create_connection
    try:
        sys.modules['recover_working']=module;urllib.request.build_opener=lambda *a,**kw:FakeOpener();urllib.request.urlopen=deny_network;socket.create_connection=deny_network
        sys.argv=['reader','UNSAVED_PARENT_MOCK']+ (subset if name=='no-whitelist' else ['--permitted-whitelist','MOCKGATE']+subset)
        with contextlib.redirect_stdout(io.StringIO()):
            try:exec(compile(raw,str(SOURCE),'exec'),{'__name__':'__main__'})
            except (AssertionError,SystemExit):pass
    finally:
        sys.argv=old_argv;urllib.request.build_opener=old_opener;urllib.request.urlopen=old_urlopen;socket.create_connection=old_connect
        if old_module is None:sys.modules.pop('recover_working',None)
        else:sys.modules['recover_working']=old_module
    assert len(calls)==expected,(name,calls)
    if name=='only-second':assert calls==[urls[1]]
    assert not network_attempts,(name,'Unexpected network')
    assert not any('source_sha256' in row for obj in saved for row in obj.get('rows',[]))
    results.append({'test':name,'expected_mock_calls':expected,'actual_mock_calls':len(calls),'network_attempts':len(network_attempts),'real_source_body_reads':0,'real_source_hashes':0,'pass':True})
print(json.dumps({'run_id':RUN.name,'parent':'/root','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_code_sha256':hashlib.sha256(raw).hexdigest(),'tests':results,'all_pass':True,'worker_files_written':0,'source_requests':0},ensure_ascii=False))
