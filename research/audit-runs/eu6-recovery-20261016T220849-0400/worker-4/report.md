# Германия — сверка восстановленного фронтира с текущей базой

Run `eu6-recovery-20261016T220849-0400`, slot **4**, country **Germany**, baseline `b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45`, фактический исполнитель `/root/oct16_de`. Работа: 2026-10-17T02:11:49Z — 2026-10-17T02:16:04Z; это время документарной работы, не посещения клиник. Отчёт собственный, не копия отчёта другой страны.

## Результат и граница завершения

Весь доступный **конечный именной followup сопоставлен**: 102 реальных кандидата получили решения по сохранённым первичным доказательствам, поздним ledgers и текущим полным каталогам. Относительно текущего baseline **NEW0, UPDATE0 providers /0 fields**. 89 DUPLICATE/уже представленных маршрутов,4 EXCLUDED,9 UNRESOLVED (7 точных внешних provider questions +2 будущих открытия).75 имеют полный сохранённый clinical/core gate; **новых первичных полных проверок в этом запуске0**. Физические адреса с неизвестными координатами допустимы и не превращены в mobile.

`finite_followup_complete=true`, собственный доступный остаток в позднем согласованном scope0. **`research_complete=false` и `coverage_complete=false` для национального доказательства**, поскольку свежий полный сетевой roster/клинический охват страны не установлен. Отсутствие доказательства не является отсутствием лечения. Переход к другой стране не разрешён. Полный национальный replay запрещён поздним owner continuation; это не замаскированный лимит времени или числа клиник.

До любого нового source request родителю сообщён точный конфликт: block07 оставлял171 professional/333 general-reference URL и национальные направления; поздние операции и Germany87/39 объявили доступный конечный проход законченным и запретили его перезапуск. Родитель подтвердил поздний scope и сверку102. **Новых source requests и поисковых запросов0**; outreach, формы, booking, paid APIs, trials, UI, commit/push/deploy, automations не выполнялись.

## Что унаследовано, что уже опубликовано, что потеряно

Последний старый удалённо проверенный block07: assigned102/processed69/fully9, NEW4/DUP8/EXCL3/UNRES54,33 identity-only — это **старый baseline2f709930**, не новые результаты нынешней работы. Его четыре SH-кандидата (Sülzle,Drensler,Sager,Genz) теперь найдены в current catalog и не продвигаются повторно. Старые1176 URLs — единицы маршрутов, не1176 провайдеров; generic references и aliases исключены из102.

Текущий supplied compiled catalog:901 listings; Германия239 =237 физических +1 mobile +1 network. Legacy location_type отсутствует у165 немецких физических записей; они не посчитаны как network/mobile из-за null поля. Дистанционных сервисов всего64, отдельный источник. Прочитаны все пять supplied stores: compiled, supplemental, source inventory, raw ACVIM и teleconsultation source.75 полных сохранённых core records — это68 физических из старого именованного фронтира +1 mobile +1 remote +5 ранее опубликованных физических; Tarp не считается полностью локально проверенным.

| Уже опубликованный пакет | Единицы | Доказательство публикации |
|---|---|---|
| Germany finish |55 physical +2 remote +1 existing availability update | `input/germany-finish-20261016/publication-receipt.json`, data SHA `7a01ccdbec5e2a51074dedeed2fa3512e1216cc1` |
| Remaining39 |17 physical +1 mobile | `input/germany-remaining39-20261016/publication-receipt.json`, SHA `f8e19c7c8d2216ceade92ef802b33cb1fec43c5a` |
| filu |1 network;0 physical | `input/filu-network-20261017/publication-receipt.json`, SHA `5b01073d4c7f0ccff07428a692d5c3330b1f098b` |

Эти receipts включают deployment/production byte readback. Они прочитаны как унаследованные квитанции, **не новая проверка live сегодня**.73 physical/mobile historical proposals сравнивались с current source_id по name/street/city/postal_code/phone/services/clinician_review/location_type:0 отличий в указанных непустых core полях. Полный список102 и точные identities/даты/цитаты находится в `reconciliation.json`.

