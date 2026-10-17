# Австрия — итог исследования slot 1

Исполнитель: /root/oct16_at. Run: eu6-recovery-20261016T220849-0400. Baseline: b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45. Фактическое начало: 17 октября 2026, 02:11:09 UTC. Окончание содержательной сверки: 2026-10-17T02:47:05.157Z.

Доступная национальная программа выполнена; research_complete=true. Это означает отсутствие известных необработанных доступных кандидатов, списков филиалов и направлений, а не доказательство отсутствия неизвестных клиник. Сохраняются 22 внешних вопроса по провайдерам и три отдельных вопроса по модальности/справочному реестру (Hutter ECT, ÖTK roster, Anif ECT). Страна передана на проверку родителю, не принята контроллером и не опубликована. Никаких commit, push, deploy, production/shared edits, подагентов, outreach, оплат, регистрации аккаунтов, trial sweep или UI-действий не выполнялось.

## Счётчики и происхождение

| Единица | Количество |
|---|---|
| Назначено уникальных фактических provider identities | 160 |
| Обработано содержательно либо по реальному точному ограничению | 160 |
| Полностью подтверждены identity/contact/current named vet role-or-qualification/local cancer care/access | 119 |
| NEW относительно полного baseline | 45 |
| UPDATE существующих identities / отдельных полей | 30 / 51 |
| DUPLICATE — существующие identities без нового изменения | 44 |
| EXCLUDED — не продвигаются по нынешним доказательствам | 19 |
| UNRESOLVED — конкретные внешние вопросы | 22 |
| Новых фактических поисковых выполнений / source-read attempts | 46 / 172 |

NEW45 = 43 физических места, одна выездная служба Angerer и одна строго типизированная сеть Stiglhuber. По происхождению: 28 унаследованных неопубликованных записей с исходными датами (27 прежних NEW плюс допустимая сетевая упаковка Stiglhuber); 14 сохранённых leads, заново проверенных сейчас; три действительных открытия текущего run — Vorgartenstraße/Wien, Seewald/Innsbruck и Elterleinplatz/Wien. Старые опубликованные 11/20 и baseline76 не считаются NEW. В r04 содержательно проверены в текущий день 45 уникальных identities; дополнительный targeted modality-review Anif17октября указан отдельно. Эти provenance counters не являются непересекающимся арифметическим разбиением160. 112 обработанных унаследованы, ещё четыре реальных исторических restriction dispositions отдельно, не новые посещения.

172 попытки чтения не равны 172 клиникам или успешным клиническим проверкам. HTTP200 для JS-shell или посторонней торговли не принят за clinical success. Board certification и координаты не обязательны; GP tumor surgery/chemo допустимы. Общая хирургия, направления, диагностическая радиология и альтернативные обещания не выданы за лечение рака.

Восстановлены реальные immutable candidate/evidence/query shards blocks01–10; прежний run eu6-20261016T142911-0400 завершился фактическим usage limit и cleanup, сохранён до checkpoint021. Поздние решения/payload11–12 потеряны и не выданы за восстановленные. Отдельные сохранившиеся source-only receipts разобраны поштучно с их исходными датами. Никакая дата сборки/восстановления не заменяет дату чтения источника.

## Национальное покрытие

| Земля | Города и районы | Фактический результат |
|---|---|---|
| Wien | Wien, Bezirke | Krestan, Herzberg, Leberberg, Schwarzspanierhof, Vorgartenstraße, Elterleinplatz |
| Niederösterreich | St.Pölten, Krems, WienerNeustadt, Mödling, Mistelbach | Lorenz, Laa, Wirnsberger, Angerer;19-Veterinaria scope |
| Burgenland | Eisenstadt, Oberwart, Neusiedl, Parndorf | Viechdoktorei, Neufeld; Keller nonpromotion, Rieder held |
| Oberösterreich | Linz, Wels, Steyr, Traun | Steyr, Wels, Steinerkirchen; SolarCity/Wurm technical gaps |
| Steiermark | Graz, Leoben, Deutschlandsberg, Liezen/Rottenmann | Kucher, Damm, Lieboch, Wies, Payer; Stiglhuber1network |
| Kärnten | Klagenfurt, Villach, Spittal, Wolfsberg | St.Peter, Rainer, Steuerberg, Feistritz; Annabichl source gap |
| Salzburg | Salzburg, Hallein, Pinzgau, Pongau | Müller, Yaldez, Anif; Pabst visiting Schmid not new provider |
| Tirol | Innsbruck, Lienz, Kufstein, Zillertal, Jenbach/Stams | Covi, Seewald, Helm, Kasbach, Speckbacher; TGZ/Hradecky gaps |
| Vorarlberg | Bregenz, Dornbirn, Feldkirch, Lustenau, Nüziders/Hard | Holzer, Lackner, Zohmann; Fürst/Planner gaps |

Для всех девяти земель выполнены current/undated local-German поиски и отдельный слой текущих новых открытий. Доказательства: input/history/checkpoints/block-04-05/block-04-query-delta.json и search-read-04-01/02/03/06.json (16 октября); current-query-r02.json и web-r02-06/07/08.json (17 октября). Все найденные provider leads разобраны в work-deltas/r01..r04.json. Часть r02 query labels нормализована по пробелам/пунктуации и не названа byte-exact журналом; точные r03 request objects сохранены. Это выполненное поисковое покрытие, не утверждение, что каждый город имеет подходящий центр.

