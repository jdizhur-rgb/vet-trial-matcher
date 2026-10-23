"""Seal this run's actual Russian report after deployment and live UI checks."""
from daily23 import ROOT, RUN, read, write, now, checkpoint
import subprocess, hashlib, json, collections

rel=str(RUN.relative_to(ROOT))
receipt=read(RUN/'receipt-final.json')
pub=read(RUN/'publication.json')
sha=pub['main_commit']
assert sha=='9e0d12a77c1b604839830b3203b4754387e39db8'
assert read(RUN/'production-byte-readback.json')['byte_readback']=='PASS'
assert read(RUN/'live-search-evidence.json')['overall']=='PASS'
assert read(RUN/'remote-main-readback.json')['overall']=='PASS'
assert read(RUN/'deploy-final-data.json')['all_completed_success']
assert receipt['processing_complete_total']==142 and receipt['source_total']==143
assert receipt['source_result_counts']==dict(partial=67,fully_reconciled=55,not_checked=18,unreachable=3)
assert read(RUN/'discovery-matrix.json')['regions_with_both_passes']==12
assert read(RUN/'issue-changes.json')['total']==127

logs=[]
commands=[['python','scripts/validate_source_inventory.py'],['python','scripts/validate_audit_receipt.py',rel+'/receipt-final.json'],['python','scripts/validate_audit_gap_review.py',rel+'/gap-review.json','--receipt',rel+'/receipt-final.json'],['python','scripts/check_evidence_keys.py'],['git','diff','--check']]
for c in commands:
 start=now(); p=subprocess.run(c,cwd=ROOT,text=True,capture_output=True)
 logs.append(dict(command=c,cwd=str(ROOT),started_at=start,finished_at=now(),exit_code=p.returncode,output=p.stdout+p.stderr,scope='Final metadata/evidence sealing; no repeated source traversal.'))
 if c[1]=='scripts/validate_audit_receipt.py':
  actual=json.loads(p.stdout);assert p.returncode==1 and actual['status']=='INCOMPLETE' and not actual['errors'] and actual['coverage_gap_count']==88
 else:assert p.returncode==0,(c,p.stdout,p.stderr)
write(RUN/'final-validation.json',logs)

baseline=read(RUN/'baseline.json')
canonical=(ROOT/'data/trials_base.json').read_bytes()
assert canonical==(RUN/'before-trials_base.json').read_bytes()
source_bytes=(ROOT/'data/source_inventory.json').read_bytes()
dates=read(RUN/'remote-main-readback.json')['rows']
assert sum(r['opened_this_run'] for r in dates)==125
assert sum(r['previous_last_checked']=='2026-10-22' and r['new_last_checked']=='2026-10-23' for r in dates)==123
assert sum(r['previous_last_checked'] is None for r in dates)==2
assert all(r['previous_last_checked']==r['new_last_checked'] and r['previous_last_checked_at']==r['new_last_checked_at'] for r in dates if not r['opened_this_run'])
end=now();short=end[11:19]
write(RUN/'run-result.json',dict(run_id=RUN.name,started_at=baseline['started_at'],finished_at=end,finish_scope='Audit, data publication, production verification and report sealing; subsequent report artifact delivery is separately verified.',overall='INCOMPLETE',new_canonical_records=0,confirmed_existing_watch_activations_published=0,new_hidden_public_records=0,new_sources=2,source_receipt={k:v for k,v in receipt.items() if k!='sources'},clinical_fresh_review_gate=dict(fresh_today=0,total_public=151,cumulative_full_review_since_original_cutoff=119,pending_original40=32),deployment='PASS',loading_regression='PASS',live_searches=read(RUN/'live-search-evidence.json')['cases'],production_bytes='PASS',remote_main_readback='PASS',publication_commit=sha,source_inventory_sha256=hashlib.sha256(source_bytes).hexdigest(),canonical_sha256=hashlib.sha256(canonical).hexdigest(),before=baseline['counts'],after=dict(canonical=311,public_matchable=151,treatment_trials=147,other_treatment_access=4,sources=143),notes=['One unconfirmed executor source action: Cambridge alias permission scope.','88 strict source gaps:87 external blockers and1 not established.','Independent full clinical review119/151, original32pending preserved; zero new full medical signoffs today.','No clinical dates, open recruitment or site changes inferred from old cases, JSON or mechanical test success.']))