Старые61 clinical payload и11 Trier old/new field operations **не восстановлены побайтово**. Они не реконструированы по snippets или профессиональным реестрам. Поздние независимо подтверждённые и опубликованные записи снимают необходимость их повторной интеграции, но не восстанавливают потерянную историю. Текущий Trier уже имеет Herzogenbuscherstr.3, телефон +4965199790740, Chemotherapy, Lara Hafenecker и доступ по записи; новой UPDATE нет. Am Westend уже сохраняет закрытие12–17октября и объявленный19октября переезд; будущий адрес не подставлен преждевременно.

## Национальное покрытие: факты и пределы

Ниже фактически сохранённые исторические query layers. Все пути — внутри `input/history/search-shards/`; время этих запросов16октября с исходной точностью до даты. Ни один из них не объявлен новым поиском этого worker.

| Земля | Текущий/недатированный + new-signal слой | Предел |
|---|---|---|
| Baden-Württemberg | search-01.json + search-new-1.json | Исторический поиск 16.10; не новая клиническая проверка |
| Bayern | search-01.json + search-new-1.json | Исторический поиск 16.10; не новая клиническая проверка |
| Berlin | search-01.json + search-new-1.json | Исторический поиск 16.10; не новая клиническая проверка |
| Brandenburg | search-01.json + search-new-1.json | Исторический поиск 16.10; не новая клиническая проверка |
| Bremen | search-02.json + search-new-2.json | Исторический поиск 16.10; не новая клиническая проверка |
| Hamburg | search-02.json + search-new-2.json | Исторический поиск 16.10; не новая клиническая проверка |
| Hessen | search-02.json + search-new-2.json | Исторический поиск 16.10; не новая клиническая проверка |
| Mecklenburg-Vorpommern | search-02.json + search-new-2.json | Исторический поиск 16.10; не новая клиническая проверка |
| Niedersachsen | search-03.json + search-new-3.json | Исторический поиск 16.10; не новая клиническая проверка |
| Nordrhein-Westfalen | search-03.json + search-new-3.json | Исторический поиск 16.10; не новая клиническая проверка |
| Rheinland-Pfalz | search-03.json + search-new-3.json | Исторический поиск 16.10; не новая клиническая проверка |
| Saarland | search-03.json + search-new-3.json | Исторический поиск 16.10; не новая клиническая проверка |
| Sachsen | search-04.json + search-new-4.json | Исторический поиск 16.10; не новая клиническая проверка |
| Sachsen-Anhalt | search-04.json + search-new-4.json | Исторический поиск 16.10; не новая клиническая проверка |
| Schleswig-Holstein | search-04.json + search-new-4.json | Исторический поиск 16.10; не новая клиническая проверка |
| Thüringen | search-04.json + search-new-4.json | Исторический поиск 16.10; не новая клиническая проверка |

21 крупный город (Berlin,Hamburg,München,Köln,Frankfurt,Stuttgart,Düsseldorf,Leipzig,Dortmund,Essen,Bremen,Hannover,Dresden,Nürnberg,Kiel,Magdeburg,Erfurt,Saarbrücken,Potsdam,Schwerin,Mainz) имеет сохранённые query entries в `input/history/queries.json` и шесть city-shards. Манифест содержит91 точный запрос; block07 сообщает115 с последующими отдельными shards. Это разная сохранённая полнота, не115 новых запросов.

