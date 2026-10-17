import pathlib,json,datetime,shutil,hashlib
root=pathlib.Path('/workspace/scratch/2d03a6db0cc6/recovered-vet-trial-matcher')
rest=pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-restored-evidence')
dur=pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-durable-recovery')
prior='eu6-20261016T142911-0400';old=pathlib.Path('research/audit-runs')/prior
now=datetime.datetime.now(datetime.timezone.utc);local=now.astimezone(datetime.timezone(datetime.timedelta(hours=-4)))
rid='eu6-recovery-'+local.strftime('%Y%m%dT%H%M%S%z');run=root/'research/audit-runs'/rid;run.mkdir()
base='b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45';branch='research/europe-recovery-'+rid
oldassign=json.loads((dur/old/'assignments.json').read_text());manifest=json.loads((dur/old/'backups/checkpoint-021-manifest.json').read_text())
def out(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
criteria=json.loads((dur/old/'criteria.json').read_text());criteria['version']='owner-20261016-1424-v1-plus-current-network-rule';criteria['network_rule']='Current official network usable cancer treatment+common contact may be one network listing, never branch fanout; current operations 2026-10-17.'
criteria['current_baseline']=base;out(run/'criteria.json',criteria)
assign=[]
for a in oldassign['assignments']:
 n=a['slot'];w=run/f'worker-{n}';inp=w/'input';inp.mkdir(parents=True)
 # Original immutable bytes remain historical, never rewrite their run/agent/date.
 shutil.copytree(rest/old/f'worker-{n}',inp/'history',dirs_exist_ok=True)
 original=rest/'research/audit-runs/europe-controller-20261016T092604-0400'/f'worker-{n}'
 if original.exists():shutil.copytree(original,inp/'older-salvage',dirs_exist_ok=True)
 for f in ['AGENTS.md','PROJECT_OPERATIONS.md']:shutil.copy2(root/f,inp/f)
 for f in ['oncology_centers.json','oncology_centers_supplemental.json','oncology_care_source_inventory.json','acvim_oncology_profiles.json']:shutil.copy2(root/'data'/f,inp/f)
 shutil.copy2(root/'seo/oncology_teleconsultations.py',inp/'oncology_teleconsultations.py')
 shutil.copy2(run/'criteria.json',inp/'criteria.json')
 last=manifest['latest_frozen_reports'][str(n)];shutil.copy2(rest/last['source_path'],inp/'last-verified-report.md')
 cp=(rest/last['source_path']).parent
 for f in ['result.json','remaining.json']:
  if (cp/f).exists():shutil.copy2(cp/f,inp/('last-verified-'+f))
 if n==4:
  for name in ['germany-finish-20261016','germany-remaining39-20261016','filu-network-20261017']:
   p=root/'research/audit-runs'/name
   if p.exists():shutil.copytree(p,inp/name,dirs_exist_ok=True)
 fresh={k:a[k] for k in ['slot','country','regions','cities','universities','networks','languages']}
 fresh.update(run_id=rid,baseline_sha=base,worker_directory=str(w.relative_to(root)),input_path=str(inp.relative_to(root)),agent_id=None,status='ASSIGNED_NOT_SPAWNED',country_cursor_advance_allowed=False,prior_run=prior,prior_backup_branch='research/europe-recovery-'+prior,prior_backup_sha='67697594526d4a0e60e23f584ed212301d845115',last_verified_checkpoint=last['source_path'],last_verified_report_sha256=last['sha256'],scope='Continue this ONE fixed country from last remotely verified frontier, not new country or capped test. No source visit dates renewed by restoration.',source_restrictions='Read all own historical source-events/access/restrictions and current restrictions brief before ANY source requests; no denied-output read, no retry aliases. Unknown scope quarantined. Own input history only.',own_remaining_path=str((inp/'last-verified-remaining.json').relative_to(root)),national_plan_required=criteria['completion_dimensions'])
 if n==4:fresh['latest_owner_scope']='Current operations has later Germany finish/remaining39/network continuation: reconcile all already published records; do NOT restart87/39 or broad discovery. Independently assess remaining7specific provider gaps+2future openings (not due until changed/due) and national-coverage limits from saved evidence. Follow later owner scope; incomplete is honest if broad country proof unavailable.'
 out(inp/'assignment.json',fresh);assign.append(fresh)
 h={k:fresh[k] for k in ['run_id','slot','country','baseline_sha','agent_id']};h.update(status='ASSIGNED_NOT_SPAWNED',research_complete=False,assigned=0,processed=0,fully_verified=0,NEW=0,UPDATE=0,EXCLUDED=0,UNRESOLVED=0,inherited_package=fresh['last_verified_checkpoint'],counts_basis='Current run not started; inherited candidate counts are historical, not current own execution.')
 for f in ['result.json','proposed_changes.json','evidence.json','queries.json','remaining.json']:out(w/f,{**h,'records':[]})
 (w/'report.md').write_text(f'# {fresh["country"]}: восстановление исследования\n\nПодготовлено контроллером, не итоговый ответ исполнителя. Run `{rid}`, slot {n}, baseline `{base}`. Исполнитель ещё не запущен.\n\nВосстановлен последний удалённо проверенный отчёт `{fresh["last_verified_checkpoint"]}` и исторические evidence/query/proposal/remaining shards. Исходные даты сохранены. Позднее сообщённые, но не backed-up результаты не приняты. Полный национальный поиск не объявлен завершённым.\n')
out(run/'assignments.json',{'run_id':rid,'created_at':now.isoformat(),'baseline_sha':base,'frozen_before_spawn':True,'research_branch':branch,'assignments':assign})
shutil.copy2(rest/'restoration-receipt.json',run/'restoration-receipt.json')
out(run/'controller-plan.json',{'run_id':rid,'status':'PREPARED','priority':'All available country research first, then independent all-six gate, only then site integration/build/publication. Research-only backup mandatory during search, <=15 minutes and each meaningful block.','active_other_agents_observed':[],'prior_agent_failure':'AT and NL actual usage-limit failure, all prior agents absent now; no background execution claimed.','lost_after_last_backup':'Post021 blocks: AT11/12, CZ10/public-exclusions, PL8/9, NL11-13/restrictions010-011; reports in visible history only, no payload proof. FRSevetys246 roster reported but body not remote; verify/recover before claiming.','remaining':'Each own saved remaining file and full documented national plan, except later Germany explicit no87/39restart; no country advancement.','site_publication_allowed':False})
out(run/'publication-ledger.json',{'run_id':rid,'status':'RESEARCH_NOT_STARTED','all_six_research_complete':False,'new_site_commits':[],'deploys':[],'production_readbacks':[],'existing_current_main':base})
out(run/'backup-control.json',{'run_id':rid,'created_at':now.isoformat(),'baseline_sha':base,'prior_backup_sha':'67697594526d4a0e60e23f584ed212301d845115','restoration_verified':True,'research_only':True,'site_deployment':False,'trigger_proof':'Current deploy-static-site.yml push branches main only; new research branch never main, no PR/merge/workflowdispatch.'})
(run/'report.md').write_text(f'# Контроллер: восстановление шести стран\n\nRun `{rid}`. Реальная проверка shell/Git/Python пройдена. Main `{base}`. Старых активных исполнителей нет. Восстановлены initial+21 архива с проверкой полных SHA и member hashes.\n\nНовый поиск ещё не начат; назначения зафиксированы до spawn. Research backup отличается от публикации сайта. Все страны остаются незавершёнными, кроме отдельных документированных доступных этапов; курсоры не продвинуты.\n')
print(json.dumps({'run_id':rid,'root':str(root),'run_path':str(run),'branch':branch,'baseline':base,'input_files':sum(1 for p in run.glob('worker-*/input/**/*') if p.is_file())}))