| Программа | Покрытие / результат | Сохранённое доказательство |
|---|---|---|
| Veterinaria | 19/19 филиалов сопоставлены и обработаны;17 полностью, Pegasus — horse-only, Muttendorf — точный access/clinical gap | block01 roster notes; blocks01–04; Basika fresh web-r04-01/02; точный mapping evidence-index-r04.json |
| AniCura | 6/6: Gratkorn, Hollabrunn, Korneuburg, Schwanenstadt, Erdberg, Aspern | blocks02/03/07; Aspern — одна NEW identity, не шесть |
| TIERplus | 6/6: Stadlau, Seyring, Kagran, Brunn, Klagenfurt, Innsbruck/Rum; пять подтверждённых oncology listings, Innsbruck остаётся unresolved | blocks02–04; диагностический рентген не RT |
| IVC | 2/2 Austria: Tulln и Perchtoldsdorf Ost | native-03b-ivc-roster, blocks04/05; held German workflow не посещён |
| VUK | 5 текущих: Althangrund, Vetklinikum, Schwarzmann, TAPS, Anif; Rathaus планируется на декабрь2026, не текущий центр | blocks05/07/10 и реальный public VUK post block09 |
| Vetmeduni / RT | Университетские oncology/team/LINAC/booking подтверждены; единственное подтверждённое местное RT-место среди рассмотренных первичных источников, не универсальное утверждение об отсутствии других | retained block03 |
| ECT | Fürstenfeld: ELC/chemo и Sandra Utzmann повторно подтверждены. Anif: после точечного review ECT снята как недостаточно подтверждённая patient-delivery modality, Surgery сохранена. Hutter ECT — отдельный внешний пробел. | web-r03-03/04/05; checkpoints/r05-anif/web-r05-anif-01.json и scoped amendment; Hutter restriction |
| GP и независимые | Реальная tumor surgery и узкая oncology care приняты без требования board credentials; generic surgery не продвинута | work-deltas/r01..r04 и per-field evidence |
| Выездная / visiting | Sauer — действительное сотрудничество с GP; Angerer — mobile cancer palliation, без пина; Schmid — receiving Pabst, не новая широкая mobile practice | retained mobile evidence; web-r02-13 |
| Удалённая | DocOrbit: owner/vet written oncology review route прочитан, но named veterinary oncologist/current assignment/Austria eligibility не опубликованы; не продвинут | r01 source receipts, current r03 remote queries; аккаунт/платёж не создавался |
| VONA / VÖK / ÖTK | VONA2018 — исторические имена, не текущая сеть лечения; VÖK current public section — обучение/руководство. ÖTK July2026 file требует разрешения, не реконструирован | web-r03-07; минимальная restriction metadata new-restrictions-oetk-r03-01.json |

Точный Veterinaria roster: Pegasus, Dobersberg, Muttendorf, GrazSüd, GroßEnzersdorf, Zohmann, Krebitz/Gressl, Parndorf, Pöchlarn, Scheibbs, Steinerkirchen, St.Pölten, Traiskirchen, Wels, Kagran/Basika, WienMauer, Meidling, Strebersdorf, TMZ20. Сетевые услуги не распределены автоматически всем адресам.

## Именованные NEW45

Полный baseline из centers, supplemental, inventory, ACVIM и tele-каталога проверен семантически: 4102 объектов, 45 новых identities, без совпадений existing identity/name/contact. Общие network-hosts трёх записей сопоставлены с фактическими разными адресами, не слиты по домену. Source dates, отдельные поля, цитаты, адрес/контакт/ветеринар/доступ — в proposed_changes.json и evidence.json.