| Обязательное направление | Фактическое сохранённое основание | Что не установлено |
|---|---|---|
| Все16земель/21город, GP/current/new signals | Указанные query layers; поздний finish report описывает national01–04 и triage333 как305 reference+28clinical | Search/snippets не clinical gate, не полный перечень неизвестных практик; поздние national raw queries не полностью скопированы в input |
| Университеты FU Berlin,TiHo,JLU,Leipzig,LMU | Поздний finish report: доступные clinical/contact FU/TiHo/JLU/LMU; LMU exact baseline identity + EBVS/Weiterbildungsstätte corroboration | Leipzig clinical/contact native502 +sameURL Web502; реестр подтверждает роль, не local oncology modality |
| Evidensia/AniCura и ветви | Именные ветви87/39; current catalog; exact restriction-scope-resolution | AniCura national roster403/aliases held; нельзя заявить свежий полный national roster. Старые837/854 queues потеряны |
| filu |12 исторических branch leads;10 open leads представлены одним current network contact; official network Surgery/contact/booking proof | Ни одной местной cancer-surgery allocation этим не подтверждено;2 будущих открытия не активны |
| Независимые/GP/хирургия/chemo |75 сохранённых qualifying core records, local named role/contact/access;73 exact core proposal comparisons | GP chemo допустима без board oncology; generic surgery/lump discussion/referral не cancer act |
| RT/ECT | Исторические университетские/new-signal слои, NIICE already-live Surgery-only | NIICE chemo/ECT «in Kürze» не активны; диагностический MRI/CT или external RT referral не local radiation; новых RT/ECT0 |
| Visiting/mobile/remote | callavet exact real service area без treatment-office адреса; VetOnkologie один intake identity; receiving Lichtenberge отдельная physical identity | Anke Wendel listing не доказывает самостоятельный mobile oncology service/личное назначение; remote legal office не клиника |

Никакая строка таблицы не заменяет полный свежий roster и не выдаёт «нет клиник». Незавершённость национального доказательства оставлена явной; available finite followup и national completeness — разные измерения.

## Именные qualifying записи: уже current, НЕ NEW

Ниже75 сохранённых полных core identities. Поля branch/core и короткие supporting quotes с исходными dates в `reconciliation.json`. У10filu не добавлены branch cards, уTarp не добавлена местная модальность.

