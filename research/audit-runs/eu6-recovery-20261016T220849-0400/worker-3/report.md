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