| Имя | Город / реальный район службы | Подтверждено | Официальный clinical URL |
|---|---|---|---|
| Tier & Arzt — Dr. Jennifer Covi-Dijkhuizen | Innsbruck | Local oncology care | https://tierundarzt.at/medizin/ |
| Praxis für ganzheitliche Tiermedizin — Stefan Lorenz | Mistelbach | Surgery | https://tierarzt-lorenz.at/chirurgie/ |
| Viechdoktorei — Tierarztpraxis Leithaprodersdorf | Leithaprodersdorf | Surgery | https://www.viechdoktorei.at/leistungen.html |
| Chirurgisches Zentrum für Kleintiere Dr. Lorinson | Vösendorf | Surgery | https://www.vet-lorinson.com/ |
| Tierärztin Dr. Karin Yaldez | Weißbach bei Lofer | Surgery | https://tieresalzburg.at/leistungen/kleintierpraxis/ |
| Tierarztpraxis Uderns Zillertal — Elisabeth Helm | Uderns | Local oncology care, Surgery | https://www.tierarzt-zillertal.at/leistungen/ |
| Tierordination St. Peter | Klagenfurt | Surgery | https://www.tierarzt-klagenfurt.at/chirurgie/ |
| Kleintierpraxis DDr. Georg Rainer | Klagenfurt am Wörthersee | Surgery | https://www.docc.at/ |
| Tierarztpraxis Steuerberg — Rainer & Spendier / Ingrid Schmidburg-Spendier | Steuerberg | Surgery | https://www.tieraerzte-steuerberg.at/kleintierpraxis/ |
| Praxisgemeinschaft Wies — Johannes Wipplinger | Wies | Surgery | https://www.kleintierzentrum-frauental.at/ |
| Kleintierpraxis Lieboch | Lieboch | Local oncology care, Chemotherapy, Surgery | https://lieboch.net/Fachbereiche/ |
| Kleintierpraxis Schönberg — Barbara & Thomas Fridrich | Schönberg im Stubaital | Surgery | https://www.kleintierpraxis-schoenberg.at/index.php/leistungen/chirurgie |
| AniCura Tierarztpraxis Aspern | Wien | Surgery | https://www.anicura.at/standorte/tierarztpraxis-aspern/unsere-leistungen/ |
| Kleintierpraxis Pöchlarn — Dr. Andrea Mergl | Krummnußbaum | Surgery | https://www.kleintierpraxis-poechlarn.at/unsere-praxis/ |
| Tierarztpraxis Steinerkirchen | Steinerkirchen an der Traun | Surgery | https://www.veterinaria.at/standorte/steinerkirchen |
| Tierklinik Wels | Wels | Local oncology care, Chemotherapy, Surgery | https://www.tierklinik-wels.at/onkologie/ |
| TIERplus Klagenfurt — Mag. Tanja Schurian | Klagenfurt | Local oncology care, Surgery | https://www.tierplus.at/wp-content/uploads/2023/06/Web_TIERplus_Praxenfolder_Klagenfurt_A5.pdf |
| VetZentrum Anif | Anif | Surgery | https://www.vetzentrum-anif.at/chirurgie |
| Tierklinik Perchtoldsdorf Ost | Perchtoldsdorf | Surgery | https://www.tierklinik-perchtoldsdorf-ost.at/leistungen/weichteilchirurgie |
| TAPS — Tierarztpraxis am Stadtpark | Wien | Local oncology care, Chemotherapy, Surgery | https://www.taps.vet/leistungen/onkologie/ |
| Drautalvet — Tierarztpraxis Dr. Siegfried Gütler Feistritz/Drau | Feistritz an der Drau | Surgery | https://www.tierarzt-villach-land.at/leistungen/chirurgie/ |
| Kleintierpraxis Langenzersdorf — Daniela Föttinger | Langenzersdorf | Surgery | https://www.tierarzt-praxis.at/ |
| Tierklinik Wien-Süd — Dr. Weis und Team | Brunn am Gebirge | Surgery | https://www.tkws.at/chirurgie |
| Tierarztpraxis Neufeld — Christina Böcskör | Neufeld an der Leitha | Surgery | https://www.tierdoktor.at/leistungen/ |
| Tierarztpraxis Sebernegg | Wien | Surgery | https://www.hiergehtstiergut.at/Chirurgie-und-Narkose |
| Tierarztpraxis Deutschlandsberg — Albert Payer | Deutschlandsberg | Surgery | https://www.tierklinik-dlbg.at/unsere-leistungen/chirurgie |
| Tierarztmobil — Dr. Birgit Angerer (cancer palliative care) | Mödling and surrounding area | Local oncology care | https://tierarztmobil.at/palliativmedizin.html |
| Tierklinik Steyr — Dr. Pfeil & Partner | Steyr | Surgery | https://www.tierklinik-steyr.at/weichteilchirurgie |
| Tierambulatorium Kaiserebersdorf — Reinhard Krestan | Wien | Surgery | https://www.tierarzt-krestan.at/leistungen/weichteilchirurgie/ |
| Tierarztpraxis Herzberg — Michaela Messinger | Wien | Surgery | https://www.tierarzt-messinger.com/Leistungen/ |
| Tierarztpraxis Leberberg — Alicja Kucypera | Wien | Surgery | https://tierarzt-leberberg.at/leistungen |
| Tierarztpraxis im Schwarzspanierhof | Wien | Surgery | https://www.schwarzspanierhof.at/leistung |
| Kleintierpraxis Dr. Susan Holzer | Lustenau | Surgery | https://www.kleintierpraxis-holzer.at/leistungen/ |
| Tierarztpraxis Georg Speckbacher | Stams | Surgery | https://www.speckbacherhof-stams.at/leistungen |
| Kleintierpraxis am Kasbach — Melanie Bertignol-Spörr | Jenbach | Surgery | https://www.tierarzt-jenbach.at/behandlungen-ops-untersuchungen-fuer-tiere/ |
| Tierarztpraxis Dr. Kucher | Graz | Surgery | https://www.tierarzt-dr-kucher.at/leistungen/ |
| Kleintierpraxis Dr. Heide-Maria Müller | Salzburg | Surgery | https://www.kleintierdoktor.at/leistungen/ |
| Tierarztpraxis Laa an der Thaya | Laa an der Thaya | Surgery | https://www.tierarztpraxislaa.at/leistungen/chirurgie/ |
| Tierarztpraxis Andrea Lackner-Oberle | Nüziders | Surgery | https://www.tierarzt-lackner.at/leistungen/chirurgie/ |
| Tierarztpraxis Andrea Wirnsberger | Klosterneuburg | Local oncology care | https://www.meinetieraerztin.at/leistungen/kryotherapie |
| Tierarztpraxis Heinrich & Johanna Damm | Frohnleiten | Surgery | https://www.tierarzt-damm.at/medizin.html |
| Tierarztpraxis Vorgartenstraße — Nina Leonard | Wien | Surgery | https://www.wienvet.at/ |
| Kleintierordinationen Stiglhuber — network contact | Liezen and Rottenmann, Styria; confirm treatment branch when booking | Surgery | https://tierarzt-stiglhuber.gemeindeausstellung.at/home/ |
| Chirurgische Fachpraxis Dr. Matthias Seewald | Innsbruck | Surgery | https://www.tierarzt-seewald.at/chirurgie/ |
| Tierarztpraxis Elterleinplatz — Kuen & Zedinger | Wien | Surgery | https://elterleinvets.at/leistungen/chirurgie/ |

