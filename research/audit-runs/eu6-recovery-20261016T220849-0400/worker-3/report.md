# Польша — восстановление национального исследования

run_id: eu6-recovery-20261016T220849-0400; slot:3; country:Poland; baseline_sha:b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45.
Реальный исполнитель: /root/oct16_pl. Работа начата 2026-10-17 (первый file request без измеренного времени); инициализация по реальным часам 2026-10-17 02:11:42 UTC. Точность дат старых источников не меняется.

IN_PROGRESS; research_complete=false. Последний подтверждённый block7:86 qualifying NEW claims (29 discovery+7 saved+50 inherited revalidated),77 inherited pending,20 historical already-main. Это унаследованные claims, не свежие посещения. Более поздние 123/87/37 payload потеряны и не считаются восстановленными.

Доступный национальный остаток не внешний blocker. Только собственный worker-3; production/shared state/commit/push/deploy не изменяются.

## Сохранность, единицы и первый доказательный блок

Старый полный payload147 и637 receipts реально сохранён. В позднем history/block7 отсутствуют working/candidate и source shards:86 остаётся report-level claim, а не структурно восстановленное предложение. Идентификационный audit147 против3229 строк четырёх полных baseline-inputs подтвердил20 представленных и127 absent. Это screen, не147 clinical reviews. Три первичных clinical reviews этого запуска: Vet4Pet Warszawa (Grenadierów9/1; консультации+удаление опухолей), SpecVet Mokotów (Rostafińskich4; Local oncology care), SpecVet Ursynów (Janowskiego11U6; Local oncology care). Дата источников16October сохранена;17October — дата локальной оценки. NEW3 inherited revalidated;UPDATE0;new discovery0. Координаты unknown не барьер; химиотерапия/RT из may-include не подтверждаются. Ветвевой oncology session остаётся вопросом записи, не поводом требовать board certificate.

## Полная матрица национального плана (не объявление завершённости)

Все региональные строки имеют статус IN_PROGRESS: первый слой broad/current+new queries выполнен, но explicit-OR secondary-city уточнения ещё доступны. Указанные крупные города частично покрыты inherited/main; это не заявление об их повторной свежей проверке. Query templates: «weterynarz onkologia chemioterapia [перечисленные secondary cities]» и «nowa onkologia weterynaryjna [województwo] otwarcie 2025 2026». Полные точные32queries — own-query-ledger001 и web023–030.

| Регион | Крупные/secondary города плана | Query receipt | Фактический исход к этому блоку | Candidate/source pointers |
|---|---|---|---|---|
| Dolnośląskie | Wrocław; Wałbrzych, Legnica, Jelenia Góra, Świdnica | sources/web-023.json | VetHome Długołęka NEW; NeoVet Wrocław inherited revalidated; MED-VET/Vetspec вопросы | working/candidates001/002; inherited-revalidated001#22 |
| Kujawsko-pomorskie | Bydgoszcz, Toruń; Włocławek, Grudziądz, Inowrocław | sources/web-023.json | PrzyKładce/Biegaławet NEW; z Sercem inherited revalidated | working/candidates001/003; inherited-revalidated001#21 |
| Lubelskie | Lublin; Chełm, Zamość, Biała Podlaska, Puławy | sources/web-024.json | Amicus, NaTuwima, RoyalVet, VetMedica NEW; UP Lublin revalidated; Tymiankowa/VET вопрос | working/candidates003; inherited-revalidated001#23 |
| Lubuskie | Gorzów, Zielona Góra; Nowa Sól, Żary, Świebodzin, Lubsko | sources/web-024.json | Hanusz alias; DrZOO transport gap; Paluch directory-only; новых qualifying пока0 | working/candidates002; regional-frontier-outcomes001 |
| Łódzkie | Łódź; Pabianice, Tomaszów Maz., Bełchatów, Skierniewice | sources/web-025.json | PRO-VET Łódź inherited revalidated; прежний MoonVet уже main | working/inherited-revalidated001#25; baseline-reconciliation |
| Małopolskie | Kraków; Tarnów, Nowy Sącz, Oświęcim, Myślenice, Wieliczka | sources/web-025.json | ABA-VET/DRHAU/Lupus + Promienna/Animalia/DobryWet/Serwin NEW; Provet host hold | working/candidates001/002/003; restrictions005 |
| Mazowieckie | Warszawa; Radom, Płock, Siedlce, Ostrołęka, Pruszków, Bobrowiec | sources/web-026.json | Dobrywet, Dr.Wet, AnimalCentrum, Chiron, CZZ NEW; Białobrzeska/Psychodnia/Bemowo restored | working/candidates001/003/004; inherited-revalidated001 |
| Opolskie | Opole; Kędzierzyn-Koźle, Nysa, Brzeg, Kluczbork, Prószków | sources/web-026.json | SCW уже main; Prószków/Kuchciński/VetCentrum уточнения, новых qualifying пока0 | working/regional-frontier-outcomes001; restrictions010 |
| Podkarpackie | Rzeszów; Przemyśl, Krosno, Tarnobrzeg, Stalowa Wola, Mielec | sources/web-027.json | CMZ cytology-only nonpromotion; VetKa/AlfaVet вопросы; Zwierzak ужеmain, ECT QA впереди | working/regional-frontier-outcomes001; baseline-reconciliation |
| Podlaskie | Białystok; Suwałki, Łomża, Augustów, Bielsk Podlaski | sources/web-027.json | NeoVet Białystok ложный город; ZWIERZAK/Złotorzyńscy/Dobrzyń вопросы; Azyl уже main | working/candidates002; regional-frontier-outcomes001; restrictions007 |
| Pomorskie | Gdańsk; Słupsk, Tczew, Starogard Gd., Sopot, Kosakowo | sources/web-028.json | Sosken/VetMania NEW; AMVET Gdańsk restored; Parkowa/Malec generic nonpromotion | working/candidates002/004; inherited-revalidated001#26 |
| Śląskie | Katowice, Gliwice; Częstochowa, Rybnik, Tychy, Zabrze, Chorzów | sources/web-028.json | Fivet/Vita/PRO-WET/Argo NEW; iVet generic nonpromotion; Onkovet ужеmain | working/candidates001/004; regional-frontier-outcomes001 |
| Świętokrzyskie | Kielce; Starachowice, Skarżysko-Kamienna, Sandomierz, Ostrowiec | sources/web-029.json | DOG NEW; Labrador restored; AS nonpromotion/Goldi gate; Bilscy ужеmain | working/candidates004; inherited-revalidated001#24; restrictions010 |
| Warmińsko-mazurskie | Olsztyn; Elbląg, Ełk, Ostróda, Iława, Giżycko, Szczytno | sources/web-029.json | AS/ArsVet/Szkamelski/Dogtorki NEW; GiVet/AVET вопросы; Onkowetka неEłkbranch | working/candidates002/003/004; regional-frontier-outcomes001 |
| Wielkopolskie | Poznań; Kalisz, Konin, Piła, Leszno | sources/web-030.json | REHAwet/Milovet/Hauwet/Misiu NEW; RYŚ restored; Canisia generic; Żurawiniec updateQA | working/candidates004; inherited-revalidated001#27; baseline-reconciliation |
| Zachodniopomorskie | Szczecin; Koszalin, Stargard, Kołobrzeg, Świnoujście, Białogard | sources/web-030.json | Franciszkańska/VetMedica NEW; Telvet/Białogard/Grabiec/Boliłapka вопросы | working/candidates004; regional-frontier-outcomes001; restrictions009/011 |

