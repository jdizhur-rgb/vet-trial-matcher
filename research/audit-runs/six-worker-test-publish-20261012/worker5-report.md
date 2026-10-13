# Исполнитель 5: ограниченный discovery Massachusetts, New Hampshire, Ontario

База: актуальный remote main `7c9b55485b3f0d1cb225c9d1143126c0318ef765`. Независимый исполнитель `/root/discovery_na`; numeric UUID инструменты не выдали. Начальный фактический замер часов: 2026-10-13 02:43:04 UTC, после чтения первых инструкций. Все проверки страниц выполнены 13 октября UTC / вечером 12 октября America/New_York. Reader не сообщает точные секунды посещения сайта: дата проверки и crawl metadata не подменяются временем интеграции.

Назначенных clinical/tele IDs: **0**, processed **0**, fully verified **0**. Это discovery, его результаты не увеличивают знаменатель 20 назначенных записей остальных исполнителей.

| Территория | Фактические запросы | Рассмотренные релевантные результаты* | Кандидаты с проверкой официальных маршрутов | Подтверждённое текущее локальное лечение | NEW / UPDATE / DUPLICATE / UNRESOLVED |
|---|---:|---:|---:|---:|---|
| Massachusetts | 5 | 13 | 3 | 1 | 1 / 0 / 0 / 2 |
| New Hampshire | 7 | 6 | 2 | 1 | 0 / 0 / 1 / 1 |
| Ontario | 5 | 10 | 3 | 2 | 2 / 0 / 0 / 1 |
| Всего | 17 | 29 | 8 | 4 | 3 / 0 / 1 / 4 |

\* Отдельные релевантные URL/title/snippet leads, фактически рассмотренные, без повторов. Это не все поисковые hits и не количество открытых страниц. Search tool объединяет результат batch: `queries.json` честно фиксирует этот способ атрибуции. По каждой территории выполнены и недатированный/текущий поиск провайдеров, и отдельный поиск открытия/новых услуг. GP/mobile покрывались дополнительными запросами. Международный/национальный охват не заявляется.

## Три подтверждённых отсутствующих физических филиала