Stiglhuber — одно network listing с общим контактом и branchfinder; без street/city/postcode/coordinates, с обязательным уточнением филиала, врача и доступности. Две нерешённые branch-allocation записи не превращены в два местных Surgery-центра. Angerer — mobile, без корпоративного адреса-пина. Wirnsberger — только Local oncology care для фактической криотерапии кожных опухолей; не chemo/RT/широкая Surgery. Covi — фактическая oncology assessment/care plan, не обещание местной chemo или физического присутствия неназванного консультанта. Leberberg/Kucypera и прежний Krieger — одна преемственная практика; старый auction domain не клиника.

## UPDATE30 /51 отдельных полей

Это существующие provider identities. Old/current-baseline и new/source значения разделены по каждому полю; дата источника не обновлялась механически.

| Имя | Город | Подтверждённые услуги | Изменяемые поля | Официальный URL |
|---|---|---|---|---|
| Tierklinik Dobersberg | Dobersberg | Local oncology care, Electrochemotherapy, Chemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/dobersberg |
| Kleintierzentrum Graz-Süd | Pirka | Local oncology care, Surgery | services, availability_note | https://www.veterinaria.at/standorte/graz-sued |
| Tierarztpraxis Groß-Enzersdorf | Groß-Enzersdorf | Local oncology care, Surgery | services, availability_note | https://www.veterinaria.at/standorte/gross-enzersdorf |
| Tierarztpraxis Zohmann | Hard | Local oncology care, Surgery | services, availability_note | https://www.veterinaria.at/standorte/zohmann |
| Tierklinik Parndorf | Parndorf | Medical oncology, Electrochemotherapy, Chemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/parndorf |
| TVZ Scheibbs Kleintierordination | Scheibbs | Local oncology care, Surgery | services, availability_note | https://www.veterinaria.at/standorte/scheibbs |
| Tierklinik St. Pölten | St. Pölten | Medical oncology, Chemotherapy, Electrochemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/st-poelten |
| Tierarztpraxis Traiskirchen | Traiskirchen | Local oncology care, Chemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/traiskirchen |
| Zentrum für Tiergesundheit Meidling | Wien | Local oncology care, Chemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/meidling |
| Tierarztpraxis Strebersdorf | Wien | Local oncology care, Chemotherapy | services, availability_note | https://www.veterinaria.at/standorte/strebersdorf |
| Tierarztpraxis TMZ20 | Wien | Local oncology care, Chemotherapy, Surgery | services, availability_note | https://www.veterinaria.at/standorte/tmz20 |
| AniCura Tierklinik Hollabrunn | Hollabrunn | Local oncology care, Chemotherapy, Electrochemotherapy, Surgery | services, availability_note | https://www.anicura.at/standorte/tierklinik-hollabrunn/unsere-leistungen/ |
| AniCura Tierarztpraxis Korneuburg | Korneuburg | Medical oncology, Chemotherapy, Surgery | services, availability_note | https://www.anicura.at/standorte/tierarztpraxis-korneuburg/unsere-leistungen/ |
| AniCura Tierklinik Erdberg | Wien | Medical oncology, Chemotherapy, Surgery | services, availability_note | https://www.anicura.at/standorte/erdberg/leistungen/ |
| Tierarztpraxis Kufstein — Weißbacher & Winkler | Kufstein | Local oncology care | availability_note | https://www.tierarzt-kufstein.at/ |
| AniCura Fachtierarztpraxis Gratkorn | Gratkorn | Medical oncology, Chemotherapy, Surgery | services, availability_note | https://www.schichlvet.at/tagesklinik/zur-tagesklinik |
| Fachtierarztordination Dreier-Schöpf | Baden | Medical oncology, Surgery | services, availability_note | https://www.dreier.at/leistungen/chirurgie/ |
| Tierarztpraxis Ebenthal | Ebenthal in Kärnten | Local oncology care, Chemotherapy, Surgery | clinician_review | https://tierarzt-ebenthal.at/team/ |
| Das Tierärzteteam am Rathausplatz | Spittal an der Drau | Surgery | clinician_review | https://www.tierarzt-spittal.at/team |
| Tierärztliche Gemeinschaft Reyersdorf | Reyersdorf | Surgery, Local oncology care | services, clinician_review, availability_note | https://www.tierarzt-reyersdorf.at/leistungen/onkologie/ |
| Tierärzte Fürstenfeld — Utzmann & Tiefenbacher | Fürstenfeld | Medical oncology, Chemotherapy, Electrochemotherapy, Surgery | services, availability_note | https://www.tierarzt-fuerstenfeld.at/leistungen |
| Tierärztezentrum Graz West | Graz | Local oncology care, Chemotherapy | clinician_review | https://tierarztpraxis-eggenberg.at/praxis/ |
| Tierarztpraxis Kimberger-Dorninger | Kirchdorf an der Krems | Local oncology care, Chemotherapy, Surgery | clinician_review | https://www.tierarztpraxis-kimberger-dorninger.at/ueber-uns/ |
| Tierarztpraxis Dr. Pagl | Leonding | Surgery | clinician_review | https://www.tierarztpraxis-pagl.heroldwebsites.at/kontakt/impressum |
| Kleintierpraxis Dr. Rechberger | Linz | Surgery, Local oncology care | services, availability_note | https://www.tierarzt-rechberger.at/fachgebiete-tierarzt-linz/onkologie |
| Tierklinik Sattledt | Sattledt | Local oncology care, Chemotherapy, Surgery | clinician_review | https://www.tierklinik-sattledt.at/das-team/?positionen=tieraerzte |
| Fachtierärzte Althangrund — Vet Specialists | Wien | Medical oncology, Chemotherapy, Surgery, Electrochemotherapy | clinician_review | https://althan.vet/mitarbeiter/dr-maximilian-pagitz/ |
| Tierambulanz Brigittenauerlände | Wien | Surgery | clinician_review | https://www.tierambulanz-brigittenau.at/ordination-/team |
| Tierordination Hetzendorf | Wien | Surgery | clinician_review, availability_note | https://tierordination-hetzendorf.at/ |
| Vetklinikum Wien | Wien | Medical oncology, Surgery | clinician_review | https://www.vetklinikum.at/team/ |