| Национальное направление | Факт и предел доказательства | Реально доступный evidence pointer | Статус/следующее действие |
|---|---|---|---|
| SGGW Warszawa | Inherited pl-sggw-warszawa: adrenal tumor removal, timetable/contact; ещё не own core-revalidated | input/inherited/checkpoint-28; klinikawet.sggw.edu.pl/klinika/ | IN_PROGRESS: clinical/current-team proofQA |
| UP Wrocław | Inherited current clinic vs generic university evidence; root/thoracic paths held403 | input/inherited/current-url-restrictions.json; saved national plan | IN_PROGRESS: permitted retained/other independently allowed sources only |
| UP Lublin | Действующая oral oncology Izabela Polkowska; также mammary tumor service; Local oncology care | web069 turn3095view2; retained turn1644view0/1646view1 | CORE_REVALIDATED current Głęboka30; wideruni sweep IN_PROGRESS |
| UWM Olsztyn | Inherited existing generic clinic, planned cancer center2029 не current service | input/inherited/resume-national-plan.json; checkpoint28 outcomes | IN_PROGRESS: current-v-future finalproofQA |
| URK Kraków/Rząska | Inherited pl-urk-rzaska currentpolyclinic oncology; not Kraków mailingaddress | input/inherited/checkpoint-28; upw.urk.edu.pl/uslugi?service=oncology | IN_PROGRESS: own retained/fresh coreQA |
| UMK Toruń | Inherited generic surgery alone no explicit delivered cancer therapy | input/inherited/resume-national-plan.json / checkpoint28 outcomes | IN_PROGRESS: current/new service refinements |
| UP Poznań | Inherited generic surgery/clinical units not automatic oncology delivery | input/inherited/resume-national-plan.json / checkpoint28 outcomes | IN_PROGRESS: current/new service refinements |
| UwB Białystok | Inherited May2026 future universityclinic signal not opened current oncology | input/inherited/resume-national-plan.json / checkpoint28 outcomes | IN_PROGRESS: opening/currentservice check |
| LuxVet full roster | 57 inherited entries ≠57 oncology providers; thisblock AMVET Gdańsk, RYŚ, Labrador, Psychodnia, Bemowo restored | input/inherited/network-roster-working.json; inherited-revalidated001; web067–069 | IN_PROGRESS: actual currentmaster/newbranches and everyentry reconciliation |
| AniCura full roster | 12 inherited branches, 11 draftprospects plus SosnowiecRysia2a nonpromotion; Medicavet legacyalias screened | input/inherited/checkpoint-28; candidates002 | IN_PROGRESS: currentmaster/everybranch/newsignal |
| EDINA roster | 20 known inherited named branches reviewed, master deliverygap explicitly retained; Rybicki=existingBrynówlegalidentity | input/inherited/edina-roster-working.json; candidates002 | IN_PROGRESS: mastergap and each currentbranch reconciliation |
| Maxvet / Zviropolis / Teodorowscy / Medican | Inherited actualroster/discrepancy tasks, not all branches accepted as oncology | input/inherited/resume-national-plan.json; discovery-domain-reconciliation-working.json | IN_PROGRESS: currentfullrosters/address/serviceallocation |
| Independent / ordinary GP | 29 newregional +7 saved NEW and10 restored. NamedcurrentGP sufficient; oncboard notmandatory | candidates001–004; inherited-revalidated001; web067–069 | IN_PROGRESS: remaininginherited/636hosts/secondarycities |
| RT / ECT | Dobrywet/Dr.Wet localECT; NeoVet restoredECT; RTWet alreadymain. RT referral notlocal; PsychodniaRT text contested | candidates001/004; restored001#22/28; baseline-reconciliation | IN_PROGRESS: nationwide modality refinement, existingZWIERZAKECT QA |
| Visiting / mobile | PersonalJaśkiewicz profile mapsactualElwet/RTWet; generic homevisits not mobileoncology | candidates001; inherited saved29 outcomes | IN_PROGRESS: independent mobile/visiting current+new sweep |
| Remote oncology | NeoVet ownabout explicitly noonlineconsultations; DOG online meansbooking; Malec genericemail notoncology | retained turn754view2; candidates004; regional-frontier-outcomes001 | IN_PROGRESS: currentactualremoteproviders and62tele fullsemanticcomparison |
| Current undated / newopenings | 32 own regional queries include2025/2026 opening layer; Serwin2025 newactualsite, DRHAU2025move confirmedclinicalpages | sources/web023–030 exactrequests; candidates001/003 | IN_PROGRESS: explicitOR regional refinements and networknewsignals |
| Prior query/domain frontier | 324 inheritedqueries/637receipts; 221potential title summaries read, all636host clinicalclassification notdone | input/inherited/discovery-domain-reconciliation-working.json; receipt-presence-audit002 | IN_PROGRESS: classify each actualcandidate/alias/nonprovider; unavailable work notexternal |



## Проверки и backup

Six identity fields одинаковы; текущие3 source IDs unique. Semantic screen20baseline+127absent сохранён в working/recovery-identity-audit-001.json; каждое предложение содержит old/new/officialURL/quote/branch/date/method и retained receipt refs. Первый checkpoint пока local-ready; удалённое подтверждение нового run ещё не получено. Исторические receipt/data SHA не переименованы в новый backup.

## Блок 2 — университеты и сохранённые клинические источники

Фактически reviewed15 уникальных units:9 qualifying fixed+1 qualifying network,4 nonpromotion,1 unresolved exactUPWr gates. NEW10=9 inherited physical+1 separately typed network access reclassification;fresh discovery0,UPDATE0. Старые147 кроме20baseline —127absent;9 nowreviewed,118 stillownunreviewed. Поздний86claim не сложен с10, чтобы не считать потерянные payload повторно. assigned153 пока provisional minimum namedunits, не окончательный национальный denominator.

Ещё восстановлены ALMAVET Sosnowiec (Będzińska16; currentEmiliaWiśniowska-Antonik veterinarian,localchemo), ERVet Wrocław (Morelowskiego27; AlicjaBryłkowska veterinaryrole,localchemo), OnkolVet Opole (Domańskiego16; AleksandraMarcinowska residency-trained,localchemo/cancersurgery/targeted/immunotherapy;notRT). Их полные сохранённые body датированы16Oct, не17Oct. SGGW freshclinic/currentstaffcard+officialcredentialPDF p1 закрыли coreветеринарнойквалификацииJoannaBonecka;Aprilcalendar не сталOctoberavailability. Lublinfreshmain/service/oralcare/Polkowska+reproductionmammarytherapy подтверждены. URKfreshserviceдоступен,старыйfullcredential16Octсохранён;новыйexactprofile404НЕдатаsuccess/НЕдоказательствоухода.

Матрица8universities — working/university-matrix-001.json. UMKnormalTLSexactservices200/generalonly; UWMnormalTLSexactworkshop200/generalonly; Poznańcurrentprimarytitle+officialanniversarygeneral; UwBfullMay22primaryfutureclinicwithdegreeOctober2027,notcurrent. UPWrheldmaster/thoracic403неоткрывалисьповторно. Триgenericindependentqueries web015 incidentalreturnedheldthoracicsearchcache:quarantined,notclinicalproof. SharedSpecVetcurrentprimaryexplicitchemo+common533333111email/branchfinder supports ONE network,street/cityempty/coordsnull;branchclinicalallocationforownerconfirmation,physicalLocalcardsnotexpanded.

24 actualPolishqueries now explicitly logged with actualengine/request/batchresultpointer;16 currentreceiptfiles include15Webcalls+normalTLSsummary. Noauth/CAPTCHA/heldURLreplay. Some source readers ordinaryfailed, independentlyallowednormalTLS suppliedUMK/UWM200;URK404 preserved. No successfultimestamp created from failedrequests.

Backup block1 REMOTE VERIFIED parent: data460a6c85d26a023f84df4b98fc1060566e852911;receipt/heade5d37690aaea5072efd981e8c403857f00b03249 at2026-10-17 02:15:25UTC;control/archivehashPASS. This proves listedactualpayloadshards preserved, notcountryacceptance/sitepublication. Block2 pendingremoteproof. National all16table above remains inheritedIN_PROGRESS;newuniversitymatrix addsactualproof withoutfabricatingfreshregionalvisits. Research continues SAME Poland.


## Блок 3 — AniCura и точные ограничения

Actual package:21 qualifying NEW=20 inherited fixed+1 отдельно typed SpecVet network; UPDATE0; fresh discovery0. Processed27=21 qualifying+5 nonpromotion+1 unresolved. Assigned155 provisional named units включает unprocessed Zebrzydowicka WET Rybnik lead. 107 из127 старых absent ещё требуют own clinical reconciliation;21 НЕ складывается с report-level86.

Восстановлены AniCura Animal Broniewskiego Łódź, Gliwicka Gliwice, ANIMAL.MED Gdańsk, Molicki Dąbrowa Górnicza, Wróblewscy Dąbrowa Górnicza, Legwet Legionowo, Pod Wieżami Poznań, Aksvet Oława, Animal Care Center Warszawa, MedicaVet Warszawa, Animal Młynarska Łódź. Полные адреса, телефоны, врачи/опубликованные роли, локальные модальности, URL/quotes и старые даты в working/inherited-revalidated003. Broniewskiego17Oct:Aleksandra Kimicka vet2018/currentonco; Młynarska17Oct:собственный current homepage «Lek. wet. Konrad Kalisz, kierownik przychodni»+localOnkologia. Booking403 НЕ повторялся; врач Broniewskiego не перенесён. ANIMAL.MED exoticchemo НЕ dogcat; только localdogcatcancersurgery. Остальные clinical source dates16Oct сохранены.

Current12 AniCura identities реально наблюдались в успешном web017 ДО subsequent403; сумма city counts12. 11qualifying; SosnowiecRysia2a nonpromotion, oncology attachedtoDąbrowa notSosnowiec, не утверждение отсутствия/закрытия. NewLuxVet403/AniCura403/EDINAadvertisedmapJSinaccessible сохранены restrictions001–003, не повторяются. СтарыеLuxVet57 historicalleads, неcurrentmasterproof. Independently published branch/news allowed. EDINA placeholders не clinical network contact. Web023 incidental held-master search snippets quarantined, не доказательство.

Parent004 REMOTE VERIFIED2026-10-17 02:22:49UTC data633b0123d6b3df6c7e24f44271c1beab062fbd66 receiptf7e2bc259e217fc93a3a57c230297be905b8dc0c includesblock2actualfiles. Parent005 VERIFIED02:24:18UTC data1208993df6ff2a41d9ee1de899c9cd74bf0543db receiptbc6c398764bcfce84ee2cb4ceedd209d974cb5f6 includesnewrestrictions001–003explicitmembers. Fullcontrol/archiveSHA PASS, неcountryacceptance/sitepub. Block3localready pendingremoteproof. Research_complete=false; продолжаюPoland.


