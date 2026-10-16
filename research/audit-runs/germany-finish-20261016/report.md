# Германия: полный итог доступного прохода 16 октября 2026

Доступный конечный проход завершён. **Опубликованы 55 новых физических мест лечения,2 новых дистанционных сервиса и 1 содержательное обновление существующей клиники.** Это не 58 новых клиник. В Германии каталог меняется с **165 до 220 физических мест**, глобально с 827 до 882; дистанционный каталог с 62 до 64 сервисов.

Страна **не объявляется полностью проверенной без остатка**: обязательные сведения по 39 из 87 ранее именованных кандидатов не достигли порога публикации. Из них 9 затронуты автоматическими отказами чтения результатов,1 ограничен реальным 403,3 недоступны обычными методами,26 имеют конкретные недостатки доступных первичных сведений. Проверенные результаты публикуются только после этого конечного прохода и проверки diff. Публикация подтверждена main data SHA7a01ccdbec5e2a51074dedeed2fa3512e1216cc1, успешным deployment и побайтовым чтением обеих production страниц; квитанция publication-receipt.json. Документальные последующие commits не меняют этот SHA развёрнутых данных.

## Что фактически проверено

В явном разрешённом списке доказательств 210 записей обращений к 209 уникальным URLs:196 читаемых ответов 200,1 пустой ответ,12 HTTP ошибок,1 транспортный сбой. Это маршруты источников, не число клиник.202 записи имеют фактический timestamp обращения;8 восстановлены из ранее успешно сохранённого raw без точного времени запроса. Дата 16 октября и фактическое время сохранения остаются отдельно. Повторная сборка не обновляет дату визита. Содержимое двух запрещённых результатов batch25 / named-finite-last-nine не использовалось и не включено в резервные копии.

Рассмотрены все 87 старых именованных кандидатов:47 физических NEW,1 remote NEW,26 отложены по недостаточности первичного подтверждения,9 заблокированы автоматической проверкой,1 реальным ограничением сайта,3 недоступны. Отдельно добавлены 4 ранее готовых Schleswig-Holstein и 4 новых физических результата национального sweep; Cristina Popa — второй remote результат вне 87.87 dispositions сохранены построчно, а не заменены счётчиком успешных GET.

## Национальное покрытие и пределы

| Направление | Выполнено | Точный предел |
|---|---|---|
| Все 16 земель | Новый немецкоязычный sweep в national-01…04-search.json; сохранены текущие/недатированные и новые сигналы, использована прежняя региональная/городская карта | Поиск не доказывает актуальность лечения; новые результаты включены только после собственных клинических страниц |
| Города | Унаследованный набор 21 крупного города и новые городские результаты в 16 региональных запросах, включая независимые GP | Не выдаётся за перечень каждого неизвестного GP страны |
|5 университетов | LMU, TiHo, JLU, FU прочитаны по доступным официальным страницам; Leipzig обязательные clinical/contact маршруты фактически 502 и same-URL Web502 | У FU подтверждён текущий отдел oncology/contact, но общий отдел не расширяет подтверждённые модальности; у Leipzig сохраняется внешняя clinical-gap |
| Сети и ветви | Сверены именные ветви Evidensia/AniCura по доступным собственным clinical/team/contact источникам; filu12 ветвей прочитаны полностью | AniCura национальный roster имеет сохранённый 403; нельзя объявлять полный свежий roster. Исторические 837/854 пакетных holds не считаются клиническими проверками. У 12 filu общая tumor surgery не распределена по ветвям |
| GP, хирургия, химиотерапия | Обычная практика допускается без oncology board; услуги и квалификация проверяются отдельно | Generic Surgery и справочник Patella не подтверждают cancer surgery; chemo не копируется из объяснений/направления в другую клинику |
| RT/ECT | Отдельный просмотр текущих университетских и новых oncology сигналов; NIICE остаётся Surgery-only, chemotherapy/ECT «in Kürze» не активированы | Новых достоверных локальных RT/ECT в этом пакете 0. Dresden и Wasbek прямо направляют на RT вовне; generic laser не RT |
| Выездные/remote | Nestler физический адрес с дополнительными выездами; VetOnkologie и HaustierDocs подтверждены как дистанционные | Anke Wendel — consiliary listing без полного самостоятельного intake; Callavet held. Адрес партнёра/регистрации не становится кабинетом лечения |