| Провайдер | Город/доступ | Подтверждённая помощь | Официальный URL |
|---|---|---|---|
| Kleintierpraxis Eckernförde – Dr. med. vet. Eva Brockhaus | Eckernförde | Surgery | https://kleintierpraxis-brockhaus.de/leistungen/ |
| Nestler Mobile Tierärzte | Dohna | Surgery | https://www.tierarzt-nestler.de/ |
| 5-E Tierarztpraxis Thomas Backhaus | Thalfang | Surgery | https://www.tierarztpraxis-thomasbackhaus.de/ |
| Tierarztpraxis Dr. Mario Erler | Kassel | Surgery | https://www.drerler.de/ |
| Kleintierpraxis Stockelsdorf | Stockelsdorf | Chemotherapy, Surgery | https://www.tierarzt-stockelsdorf.de/onkologie.html |
| Tierklinik Oberhaching | Oberhaching | Surgery | https://tierklinik-oberhaching.de/fachbereiche/chirurgie/weichteilchirurgie/ |
| Fachtierärztliche Praxis Dr. Peter Beck | Rossach | Chemotherapy | https://www.dr-beck.com/ |
| Kleintierzentrum am Obermain | Lichtenfels | Chemotherapy, Surgery | https://kleintierzentrumobermain.de/leistungen/onkologie/ |
| Zentrum für Tiergesundheit Linkenheim-Hochstetten | Linkenheim-Hochstetten | Surgery | https://www.tierarzt-liho.de/leistungen/chirurgie/ |
| callavet – mobile veterinary service | Wiesbaden / Frankfurt / Mainz area | Chemotherapy | https://callavet.de/leistungen/tieraerztliche-leistungen/ |
| Tiergesundheitszentrum Bad Birnbach | Bad Birnbach | Surgery | https://tierarzt-badbirnbach.de/leistungen/chirurgie/ |
| Tierarztpraxis Dr. Boris Sülzle | Nortorf | Surgery | http://www.tierarztpraxis-nortorf.de/kleintierpraxis.php |
| Tierarztpraxis Karl Sewastianiuk | Stockach | Surgery | https://www.tierarzt-bodensee.de/therapien.html |
| Kleintierpraxis Strutz | Schwentinental | Surgery | https://www.kleintierpraxis-strutz.de/onkologie/ |
| Kleintierpraxis Stauferland | Rechberghausen | Surgery | https://www.kleintierpraxis-stauferland.de/leistungen/ |
| Kleintierklinik Wasbek | Wasbek | Surgery, Chemotherapy | https://www.kleintierklinik-wasbek.de/unsere-leistungen/fachgebiete/ |
| Kleintierzentrum Uetersen | Uetersen | Chemotherapy, Surgery | https://www.kleintierzentrum-uetersen.de/leistungen/chirugie |
| Kleintierpraxis Alexander Schumacher | Simmerath-Lammersdorf | Chemotherapy, Surgery | https://www.eifel-kleintierpraxis.de/leistungen.html |
| Tierarztpraxis Almenhof – Dr. Andreas Haag | Mannheim | Surgery | https://www.tierarzt-in-mannheim.de/leistungen/ |
| Kleintierpraxis Blankenese | Hamburg-Blankenese | Surgery | https://kleintierpraxis-blankenese.de/chirurgie-operationen/ |
| Tierarztpraxis Rahnsdorf | Berlin | Surgery | https://tierarztpraxis-rahnsdorf.de/leistungen/ |
| Kleintierpraxis Müllheim | Müllheim | Chemotherapy, Surgery | https://www.kleintierpraxis-muellheim.de/leistungen |
| Kleintierzentrum Beyen Hirschberg | Hirschberg an der Bergstraße | Surgery | https://www.kleintierzentrum-hirschberg.de/home/ |
| Tierarztpraxis Reinhard Seffner | Bremervörde | Surgery | https://www.tierarzt-seffner.de/leistungen/chirurgische-eingriffe |
| Tierarztpraxis Biet & Wanschura | Nagold | Surgery | https://www.biet-wanschura.de/leistungen/chirurgie/ |
| Tierarztpraxis Dr. Volker Janssen | Halle (Westfalen) | Surgery | https://www.tierarzt-janssen.de/de/ |
| Kleintierpraxis Weimar – Olma & Zeise | Weimar | Surgery | https://www.kleintierpraxis-weimar.de/leistungen |
| Tierklinik Bockenheim | Frankfurt am Main | Local oncology care | https://www.tierklinik-bockenheim.de/team-tierklinik-praxisrundgang/onkologie/ |
| Tierarztpraxis im Sonnenschein – Dr. Britta Richter | Handewitt | Local oncology care | https://tierarztpraxisimsonnenschein.de/Leistungen/ |
| Kleintierpraxis Wissenbach | Eschenburg-Wissenbach | Surgery | https://www.kleintierpraxis-wissenbach.de/leistungen/chirurgie/ |
| Tierarztpraxis Daniela Pommerening | Wolfenbüttel | Surgery | https://tierarztpraxis-pommerening.de/leistungen/operation.html |
| Dr. Stief – Tagesklinik für Tiere | Mühlhausen | Chemotherapy, Surgery | https://www.drstief.de/onkologie/ |
| Tierarztpraxis Westerhorn | Westerhorn | Surgery | https://www.tierarztpraxis-westerhorn.de/ |
| KleinTierzentrum Asterlagen | Duisburg-Asterlagen | Chemotherapy, Surgery | https://www.tierklinik-duisburg-asterlagen.de/index.php/auf-einen-blick/alle-fachbereiche/onkologie?view=article&id=9 |
| Tierarztpraxis Dr. Peter Saur | Garmisch-Partenkirchen | Chemotherapy | https://www.tierarzt-garmisch.com/leistungen/onkologie/ |
| Kleintierpraxis Dr. Tanja Kruse | Bremen-Oberneuland | Surgery | https://www.kleintierpraxis-kruse.de/unsere-leistungen/innere-medizin-orthopaedie-und-chirurgie |
| Fachtierarztpraxis Grünheide – Ariane Valentin | Grünheide (Mark) | Chemotherapy, Surgery | https://www.tierarztpraxis-valentin.de/unsere-leistungen.html |
| Tierarztpraxis Dr. Jessica Höch | Mühlhausen OT Saalfeld | Surgery | https://tierarztpraxis-hoech.de/ |
| Tierarztpraxis in Rondorf | Köln-Rondorf | Surgery | https://www.vet-rondorf.de/leistungen/ |
| Kleintierpraxis in Arsten | Bremen | Surgery | https://www.tierpfoetchen.de/de/unsere-leistungen |
| Kleintierpraxis Preetz / Schellhorn – Dr. Gesine Krefft | Schellhorn | Local oncology care | http://www.kleintierpraxis-preetz-schellhorn.de/leistungen.html |
| Tierarztpraxis Hamburg Altona | Hamburg | Surgery | https://www.tierarzt-hh-altona.de/de/unsere-leistungen |
| Tierarztpraxis an der Elbe – Nicolas Genz | Wedel | Surgery | https://www.tierarztpraxis-elbe.de/chirurgie |
| Tierarztpraxis Nicole Hänel | Hartmannsdorf-Reichenau | Surgery | https://tierarzt-haenel.de/leistungen.html |
| Tierarztpraxis Dr. Jörg Waschbüsch | Saarwellingen | Chemotherapy, Surgery | https://tierarzt-waschbuesch.de/behandlungsspektrum/ |
| ZweitmeinungTierarzt / VetOnkologie one remote intake group | Дистанционно | Онкологическое второе мнение | https://www.vetonkologie.de/zweitmeinung/ |
| Tierarztpraxis Bramfeld | Hamburg | Surgery | https://tierarztpraxis-bramfeld.de/leistungen/ |
| Tierarztpraxis Schwachhausen – Dr. Claudia Kellermeier | Bremen | Local oncology care | https://tierarztpraxis-schwachhausen.de/ |
| Tierklinik Ganal & Ewert | Weingarten | Surgery | https://www.tierklinik-ganal-ewert.de/ueber-uns/leistungen/operative-eingriffe-chirurgie |
| Kleintierpraxis Dr. Astrid Fritzenschaf | Eggenstein | Surgery | https://www.tierarztpraxis-fritzenschaf.online/leistungen/behandlung/ |
| Tierarztpraxis Rosenhof – Claudia Hartke | Mühlhausen | Surgery | https://tierarzt-muehlhausen.de/ |
| Tierärztliche Praxis Dres. Arui | Donaueschingen | Surgery | https://www.kleintierpraxis-arui.de/leistungen/ |
| Kleintierpraxis Eckhard Bürgener | Wermelskirchen | Surgery | https://www.tierarzt-buergener.de/seite/492776/operationen.html |
| Tierarztpraxis Harald Pfeiffer | Murrhardt | Surgery | https://www.tierarztpfeiffer.de/leistungen/kleintierpraxis |
| Tierarztpraxis Schmidl | Bremen | Surgery | https://www.tierarztpraxis-schmidl.de/leistungen.php |
| Tierarztpraxis Dr. Anja Zogall | Schwerin | Surgery | https://www.tierarztpraxis-schwerin.de/ |
| Kleintierpraxis Wendel | Mannheim | Surgery | https://kleintierpraxis-wendel.de/leistungen/ |
| Tierärzte Wiblingen | Ulm | Local oncology care | https://www.tieraerzte-wiblingen.de/fachgebiete |
| Internistische Kleintierpraxis Hoppe & Stech | Schenefeld | Local oncology care | https://kleintierpraxis-hoppe-stech.de/leistungen/ |
| Kleintierpraxis Oberhausen – K. Büttner | Oberhausen | Surgery | https://www.kleintierpraxis-oberhausen.de/leistungen/ |
| Tierklinik auf dem Lichtenberge | Steyerberg | Surgery | https://tierklinik-lichtenberge.de/leistungen/chirurgie-bei-kleintieren/ |
| Tierarztpraxis am Rotenbühl | Saarbrücken | Surgery | https://tierarztpraxisrotenbuehl.de/ueber-mich/chirurgie/ |
| Kleintierpraxis Schönberg – Dr. Steffen Sager | Schönberg | Surgery | https://www.tierarzt-schoenberg.de/leistungen/chirurgie |
| Tierarztpraxis Dr. Bungartz | Reuth | Surgery | https://tierarztpraxis-bungartz.de/leistungen/kleintiere |
| Tierarztpraxis Liane Kruse | Österdeichstrich | Surgery | https://www.tierarzt-kruse.de/Leistungen/ |
| Tierarztpraxis Rudloff | Elzach | Surgery | https://www.tierarzt-rudloff.de/leistung.html |
| Kleintierzentrum Kiel – kielVET Elmschenhagen | Kiel | Surgery | https://kielvet.de/leistungen/ |
| Fachtierarztpraxis Dr. Peter Grommelt | Kehl-Kork | Surgery | https://www.tierarztpraxis-grommelt.de/chirurgie/ |
| Tierarztpraxis Itterburg | Eberbach | Surgery | https://www.tierarztpraxis-itterburg.de/portfolio_page/weichteilchirurgie/ |
| AniCura Tierärztliche Praxis Ingelheim | Ingelheim | Surgery | https://ingelheimer-tieraerzte.de/leistungen/ |
| Nord-Ostsee Tierärzte – Schafflund | Schafflund | Surgery | https://nordostsee-tieraerzte.de/kleintiere/onkologie |
| Kleintierpraxis Niendorf – Dr. Sabine Rudat | Hamburg | Surgery | https://www.kleintierpraxis-niendorf.de/ |
| Fachtierarztpraxis Dr. Angelika Drensler | Elmshorn | Chemotherapy, Surgery | https://www.tierarzt-drensler.de/leistungen/ |
| Tierarztpraxis Markus Sliwon | Dormagen (Delrath) | Surgery | https://www.tierarzt-sliwon.de/ |
| Tierärztin Karin Rieckhoff – Fachpraxis für Kleintiere und Zahnheilkunde | Rendsburg | Surgery | https://www.fachtierarzt-rendsburg.de/seite/697815/leistungen.html |