## Блок 4 — authoritative current tally и сохранённые LuxVet branch proofs

Измеренный clock при подготовке: 2026-10-17 02:34:01 UTC. Actual qualifying47 NEW=46 inherited fixed+1 network reclassification; UPDATE0; freshdiscovery0. Processed54=47 qualifying+6 nonpromotion+1 unresolved; assigned155 provisional namedunits. Remaining81of127 olderabsent. Это НЕ47 поверх потерянного86. Rootresult checkpoint_at теперь measured; прежнееblock3значение02:31:30Z недостоверно и отменено append-only working/clock-correction001; реальныйready.created_at не отменяется.

Retained primary service/team/contact bodies с фактической датой16Oct достаточны для следующих самостоятельных локальных GP/provider units;17Oct здесь дата пересмотра, не свежий интернетвизит. Независимые current17Oct Ostródzka clinical page и openingnews подтверждают действующуюbranchcare после planned5Octoberopening, NataliaWiak lek.wet.oncology на ownservicepage; failedprofile НЕпревращён вsuccess.

| Единица | Город | Подтверждённый локальный объём | Primary URL |
|---|---|---|---|
| Przychodnia Weterynaryjna 4 Łapy | Reńska Wieś | Local oncology care | https://4lapywet.pl/uslugi/onkologia/ |
| Centrum Weterynaryjne Zwierzyniec | Lębork | Surgery | https://centrum-zwierzyniec.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Pavet | Warszawa | Surgery | https://pavet.pl/uslugi/zabiegi-chirurgiczne/ |
| Animal Doctor Gabinet Weterynaryjny | Gorzów Wielkopolski | Surgical oncology | https://animal-doctor.pl/uslugi/chirurgia-miekka/ |
| Gdyński Szpital Weterynaryjny | Gdynia | Surgery | https://gswet.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Multivet | Kraków | Surgical oncology | https://multivet.com.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Ostródzka | Warszawa | Medical oncology | https://ostrodzka-wet.pl/uslugi/onkologia/ |
| Gabinet Weterynaryjny Nesta | Grodzisk Mazowiecki | Surgery | https://nesta-wet.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Orka | Czechowice-Dziedzice | Surgical oncology | https://klinikaorka.pl/uslugi/chirurgia-ogolna/ |
| Przychodnia Weterynaryjna Ampułka | Mińsk Mazowiecki | Surgery | https://ampulka.com.pl/uslugi/chirurgia/ |
| Lubelska Poliklinika Weterynaryjna | Lublin | Surgical oncology | https://poliklinikaweterynaryjna.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Bokserska | Warszawa | Surgery | https://bokserska.waw.pl/uslugi/zabiegi-chirurgiczne/ |
| Przychodnia Weterynaryjna Bytom | Bytom | Surgery | https://weterynariabytom.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Bajeczna — Bajeczna 1 | Kraków | Surgery | https://bajeczna.com.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Help | Zielona Góra | Surgery | https://help.zgora.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Kościuszki | Toruń | Surgery | https://weterynariakosciuszki.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Tarnowskie Góry | Tarnowskie Góry | Surgery | https://weterynariatarnowskiegory.pl/uslugi/chirurgia-miekka/ |
| Przychodnia Weterynaryjna US-WET | Szówsko | Surgery | https://us-wet.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna VET-MED Toruń | Toruń | Surgery | https://vet-med.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna VETIKA | Grodzisk Mazowiecki | Surgical oncology | https://vetika-grodzisk.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna Wesoły Kundelek | Lesko | Surgical oncology | https://przychodniawesolykundelek.pl/uslugi/chirurgia/ |
| Przychodnia Weterynaryjna WIBRYS | Płock | Surgery | https://wibrys.pl/zespol/piotr-pawlowski/ |
| Przychodnia Weterynaryjna Żernicka | Wrocław | Surgery | https://wroclaw-weterynarz.pl/uslugi/chirurgia-weterynaryjna/ |
| Przychodnia Weterynaryjna Toruń Wyszyńskiego | Toruń | Surgery | https://wyszynskiego.lecznicatorun.pl/uslugi/chirurgia/ |
| Gabinet Weterynaryjny Toruń Migdałowa | Toruń | Surgery | https://migdalowa.lecznicatorun.pl/uslugi/chirurgia-miekka/ |
| Gabinet Weterynaryjny Lubicz | Lubicz Górny | Surgery | https://lubicz.lecznicatorun.pl/uslugi/chirurgia/ |

4Łapy/ReńskaWieś narrowed Local: no antineoplasticdrug modality proven. ZwierzyniecLębork limitedeyelidtumorremoval; GdyńskiSzpital limitedocular/aural cancersurgery; do not infer24/7 fromname, RT fromimaging, ECT fromCO2laser. Bajeczna explicitaboutpage assigns advancedoperations toBajeczna1, notOfiarDąbia4; no automatic servicefanout. Lubicz narrowselectedtumorremoval; ToruńWyszyńskiego/Migdałowa differentactualbranches andownservicebodies. Migdałowa ownrepeated14 prioritizedoveroldnetwork13, retainedcaveat/no pin. Wibryspostcode09-409vsold09-410 optionaldetail, exactHubalczyków6 proven; Poliklinika20-718vsold20-400 likewise, not disqualification byoptionalpostcode.

ZebrzydowickaWET Rybnik processednonpromotion: currentqualifiedteam/identity/contact but service/surgeryheadingalone no localcancerproof; thirdpartyoncologyiconnotpromotion. Group31March2026acquisitionnews is realindependent newbranchsignal, notcurrentheldmasterreconstruction. EDINAblog/placowki successfulvisibleHTMLempty; no placeholderphone/networkcancerlisting; heldmapJS neverretried. Currentinputtele AST64 actualservices fullyidentity-reviewed (not62staleclaim), zeroPL; existingPolish-speakingUKVOS/Purzycka notnewPolandteleunit. Baseline3229rows+64tele noqualifyingidentitycollision found.

Newdeltas004–006 actualfullcandidates+retained sourcekeys/refs saved; query003 actual3queries; web024–028 actualreceipts. Block4localready; remoteproofpending. Own nationalfrontier all16/smallnetworks/EDINA/RT-ECT/mobile-remote stillavailable: research_complete=false, continuingPoland.


## Блок 5 — authoritative current tally:82 qualifying units

Measured metadata clock:2026-10-17 02:38:59 UTC. Actual82NEW=81inheritedphysical+1separatelytypednetwork; UPDATE0; freshdiscovery0. Processed91=82qualifying+6nonpromotion+3unresolved(UPWr genuineexternalgate; Pasiak/Przasnysz ownavailable). Assigned156provisional actualnamedunits, not aliases.45of127oldabsent unreviewed, exactlyindices20–69excludingalready23/41/55/64/69. Старый86reportclaim НЕ cumulativepayload, позже123/87/37по-прежнему LOST.20baselineunits неNEW.

Ниже35дополнительно восстановленных clinical units: actual retained16Oct bodies/qualification/contact/branch scope; не35 freshvisits. Полныеold/new/sourceid/quotes/URLs/date/method в deltas007–011. Sourceidentity/date remains16Oct; этотrunreview17Oct.

