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