При одинаковом пороге ограниченная карточка Local oncology care допустима для Preetz, Bockenheim и Britta Richter: текущая собственная клиническая услуга, ветеринар, адрес, связь и запись подтверждены. Специфические Chemotherapy/Surgery не присваиваются. Schafflund получает только Surgery по явному направлению операций из Tarp в главную практику и её операционным; Tarp не получает эти услуги автоматически.

## Почему предыдущая работа не заканчивалась

1. Сохранившийся frontier смешивал клиники и справочные маршруты: из 333 URLs только 28 относились к clinical/provider routes.305 справочных/неклинических маршрутов увеличивали счётчики без решения вопроса местного лечения.
2. По 87 кандидатам было 54 unresolved и 33 identity-only. Профессиональные справочники восстанавливали личность, но не утраченные clinical payloads.61 потерянный clinical payload и поля 11 Trier updates нельзя объявлять восстановленными по snippets.
3. У старых автоматических отказов 837/854 сохранилась ретроспектива, но не исходный stated reason и не полная исходная очередь. Это реальная потеря scope/доказательств, а не установленный технический reset. Новое адресное разрешение пользователя позволило заново читать клинические источники; реальный 403 не исчез от разрешения.
4. Первый новый парсер останавливался на пустом HTML. Успешные raw первых запросов сохранились, точные timestamps части запросов нет. Исправлено инкрементальное сохранение и обработка пустого тела; недостающие времена не придуманы.
5. Смешанные пакеты с маршрутами AniCura были остановлены автоматической проверкой при опросе процесса. Это задержало и соседние независимые targets. Их результаты не использованы; последующая работа продолжена только по другим разрешённым источникам. Отчёт фиксирует это как blocker, а не как «все сайты недоступны».
6. Публикация и цикл проверки раньше подменяли окончание поиска. Здесь сначала завершены доступные именные и национальные направления, затем сформирован минимальный field diff и отдельная publication branch. Неподтверждённое осталось в research.

## Проверенные новые физические места