| Единица | Город | Локально подтверждено | Primary URL |
|---|---|---|---|
| Lecznica Weterynaryjna VET-MED Brwinów | Brwinów | Surgery | https://brwinow.vetmed.com.pl/uslugi/chirurgia/ |
| Gabinet Weterynaryjny MAXVET PLUS Pułtusk | Pułtusk | Surgery | https://maxvetplus.com.pl/uslugi/chirurgia-miekka/ |
| Przychodnia Weterynaryjna VIVOVET | Iwiny | Local oncology care; Surgery | https://vivovet.pl/uslugi/onkologia/ |
| Klinika Weterynaryjna VETS | Warszawa | Surgery | https://vets.pl/uslugi/chirurgia/ |
| Vets&Pets Zakładowa | Wrocław | Surgery | https://zakladowa.vetsandpets.pl/uslugi/chirurgia-miekka/ |
| Vets&Pets Brzozy | Wrocław | Surgery | https://brzozy.vetsandpets.pl/uslugi/chirurgia-miekka/ |
| Vets&Pets Kamienna | Wrocław | Surgery | https://kamienna.vetsandpets.pl/uslugi/chirurgia-miekka/ |
| Przychodnia Weterynaryjna GAJA | Warszawa | Surgery | https://www.przychodniagaja.pl/chirurgia/ |
| Przychodnia Weterynaryjna HYRAX | Kraków | Surgery | https://www.hyrax.pl/chirurgia-miekka/ |
| Lecznica Weterynaryjna LuxVet24 | Kraków | Local oncology care | https://luxvet24.pl/team/julia-sliwa/ |
| Przychodnia Weterynaryjna Na Polance | Poznań | Surgery | https://www.napolance.pl/chirurgia/ |
| Klinika Weterynaryjna NEW VET 24h | Gdynia | Surgery | https://www.newvet24h.pl/chirurgia/ |
| Klinika Weterynaryjna MULTIWET | Warszawa | Surgical oncology | https://multiwet.pl/uslugi/chirurgia-miekka/ |
| ŻKW Przychodnia Weterynaryjna | Warszawa | Local oncology care | https://weterynaria.waw.pl/stomatologia-weterynaryjna/ |
| Klinika Weterynaryjna Marysin | Warszawa | Medical oncology; Chemotherapy; Surgery | https://www.wetmarysin.pl/onkologia |
| HemaTeamVet | Warszawa | Local oncology care | https://hemateamvet.pl/uslugi/ |
| Zviropolis Klinika Wilanów | Warszawa | Surgery | https://zviropolis.pl/weterynarz-stomatolog-warszawa/ |
| Zviropolis Klinika Ochota | Warszawa | Surgery | https://zviropolis.pl/weterynarz-stomatolog-warszawa/ |
| Zviropolis Klinika Praga | Warszawa | Medical oncology; Chemotherapy; Surgery | https://zviropolis.pl/weterynarz-stomatolog-warszawa/ |
| Zviropolis Klinika Żoliborz | Warszawa | Surgery | https://zviropolis.pl/weterynarz-stomatolog-warszawa/ |
| Vet-Service Przychodnia Weterynaryjna | Siedlce | Surgical oncology | https://www.vetservicesiedlce.pl/chirurgia |
| Wetmedic | Warszawa | Medical oncology; Chemotherapy; Surgical oncology | https://wetmedic.pl/onkologia-2/ |
| Klinika Teodorowscy Warszawa | Warszawa | Local oncology care | https://www.klinikadlazwierzat.pl/nasz-zespol/ |
| Klinika Weterynaryjna dr n. wet. Dariusz Niedzielski | Wrocław | Surgery | https://www.klinikapsaikota.pl/chirurgia-miekka |
| Przychodnia Weterynaryjna Vetin | Wrocław | Surgical oncology | https://vetin.wroclaw.pl/leczenie-zwierzat |
| Przychodnia Weterynaryjna Strzyża | Gdańsk | Local oncology care | https://przychodniastrzyza.pl/uslugi/onkolog-zwierzecy/ |
| Przychodnia Weterynaryjna Zdrowy Kurczak i Azorek | Siedlce | Surgical oncology | https://weterynarz-siedlce.pl/chirurgia/ |
| Przychodnia Weterynaryjna Piotr Dąbrowski | Poznań | Medical oncology; Chemotherapy; Surgery | https://www.wet.pl/specjalizacje.html |
| Animal Center | Warszawa | Medical oncology; Chemotherapy; Surgical oncology | https://animal-center.pl/chemioterapia-psow-i-kotow/ |
| KoniczynaVET | Warszawa | Medical oncology; Chemotherapy | https://koniczynavet.pl/konsultacja-onkologiczne |
| Lubelskie Centrum Małych Zwierząt | Lublin | Medical oncology; Chemotherapy; Surgical oncology | https://lcmz.pl/klinika-24h/onkologia |
| ArkaNoego Gabinet Weterynaryjny Adam Tymiński | Białystok | Local oncology care; Surgical oncology | https://noegoweterynarz.pl/oferta/ |
| Przychodnia Weterynaryjna ADA | Rzeszów | Surgery | https://ada.rzeszow.pl/uslugi/chirurgia |
| ART VET Gabinet Weterynaryjny | Grębocin | Local oncology care; Surgical oncology | https://www.art-vet.pl/ |
| Gabinet Weterynaryjny Barbara Szarszewska | Toruń | Surgery | https://weterynarz.torun.pl/chirurgia/ |

GAJA current own contact/dayhours prioritizedoverold24h biography; failedMichałImbierski challenge notused/retried, independent ŁukaszSokalskiSGGW2007/surgeryspecialist body supportscurrentqualifiedstaff. VIVOVET/GAJA optionalpostcodes conflict retainednotbarrier. LuxVet24Kraków currentJuliaŚliwa ownfullbody oncologycasecare valid despiteheld429serviceindex; notsameentityasLuxVetgroupmaster. NaPolance: ownSurgery+lek.wet.MilenaSobótka fullysupported, extraLocalconsultation claim fromoldnativeZattbody NOTstructurallyrecovered, narrowedtoSurgery; explicitappend-only noteamendmentnetwork-frontier-outcomes002. HemaTeamVet currentSebastianBorowikSGGW2005+actualhematologic/neoplasmtherapy qualifiesLocal, notunpublishedspecificdrugmodality. TeodorowscyWarsaw AliaksandrAnisko explicitlywithinWarsawroster, Polishpracticeauthorized, Localcareonly; do notfanoutsharedtumorsurgeryacross3clinics.

Zviropolisfouractualaddresses have explicitdentalstatement proceduresperformedall4+oral-tumorremoval and qualifiedshared/localGPs: this is directpublishedall4allocation, notautomaticfanout. Chemo ONLYPraga viaexplicitlyassignedKarolBaranowski currentvetWrocław2021+ownfullbioIV/intracavity/metronomictherapy. No oncologydiplomateinferred. AnimalCenterZamiany12 differentAniCuraSarmacka9; WołominSEOcatchmentnotnewbranch; ownIV/oralchemo andcancersurgerysupported; ECT404notcareabsence/noRTfromeducation. ART VET Grębocin87-122top/87-162footer optionalconflict retainednotbarrierexactKowalewska11, no countywidehomeoncologyclaim. Currentofficialstatedtreatment counts independentlyfromGPqualification, unknowncoords notbarrier.

PasiakSiedlce retainedspecifictumorremoval+namedqualifiedGP/contact38 are real; about25 remainscorestreetconflict pendingindependentmunicipalrecordprioritycheck, notpromotedfullyyet. MAXVETPLUSPrzasnysz olddistinctbranchlead nowexactredirectPułtusk, cannotcopyPułtusk surgery/callclosed; remains ownavailable. Allbroadnational/roster/region/mobileRTremote tasks continue. Earlierfullall16table is explicitly inheritedreport-level context, currentexactowncandidateproofs are the immutable delta shards; missinglateworkingpaths notrestoredbytableassertions.

Block5localready pendingremotereadback; no newbackupproofasserted. Research_complete=false. Continuing SAMEPoland saved45frontier then remainingnetwork/regionaldimensions.


## Блок 6 —92 qualifying, точный provider denominator и Pasiak

Measured clock:2026-10-17 02:49:53 UTC. Actual NEW92=91inheritedfixed+1network; UPDATE0;EXCL6;UNRES2;processed100. Нет freshdiscovery и нельзя складывать92 с late86reportclaim. Named ledger001:156assigned=100processed+36oldabsentunprocessed+20alreadybaselineexistingQAunprocessed. ДоPrzasnyszбыло155. Старые20 — реальныеcandidateunits, но identityscreen неclinicalreview: отдельноpendingexistingQA, неNEW. Processed100=92qualifying+6nonpromotion+2unresolved; никакой подгонкипоURL/alias/reference.

9 восстановленных units: BiałobrzeskaWarszawa (chemo/cancersurgery/targeted/immunotherapy, RTreferralonly); zSercemWłocławek (GPchemotherapy/cancersurgery); NeoVetWrocław (chemo/ECT/targeted/Surgery); LABRADOROstrowiec (Surgeryonly); PRO-VETŁódź (chemo/immunotherapy/Surgery); AMVETGdańsk (Localonly); RYŚPiła (IVcytostatics/metronomic/cancersurgery); PsychodniaWarszawa (chemo/immunotherapy/Surgery;RTclaimnotindependentlycorroborated); BemowoWarszawa (chemo/Surgery, externalRTconsultationonly, outdatednationwideRTclaimnotadopted). Fulladdresses/phones/currentqualifiedroles/URLs/fieldquotes/provenance inimmutable012. Retainedclinical16Oct dates preserved; successful17Oct roles/access/ECT/localcare specifically identified perfield. Białobrzeska current ownerform selectablefourqualifiedclinicians; no mandatoryreferral inference. NeoVet foreigntraining notboardqualification; irrelevantgamblinghomepage ignored, no links followed.

PasiakSiedlce corepartial nowresolved: successful17Oct cityprimary record turn3464view2 lines199–203 and2026programme context confirms Graniczna38/256447453, matchingowncontact16Oct; olderabout25historicaldiscrepancyretained. Optionalpostcodeown08-119vsmunicipal08-110disclosed; usemunicipaloromit, noextraunit/pin. Surgerytumorremoval andprofessionalrole remain retained16Oct. Separatefullqualifyingdelta013 supersedespartial001 disposition; noUPDATE existingidentity because absentbaseline. Parent mustnotcountbothpartial+newas2providers.

MAXVETPLUSPrzasnysz current independentsearchsurfaced exactbranchsurgerypage withmammarytumorresection/contact28, but directWebserviceInternalError andteamredirectPułtusk: stillUNRESOLVED, notfanout/notclosure; ordinarysameofficialURLtransport route remainsallowed, noauthdenial. UPWr genuineexactgatesremainexternal. National16regions and allremainingdimensions stillIN_PROGRESS.