## Исключения и дубли

EXCLUDED не означает «не лечит рак» или «закрыто»: имеющиеся первичные доказательства не обосновывают продвижение.

| Имя | Основание | Источник / собственный URL |
|---|---|---|
| pegasus | Недостаточно подтверждения целевого лечения собак/кошек | https://www.veterinaria.at/standorte/pegasus |
| MobilVET | Nonpromotion after full current official service/team/contact and targeted search: generic mobile care and hub surgery,not explicit cancer-focused service. Primary surgery page expressly rules out home-visit surgery. Generic surgery/palliation directories not tumor surgery/oncology proof; no claim provider never treats cancer. Current phone0577600,StefanMoserMag.med.vet.; twohubsnotautomaticallytwoqualifiedcancerbranches. | input/history/checkpoints/block-06-07-08/block-06-quality-reviewed.json |
| TIERplus Innsbruck | Current branch/team/contact read and targeted search give only generic surgery/internal medicine; no cancer-specific local service sufficient for promotion. Not a claim that cancer care is absent. | https://www.tierplus.at/tierarzt-innsbruck/ |
| Tierklinik Neusiedl am See — Sabine Keller | Own current tumor page describes alternative adjunct homeopathy/bioresonance/modified mistletoe/diet. General oncology and combination discussion does not establish delivered conventional cancer treatment; no unsupported efficacy/service promotion. | https://www.tierklinik-neusiedl.at/ |
| Tierklinik Leoben — Josef Schlederer | Current own home/surgery/team fully read; broad soft-tissue surgery and diagnostics do not establish actual cancer treatment. Nonpromotion, not proof of no cancer care. | https://www.tierklinikleoben.com/ |
| Tierordination Fröbelstraße — Christine Nöbauer | Own published comprehensive service list has only general soft-tissue surgery, no explicit cancer treatment. Targeted official-site tumor search found no new primary route. Nonpromotion, not absence claim. | https://www.tierordination-linz.at/ |
| TCVM — Susanne Lam | Own service describes acupuncture/herbs/nutrition/massage as supportive to chemotherapy elsewhere, not administered anticancer treatment. Do not adopt efficacy claims or convert support into chemotherapy. | https://www.tcvm.at/ |
| Vetservice — Herbert Ladstätter Hermagor | Own complete current public page confirms generic consultations/operations and named veterinarian, but no explicit cancer treatment. Nonpromotion only; generic surgery is not cancer surgery and no absence claim. | https://www.vetservice.at/ |
| Fachtierarztzentrum Tierarztpraxis am Rathaus — Dorothee Krainer | Retained full current official VUK public post explicitly plans opening December2026. Future-opening watchlist, not usable current clinic on17October; not a closure. | work-deltas/r02.json |
| Kleintierpraxis Josefiau | Current own complete one-page root confirms Heil/Immler and practice/contact, no explicit cancer treatment. Not promoted; no absence assertion. | https://kleintierpraxis-josefiau.at/ |
| Tierarztpraxis Liebenau-Arche Noah | Full current own clinical page confirms general surgery/diagnostics and generic mobile Graz service, not explicit cancer treatment or mobile cancer delivery. Nonpromotion, not absence. | https://tierarztpraxis-liebenau.com/ |
| Tierarztpraxis am Steinberg | Current own full small-animal/services/team page general surgery, specialist cooperation and diagnostics only; cancer-specific treatment not explicit. Current Hauptstraße41 differs stale child-footer SteinbergerStraße17, no card promoted from either. Current reopening/newbuilding2026 is real practice, not proof oncology. | https://www.tieraerzte-steinberg.at/ |
| Tierarzt Dr. Markus Greißing | Current full own service page general soft-tissue/bone surgery, imaging, dental and diet; no explicit tumor therapy. Nonpromotion not absence. | https://www.tierarzt-bregenz.at/ |
| Tierpraxis Annemarie Salzlechner | Current own comprehensive service/contact page gives general surgery only, no explicit cancer treatment. Nonpromotion, not no-offering claim. | https://www.tierpraxis.eu/ |
| Tierarztpraxis am Untersberg — Nadja Weissenbacher | Full current single-page practice/services/team/contact read: general surgery/diagnostics, no explicit actual cancer treatment. Nonpromotion, not absence claim. | https://www.tierarztpraxis-am-untersberg.at/ |
| Tierarztpraxis Hanl Vorau | Current full joint primary roster establishes Vorau and Wolfau, veterinary team and general surgery; no cancer-specific treatment offering. No network cancer entry justified either. Nonpromotion, not absence claim. | https://tierarzt-hanl.at/ |
| Tierarztpraxis Hanl Wolfau | Distinct Wolfau branch confirmed by full current joint roster; shared general surgery not actual cancer treatment. No branch/network cancer promotion, not absence claim. | https://tierarzt-hanl.at/ |
| Tierarztpraxis Auhof — Els Julienne Nys | Full current own services/team/contact and dated2026 breaks read. Only general soft-tissue surgery and generic palliative medicine, no explicit cancer treatment; do not convert palliative care or euthanasia into oncology. Distinct from d'Orazio/Zekic. Nonpromotion, not absence. | https://tierarztpraxis-auhof.at/ |
| Tierärztegemeinschaft Kölbel & Sverak | Current full own services and surgery pages read. Only general surgery and alternative mistletoe claim instead chemo/RT; no verified conventional cancer treatment. Alternative efficacy not adopted; generic house calls not mobile oncology. | https://www.ganzheitliche-tiermedizin.net/ |