LMU и две Bremen aliases также уже представлены, но не включены в75 как свежее полное клиническое доказательство. Tarp направляет сложные операции в существующий Schafflund; одна receiving identity не новое местоTarp. Anke Wendel lead разрешён в реальную принимающую Tierklinik auf dem Lichtenberge, не в новый самостоятельный visiting service.

filu — **одна** `de-filu-network-germany`, `location_type=network/service_scope=network`, Surgery; service@filu.vet, https://my.filu.vet/book и https://www.filu.vet/standorte. Нет улицы/города/индекса/координат/расстояния и branch fanout. Оговорка остаётся: подтвердить филиал, врача и доступность при записи. Управляющий директор Anna Magdalena Naderer не приписана всем операциям. В10 branch leads local allocation=false.

## Исключённые и нерешённые

EXCLUDED4: Pferdeklinik Eutin и Pferdeklinik Bilsen — собственный horse-clinic scope, не dog/cat oncology; vetmrt.de — диагностическая MRI/CT referral practice, не therapeutic RT; KlickVet Quickborn — недостаточный собственный cancer-care сигнал, не доказательство отсутствия лечения. Их исходные официальные URLs/короткие цитаты/даты сохранены построчно. Новых exclusions production нет.

Точные7 внешних provider questions:

| Провайдер | Состояние | Сохранённые URL |
|---|---|---|
| AniCura Krefeld Saumstraße | DIRECT_ANICURA_ROUTE_REMAINS_ACTION_RESTRICTED | https://www.tieraerzteverband.de/bpt/ueber-den-bpt/tierarztsuche/?town=Krefeld |
| Düsseldorf Münsterstraße359 | DIRECT_ANICURA_ROUTE_REMAINS_ACTION_RESTRICTED | https://www.tieraerztekammer-nordrhein.de/wp-content/uploads/2023/11/Klinikliste-fuers-Internet.pdf |
| Stahl Menden | GENUINE_SITE_ACCESS_RESTRICTION | https://www.tierarztpraxis-stahl.de/de/leistungen |
| Neufahrn | UNREACHABLE_PRIMARY_REQUIRES_PROVIDER_CONFIRMATION | https://www.tierarzt-neufahrn.de/index.php/de/praxisinformation ; https://www.tierarzt-neufahrn.de/ |
| AniCura Neu-Ulm | DIRECT_ANICURA_ROUTE_REMAINS_ACTION_RESTRICTED | Точный held AniCura action; URL не восстанавливался по догадке |
| Weichert Sandhausen | UNREACHABLE_PRIMARY_REQUIRES_PROVIDER_CONFIRMATION | https://www.tierarzt-sandhausen.de/ ; https://www.tieraerzteverband.de/bpt/ueber-den-bpt/tierarztsuche/?name=Weichert&town=Sandhausen |
| praxis-fuer-kleine-haustiere.jimdo.com | UNREACHABLE_PRIMARY_REQUIRES_PROVIDER_CONFIRMATION | https://praxis-fuer-kleine-haustiere.jimdo.com/ |