Remote010 VERIFIED perparent: data20a3d05428036e1357d6067b553121c593fe1dc6 receipteda2d75f537b7be20295260275305962725f378d includesblock4/5actualpayloads; source/data proof, notcountryacceptance/sitepub. Earlier008 data1a9e16a4e5847a61f63c8aa3fedaf58850905492 receipt839ce21d260e1ca6e829fad9d8b0ea0147eee212 measured02:34:28UTC includesblock3+amendments; fakeblock3checkpoint_at remainscancelled. Block6localready pendingremoteproof; research_complete=false. ContinuePoland.


## Блок 7 —103 квалифицируемые единицы, не завершение страны

Измеренное время:2026-10-17 02:53:48 UTC. Actual NEW103=102inheritedphysical+1SpecVetnetwork, UPDATE0; processed111=103qualifying+6nonpromotion+2unresolved. Namedledger002:159assigned=111processed+25oldabsentunprocessed+20alreadybaselineexistingQA+3newactualLuxVetPremiumbranches. Полный национальный denominator пока provisional, не числоURL/aliases. Старые20 неNEW/неавтоматическиprocessed. Sourcefielddates fresh17Oct толькогдеуспешнопрочитаны; olderunchangedreceipts16Oct остаются16Oct.

| Единица | Город | Локально подтверждено | Primary URL |
|---|---|---|---|
| Veterio — Całodobowa Klinika Weterynaryjna | Warszawa | Medical oncology; Chemotherapy; Surgical oncology; Targeted therapy; Immunotherapy | https://veterio.pl/onkologia-weterynaryjna-warszawa/ |
| Przychodnia Weterynaryjna LoVeT | Kraków | Medical oncology; Chemotherapy; Surgical oncology | https://lovet-przychodnia.com/ |
| Klinika Weterynaryjna Szmaragdowa | Lublin | Medical oncology; Chemotherapy; Surgical oncology | https://klinikaszmaragdowa.pl/uslugi/onkologia-weterynaryjna/ |
| Przychodnia Weterynaryjna REX | Lublin | Medical oncology; Chemotherapy; Surgery | https://lublin-weterynarz.pl/uslugi/onkologia/ |
| Trójmiejska Klinika Weterynaryjna | Gdańsk | Medical oncology; Chemotherapy; Surgery; Electrochemotherapy | https://tkw24.pl/uslugi/onkologia/ |
| Ostrowskie Centrum Weterynaryjne | Ostrów Wielkopolski | Medical oncology; Chemotherapy; Surgical oncology | https://ocw.com.pl/onkologia |
| Centrum Weterynaryjne Boliłapka | Białystok | Surgical oncology | https://www.bolilapkabialystok.pl/chirurgia-i-ortopedia |
| Przychodnia Weterynaryjna Tropek — Katarzyna Żakiewicz | Białystok | Surgical oncology | https://www.tropek-wet.pl/oferta/chirurgia-miekka |
| Vet Premium Kraków — Lux-Vet Premium | Kraków | Local oncology care | https://lux-vet.pl/uslugi/onkologia/ |
| Specjalistyczna Przychodnia Lux-Vet Premium — Bielsko-Biała | Bielsko-Biała | Local oncology care | https://lux-vet.pl/uslugi/onkologia/ |
| Vet Clinic — Przychodnia Weterynaryjna | Łódź | Medical oncology; Chemotherapy | https://vetcliniclodz.pl/onkologia |

Veterio currentnamedqualifiedGPAnnaHałka/internalmedicine+explicitcurrentlocalclinicaldrug/surgerycare sufficiently establishcore; specificoncologyappointmentclinician/session remainsbookingdetail, priorIrishoncologyexperience notassignedasWarsawservice. Oldwkrótce conflict preservedhistorically; currenttreatmentpresenttense/contactbookingnotfuture. LoVeT currentteam oncologyDrewniak/Gromny+cancersurgeonŻukowski; SzmaragdowacurrentMucha/Kot/Więcek roles separatefrommodalities; REX localparagraph supportschemo/Surgery butnotgenericRT/immunotherapy. TKW currentreadableoncologyserviceexplicitchemo/ECT andnamedlek.wet.AnnaKurczewska; heldbiography/aboutneverretried, nootherbranchfanout. OCW localRTclaim remains specificunresolvedpubliccorroboration question, noRTfilter. BoliłapkaBiałystok explicitoncologicsurgery+TomaszBiedulewicz1998vet/2007surgeon. Tropek optionalpostcode15-703/15-777notcorebarrier; actualJanaPawłaII59a/2+phone/KatarzynaŻakiewiczqualifiedrole/surgeryverified, stricttrue.

Lux-Vet/VetPremium current5actualbranches: Kraków/Bielsko Localonly restoredwithownbranchrosters/contacts, sharedservice explicitlynames2cities. BroadsharedRT/chemo/surgeryparagraph is notbranchmodalityassignment. JaworzeSłoneczna118, SkoczówTargowa26, WilamowicePaderewskiego28G nowactualunprocessedcandidateunits; 40+ SEOcatchmenttownlinks explicitlypatientsfromtowns, NOTbranchfanout. No extra networklisting: commononcologycontact notindependentlyestablished. VetClinicŁódź dedicatedoncopage explicitchemo, linkedownroster nameslek.wet.AlicjaFornalczyk; unrelatedgamblinginjectedhomepage text ignored, noexternalgamblinglinksfollowed.

Przasnysz independentpre403searchdiscoveredbranchsurgeryclaim, ordinarysameURLnormalTLSfallback got403at2026-10-17T02:50:56.579669+00:00. Exactnewhold restrictions005+native004sealedimmediately; nofurtherreplay/client/cache/variant. ClinicnotpromotedfromdeniedsearchcacheorPułtuskprofile. Savedleader remains genuineunit notclosure. Allavailablecountryfrontier continues, research_complete=false.

PathQA: four task-created mistargetduplicates under /workspace/scratch/2d03a6db0cc6/undefined were recoverably quarantined byparent into controller-quarantine/pl-path-error; authoritative absoluteownroot deltas012/013 andweb029–033 aretheonlynewproof. Notcountedtwice/notdeletedpermanently. Blocks6/7remoteproofpending; earlierremote010 actualdata/receipt remains lastproved atthiswrite. ContinuePoland.


## Блок 8 —112 qualifying; GP chemo/ECT и независимая гематология

Измеренныечасы:2026-10-17 02:56:02 UTC. NEW112=111inheritedfixed+1network; UPDATE0; processed120=112qualifying+6EXCL+2UNRES. Ledger003:159=120processed+16oldabsentunprocessed+20baselineexistingQA+3actualLuxVetPremiumbranches. Freshdiscovery0; report-level86 НЕплюсуется. All9clinicalunits below current17Octsuccessfulsourceproof; не timestampотfailures.

| Единица | Город | Локально подтверждено | Primary URL |
|---|---|---|---|
| Przychodnia Weterynaryjna 4PET | Toruń | Medical oncology; Chemotherapy; Surgical oncology | https://www.przychodnia4pet.pl/uslugi/ |
| Centrum Zdrowia Małych Zwierząt | Gorzów Wielkopolski | Medical oncology; Chemotherapy; Surgery | https://czmz-gorzow.pl/uslugi/onkologia-zwierzat-onkologia-weterynaryjna/ |
| Klinika Weterynaryjna SFORA | Warszawa | Medical oncology; Chemotherapy; Electrochemotherapy | https://klinikasfora.pl/uslugi/onkologia/ |
| Przychodnia Weterynaryjna Jamniczek | Piotrków Trybunalski | Medical oncology; Chemotherapy; Surgical oncology | https://jamniczek24.pl/uslugi/onkologia/ |
| Klinika Weterynaryjna Giszowiec | Katowice | Local oncology care | https://wetklinika.pl/uslugi/hematologia-weterynaryjna/ |
| Przychodnia dla Zwierząt Wnuk | Kraków | Medical oncology; Chemotherapy; Surgery | https://www.przychodniawnuk.pl/onkologia |
| Całodobowa Klinika Weterynaryjna Elwet | Warszawa | Medical oncology; Chemotherapy; Surgical oncology | https://www.elwet.pl/onkologia |
| Klinika Weterynaryjna Arka | Kraków | Medical oncology | https://arka-vet.pl/uslugi/onkologia-weterynaryjna/ |
| Napieraj i Synowie | Radom | Medical oncology; Chemotherapy | https://weterynarz.radom.pl/uslugi/onkologia/ |

4PET currentIV/oralchemo+cancersurgery+qualifiedMarcinPrzystalski2010vet/2017surgery; explicitlyNOhomevisits/weekend/holiday. CZMZGorzów fullcurrenthighdose/metronomic/etc chemo+tumorremoval; PawełStolarek1995vet/2007surgery, cryo/electrosurgeryNOTECT. SFORA fullcurrentPha-Seal/metronomic/ECT andpublishedcurrentJacekMicuńprofessionalrole, notboardcredential. Jamniczek IV/oralchemo+explicitcancersurgery, namedqualifiedGPstaffsufficientwithoutindividualoperatorassignment; externalRTonly. Wnuk currentGPchemo/surgery; RCVSanesthesia/ECC credentialsnotoncologyboard. Elwet currentAnnaJaśkiewiczoncology/MarekGalantysurgery, no24honcologistpromise. Arka currentGrażynaGaworvet1992+explicitcurrentoncopharmacologicalcare, noPhDfromgenericdrlabel.