| Название | Город | Подтверждённые услуги | Официальный клинический источник |
|---|---|---|---|
| Kleintierpraxis Eckernförde – Dr. med. vet. Eva Brockhaus | Eckernförde | Surgery | https://kleintierpraxis-brockhaus.de/leistungen/ |
| Tierärztin Karin Rieckhoff – Fachpraxis für Kleintiere und Zahnheilkunde | Rendsburg | Surgery | https://www.fachtierarzt-rendsburg.de/seite/697815/leistungen.html |
| Nestler Mobile Tierärzte | Dohna | Surgery | https://www.tierarzt-nestler.de/ |
| 5-E Tierarztpraxis Thomas Backhaus | Thalfang | Surgery | https://www.tierarztpraxis-thomasbackhaus.de/ |
| Fachtierärztliche Praxis Dr. Peter Beck | Rossach | Chemotherapy | https://www.dr-beck.com/ |
| Kleintierpraxis Stauferland | Rechberghausen | Surgery | https://www.kleintierpraxis-stauferland.de/leistungen/ |
| Tierarztpraxis Almenhof – Dr. Andreas Haag | Mannheim | Surgery | https://www.tierarzt-in-mannheim.de/leistungen/ |
| Tierarztpraxis Rahnsdorf | Berlin | Surgery | https://tierarztpraxis-rahnsdorf.de/leistungen/ |
| Tierarztpraxis Dr. Volker Janssen | Halle (Westfalen) | Surgery | https://www.tierarzt-janssen.de/de/ |
| Tierarztpraxis Westerhorn | Westerhorn | Surgery | https://www.tierarztpraxis-westerhorn.de/ |
| Tierarztpraxis Dr. Bungartz | Reuth | Surgery | https://tierarztpraxis-bungartz.de/leistungen/kleintiere |
| Kleintierpraxis Dr. Astrid Fritzenschaf | Eggenstein | Surgery | https://www.tierarztpraxis-fritzenschaf.online/leistungen/behandlung/ |
| Tierarztpraxis Schmidl | Bremen | Surgery | https://www.tierarztpraxis-schmidl.de/leistungen.php |
| Tierarztpraxis Rudloff | Elzach | Surgery | https://www.tierarzt-rudloff.de/leistung.html |
| Tierarztpraxis Dr. Jessica Höch | Mühlhausen OT Saalfeld | Surgery | https://tierarztpraxis-hoech.de/ |
| Tierarztpraxis Markus Sliwon | Dormagen (Delrath) | Surgery | https://www.tierarzt-sliwon.de/ |
| Kleintierpraxis Strutz | Schwentinental | Surgery | https://www.kleintierpraxis-strutz.de/onkologie/ |
| Kleintierzentrum Uetersen | Uetersen | Chemotherapy, Surgery | https://www.kleintierzentrum-uetersen.de/leistungen/chirugie |
| Tierarztpraxis Liane Kruse | Österdeichstrich | Surgery | https://www.tierarzt-kruse.de/Leistungen/ |
| Kleintierzentrum am Obermain | Lichtenfels | Chemotherapy, Surgery | https://kleintierzentrumobermain.de/leistungen/onkologie/ |
| Tierarztpraxis Biet & Wanschura | Nagold | Surgery | https://www.biet-wanschura.de/leistungen/chirurgie/ |
| Kleintierpraxis Weimar – Olma & Zeise | Weimar | Surgery | https://www.kleintierpraxis-weimar.de/leistungen |
| Tierarztpraxis Reinhard Seffner | Bremervörde | Surgery | https://www.tierarzt-seffner.de/leistungen/chirurgische-eingriffe |
| Dr. Stief – Tagesklinik für Tiere | Mühlhausen | Chemotherapy, Surgery | https://www.drstief.de/onkologie/ |
| Tierarztpraxis Nicole Hänel | Hartmannsdorf-Reichenau | Surgery | https://tierarzt-haenel.de/leistungen.html |
| Tierarztpraxis in Rondorf | Köln-Rondorf | Surgery | https://www.vet-rondorf.de/leistungen/ |
| Tierarztpraxis Harald Pfeiffer | Murrhardt | Surgery | https://www.tierarztpfeiffer.de/leistungen/kleintierpraxis |
| Tierärztliche Praxis Dres. Arui | Donaueschingen | Surgery | https://www.kleintierpraxis-arui.de/leistungen/ |
| Tierarztpraxis am Rotenbühl | Saarbrücken | Surgery | https://tierarztpraxisrotenbuehl.de/ueber-mich/chirurgie/ |
| Fachtierarztpraxis Dr. Peter Grommelt | Kehl-Kork | Surgery | https://www.tierarztpraxis-grommelt.de/chirurgie/ |
| Kleintierpraxis Alexander Schumacher | Simmerath-Lammersdorf | Chemotherapy, Surgery | https://www.eifel-kleintierpraxis.de/leistungen.html |
| Kleintierpraxis in Arsten | Bremen | Surgery | https://www.tierpfoetchen.de/de/unsere-leistungen |
| Kleintierpraxis Müllheim | Müllheim | Chemotherapy, Surgery | https://www.kleintierpraxis-muellheim.de/leistungen |
| Kleintierpraxis Blankenese | Hamburg-Blankenese | Surgery | https://kleintierpraxis-blankenese.de/chirurgie-operationen/ |
| Tierarztpraxis Hamburg Altona | Hamburg | Surgery | https://www.tierarzt-hh-altona.de/de/unsere-leistungen |
| Tiergesundheitszentrum Bad Birnbach | Bad Birnbach | Surgery | https://tierarzt-badbirnbach.de/leistungen/chirurgie/ |
| Kleintierpraxis Wissenbach | Eschenburg-Wissenbach | Surgery | https://www.kleintierpraxis-wissenbach.de/leistungen/chirurgie/ |
| Tierarztpraxis Itterburg | Eberbach | Surgery | https://www.tierarztpraxis-itterburg.de/portfolio_page/weichteilchirurgie/ |
| Diagnostikzentrum für Kleintiere – Tagesklinik | Dresden | Chemotherapy, Surgery | https://www.tagesklinik-kleintiere.de/leistungen/onkologie/ |
| Tierarztpraxis Hinter den Höfen | Schimberg OT Ershausen | Surgery | https://www.tierarzt-hinterdenhoefen.de/kleintierpraxis.html |
| Tierärztliche Praxis Dr. Theo Schöne & Dr. Birgit Schepp-Schöne | Herborn | Surgery | https://www.tierarztpraxis-herborn.de/leistungen/onkologie |
| Tierarztpraxis Dr. Ammon | Much | Chemotherapy, Surgery | https://tierarztpraxis-ammon.de/onkologie/ |
| Kleintierklinik Wasbek | Wasbek | Surgery, Chemotherapy | https://www.kleintierklinik-wasbek.de/unsere-leistungen/fachgebiete/ |
| Tierarztpraxis Dr. Peter Saur | Garmisch-Partenkirchen | Chemotherapy | https://www.tierarzt-garmisch.com/leistungen/onkologie/ |
| Tierarztpraxis Karl Sewastianiuk | Stockach | Surgery | https://www.tierarzt-bodensee.de/therapien.html |
| Fachtierarztpraxis Grünheide – Ariane Valentin | Grünheide (Mark) | Chemotherapy, Surgery | https://www.tierarztpraxis-valentin.de/unsere-leistungen.html |
| Tierarztpraxis Bramfeld | Hamburg | Surgery | https://tierarztpraxis-bramfeld.de/leistungen/ |
| Kleintierpraxis Preetz / Schellhorn – Dr. Gesine Krefft | Schellhorn | Local oncology care | http://www.kleintierpraxis-preetz-schellhorn.de/leistungen.html |
| Tierarztpraxis Dr. Boris Sülzle | Nortorf | Surgery | http://www.tierarztpraxis-nortorf.de/kleintierpraxis.php |
| Fachtierarztpraxis Dr. Angelika Drensler | Elmshorn | Chemotherapy, Surgery | https://www.tierarzt-drensler.de/leistungen/ |
| Kleintierpraxis Schönberg – Dr. Steffen Sager | Schönberg | Surgery | https://www.tierarzt-schoenberg.de/leistungen/chirurgie |
| Tierarztpraxis an der Elbe – Nicolas Genz | Wedel | Surgery | https://www.tierarztpraxis-elbe.de/chirurgie |
| Tierklinik Bockenheim | Frankfurt am Main | Local oncology care | https://www.tierklinik-bockenheim.de/team-tierklinik-praxisrundgang/onkologie/ |
| Tierarztpraxis im Sonnenschein – Dr. Britta Richter | Handewitt | Local oncology care | https://tierarztpraxisimsonnenschein.de/Leistungen/ |
| Nord-Ostsee Tierärzte – Schafflund | Schafflund | Surgery | https://nordostsee-tieraerzte.de/kleintiere/onkologie |