Для трёх AniCura не угадан новый branch URL и не искался alias национального roster. Допустимый следующий шаг — действительное применимое изменение access-review или независимое разрешённое первичное подтверждение local treatment/current vet/contact/intake; outreach требует отдельного решения. Krefeld имеет BPT identity/contact, Düsseldorf statutoryPDF даёт Münsterstr359 и tkd.de; это не клиническая услуга. Stahl exact services403 сохранён; не повторяется другим клиентом/маршрутом. Neufahrn/Sandhausen: прежние Web timeout+native502; Jimdo: Web inaccessible+native502. Не closure. Их next step — новое первичное evidence/изменение доступности или due check, не немедленный одинаковый retry без сигнала.

Будущие: filu Prenzlauer Berg — объявлено19.10.2026 (https://www.filu.vet/standorte/prenzlauer-berg); Waiblingen — ноябрь, без выдуманного дня (https://www.filu.vet/standorte/waiblingen). На17октября ни один срок не наступил. Проверять фактическое открытие и местную cancer service только после срока/нового сигнала, не автоматически продвигать.

Старые actual restrictions tknds.de403, professional-map consent и Halle3 incident исключены из новых действий. Смешанный aggregate rejection не превращён в403 всех независимых доменов. Exact1701 heldqueue bytes по-прежнему потеряны; они не восстановлены догадкой, denied outputs не использовались.

## Даты источников, проверки и backup

Текущий запуск: source attempts0 / fresh successes0 / source-date writes0. Original successful dates сохранены; интеграция/реставрация не обновляет source freshness. filu inherited native range2026-10-17T00:23:36.070066–00:23:39.629910+00:00; ранние Web dates-only отдельно. Brockhaus recovered raw без точного request time остаётся null; file completion time не превращён в успешный визит. Транспортные/403 timestamps не выданы за successful clinical dates.

Локально проверены JSON identity всех6файлов,102 уникальных candidate IDs, суммы89+4+9=102,75 full core без Tarp/filu branch inflation,0 new operations и0 differing core fields73 inherited proposals. Это документарная QA, не validator/build/production medical-audit PASS. Общие production валидаторы/скрипты за пределами собственного subtree не запускались.

Удалённый исходный backup, сообщённый родителем до запуска: branch `research/europe-recovery-eu6-recovery-20261016T220849-0400`, initial SHA `b159daa3ceb5de3feee6c539bc59ebd14a092eba`, содержит21старый архив. Предыдущий block07 data backup `089d7fa746c98d6aa6faae6a92bee17828dc1f91`, receipt `87f114dfb7381672e1ba302a89aaaa9a44aa336d` — исторические parent proofs. Этот worker не commit/push. Собственный immutable `checkpoints/block-01/ready.json` должен быть сериализован родителем и получить отдельный remote SHA/readback; до ответа родителя собственный новый remote backup **PENDING**, не заявлен успешным.

Итог блока01: конечный доступный Germany followup сопоставлен; production delta0. Национальное доказательство не объявлено завершённым. Родитель сообщил о предстоящем восстановлении разрешённого curated national evidence supplement; его фактическое чтение и оценка ещё не выполнены. Поэтому это interim checkpoint, не финальная приёмка страны. Ожидаю supplement, независимой parent review и remote-backup receipt; фоновых обещаний нет.