Giszowiec surgery429 NEVERretried. Independent currenthematologyprimary explicitly treatsbloodcancers/leukemia/lymphoma andnameslek.wet.AgataHandy/KrystynaOchman-Bojarska, actualMysłowicka65aKatowice/322201010. CurrentpackageLocaloncologycareONLY: olderpre429surgerysuccessclaimisretainedhistorically,butfullsuccessfulbodynotlocatedinretained637yet; no chemo/Surgicaltagfrommissingbody. Thisdoesnotmeanactualsurgeryabsence orclinicclosure. SeparateBrzęczkowicenotfanout. Napieraj currentnamedMichałNapierajrole+actualLaluniachemocase12September2024onowncurrentservicepagequalifyMedical/Chemo; currentmayincludeparagraphandguzowatecasesnotalonecancerdirectedSurgeryproof, soSurgeryheldasdetailQA.

Delta016,actualweb043–046,ledger003 savedimmutable; fullproposal112uniqueQA tofreeze. Newsourcefactsnotolderreportcounts. Block8localreadyremoteproofpending; research_complete=false, available16+20+3+regional/roster/RT/mobile/remote frontiercontinues SAMEPoland.


## Блок 9 — восемь текущих официальных пакетов

Время фиксации: 2026-10-17 03:01:03 UTC. Текущий итог: assigned159 = processed128 + unprocessed31; NEW120 =119 унаследованных физических +1 сеть; UPDATE0; EXCLUDED6; UNRESOLVED2; fully120. Оставшиеся31:8 старых неопубликованных+20baseline QA+3 фактических филиала Premium. Все числа provisional до полного национального frontier.

| Клиника | Город | Подтверждённый местный объём | Официальный источник |
|---|---|---|---|
| Przychodnia Weterynaryjna HALIVET | Halinów | Surgical oncology | https://www.halivet.pl/uslugi/ |
| Przychodnia Weterynaryjna Kochanowskiego — Kondratowicza | Warszawa | Local oncology care | https://www.kochanowskiegowet.pl/onkologia-weterynaryjna |
| Przychodnia Weterynaryjna Zalesie | Rzeszów | Surgery | https://przychodniazalesie.pl/uslugi/chirurgia/ |
| Przychodnia i Szpital dla Zwierząt Podkarpacka 52 | Rzeszów | Surgery | https://weterynarz-rzeszow.pl/chirurgia |
| Przychodnia Weterynaryjna VETKA | Bielsko-Biała | Surgery | https://vetka.pl/uslugi/onkologia/ |
| Przychodnia Weterynaryjna Węgrzyn Weterynaria | Strzelce Krajeńskie | Local oncology care | https://strzelce.wegrzynweterynaria.pl/uslugi/onkologia/ |
| Przychodnia Weterynaryjna Zielona Góra | Zielona Góra | Surgery | https://lecznica.zgora.pl/uslugi/chirurgia-ogolna/ |
| Specjalistyczna Przychodnia Weterynaryjna Tomasz Dmuchała | Gdynia | Surgery | https://dmuchala.pl/uslugi/chirurgia/ |

Для Węgrzyn не переношу историческую onkochirurgia со страницы LuxVet403: новая текущая карточка только Local oncology care. Kochanowskiego физический филиал Kondratowicza остаётся Local; общая химиотерапия/иммунотерапия рассматривается отдельно как сеть без адреса/фан-аута; RT явно внешнее сотрудничество. HALIVET общие домашние визиты не подтверждают мобильное лечение рака. Все даты текущих успешных источников17Oct; неоткрытые исторические ссылки/даты квалификаций не становятся новыми посещениями.

Родитель подтвердил remote013 для блока6: data6025992d8618f83f319759086b5e15926a17e991, receiptcf68e465ffa56438605cf1f322b5b0bc694d04ac, verified02:51:14UTC. Remote015 для блоков7/8 и ограничения005: data7404260a0dc64be5109c7619403b5d2a186304ba, receipt333fce04c3b37381db989c8d1d051ebff5466ad1, verified02:57:15UTC. Все readbacksPASS; это backup, не приёмка страны/публикация.


## Блок10 — весь сохранившийся старый неопубликованный пакет восстановлен

2026-10-17 03:03:30 UTC. 127/127 старых отсутствующих идентичностей теперь имеют собственные содержательные первичные пакеты; исторические20 опубликованных не считаются NEW и ещё проходят отдельный QA. Итог161assigned=138processed+23unprocessed. NEW129=127physical+2network, UPDATE0, EXCLUDED7, UNRESOLVED2, fully129. К старым неподкреплённым86 это не прибавляется.

| Провайдер | Город | Подтверждённый объём | URL |
|---|---|---|---|
|Przychodnia Weterynaryjna Hołdowańscy|Pszenno|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy|https://weterynarz.swidnica.pl/specjalizacje/onkologia/|
|Specjalistyczna Przychodnia Weterynaryjna Akacjowa|Kiełczów|Medical oncology, Chemotherapy, Surgery|https://weterynarz-akacjowa.pl/onkologia/|
|Przychodnia Weterynaryjna Sanatus|Krosinko|Surgery|https://www.weterynarz-krosinko.pl/neurochirurgia|
|Przychodnia Weterynaryjna Małych Zwierząt Leonard Gugała — Mieszka I|Szczecin|Local oncology care|https://przychodniawet-szczecin.pl/|
|Lecznica Weterynaryjna MIRAK|Toruń|Local oncology care, Surgery|https://mirak.pl/uslugi/onkologia/|
|Klinika Weterynaryjna TENVET|Kraków|Medical oncology, Chemotherapy, Surgical oncology|https://kwt24.pl/nasze-specjalizacje-onkologia.html|
|AMVET Kraków|Kraków|Local oncology care|https://krakow.amvet.pl/uslugi/onkologia/|
|Całodobowa Klinika Weterynaryjna PUŁAWSKA|Warszawa|Local oncology care|https://weterynarzpulawska.pl/uslugi-weterynaryjne/onkologia-weterynaryjna/|

AMVET Kraków текущий пакет сужен до Local oncology care: фактическое ведение онкобольных подтверждено, условный список может включать химиотерапию/хирургию не подтверждает проведение. Почтовый индекс не блокирует ядро карточки.

Kochanowskiego — ONE новая сетевая запись (Medical/Chemotherapy/Immunotherapy), общий контакт221503500/604711716 явно одинаков для двух филиалов, текущие полные официальные chemo/immuno/team/contact. Без адреса, city, pin и фан-аута; branchfinder https://www.kochanowskiegowet.pl/kontakt . RT только внешнее сотрудничество, ECT не подтверждена отдельно от образовательного описания. Физический Kochanowskiego23/H6 имеет текущую идентичность и GP, но местная онкология не распределена; именованная EXCLUDED_NONPROMOTION, не утверждение отсутствия/закрытия. Кондратовича18B отдельная уже подтверждённая Local запись.

Продолжается весь доступный национальный frontier, включая20baseline QA,3actualPremiumbranches, networks/16regions/mobile/RT/newsignals. research_complete=false.


## Блок11 —20 уже опубликованных, реальные изменения отдельно

2026-10-17 03:07:55 UTC. 161assigned=158processed+3unprocessed. Взаимоисключающая сумма158=129NEW+3UPDATE+17DUPLICATE_ALREADY_APPLIED+7EXCLUDED+2UNRESOLVED. Fully149=129новых+20существующих с текущим полным ядром. NEW129=127physical+2network;20baseline никогда не NEW. Текущие первичные059–068 просмотрены содержательно; старые поисковые snippets не заменяют body.

