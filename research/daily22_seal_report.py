"""Seal this run's visible Russian report and factual final evidence."""
from daily22 import ROOT,RUN,read,write,now,checkpoint
import subprocess,hashlib,json
from datetime import datetime
rel=str(RUN.relative_to(ROOT));logs=read(RUN/'validators.json')
for c in [['python','scripts/validate_source_inventory.py'],['python','scripts/validate_audit_receipt.py',rel+'/receipt-final.json'],['python','scripts/validate_audit_gap_review.py',rel+'/gap-review.json','--receipt',rel+'/receipt-final.json'],['python','scripts/check_evidence_keys.py'],['git','diff','--check']]:
 at=now();p=subprocess.run(c,cwd=ROOT,text=True,capture_output=True);logs.append(dict(command=c,cwd=str(ROOT),started_at=at,finished_at=now(),exit_code=p.returncode,output=p.stdout+p.stderr,scope='Final evidence/report sealing; no source re-traversal.'))
write(RUN/'validators.json',logs);write(RUN/'validator-summary.json',{' '.join(r['command']):r for r in logs})
pub=read(RUN/'publication.json');receipt=read(RUN/'receipt-final.json');end=now();short=datetime.fromisoformat(end).strftime('%H:%M:%S');sha=pub['main_commit'];base='https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/'+rel+'/'
assert pub['status']=='PUBLISHED_AND_PRODUCTION_VERIFIED'
assert read(RUN/'production-byte-readback.json')['byte_readback']=='PASS'
assert read(RUN/'live-search-evidence.json')['overall']=='PASS'
assert read(RUN/'remote-main-readback.json')['overall']=='PASS'
write(RUN/'run-result.json',dict(run_id=RUN.name,started_at=read(RUN/'baseline.json')['started_at'],finished_at=end,overall='INCOMPLETE',confirmed_existing_watch_activations_published=1,new_canonical_records=0,new_hidden_public_records=0,new_sources=8,source_receipt={k:v for k,v in receipt.items() if k!='sources'},clinical_fresh_review_gate=dict(fresh_today=1,total_public=151,cumulative_full_review_since_original_cutoff=119,pending_original40=32),deployment='PASS',loading_regression='PASS',live_searches=read(RUN/'live-search-evidence.json')['cases'],production_bytes='PASS',remote_main_readback='PASS',publication_commit=sha,source_inventory_sha256=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),notes=['One unconfirmed source action: Cambridge alias permission scope; not claimed complete.','Strict source evidence86 gaps and original clinical32 pending are separate from technical PASS.','No fresh clinical/funding dates inferred from unchanged pages, old cases, JSON or tests.']))
report=f'''**22 октября 2026, 03:05:31–{short}, America/New_York.**
**Режим: DAILY GLOBAL WORK AUDIT. Итог: INCOMPLETE.** Новых canonical ID: **0**; активирована **1** существующая запись наблюдения. Изменение опубликовано, production проверен.

**Новые исследования:** **1 новая возможность для подбора** — University of Missouri, Columbia, США: [облучение всей брюшной полости с последующей COP/doxorubicin-химиотерапией](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/) для кошек с высокозлокачественной/крупноклеточной желудочно-кишечной лимфомой, ограниченной брюшной полостью. Требуются отсутствие прежней химиотерапии, отрицательные FeLV/FIV и возможность анестезии. Исследование оплачивает облучение и предоставляет **кредит $1000 в VHC после облучения**. Покрытие обследования, химиотерапии, прочего лечения и поездок не опубликовано. Новый ID не создан: активирована прежняя watch-запись этого же протокола.

**Что исправлено:** **1 запись** Missouri получила подтверждённый набор, критерии, расходы и ограничения подбора. Добавлены девять проверок поведения матчера по первичному протоколу; обновлены создаваемая из правил таблица JS и версия скрипта. Новая возможность реально появилась в поиске кошек на production.

**Закрыто или скрыто:** **0**. Прежние решения по CMP002 и Ghent сохранены. Завершение двух Paccal-исследований подтверждено повторно; они уже были скрыты.

**Новые источники: 8:** JASMINE — Япония; Gongwin — Тайвань; Nowon Animal Medical Center — Южная Корея; ICAR-IVRI — Индия; Australian Animal Cancer Foundation — Австралия; USP FMVZ — Бразилия; Calusa/UConn — США; Pet Trial Finder — вторичная международная площадка. Источники добавлены для дальнейших проверок; их сигналы не стали автоматически активными trials.

**Поиск и охват:** обработка очереди — **140/141 источника, 12/12 регионов; неподтверждённых действий исполнителя в очереди: 1**. Все исходные **133** источника сохранены. Фактические визиты выполнены для **124/141**; у 17 непосещённых источников сохранены прежние ограничения и даты. Для Cambridge остаётся вопрос допустимости alias-маршрута; запрещённый маршрут не повторялся.

Выполнены оба мировых прохода: текущие/недатированные возможности и свежие сигналы **15–22 октября**. Сохранены **78 поисковых запросов, 612 ответов, 450 уникальных URL**. Использованы английский и местные языки, включая японский, китайский, корейский, французский, немецкий, испанский, португальский, хинди, тайский, индонезийский, малайский, арабский и турецкий. Пройдены 70 предусмотренных native-fallback URL; 19 маршрутов отмечены как ограниченные. Всего: **432 native-запроса**, включая 142 разрешённых transient-повтора, и **75 Web-чтений**. Невыполненных обязательных same-URL Web-восстановлений не осталось. Новые primary-сигналы и их пробелы квалифицированы отдельно; мировой поиск не объявлен исчерпывающим перечнем всех сайтов.

**Что осталось нерешённым:**

| Достаточность evidence | Источников |
|---|---:|
| fully reconciled | 55 |
| partial | 66 |
| unreachable | 3 |
| not checked | 17 |

Из **86 пробелов**: 85 имеют документированные внешние причины; 1 — `not_established` по обработке исполнителем. Причины: неопределённость протокола — 36; ограничения/недоступность — 22; исследовательская или навигационная страница вместо trial roster — 17; неподтверждённая свежесть — 8; неустановленный roster — 3. Справочники и pipeline не оценивались как обязанные публиковать полный recruiting roster.

Отдельно сохранены вопросы о текущем наборе JASMINE, точном препарате и доступе Gongwin, протоколах Nowon и Calusa/UConn. Индийский документ подтверждает исследовательский проект, но набирает сотрудников. Свежая публикация по STING-терапии четырёх собак принята **19 октября 2026**; текущий доступ владельцев к лечению не подтверждён. Новая Penn-страница описывает визуализацию краёв опухоли при операции и исключена по treatment-only правилу. Вероятных дублей canonical — **0**; ledger нерешённых вопросов — **117**: 109 прежних и 8 новых.

Независимая полная клиническая перепроверка остаётся **INCOMPLETE: 119/151**, остаток **32 записи**. Сегодня выполнена одна новая полная проверка — Missouri, вне исходного остатка 40. Прежние проверки и тесты не выданы за сегодняшние медицинские заключения. Семь публикационных сигналов сохранены без подтверждённого текущего доступа. Ручные действия Юли сейчас не требуются.

**Каталог до → после:**

| Показатель | До | После |
|---|---:|---:|
| canonical | 311 | 311 |
| public matchable | 150 | 151 |
| treatment trials | 146 | 147 |
| other treatment access | 4 | 4 |
| sources | 133 | 141 |

**Технический результат:** среда **PASS** — Python 3.12.14, Git 2.51.1; `pwd`, проверки версий и обязательные команды реально выполнены. Schema, sanitation, semantic dedupe, matcher logic/selection, build, production-sync, source inventory и evidence-key checks — **PASS**. Строгий audit receipt — **INCOMPLETE**, структурных ошибок 0; gap-review validator — **PASS**, завершение обработки **NOT VERIFIED**. Дополнительный legacy Streamlit smoke — **NOT VERIFIED**: модуль не установлен.

**Loading regression — PASS. Live USA — PASS: 97; Japan — PASS: 10.** Проверены Dog / Cancer — any type, diagnosis certainty I don't know, пустые age/weight/ZIP, все шесть вариантов лечения и Any approach. SHA-256 полного состава отображённых названий и центров совпал с расчётом по текущему каталогу.

Commit публикации данных: [5f803cc9346a773f40ef8811b97dcc3ebe508bfb](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/{sha}). Все шесть workflows — PASS; [deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39744844468) — PASS. Живые HTML, JS и каталог побайтно совпали со сборкой. HTML содержит `matcher.js?v=clinical-gi-20261022` и каталог версии `345fb1c23f98484d`.

**Даты проверки источников:** у 116 прежних посещённых источников **21 → 22 октября**, у 8 новых **null → 22 октября**. У 17 непосещённых сохранены даты 14/17/18/19 октября. Local и remote-main readback — **PASS для всех 141 строк** на SHA публикации выше. SHA-256 inventory: `eed6bc301f99599afbf4090a199a26c9a508f1f50dcd9ef0506e75e9fe3047d1`.

**Обработка очереди INCOMPLETE: 140/141, одно неподтверждённое действие. Достаточность доказательств INCOMPLETE: 55/141 полностью сверены. Публикация и живой поиск PASS.**

Подробности: [receipt]({base}receipt-final.json), [gap-review]({base}gap-review.json), [мировой поиск]({base}discovery-ledger.json), [primary-проверки]({base}primary-lead-review.json), [клинический остаток]({base}clinical-pending-review.json), [изменения и hashes]({base}change-manifest.json), [команды и validators]({base}validator-summary.json), [даты local/remote]({base}remote-main-readback.json), [production bytes]({base}production-byte-readback.json), [живые USA/Japan]({base}live-search-evidence.json), [отчёт]({base}report.md).
'''
(RUN/'report.md').write_text(report);write(RUN/'report-integrity.json',dict(sealed_at=end,file=rel+'/report.md',sha256=hashlib.sha256(report.encode()).hexdigest(),exact_visible_report_required=True));checkpoint();print('SEALED',end,'report bytes',len(report.encode()))