44 DUPLICATE — существующие identities с содержательной проверкой, не 44 URL-дубля. Aliases Frauental→Wies, Schichlvet→AniCuraGratkorn, docc→Rainer, tierarzt-hietzing→d’Orazio, tieresalzburg→Yaldez и AndreaSchmid→receivingPabst не отдельные клиники и не увеличивают denominator.

## Собственный frontier и внешние вопросы

Собственный доступный необработанный frontier: **0**. Ни координаты, ни отсутствие board credentials не использованы как причина остановки. Внешние 22 вопроса ниже сохраняются после разрешённых маршрутов; конкретные причины и исходные даты оставлены в remaining.json, без вывода об отсутствии услуги.

| Имя | URL | Недостающий факт | Следующий разрешённый шаг / контроль |
|---|---|---|---|
| Tierarztpraxis Stadtgraben / Wolf | https://www.tierarztpraxis-stadtgraben.at/ | Actual inherited provider-task hold reviewed; no fresh request. Four coordinate fields remain WITHHELD. Need genuine restriction lift/new independent primary evidence, not alias reconstruction. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Tierklinik Fürst Bregenz | https://www.tierklinik-fuerst.at/ | Own current public root confirms Holzackergasse13,+43557483500 and phonebooking. Service/team exactURLs are inherited real denied sources; no bypass. Existing published Surgery retained historically,no fresh successful clinical service date. External access gap,not no-offeringclaim. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| muttendorf | https://www.veterinaria.at/standorte/muttendorf | Independent branch current service route for cancer-specific context; silence not evidence of absence | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Daniel Rieder Weiden am See | https://www.hund-katz.at/ | Actual inherited hund-katz.at whole provider-task hold reviewed; no fresh request, no address/credentials recovery via legal or referral aliases. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Dolomitenvets Hradecky | https://www.dolomitenvets-hradecky.com/ | EXTERNAL_SOURCE_INTEGRITY_GAP: current official-host native homepage200is unrelated RUSA33 commerce/login content,not veterinary clinical source. Own serviceURL404. The original automated source_success=true flag is HTTP/parser only and is overridden clinical_success=false here without modifying original receipt. Search cached veterinary material is not fresh primary evidence. Do not follow unrelated login/commerce links; no cancer promotion/current successful clinical date. Alternative current official clinical host not found in targeted query. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Kleintierpraxis Annabichl — Herwig & Diana Woschnjak | https://www.tierarzt-annabichl.at/ | Independent current primary TiKo venue fully read: current named Dr.med.vet.Herwig/Mag.med.vet.Diana Woschnjak and private patients, but no cancer treatment scope. Own exact clinical site retained502/timeout. Venue route now exhausted, not own unfinished; need new primary actual cancer-service statement, no inference from general diagnostics/counseling. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Tierarzt Zarfl | https://www.zarflvet.at/ | EXTERNAL_TECHNICAL_CLINICAL_GAP: current self-owned official microsite verifies name/address/contact,not cancer service. Actual ownhomepage native502,Webnotaccessible,official linked embeddingempty. No local oncology modality established,no successful clinical refresh. Only independent newly published primary clinical route could resolve; directories not proof. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| DocOrbit remote second opinion platform | https://www.docorbit.com/de/veterinary/ | Current official veterinary route offers owner/vet oncology written second opinions. Public specialist list names human MDs, not named veterinary oncologist; terms identify Turkish company and non-treating marketplace. Missing named veterinary qualification, current oncology assignment and Austrian provider/geographic eligibility. No account creation or paid submission performed. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Drautalvet Spittal | https://www.tierarzt-villach-land.at/ordination-spittal-drau/ | EXTERNAL_PUBLISHED_BRANCH_SCOPE_AMBIGUITY: current own Spittal page describes SusanneSchulzeMag.med.vet. and access to Feistritz OPcenter by cooperation. Shared practice tumoroperations read,not explicitlocalSpittalprocedure. Full bothbranches/groupservice/chirurgie/interne reads+targetedsearch exhausted current public allocation evidence. Do not promote Spittal Surgery or transfer Feistritz; directoryOnkologieonlylead. Resolve only with new explicit permitted primary branch statement; no outreach authorized. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Tiergesundheitszentrum Innsbruck — Marcus Egger | https://tierarzt-innsbruck.at/ | Own home/services/team native and Web are JS shells. Public frontend contains clinic identity/general-services literals, but clinical services/team drawn dynamically. No cancer-specific literal found. No credential/backend use; current cancer treatment remains unconfirmed, not absent. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Tierklinik Vöcklabruck | https://tierklinik-voecklabruck.at/ | Actual inherited403/provider-task hold reviewed; no fresh request, parent/home routes not used to recover denied oncology content. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Doris Hampel Felixdorf | https://www.tierarztpraxis-hampel.at/ | Own root native502 retained/current Web502; own service Web inaccessible. Municipality/contact directory cannot establish actual current cancer service. Missing primary clinical source; no closure or absence claim. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Kleintierordination Stiglhuber Liezen | https://tierarzt-stiglhuber.gemeindeausstellung.at/home/ | EXTERNAL_PUBLISHED_BRANCH_SCOPE_AMBIGUITY: current joint ownhomepage says routine tumoroperations and lists two clinics,without allocating OP-room to Liezen vsRottenmann. Full official homepage/two exact branchcontacts/two veterinary imprints and targetedtumorsearch read;only sharedparagraph found. Currentcredentials/phone/address/accessknown,physicalcancerservicescopeunallocated. No NEW physical surgery record until explicitbranchallocation; retiredOctober9closureisnotcurrentclosure. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Kleintierordination Stiglhuber Rottenmann | https://tierarzt-stiglhuber.gemeindeausstellung.at/home/ | EXTERNAL_PUBLISHED_BRANCH_SCOPE_AMBIGUITY: shared ownclinic tumoroperations cannot be allocated to either actualphysicalbranch. Current exactRottenmanncontact/DrAstrid veterinaryimprint and jointclinicalhomepagefullread; permittedpublicroute allocationexhausted asLiezen. Do not duplicate sharedserviceas two localSurgeryproviders. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Ulrike Wurm Traun | https://www.tierarzt-wurm.at/ | Current Web502 and same official root native502; targeted search found municipal/contact references but no independent owned current clinical source. Missing current explicit cancer treatment. No closure claim. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Tierarztpraxis Hartberg | https://www.tierarztpraxis-hartberg.at/ | Current Webtimeout/native502 TLS hostname mismatch; targeted search did not establish new current clinical host. Missing primary service/current veterinarian and access evidence. No TLS bypass and no closure inference. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| SolarCity Tierarzt Linz | https://solarcity-tierarzt.darstellung.at/ | Own microsite verifies actual location/contact/vets/general appointments; linked owned full site Webinaccessible/native502 TLS mismatch. No current primary cancer-specific treatment proof; directories not sufficient. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Zoodoc — Tierärztliche Ordination Tiergarten Schönbrunn | https://zoodoc.at/ | Current full service/team/contact confirms active practice but only generic surgery. Oncology announcement is explicitly26September2011; associated clinician Folko Balfanz not current team. Historic service news cannot establish current oncology availability. Missing current cancer-specific primary statement; no closure/absence claim. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Tierklinik Planner-Winsauer | https://www.tierklinik-planner.at/ | Own exact root failed Web502 and ordinary native502 certificate transport, not auth; primary clinical service/currentteam unreadable. No oncology inferred from directory or historical physician. Recheck same official URL when transport recovers. | Новая или восстановленная открытая собственная clinical/service/team публикация с недостающим фактом; без outreach, аккаунтов, paid submission и backend credentials. 2026-10-24, лишь как ручная контрольная дата, не созданная автоматизация. |
| Fachtierärzte Knafl — Maria Saal | https://www.knafl.at/praxis/maria-saal | Own branch identity/appointments/current doctors and joint conventional-medical Tumorerkrankungen label read, but no actual treatment/consultation description beyond label and alternative testimonials. No chemo/surgery inference. Exact team URL429 held; no bypass. Shared scope does not yet substantiate usable network cancer treatment. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Fachtierärzte Knafl — Klosterneuburg | https://www.knafl.at/praxis/klosterneuburg | Own current branch allocates Peter Knafl, address and intake; joint Tumorerkrankungen label not an explicit treatment description. No local surgery/chemo or network entry inferred. Team429 held, no additional provider requests. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |
| Tierarztpraxis Judenburg (held exact clinical root) | https://tierarztpraxis-judenburg.at/ | Actual retained exact root403 restriction substantively reviewed; no alternate transport/host/slash/query reconstruction. Earlier200receipt bytes not retained in own inputs, so no clinical/team/address claim restored. Need current cancer service, clinician, address/booking. Only actual restriction lift or genuinely independent new primary publication permitted. | Только реальное снятие ограничения/разрешённый доступ или новая независимая первичная публикация; не повторять held workflow/alias/client/cache/query. Нет календарного разрешения на повтор; только после реального permission/source change. |