| Уже существующая запись | Город | Решение | Текущий официальный источник |
|---|---|---|---|
|RTWet — Polski Ośrodek Radioterapii Weterynaryjnej|Wiskitki|DUPLICATE_ALREADY_APPLIED|https://radioterapiaweterynaryjna.pl/en/home-english/|
|Onkovet Przychodnia Weterynaryjna|Gliwice|UPDATE|https://onkovet.pl/uslugi/|
|Przychodnia Weterynaryjna Neo Vet|Poznań|DUPLICATE_ALREADY_APPLIED|https://neo-vet.pl/onkologia|
|GreenVet Przychodnia Weterynaryjna|Zielona Góra|DUPLICATE_ALREADY_APPLIED|https://greenvet.zgora.pl/onkologia/|
|Przychodnia Weterynaryjna VETHOUSE|Lublin|DUPLICATE_ALREADY_APPLIED|https://vethouse.pl/uslugi/onkologia/|
|Praska — Przychodnia Weterynaryjna|Kraków|DUPLICATE_ALREADY_APPLIED|https://weterynarzpraska.pl/uslugi/onkologia/|
|Dom-Vet Przychodnia Weterynaryjna / OnkoWet|Warszawa-Wesoła|DUPLICATE_ALREADY_APPLIED|https://www.domvet.pl/onkologia-weterynaryjna|
|Moonvet — Przychodnia Weterynaryjna Moniki Morawskiej|Łódź|DUPLICATE_ALREADY_APPLIED|https://moonvet.pl/|
|Przychodnia Weterynaryjna Żurawiniec|Poznań|DUPLICATE_ALREADY_APPLIED|https://zurawiniec.grupaluxvet.pl/uslugi/onkologia/|
|Weterynaryjne Centrum Kliniczne Kurosz|Gorzów Wielkopolski|DUPLICATE_ALREADY_APPLIED|https://klinikakurosz.pl/uslugi/onkologia/|
|Przychodnia Weterynaryjna Pobłocki i Miazga|Kosakowo|DUPLICATE_ALREADY_APPLIED|https://poblocki-miazga.pl/chemioterapia/|
|Całodobowa Klinika Weterynaryjna VETKA|Warszawa|DUPLICATE_ALREADY_APPLIED|https://www.lecznica-vetka.pl/zakres-uslug/onkologia/|
|Mokotowska Klinika Weterynaryjna|Warszawa|DUPLICATE_ALREADY_APPLIED|https://mkw-24.pl/nasze-specjalizacje-onkologia.html|
|LEW Weterynaryjne Centrum Zdrowia|Olsztyn|DUPLICATE_ALREADY_APPLIED|https://www.wetlew.pl/onkologia|
|Azyl Przychodnia Weterynaryjna|Horodniany|DUPLICATE_ALREADY_APPLIED|https://azylweterynarz.pl/uslugi/chirurgia/|
|Przychodnia Weterynaryjna Bilscy|Kielce|DUPLICATE_ALREADY_APPLIED|https://przychodniawet.pl/uslugi/|
|Gabinet Weterynaryjny ZWIERZAK|Rzeszów|UPDATE|https://zwierzak.rzeszow.pl/uslugi/|
|Przychodnia Weterynaryjna Krzycka|Wrocław|DUPLICATE_ALREADY_APPLIED|https://weterynarz.wroclaw.pl/uslugi/onkologia/|
|Specjalistyczne Centrum Weterynaryjne — Stanisław Firlik|Opole|DUPLICATE_ALREADY_APPLIED|https://www.klinika.opole.pl/zakres-uslug/onkologia/|
|Przychodnia Weterynaryjna Leonard Gugała 24h — Grupa EDINA|Szczecin|UPDATE|https://www.klinikavet24h.pl/|

Три UPDATE /три поля: Onkovet Gliwice access_note — действующий местный список явно включает Stelfonta (без обещания исхода/универсальной пригодности); ZWIERZAK Rzeszów clinician_review — Jakub Szpunar теперь прямо опубликован как завершивший специализацию хирургии, вместо прежнего «учится» (дата завершения не выдумана); Gugała SzosaStargardzka61 services — Local oncology care вместо Medical, так как актуальная подтверждённая первичная формулировка описывает клиническое ведение рака, не самостоятельное системное введение препаратов. Это не закрытие/исчезновение помощи. Конкретные old/new+URL/цитата/branch/date в baseline-updates001; эквивалентный rawbaseline уже существует в собственномinput, не копирую20полных payloadов заново.

Текущий RTWet подтверждает действующий приём на RT и свой квалифицированный штат. Противоположная старая национальная фраза Kurosz «недоступно в Польше» не используется как актуальный факт. VETHOUSE и Krzycka общие RT-описания не становятся localRT. Praska Sirolimus оказался каплями для пигментного кератита, не раковой услугой; не создаёт онкологическую возможность по названию препарата. Домашние визиты ZWIERZAK/MIRAK не доказывают мобильную химиотерапию.

Продолжение:3actualPremiumbranches, все региональные/сетевые/мобильные/новые сигналы, точный разбор actual636host frontier. research_complete=false.


## Блок12 — Premium3 и честный полный именованный frontier

2026-10-17 03:11:26 UTC. Все5 actualPremiumbranches рассмотрены:2ранее qualifiedLocal(Kraków/Bielsko),3ныне nonpromotion(Jaworze/Skoczów/Wilamowice). Их полные собственные body содержат общую хирургию, не подтверждают cancer-directed delivery; меню сети не становится местной процедурой. Branches не закрыты/не объявлены нелечащими. Общий онкологический центральный контакт не установлен: Jaworze730080700 — emergencyline, не centraloncology. Отдельная networkcard не создаётся. CurrentSkoczów body/contacts694589016 против navigation794700910 — честный конфликт.

Предыдущий assigned161 был явно provisional ограниченным ledger, а не национальным знаменателем. Теперь из полных собственных input-кандидатур и retained named report извлечены ещё98 уникальных фактических provider candidates:15saved +8identity +54regional +3CZZ/Dogtorki additionalbranch +17LuxVet/EDINAclinicalbranch +1MultiVetLutynia. Все98 UNPROCESSED: старые заявленные86/123 без потерянных body не принимаются. Контекст старых кандидатов001/002 присутствует, но утраченные clinicalsources не выдуманы восстановленными. Никакие636доменов не названы636клиниками. PerfectVettraining, Anikaclinicianreference, MyTailblog, Jagielski/Jaśkiewicz educational/personalreferences, Hanusz/Rybicki/falsecityNeoVet/legacyMedicaVet не дополнительные providerunits.

Текущий259assigned=161processed+98unprocessed. Сумма161=129NEW+3UPDATE+17DUP+10EXCL+2UNRES, fully149. NEW129 остаётся127physical+2network. Структурная инвентаризация98 не клиническое выполнение. Полный именной список с URL/типом происхождения — ledger007. Сначала их собственные разрешённые primaryмаршруты, затем остаток636классификации, explicitOR16regions/currentnew, networks/mobile/RT. research_complete=false.


## Блок13 — семь поздних saved leads проверены заново

2026-10-17 03:13:57 UTC.259=168processed+91unprocessed.168=135NEW+3UPDATE+17DUP+11EXCL+2UNRES,fully155. NEW135=127старыхphysical+6late-savedphysical+2network; собственное freshdiscovery по-прежнему0: это реальные повторные проверки сохранённых кандидатов, не выдуманный возврат потерянных sources.

| Провайдер | Город | Текущий объём | URL |
|---|---|---|---|
|Przychodnia Weterynaryjna Przy Kładce|Bydgoszcz|Surgical oncology|https://weterynarz-przykladce.pl/chirurgia/|
|Przychodnia Weterynaryjna DR HAU|Kraków|Surgical oncology|https://drhau.pl/uslugi/chirurgia|
|Całodobowa Lecznica Weterynaryjna Dobrywet|Bobrowiec|Medical oncology, Chemotherapy, Surgical oncology, Electrochemotherapy|https://dobrywet.com/services/onkologia/|
|Przychodnia Weterynaryjna VetHome|Długołęka|Surgical oncology|https://vethome.pl/uslugi/chirurgia/|
|Lecznica Weterynaryjna AS|Olsztyn|Local oncology care|https://lecznica.olsztyn.pl/zakres-swiadczen/|
|Przychodnia Weterynaryjna Lupus|Kraków|Local oncology care|https://lupusvet.pl/|

ABA-VETWarzycka37 не восстановлен автоматически из старого savedNEW: полные service/doctor/experience и отдельный официальный поиск подтверждают GP и общую строку «usuwanieguzów», но не явный противоопухолевый контекст в лечебной услуге. История онкокурсов сама по себе не лечение. Именованная nonpromotion, не отсутствие реального лечения. При появлении явного neoplasm/cancer localstatement вопрос можно пересмотреть. Это применение границы cancer-directed service, а не требование onc-board.

6квалифицирующих совпадений в полном4JSONbaseline3229rows нет; отдельный полныйtele64Poland0. Каждая currentclinical/GP/contactстраница17Oct реально прочитана; старые утраченные sourcebody не называются восстановленными.35ownactualsearchqueries: новый query35 официальныйABA, exactrequest sources076 иqueries005. Остальной национальный фронт продолжается.


## Блок14 — 2026-10-17 03:23:27 UTC
259=177обработанных+82необработанных;177=135NEW+3UPDATE+17DUP+16EXCL+6UNRES. Полных155 безизменения. Пять непродвигаемых: iVetKatowice,Duo-WetWrocław,JaśminvetOrzesze,MultiVetOłowiana,MultiVetLutynia. Общие операции/курсы/направления не доказывают местное лечение рака; отсутствие лечения не утверждается. Четыре сохранённых unresolved: VETJaniszewskiLublin(онкохирургия есть, нет опубликованной текущей квалифицированной роли); MED-VETPałucka/Zachodnia(официальный независимый ZLZ10.09.2026 подтвердил руководителей IwonaWarulik/KatarzynaBajcar и адреса/телефоны, но распределение онкохирургии неясно); Vetspec(timeout+3exactHTTP502,безbody). Доступные шаги остаются; research_complete=false.
PDFskill использован для контроля табличной структуры; текущий screenshot вернул только текстовые маркеры, поэтому визуальный просмотр2026 не заявлен. Сохраняются URL/дата/страница/релевантные факты; полныйPDF и mixedraw079/080 не включены и не хэшированы. Хэш PDF не заявлен. Реальные11запросов, всего46. Подробные поимённые причины/следующие шаги: working/saved-frontier-outcomes-002.json.
Remote017block10: data0c1c7b4bbfd33f3bb50d4a6d5b7b0f4e0cdeb792,receipte5ec6553fba1fe105c34a9b68ab5c8bd4cb251ed,03:06:32UTC;018block11/12:data27e6f05a83c7001c2a701bd44d580930a93c6320,receipt7433ea62791d4812252890e90085bd2375bd7ea1,03:13:23UTC,parentreadbacksPASS.019pending не считается verified и не означает приёмку страны.


