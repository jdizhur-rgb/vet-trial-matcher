"""Seal the visible Russian report and actual final validation evidence."""
from daily21 import ROOT,RUN,read,write,now,checkpoint
import subprocess,hashlib,json
from datetime import datetime
from zoneinfo import ZoneInfo
rel=str(RUN.relative_to(ROOT));logs=read(RUN/'validators.json')
for c in [['python','scripts/validate_source_inventory.py'],['python','scripts/validate_audit_receipt.py',rel+'/receipt-final.json'],['python','scripts/validate_audit_gap_review.py',rel+'/gap-review.json','--receipt',rel+'/receipt-final.json'],['python','scripts/check_evidence_keys.py'],['git','diff','--check']]:
 at=now();p=subprocess.run(c,cwd=ROOT,text=True,capture_output=True);logs.append(dict(command=c,cwd=str(ROOT),started_at=at,finished_at=now(),exit_code=p.returncode,output=p.stdout+p.stderr,scope='Final evidence/readback/report sealing; no new source traversal'))
write(RUN/'validators.json',logs)
summary={}
for r in logs:summary[' '.join(r['command'])]={k:r.get(k) for k in ['cwd','started_at','finished_at','exit_code','output']}
write(RUN/'validator-summary.json',summary)
pub=read(RUN/'publication.json');receipt=read(RUN/'receipt-final.json');end=now();short=datetime.fromisoformat(end).strftime('%H:%M:%S');sha=pub['main_commit']
assert pub['status']=='PUBLISHED_AND_PRODUCTION_VERIFIED'
assert read(RUN/'production-byte-readback.json')['byte_readback']=='PASS'
assert read(RUN/'live-search-evidence.json')['overall']=='PASS'
assert read(RUN/'remote-main-readback.json')['overall']=='PASS'
write(RUN/'run-result.json',dict(run_id=RUN.name,started_at=read(RUN/'baseline.json')['started_at'],finished_at=end,overall='INCOMPLETE',confirmed_updates_published=1,new_active_trials=0,new_hidden_public_records=0,new_sources=10,source_receipt={k:v for k,v in receipt.items() if k!='sources'},clinical_fresh_review_gate=dict(fresh_today=0,total_public=152,cumulative_full_review_since_original_cutoff=120,pending_original40=32,blocked_primary_routes=28,remaining_missing_protocol_facts=4),deployment='PASS',loading_regression='PASS',live_searches=read(RUN/'live-search-evidence.json')['cases'],production_bytes='PASS',remote_main_readback='PASS',publication_commit=sha,source_inventory_sha256=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),notes=['One source action not established: Cambridge alias permission scope; not claimed complete.','Strict source evidence76 gaps, independent clinical32 pending, retained separately from technical PASS.','No fresh medical/funding dates inferred from unchanged pages, JSON or passing tests.']))
base='https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/'+rel+'/'
report=f'''**21 октября 2026, 03:00:35–{short}, America/New_York**
**Режим: DAILY GLOBAL WORK AUDIT**
**Итог: INCOMPLETE. NEW: 0 исследований; UPDATE: 1 запись. Изменения опубликованы, production проверен.**

**Новые исследования:** 0 добавлено в активный матчинг. У Midwestern найдено приглашение с бесплатной химиотерапией для собак, но препарат и полный протокол не названы. Это сохранено как кандидат для проверки, без новой активной записи.

**Что исправлено:** у эдинбургского исследования tigilanol tiglate общий европейский список заменён [официальным описанием исследования](https://vet.ed.ac.uk/news/latest-news/2024/drug-trial-studies-plant-based-oral-cancer-therapy-dogs). Критерии, статус и прежняя дата клинической проверки сохранены. У CSU текущая пагинация сошлась: 37/37 объектов; прежнее расхождение счётчика устранено на стороне источника.

**Закрыто или скрыто:** 0. Отсутствие на странице не использовано как доказательство закрытия.

**Новые источники: 10**, все добавлены для наблюдения, без автоматического включения исследований:

| Страна | Источники |
|---|---|
| США | Midwestern University; TheraJan |
| Испания | Aúna; Complutense University veterinary hospital |
| Бразилия | USP / FAPESP — ONVEX |
| Япония | VMDP; лаборатория Mizuno, Yamaguchi; лаборатория Maeda, University of Tokyo |
| Австралия | The Kids Research Institute; University of Adelaide — FiDo |

**Поиск и охват:** обработка очереди — **132/133 источника, 12/12 регионов; незавершённых или неподтверждённых действий исполнителя: 1**. Фактические визиты выполнены для **116/133** источников; 17 не посещены из-за прежних ограничений и не получили новых дат. Единственное неподтверждённое действие — определение допустимости Cambridge alias, без повторения запрещённого маршрута.

Выполнены оба мировых прохода: текущие/недатированные возможности и свежие сигналы за 14–21 октября. Сохранены 86 запросов, 1 174 поисковых ответа и 898 уникальных URL. Использованы английский и местные языки, включая японский, китайский, испанский, португальский, французский и арабский. Выполнены 62 запланированных чтения официальных fallback; ещё 19 маршрутов отмечены как ограниченные. Всего сохранены 330 native-запросов, включая 27 разрешённых transient-повторов, и 44 Web-чтения. Невыполненных обязательных same-URL Web-восстановлений не осталось.

**Что осталось нерешённым:**

| Достаточность evidence | Источников |
|---|---:|
| fully reconciled | 57 |
| partial | 56 |
| unreachable | 3 |
| not checked | 17 |

Из 76 пробелов 75 классифицированы как внешние, 1 — `not_established` по обработке исполнителем. Причины: недостающие сведения о протоколах — 33; ограничения/недоступность источника — 19; исследовательские или навигационные страницы вместо trial roster — 16; неподтверждённая свежесть — 6; неустановленный roster — 2. Три недоступных источника: Anivive, Oklahoma State и Veterinary Oncology Services; разрешённые native/Web-маршруты испробованы.

Отдельные вопросы: у **Kv9** изменились формулировки критериев и исчезла таблица центров; это не подтверждает совместимость с химиотерапией или закрытие площадок. У **TheraJan** одобрение Manassas не подтверждает текущий набор; также сохранён конфликт адресов Stamford. Старые объявления, лабораторные, диагностические и поддерживающие исследования не добавлены как новые лечебные trials. Новых вероятных дублей canonical: 0. Ledger содержит 109 вопросов: 87 унаследованных и 22 новых/уточнённых.

Полная независимая клиническая перепроверка остаётся **INCOMPLETE: 32 записи исходного остатка** — 28 с ограниченным primary-маршрутом и 4 с недостающими опубликованными сведениями. Сегодня новых полных клинических заключений: 0. Ранее выполненные проверки не выданы за сегодняшние. Ручные действия Юли сейчас не требуются.

**Каталог до → после:**

| Показатель | До | После |
|---|---:|---:|
| canonical | 311 | 311 |
| public matchable | 152 | 152 |
| treatment trials | 148 | 148 |
| other treatment access | 4 | 4 |
| sources | 123 | 133 |

**Технический результат:** среда PASS — Python 3.12.14, Git 2.51.1; обязательные команды реально выполнены. Schema, sanitation, semantic dedupe, matcher logic/selection, build, production-sync, source inventory и проверка evidence keys — PASS. Строгий audit receipt — **INCOMPLETE**, 76 пробелов; gap-review validator — **PASS**, завершение обработки **NOT VERIFIED**. Накопительный полный клинический gate: 120/152; строго за этот запуск — 0/152 новых полных проверок. Дополнительный legacy Streamlit smoke — NOT VERIFIED: модуль не установлен.

Loading regression — **PASS**. Живой поиск Dog / Cancer — any type — **USA PASS: 98; Japan PASS: 10**. Проверены неизвестная достоверность диагноза, пустые age/weight/ZIP, все шесть вариантов лечения и Any approach. Полные отображённые списки совпали с расчётом по текущему каталогу.

Commit публикации в main: [b5966992](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/{sha}). [Deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39566247681) — PASS. Живые HTML, JS и каталог побайтно совпали со сборкой. HTML использует новый каталог `9d048dea595a4a9d`; неизменённый JS сохраняет версию `target-scope-20261018`.

**Даты проверки источников:** previous — 14/17/18/19/20 октября; new — 21 октября только для 116 посещённых источников. У 17 непосещённых даты и результаты сохранены. Например, AVMA: `2026-10-20T03:14:39-04:00` → `2026-10-21T03:11:05-04:00`, результат остаётся partial. Local и remote-main readback — **PASS для всех 133 строк**; SHA-256 inventory: `e3aa53b2684504be25328a0bac85463429040f5fc79b949b08209a078f55c309`.

**Обработка очереди INCOMPLETE: 132/133, одно неподтверждённое действие. Достаточность доказательств INCOMPLETE: 57/133 полностью сверены. Техническая публикация и живой поиск PASS.**

Подробности: [receipt]({base}receipt-final.json), [gap-review]({base}gap-review.json), [поиск и primary-проверки]({base}primary-lead-review.json), [все поисковые ответы]({base}discovery-ledger.json), [клинический остаток]({base}clinical-pending-review.json), [изменённые данные и hashes]({base}change-manifest.json), [команды и validators]({base}validator-summary.json), [даты local/remote]({base}remote-main-readback.json), [production bytes]({base}production-byte-readback.json), [живые USA/Japan]({base}live-search-evidence.json).
'''
(RUN/'report.md').write_text(report)
write(RUN/'report-integrity.json',dict(sealed_at=end,file=rel+'/report.md',sha256=hashlib.sha256(report.encode()).hexdigest(),exact_visible_report_required=True))
checkpoint();print('SEALED',end,'report bytes',len(report.encode()))