Отдельно: Hutter/Wien ECT — собственные oncology/team/contact подтверждены, но точный Facebook post/profile workflow throttled; заголовок не подтверждает модальность. ÖTK July2026 holder file — явный permission/login gate, не клинический roster; сохранена минимальная metadata, raw login response не включён в remote manifest. Никаких held URL variants, alternate clients, cache/query reconstruction. Hradecky root — посторонняя торговля, не клиническое подтверждение. Rathaus — planned December2026; контроль не ранее1декабря, точный день открытия не выдуман. Hetzendorf16октября foods-only — временное сообщение, не permanent closure.

## Доказательства, сохранность и вывод

Все ссылки evidence_files/retained records разрешены до реальных файлов и SHA256 в evidence-index-r04.json: **0 отсутствующих references**. Full-baseline-qa-r04-v2.json фиксирует проверку всех пяти входных каталогов. JSON roots содержат точные run_id, slot, country, baseline_sha, agent_id. Шесть обязательных файлов заполнены: report.md, proposed_changes.json, result.json, evidence.json, queries.json, remaining.json.

Initial research branch: research/europe-recovery-eu6-recovery-20261016T220849-0400; backup b159daa3ceb5de3feee6c539bc59ebd14a092eba. Подтверждённые родителем remote receipts:

| Own checkpoint / parent checkpoint | Data SHA | Receipt SHA | Реальное подтверждение |
|---|---|---|---|
| r01 / 003 | 61faedaadcaeae4c1a701df41f41b9e3b859c0e1 | 7433f0216d775e8c3e2bb781deaf5d8fc35c8fcb | 2026-10-17T02:20:28Z |
| safety-knafl-01 / 005 | 1208993df6ff2a41d9ee1de899c9cd74bf0543db | bc6c398764bcfce84ee2cb4ceedd209d974cb5f6 | 2026-10-17T02:24:18Z |
| r02 / 008 | 1a9e16a4e5847a61f63c8aa3fedaf58850905492 | 839ce21d260e1ca6e829fad9d8b0ea0147eee212 | 2026-10-17T02:34:28Z |
| r03 / 010 | 20a3d05428036e1357d6067b553121c593fe1dc6 | eda2d75f537b7be20295260275305962725f378d | Подтверждено сообщением родителя; точный clock не предоставлен |

Финальный полный delivery: worker-1/checkpoints/final-delivery/ready.json. Он содержит шесть полных cumulative-файлов с учтённым Anif amendment, а effective-manifest.json фиксирует точные запечатанные r04+r05 пути и SHA256. r04 реально подтверждён родителем как REMOTE013: data6025992d8618f83f319759086b5e15926a17e991, receiptcf68e465ffa56438605cf1f322b5b0bc694d04ac, 02:51:14UTC; archive/member/control/receipt readbackPASS. r05 и final-delivery remote proof пока не получены. Это исследовательская сохранность, не production publication.

Основание research_complete=true: выполнены все девять земель, current/undated и new-opening local-German слои, университет, все обнаруженные сети и филиалы, GP/independents, RT/ECT, visiting/mobile/remote; все известные доступные кандидаты и направления разобраны; ограничения и оставшиеся внешние вопросы названы поимённо. Проверка/сборка/контроллер не использованы как причина преждевременной остановки поиска. Ожидается review родителя и затем отдельная all-six acceptance/publication. Никакого фонового наблюдения после этого handoff не обещается.


---

## История точечной Anif-поправки, включённой в полный итог


Исполнитель /root/oct16_at; run eu6-recovery-20261016T220849-0400; slot1 Austria; baseline b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45. Targeted review 2026-10-17T02:54:15.745Z. r04 immutable не изменён.

Вердикт: из NEW vetzentrum-anif снят только Electrochemotherapy tag; Surgery и NEW identity сохранены. Не установлено отдельного прямого утверждения о текущем ECT-приёме/доставке пациентам. Это не отсутствие услуги.

Кроме career equipment mention реально сохранена team-страница https://www.vetzentrum-anif.at/team: Mag.Wolfgang Biebl, LEITUNG,TIERARZT, в clinical-area list указана Elektrochemotherapie. Exact native receipt: input/history/checkpoints/block-03/native-03c-anif-team.json, attempted2026-10-16T18:57:04.718Z, received18:57:08.068Z, HTTP200. Это описание роли/области врача, не новое посещение и не самодостаточный patient-access proof.

Сегодня прочитаны только четыре разрешённых опубликованных маршрута: /leistungsuebersicht, /aktuelles, /chirurgie, /team. Полные Web reads в web-r05-anif-01.json. Team по-прежнему содержит ECT clinical area; overview и news не описывают ECT treatment access, surgery прямо перечисляет операции Mammatumore/Vaginaltumore, не ECT. Меню не даёт отдельного ECT service route. Не выполнялись broad search, held routes, URL guessing, outreach, аккаунты или платежи.

AMEND_NEW services: [Surgery,Electrochemotherapy] → [Surgery]. Availability note отдельно переписан, чтобы не обещать ECT. Clinician role и equipment остаются честной provenance, не services proof. Исходные даты и retained факты не переписаны. Полные точные old/new поля — proposed_changes.json этого amendment.

Counts unchanged:160unique/160processed/119fully; NEW45,UPDATE30identities/51fields,DUP44,EXCL19,UNRES22. Это не новый UPDATE существующего baseline-провайдера, а поправка модальности внутри NEW. Отдельных modality/reference gaps теперь3 (HutterECT,ÖTKroster,AnifECT). National research_complete=true сохраняется: известный доступный targeted route исчерпан, unknowncoords/board не причина исключения. Всего172source attempts,46queries; текущий targeted блок4reads/0queries. Provenance counters retained112/current45 в r04 не являются непересекающимся разбиением160.

Родитель реально подтвердил r04 REMOTE013: data6025992d8618f83f319759086b5e15926a17e991,receiptcf68e465ffa56438605cf1f322b5b0bc694d04ac,02:51:14UTC; archive/member/control/receipt readbackPASS. r04 reportSHA3863b71e254dc8dbdd22c22d554072f91748535f33da5900409bc240062bf126. Remote proof r05 ещё не получен. Production/publication не изменены.


## Окончательная доставка полного отчёта

Сборка 2026-10-17T02:55:51.061Z — только доставка существующих доказательств, не новый source visit. Счётчики160/160/119, NEW45, UPDATE30/51, DUP44, EXCL19, UNRES22 неизменны;172reads,46queries,3modality/referencegaps. Anif в основной NEW-таблице уже только Surgery. Общенациональный поиск не перезапускался. Все шесть окончательных cumulative-файлов заморожены вместе; короткий Anif amendment не заменяет этот полный отчёт.