## Блок15 — 2026-10-17 03:25:33 UTC
259=183обработанных+76необработанных;183=140NEW+3UP+17DUP+16EXCL+7UNRES. Полных160:138NEWphysical+2network+20baseline. Новые не являются новым открытием этого исполнения: пять сохранённых региональных leads теперь подтверждены первичными источниками и отсутствуют во всех3229baselineстроках/64tele.
| Кандидат | Город | Подтверждённое лечение | Официальный источник |
|---|---|---|---|
| Biegaławet | Inowrocław | Surgical oncology | https://www.biegalawet.pl/oferta/chirurgia |
| Przychodnia Weterynaryjna Amicus | Chełm | Surgery | https://www.amicus-chelm.pl/chirurgia.html |
| Przychodnia Weterynaryjna NaTuwima | Zamość | Surgery | https://www.natuwima.pl/uslugi/laser-chirurgiczny-co2/ |
| Przychodnia Weterynaryjna Royal Vet | Zamość | Surgical oncology | https://royalvet.eu/chirurgia |
| Gabinet Weterynaryjny VetMedica | Zamość | Surgery, Local oncology care | https://vetmedica-zamosc.pl/chirurgia/ |
Biegaławet: текущий контактPopiełuszki12, старая биография упоминаетWojskaPolskiego17; это не второй новый филиал. NaTuwima: CO2хирургия неRT/ECT; cachedстарыйsurgeryтекст не назван свежейпроверкой. AnimalVETPuławy: текущие врачи/адрес проверены, но онкологический интерес врача не заменяет местное лечение; bookingстарыйадрес и рекламируемыйстарыйсайт502, разрешённыйfallback остаётся. Всего48реальныхзапросов,100receiptunits. research_complete=false; полный текущий nationalfrontier ещё доступен.


## Блок16 — 2026-10-17 03:28:47 UTC
259=195обработанных+64необработанных;195=146NEW+3UP+17DUP+17EXCL+12UNRES. Полных166=144NEWphysical+2network+20baseline.
| Сохранённый кандидат, теперь подтверждённый | Город | Лечение | Официальный источник |
|---|---|---|---|
| Przychodnia Weterynaryjna Promienna | Tarnów | Surgical oncology, Local oncology care | https://weterynarztarnow.com.pl/ |
| Gabinet Weterynaryjny Dobry Weterynarz | Myślenice | Surgery, Local oncology care | https://dobryweterynarz.pl/leczenie |
| Animal Centrum | Ostrołęka | Surgical oncology | https://www.animal-centrum.pl/ |
| Przychodnia Weterynaryjna Chiron | Płock | Local oncology care | https://chiron.com.pl/onkologia/ |
| Centrum Zdrowia Zwierząt — Radom | Radom | Surgical oncology | https://www.czz.com.pl/oferta-medyczna/onkologia |
| Przychodnia Weterynaryjna Dogtorki — Szczytno | Szczytno | Local oncology care | https://dogtorki.pl/onkologia/ |
Chiron ограничен Local oncology care: текущая собственная онкологическая страница прямо называет lek.wet.KamilaFormańska-Zimoń; неудачный team/загружаемый календарь не назван свежей проверкой биографии/назначений. DogtorkiSzczytno ограничен Local: планирование терапии не подтверждает фактическую инъекционнуюхимиотерапию/операции. CZZRadom имеет собственную хирургическуюонкологию/контактSylwiaMolenda; нет переноса наIłża/Krzyżanowice. ParkowaSłupsk EXCLnonpromotion(общиеуслуги), отсутствие реального лечения не утверждается. AnimaliaMedicaNowySącz UNRESтекущийврач (2009founderнеавтоматически2026клиницист); CZZIłża/Krzyżanowice/DogtorkiDźwierzuty UNRESместнаяонкология;GiVet UNREStimeout+доступныйfollowup. Реальные3запроса→51,107receiptunits. Подробно:regional-outcomes002. research_complete=false.
Parent подтвердил remote019 в03:21:14UTC:datae85bb6829d0620a1f89d8b5a569e41d3e978b68d,receipt66b1508ed06b413fe78d7662edb124dc96325af1,archive/control/members/receiptreadbackPASS(block13+restriction006). Blocks14/15pending020, не выдаются за backup или приёмкустраны.


## Блок17 — 2026-10-17 03:32:08 UTC
259=206обработанных+53необработанных;206=150NEW+3UP+17DUP+18EXCL+18UNRES. Полных170=148NEWphysical+2network+20baseline.
| Сохранённый кандидат, теперь подтверждённый | Город | Лечение | Официальный источник |
|---|---|---|---|
| Przychodnia Weterynarii Specjalistycznej PRO-WET | Częstochowa | Medical oncology, Chemotherapy, Surgical oncology | https://pro-wet.pl/zakres-us%C5%82ug-pro-wet.html |
| Przychodnia Weterynaryjna VITA | Częstochowa | Surgical oncology, Local oncology care | https://www.lecznicavita.pl/uslugi/leczenie |
| Gabinet Weterynaryjny ARGO | Częstochowa | Surgery | https://argowet.pl/chirurgia-weterynaryjna-czestochowa/ |
| Sosken Vet 24h | Gdańsk | Local oncology care | https://sosken.pl/zakres-uslug/onkologia/ |
PRO-WET: собственные актуальные service/teamстраницы подтвердилихимиотерапию иврачей, не отзывы/старыйреестр. Designerhostaliasнеотдельнаяклиника. VITA: наружнаяконсультацияцентраRTне местнаяRT; ARGO:NuQдиагностика не лечение; Sosken ограниченLocalconsultation/therapeuticassessment,безchemo/Surgery. OpolskiePogotowiePrószków EXCLnonpromotion:oxygenadjunct/emergencycareне противоопухолевое лечение. VetCentrumKluczbork/ZłotorzyńscySuwałki Webtimeout+native502, cachedиндекс не свежаяверификация. CMZPrzemyśl possiblegate007metadataonly безвыдуманного403/CAPTCHA. ProvetNowySącz/ZapiesekMyślenice/DagmaraDobrzyńSuwałki обработаны по реальным сохранённым16Octclinicalfailedattempts, не повторялись и датыуспеха не обновлены; независимые допустимыешаги ещёнеисчерпаны.62реальныхзапроса:4system1изэтогоблокадали нерелевантныйnoise, не доказательствоотсутствия; корректныеdomainfilteredsystem2 иfullprimaryseparate.116receiptunits. research_complete=false.
Remote020 parentPASS03:30:12UTC:data9e89ce6c4d9caed91856911fb18a6a77294d6fc3,receipt9a73aaaa602abb7316064f539419e37372fde568,explicitmembers14/15. Block16/007pending021, неclaimedremoteдоreadback.


## Блок18 — 2026-10-17 03:35:00 UTC
259=214обработанных+45необработанных;214=155NEW+3UP+17DUP+19EXCL+20UNRES. Полных175=153NEWphysical+2network+20baseline.
| Сохранённый кандидат, теперь подтверждённый | Город | Лечение | Официальный источник |
|---|---|---|---|
| Gabinet Weterynaryjny FIVET | Zabrze | Surgical oncology | https://fivet.pl/zakres-uslug |
| Centrum Weterynaryjne Ars-Vet | Ełk | Surgical oncology | https://www.arsvet-elk.pl/chirurgia |
| Klinika Weterynaryjna REHAwet | Piła | Medical oncology, Chemotherapy, Surgical oncology | https://rehawet.pila.pl/uslugi/onkologia |
| Przychodnia Weterynaryjna MILOVET | Konin | Medical oncology, Chemotherapy | https://milovetkonin.pl/ |
| Gabinety Weterynaryjne Franciszkańska | Koszalin | Surgical oncology | https://lecznica.org/chirurgia/ |
REHAwetexplicitchemo+surgery, RTвнешняякооперация; MILOVETexplicitподготовкаИвведениецитостатиковсобакам/кошкам,квалифицированнаяJustynaCaganowskaтекущаяроль. Ars-Vetместнаяонкохирургия,химиотерапия/RTпоexternalreferral. FIVETZabrzeгородresolved,направлениямеждународныйconsiliumнеотдельныйremote. Franciszkańska:733753739клиника,943416399магазин. MaciejMalecTczewnonpromotiongeneraloperations,freeemailнеотдельныйremoteoncology. IławaUNRES:онкоразделдиагностический,общиеguzy/mammaryproceduresнеподтверждаютточнуюместнуюпротивоопухолевуюуслугу. BiałogardUNRES:услугиchemo+surgeryесть,homepage200не даётявнойветеринарнойроли/точнойулицы;heldabout/contactнеповторены.64реальныхзапроса,121receiptunits. research_complete=false.
Parentremote021PASS03:32:12UTC:datadc4d7c590bf3c8bf4b74fcd39d87f4009d32f8f7,receipt82d0ffdbdc876405e2efcc2d99e1fad30ba7fb46,block16+007saved. Block17pendingnext. Это backupнеcountryacceptance/sitepublication.