base='https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/'+rel+'/'
report=f'''**23 октября 2026, 03:05:10–{short}, America/New_York.**
Режим: **DAILY GLOBAL WORK AUDIT**. Итог: **INCOMPLETE**. NEW: 0 активных исследований, 2 официальных источника. UPDATE: evidence, даты фактических посещений и техническая сводка. Изменения опубликованы; deploy и production — PASS.

**1. Новые исследования**

В активном подборе — **0**.

Новый кандидат для наблюдения: **FAM-010, Familiar Therapeutics / University of Illinois, Urbana, США** — собаки с гемангиосаркомой селезёнки после операции; доксорубицин, связанный с альбумином. Индивидуальная [официальная страница](https://familiartx.com/studies/fam-010), обновлённая 15 октября, говорит **ENROLLING SOON**; открытый приём пока не подтверждён. Спонсор оплачивает исследовательское обследование, лечение и последующее наблюдение; проезд оплачивает владелец. Покрытие предшествующей спленэктомии не установлено. Запись в подбор не добавлена.

**2. Что исправлено**

- Изменений лечебных записей canonical — **0**. Исправлена техническая сводка `audit_state`: у сегодняшнего run_id оставались счётчики и ссылки на receipt от 20 октября; теперь она соответствует фактическому receipt 23 октября.
- PetTrials Australia разобран полностью: **7/7** объявлений; VetTrials — **293/293** объектов, включая 102 онкологических записи разных статусов. Будущий набор, диагностические исследования и обновления вторичного реестра не превращены в новые доступные лечебные trials.
- Для Calusa/UConn уточнено: исследование ASO при лимфоме собак; бесплатность опубликована для конкретного пациента. Открытый набор, точный препарат и общие расходы всех участников не подтверждены.
- Сбой AVMA зафиксирован как неизвестный текущий roster: ошибки страниц/API и недостаточный Web-readback. Отсутствие полученных объектов не принято за ноль исследований или закрытие прежних записей.

**3. Закрыто или скрыто; новые источники**

Закрыто или скрыто — **0**. Предыдущие решения о скрытии сохранены.

Новые источники — **2**: [Familiar Therapeutics](https://familiartx.com/) — США; [CimCure](https://cimcure.com/news/) — Нидерланды. У CimCure подтверждены исторические ветеринарные исследования вакцины eVim; текущий набор собак/кошек и расходы владельца не опубликованы. Нынешние сообщения о человеческих trials отдельно квалифицированы.

**4. Поиск и охват**

**Обработка очереди: 142/143 источника, 12/12 регионов; незавершённая или неподтверждённая работа исполнителя: 1.** Фактические посещения — **125/143**. Для 18 непосещённых источников сохранены прежние ограничения доступа и даты; один из них, Cambridge, не признан завершённым.

Проверены разрешённые master/fallback и необходимые индивидуальные протоколы. Сохранены **329 shell-запросов** к источникам/протоколам, включая 22 transient-повтора, и **37 Web-чтений**; обязательных незавершённых same-URL Web-проверок после обычных транспортных ошибок — **0**. Явные запреты доступа не обходились.

Выполнены оба discovery-прохода: текущие/недатированные возможности и свежие сигналы **16–23 октября**. Всего **97 запросов, 1 047 результатов, 777 уникальных нормализованных URL**. Охвачены США, Канада, Великобритания, континентальная Европа, Латинская Америка/Карибы, Австралия/Новая Зеландия, Восточная, Южная и Юго-Восточная Азия, Ближний Восток, Северная Африка и Африка южнее Сахары. Использованы английский и местные языки, включая японский, китайский, корейский, французский, немецкий, испанский, португальский, хинди, тайский, малайский, индонезийский, вьетнамский, иврит, турецкий, арабский и африкаанс. Это выполненная поисковая матрица, а не доказательство отсутствия иных мировых исследований.

**5. Что осталось нерешённым**

| Достаточность evidence | Источников |
|---|---:|
| fully reconciled | 55 |
| partial | 67 |
| unreachable | 3 |
| not checked | 18 |

Строгий receipt: **INCOMPLETE**, 0 ошибок структуры, **88 пробелов**. Из них **87 — external_blocker**, **1 — not_established**, учтённый в незавершённой работе исполнителя. Cambridge: не установлено, допускается ли обращение к alias `/node/2971` после прежнего запрета; маршрут не использован для обхода ограничения.

Категории пробелов: вопросы конкретных протоколов — **42**; источник discovery не является roster trials — **16**; недоступность официальных маршрутов — **23**; roster не установлен — **2**; свежесть не подтверждена — **5**. Для каждой строки сохранены вопрос, URLs/evidence и следующий допустимый шаг. Справочники, новости и pipeline не объявлены недоступными лишь потому, что не публикуют полный recruiting roster.

Отдельный клинический остаток: полная независимая проверка подтверждена для **119/151** публичной записи; прежние **32** незакрытых вопроса сохранены. Сегодня новых полных клинических sign-off — **0**. Всего unresolved — **127**: 117 прежних и 10 новых; прежние сроки повторной проверки сохранены. Отсеян **521 поисковый URL** как нерелевантный, исключённый тип материала или ссылка на собственный сайт. Вероятных семантических дублей в лечебном каталоге — **0**.

**6. Каталог до → после**

| Показатель | До | После |
|---|---:|---:|
| Canonical | 311 | 311 |
| Public matchable | 151 | 151 |
| Treatment trials | 147 | 147 |
| Other treatment access | 4 | 4 |
| Sources | 141 | 143 |

**7. Технический результат**

Среда — **PASS**: реально выполнены `pwd`, `python --version` — Python 3.12.14, `git --version` — Git 2.51.1. Schema, sanitation, semantic dedupe, source validator, сборка, matcher logic/selection и production-sync — **PASS**. Loading regression — **PASS**, включая ранний поиск, задержанную загрузку USA/Japan и отказ загрузки. Gap-review validator — **PASS**; подтверждение полноты обработки — **NOT VERIFIED**. Полный клинический gate — **INCOMPLETE**, отдельно от технических тестов.

Опубликованное состояние данных main: [`{sha}`](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/{sha}); исходный main — `b9a12fe7ec54557108c01a36b9edcc25e2d00c2b`. [Deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39923765520) и две сопутствующие проверки GitHub — **PASS**. Production HTML/JS/catalog совпали со сборкой побайтно. В HTML подтверждён `matcher.js?v=clinical-gi-20261022`; JS и публичный каталог сегодня не менялись, их версии сохранены.

Реальный поиск после deploy — **USA 97/97, Japan 10/10: PASS**. Проверены Dog / Cancer — any type, diagnosis certainty I don't know, пустые age/weight/ZIP, все шесть вариантов лечения, Any approach. Сравнены полные отображённые наборы карточек, а не только числа или наличие JSON; ожидаемые результаты рассчитаны из текущего каталога.

**8. Даты проверки источников и итог**

Для **123** посещённых прежних источников даты изменены **22 → 23 октября**; для двух новых — **нет → 23 октября**. У **18** непосещённых даты и timestamps сохранены. Неуспешные попытки не получили успешный результат. Local/remote-main readback — **PASS** на `{sha}`, все 143 строки дат/результатов совпали. SHA-256 inventory: `2d7233088f52c32d3d357affab63247636058cf59029999c1ae68828bdbf3860`.

**Итог обработки очереди — INCOMPLETE: 142/143, одно неподтверждённое действие. Итог достаточности доказательств — INCOMPLETE: 88 пробелов источников; клинический остаток указан отдельно.**

Подробности: [receipt]({base}receipt-final.json), [gap-review]({base}gap-review.json), [поиск и языки]({base}discovery-matrix.json), [квалификация результатов]({base}discovery-ledger.json), [primary-проверки]({base}primary-lead-review.json), [клинический остаток]({base}clinical-pending-review.json), [изменения и hashes]({base}change-manifest.json), [исправление сводки]({base}state-summary-correction.json), [команды и validators]({base}validator-summary.json), [финальные проверки]({base}final-validation.json), [даты local/remote]({base}remote-main-readback.json), [production bytes]({base}production-byte-readback.json), [живые USA/Japan]({base}live-search-evidence.json), [timestamps и итог]({base}run-result.json).

Точный текст: [report.md](sandbox:{RUN}/report.md).
'''
(RUN/'report.md').write_text(report)
write(RUN/'report-integrity.json',dict(sealed_at=end,file=rel+'/report.md',sha256=hashlib.sha256(report.encode()).hexdigest(),exact_visible_report_required=True))
checkpoint()
print('SEALED',end,'report bytes',len(report.encode()),'source evidence INCOMPLETE; production PASS')