Ранее готовые Sülzle, Drensler, Sager и an der Elbe используют сохранённые реальные 16 октября clinical excerpts и отдельные профессиональные источники. Они не представлены как вновь прочитанные clinical pages; сохранённое клиническое содержимое частичное. Не перенесены справочные даты на клинические услуги.

## Обновление, дистанционные сервисы и отсутствие изменений

* **Am Westend, Berlin — UPDATE:** существующая Chemotherapy карточка сохранена. Добавлены закрытие 12–17 октября и объявленное открытие 19 октября по Heerstraße18–20,14052Berlin. Текущий адрес не заменён будущим до даты переезда. Телефон/email по объявлению прежние. Источник: https://www.tierarztamwestend.de/ .
* **VetOnkologie / Zweitmeinung Tierarzt — NEW remote:** одна реальная intake identity, Sandra Kühnel-Lawatsch; owner email/phone/video и предварительные документы. EUR220–400 плюс НДС за первичную 30–60 мин, больший объём дороже. https://www.vetonkologie.de/zweitmeinung/ ; https://www.vetonkologie.de/home/ueber-mich/ ; https://zweitmeinung-tierarzt.de/preise . Не создана новая физическая клиника по партнёрам.
* **HaustierDocs / Cristina Popa — NEW remote:** собственная booking страница требует Premium для oncology/second opinion, EUR139.95; WhatsAppvideo или phone, документы заранее. Certificate of Knowledge in Canine and Feline Oncology2025 не превращён в board certification. https://haustierdocs.de/profil/dr-cristina-popa/ .
* **NIICE Potsdam — NO CHANGE:** уже существующая Surgery-only запись, те же «in Kürze» chemo/ECT. Не новый центр и не новая активная модальность.
* **Новые сигналы без публикации:** Hafencity — generic oncology без специфической местной модальности и полного clinical core; Ettlingen и Frankenthal — обсуждение вариантов само по себе не подтверждает местные Chemo/RT; frontier.vet medical-oncology native502 и same-URL Web502. Эти 4 дополнительных national leads не замаскированы под 87 или под новые клиники.