**Bay State Veterinary Emergency and Specialty Services, Swansea MA.** В supplied full catalog нет отдельной карточки Swansea, хотя уже есть sister hospital Ocean State в East Greenwich RI и её заметка о направлении в Bay State. Это разные физические филиалы. Официальные service, team и contact страницы подтверждают 463 Swansea Mall Drive, Swansea MA 02777, 508-379-1233; Amy Koterbay с literal BVMS, MS, DACVIM / oncology и Kevin Ware с literal DVM, ACVR-RO / radiation oncology. На местной service page есть routinely administered chemotherapy и installed Varian Edge photon/electron radiation, иммунологические лекарства и melanoma vaccine без подтверждённого бренда. Рекомендация: NEW физический филиал; не добавлять хирургическую онкологию из общего списка хирургов и их интересов; 24-hour emergency не превращать в часы oncology. [service](https://www.bsvess.com/oncology/) · [team](https://www.bsvess.com/veterinary-specialists/) · [contact](https://www.bsvess.com/contact/).

**Ottawa Animal Emergency & Specialty Hospital, Ottawa ON.** 1155 Lola Street, Ottawa ON K1K 4C1, 613-745-0123. Текущий named medical oncologist Charles Boisclair DVM, MSc, DACVIM (Medical Oncology). Прямое подтверждение местного IV/oral chemotherapy, home medications и palliation. Referred new cases — 1-hour consultation; при показаниях выбранное лечение может начаться в тот же день. Surgery направляется к surgeon, radiation/ECT — в Montreal; эти внешние маршруты не включены в местные filters. Рекомендация NEW. [service/team](https://oaesh.com/specialty-services/oncology/) · [referral/contact](https://oaesh.com/contact/referring-vets/).

**King Animal Hospital, King City ON.** 1265 19th Sideroad, King City ON L7B 1K5, 1-888-622-7345; specialty referral appointments Mon–Fri 8 am–8 pm, Oncology@kinganimalhospital.com. Текущий oncology roster — Sarah Laliberté, literal DVM, DVSC, ACVIM, title board-certified veterinary oncologist; acronym не расширен самовольно до другого написания. Local chemotherapy, targeted therapy, immunotherapy подтверждены branch page. Tumor-removal surgery описана, но специализированный surgical oncology credential не присвоен. Рекомендация NEW. [service](https://www.kinganimalhospital.com/oncology/) · [team](https://www.kinganimalhospital.com/our-team/) · [contact](https://www.kinganimalhospital.com/contact-us/).

## Остальные проверенные кандидаты

- **Acoaxet, Westport MA — UNRESOLVED.** Действующий официальный branch, адрес, phone, team, ABVP credential и booking подтверждены. Oncology page содержит generic explanatory NVA wording одновременно о radiation и chemotherapy. Этого недостаточно, чтобы присвоить достоверный local chemotherapy/radiation filter; ABVP не является oncology certification. Доступные service/team routes прочитаны, а Grossi biography reader не открылся. Следующий вопрос: кто здесь реально вводит injectable chemotherapy и какие услуги выполняются локально? [service](https://www.acoaxetvet.com/services/oncology) · [team](https://www.acoaxetvet.com/staff).
- **Watertown Animal Hospital MA — UNRESOLVED.** Current official page называется Chemotherapy Referrals and Cancer Treatment; 404 Main Street, Watertown MA 02472, 617-926-8888. Общая дискуссия лечения не подтверждает local chemotherapy. Перечисленные ниже emergency referral destinations нельзя принять за oncology treatment в этом филиале. Новая confirmed treatment card не предлагается. [official page](https://watertownanimalhospitalma.com/services/chemotherapy-and-cancer-treatment/).
- **VCA Lakes Region, Laconia NH — UNRESOLVED.** Лид внешнего старого directory говорит о chemotherapy. Current official branch/team/service/advanced-care/visit routes реально прочитаны: 1266 Union Avenue, Laconia NH 03246, 603-524-8387, current GP roster. Chemotherapy не подтверждена; её отсутствие не утверждается. Shared team с VCA Laconia — не доказательство переносимости услуг. Прямая guessed chemo URL не открылась; реальные опубликованные пути исчерпаны. [branch](https://vcahospitals.com/lakes-region) · [team](https://vcahospitals.com/lakes-region/team) · [advanced care](https://vcahospitals.com/lakes-region/services/advanced-care).
- **Port City NH — DUPLICATE.** Поисковые новости о radiation launch 2025 проверены по current official radiation page: местная Elekta Versa HD, IMRT/SRT/VMAT/IGRT и Maegan Watson-Skaggs. Всё уже есть в baseline, включая Radiation oncology; новое предложение не создано. Это проверка discovery-лида, не повторный полный hospital audit. [current radiation](https://www.portcityvet.com/services/radiation-oncology).
- **OVC Mona Campbell Centre, Guelph ON — UNRESOLVED.** Отсутствует в supplied care/inventory, official indexed service/contact/referral leads найдены. Direct service/master/contact/team/FAQ/PDF routes дали 403/reader errors; shell fallback тоже 403. University faculty URL дал empty one-line reader shell. Indexed snippets не объявлены текущей проверкой локальных услуг, поэтому active addition не предлагается. [official service lead](https://www.ovchsc.ca/animal-cancer-care-services/chemotherapy/).

## Остаток и ограничения

Шесть дополнительных leads сохранены с URL в `queries.json`/ `result.json`: historical VCA Boston Road MA (проверить современную идентичность), Toronto Animal Health Partners, Lakeshore Animal Health Partners, MOVEH, Belleway GP и Morgan GP (последние пять Ontario). Их search results рассмотрены, но полный official branch/team/contact pass не выполнен: это явный **unprocessed remainder**, не подтверждённые NEW и не external blockers.

У восьми выбранных кандидатов семь успешно прочитанных official sites; четыре current local treatment confirmations, из них три достаточно полных NEW proposals. У OVC direct source proof недостаточно. Остальные source helper errors локализованы и описаны; доступные альтернативы прочитаны. Не получено доказательств отсутствия лечения или закрытия ни одной практики.

Полный каталог сравнения: 439 physical/mobile care rows, 511 care inventory rows, 60 remote service rows. Сравнение по текущим именам, domains, addresses/географии и ID/history; preliminary candidate keys не выдаются за existing source IDs. Trial inventory не открывался.

## Доказательства и предложения

В `evidence.json` короткие exact quotes, official URLs, actual tool refs, branch scope, дата и честная основа времени. `proposed_changes.json` содержит три NEW-кандидата с `source_id:null`, `existing_id:false`, `old_value:null` и объяснением отсутствия baseline counterpart; отдельно восемь кандидатских решений. Никаких canonical edits, commits, push, deployment, UI, outreach, paid API или собственных subagents.

Следующий discovery-пакет можно оставить в пределах **трёх территорий, максимум трёх глубоких кандидатов на территорию**. В Ontario уже пять явных оставшихся лидов, поэтому дать Канаде следующий приоритет. Увеличивать до полного national/global sweep из этого ограниченного результата нельзя. Тест публикации не выполнялся; готовность weekly системы не заявляется.

Сохранение отчёта и предложений в долговечное хранилище выполняет главный интегратор; worker scratch files сами по себе не являются durability proof.