## Именованный остаток 87

Это 39 клинических кандидатных identities, а не 39 необработанных заданий.Ниже финальный ledger является источником точных counts:26 недостаточных,9 autoheld,1 siteheld,3 unreachable. Отложенная публикация не означает, что практика не лечит рак.

| Кандидат | Итог | Конкретный недостающий факт/ограничение |
|---|---|---|
| AniCura Krefeld Saumstraße | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; named-finite-last-nine.json and automatic-rejection-two.json preserve exact scope. No result bodies used. |
| Stockelsdorf | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; batch25 target manifest and new-automatic-rejection.json preserve exact scope. No result bodies used. |
| Bencec Linkenheim-Hochstetten | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; batch25 target manifest and new-automatic-rejection.json preserve exact scope. No result bodies used. |
| Callavet mobile service | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; batch25 target manifest and new-automatic-rejection.json preserve exact scope. No result bodies used. |
| Nord-Ostsee Tarp | REVIEWED_INSUFFICIENT_PRIMARY | Owned site confirms Tarp is small-animal branch; complex operations routed to Schafflund. Group oncology page does not allocate chemotherapy to Tarp. Do not copy main-branch surgery or chemotherapy into Tarp. |
| Düsseldorf Münsterstraße359 | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; batch25 target manifest and new-automatic-rejection.json preserve exact scope. No result bodies used. |
| Stahl Menden | BLOCKED_REAL_SITE | Preserved actual403 restriction on official service URL; no retry or alias. |
| Beyen Hirschberg | REVIEWED_INSUFFICIENT_PRIMARY | Current own veterinarian/contact/owner pages and full service home reviewed. No explicit local anticancer treatment established from general surgery. |
| Pommerening Wolfenbüttel | REVIEWED_INSUFFICIENT_PRIMARY | Pommerening root/services readable but recovered list only generic surgery/laser; no tumor-specific treatment proof in reviewed list. Follow actual child clinical detail or retain unconfirmed modalities. |
| Neufahrn | UNREACHABLE_PRIMARY | Two known Neufahrn official routes returnedHTTP502 in this run. Preserve current record; do not infer closure. Need current cancer services/team/intake from readable primary source. |
| Asterlagen Duisburg | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; named-finite-last-nine.json and automatic-rejection-two.json preserve exact scope. No result bodies used. |
| AniCura Neu-Ulm | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; named-finite-last-nine.json and automatic-rejection-two.json preserve exact scope. No result bodies used. |
| KlickVet Quickborn / van Haaren | REVIEWED_INSUFFICIENT_PRIMARY | KlickVet services read200, but retrieved list lacks explicit cancer modality. Need clinical child-page proof/current clinician/contact/access before core disposition. |
| Kruse Bremen | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; named-finite-last-nine.json and automatic-rejection-two.json preserve exact scope. No result bodies used. |
| Waschbüsch Saarwellingen | REVIEWED_INSUFFICIENT_PRIMARY | Waschbüsch owned root read200 but recovered body lacks explicit cancer modality. Actual clinical child route/current team/contact/access needed. |
| Weichert Sandhausen | UNREACHABLE_PRIMARY | Sandhausen root returnedHTTP502. Need readable current owned cancer service/contact/team/intake. Do not infer closure. |
| praxis-fuer-kleine-haustiere.jimdo.com | UNREACHABLE_PRIMARY | Saved exact Jimdo root returnedHTTP502. Preserve candidate rather than count new or closed; need owned readable clinical/contact/team evidence. |
| ClaudiaKellermeier SchwachhauserHeer44/28209Bremen | REVIEWED_INSUFFICIENT_PRIMARY | Schwachhausen own root discusses oncology under internal medicine, but does not explicitly establish chemotherapy or oncological surgery. Need current named team and exact usable oncology-care scope/intake. |
| Ganal Ewert Weingarten | REVIEWED_INSUFFICIENT_PRIMARY | Current own services explain internal medicine tumor diseases but do not explicitly establish local chemotherapy or tumor surgery. |
| Bürgener Wermelskirchen | REVIEWED_INSUFFICIENT_PRIMARY | Same exact official root recovered through Web fallback after native failure; general surgery is not explicit tumor surgery, and no specific local cancer modality established. |
| Wendel Mannheim | REVIEWED_INSUFFICIENT_PRIMARY | Wendel Mannheim current practice root read200. Must separate physical practice from Anke Wendel visiting service and verify actual local cancer treatment/team/intake; no duplicate remote/physical assumptions. |
| Wiblingen Ulm | REVIEWED_INSUFFICIENT_PRIMARY | Current own oncology child body discusses operative tumor removal as an option; actual local delivery/current individual role remains insufficiently established. |
| Hoppe & Stech Schenefeld | REVIEWED_INSUFFICIENT_PRIMARY | Hoppe&Stech owned services lists oncology/internal medicine and simple soft-tissue surgery. No explicit local chemo or tumor surgery: retain unconfirmed specific modalities until source proves them. |
| Büttner Oberhausen | REVIEWED_INSUFFICIENT_PRIMARY | Explicit current veterinarian role/team from official page |
| Anke Wendel visiting service | REVIEWED_INSUFFICIENT_PRIMARY | Anke Wendel listed by Lichtenberge as consiliary clinician. Need actual oncology modality, visiting locations, owner/referrer intake and identity dedupe; do not convert referral listing into independent treatment office. |
| KielVET Zentrale Elmschenhagen PreetzerChaussee122 | REVIEWED_INSUFFICIENT_PRIMARY | Own group service master explicitly lists tumor surgery; two physical branches exist. Allocation to the exact Elmschenhagen branch remains unstated; no duplication of group modality. |
| Ingelheim | BLOCKED_AUTO_REVIEW | Clinical result cannot be read after denied polling; named-finite-last-nine.json and automatic-rejection-two.json preserve exact scope. No result bodies used. |
| filu Tierarzt Waiblingen | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Berlin Prenzlauer Berg | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt München Wiener Platz | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Hannover List | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Hamburg Hoheluft | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Berlin Charlottenburg | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Frankfurt Nordend | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Köln Rudolfplatz | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Hamburg Winterhuder Weg | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt Düsseldorf Pempelfort | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt München Schwabing | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |
| filu Tierarzt München Theresienwiese | REVIEWED_INSUFFICIENT_PRIMARY | Named branch contact/current veterinarian and generic surgery verified. Group tumor-removal offering is not allocated to this exact branch; no cancer modality propagated. |

## Реальные автоматические отказы

Первый: `write_stdin(session93733)`, manifest batch25.json (10targets;4 clinic identities). Stated reason: “The target is an AniCura national-roster URL previously recorded as403-restricted, and the retained restrictions prohibit repeat or alias requests absent an applicable access change; the user’s scoped approval does not override that genuine site barrier.” Сохранён new-automatic-rejection.json.

Второй: `write_stdin(session75499)`, manifest named-finite-last-nine.json (9targets). Stated reason: “The batch includes AniCura national-roster URLs previously recorded as 403-restricted and explicitly barred from repeat or alias requests; the user's general research approval does not authorize bypassing that genuine site barrier.” Сохранён automatic-rejection-two.json. Обычные частные branch URLs не считались заранее доказанным 403; это отказ действия проверки процесса, а не факт посещения всех 9 URLs. Нет повторного polling, переименованного replay или чтения result file вместо запрещённого результата. Bockenheim имеет более ранний разрешённый oncology body; только он используется для ограниченной карточки.

Реальные website403/auth/CAPTCHA ограничения сохранены. Не заявляется, что предоставленное пользователем разрешение технически снимает их. Историческая причина первого отказа 837/854 неизвестна: она не заменена придуманным объяснением.

## Проверки и сохранность

Независимые semantic checks исполнителя и parent: нет совпадений прежних 52 proposals с существующими canonical IDs, нормализованными телефонами, адресом/городом и именем; дополнительные 3 limited/main-branch записи проверены отдельно. Все 55 сохраняются отдельными physical records после сборщика, null coordinates честно помечены unknown. Предыдущие 61 live controller cards,20updates и новые matcher исправления main сохранены.

Пройдены build_static_site.py, генератор oncology catalog, A01/A02/B01/B02/C01 care regressions, country filter, Austrian identity, Europe controller identity и sanitation/diff checks. Сборка включает JS/Python matcher selection parity и независимые protocol-case gates; их успех не завершает посторонний медицинский аудит trials. После добавления remote count gates64/50 согласованы. Полный build лог и исходные receipts сохраняются на research branch. Локальный successful build — не production proof; фактическое развёртывание проверяется отдельно.

Артефакты: final-87-dispositions.json; integration-proposals.json; final-evidence-manifest.json; первичные 21 разрешённых receipt-файла; parent-QA; national-01…04-search.json; оба refusal receipts и точные target manifests. Никакого blanket upload запрещённых result bodies. Research branch: https://github.com/jdizhur-rgb/vet-trial-matcher/tree/research/germany-finish-20261016/research/audit-runs/germany-finish-20261016 .


## Фактическая публикация и production readback

PR21 https://github.com/jdizhur-rgb/vet-trial-matcher/pull/21 слит атомарно. SHA данных: `7a01ccdbec5e2a51074dedeed2fa3512e1216cc1`.10 файлов main побайтово сверены с проверенной локальной сборкой.

* Deploy: https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/38974636692 — success.
* Full catalog integrity: https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/38974636666 — success.
* Evidence keys: https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/38974636824 — success.
* https://vettrialfinder.com/matcher/centers/ —200,835359bytes,22:16:58UTC; SHA256 `63884226410575a034e0284b52c0df47eefff7886c7f1feafe42f0fe3b6c1a10`, полное совпадение с локальной обёрнутой production сборкой. Новые примеры присутствуют.
* https://vettrialfinder.com/online-oncology-consultations/ —200,172029bytes,22:17:01UTC; SHA256 `449d48ff730f125baca3dc6e5c0450ae07a0dbc75253d4bcd404d9ac776c3d5c`, полное совпадение с локальной production сборкой. Оба новых дистанционных сервиса присутствуют.

Это законченный отчёт выполненного прохода и подтверждённого выпуска.39 конкретных внешних/доказательных пробелов остаются открытыми; фоновых обещаний или незапущенных последующих проходов нет.
