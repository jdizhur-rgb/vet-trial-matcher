# Польша — итог доступного национального поиска

Исполнитель `/root/eu17_pl`; slot3; run `eu6-recovery-20261018T020312Z`; baseline `2fed31c822a626339b86d752c49949259de7b1ee`.

Доступный документированный национальный фронт завершён. `research_complete=true` относится к выполненному разрешённому поиску и сверке, не к полноте клинических сведений обо всех учреждениях. 75 обработанных кандидатов остаются клинически нерешёнными, ещё2 имеют исчерпанную маршрутизацию без первичной клинической проверки. Они не опубликованы и не объявлены закрытыми. Независимое принятие контроллером, main/сайт и all-six gate — отдельные действия, не выполненные этим исполнителем.

Период: первое зафиксированное показание часов18.10.2026 02:12:44UTC; предварительное чтение началось до него без точного startreceipt; завершение документации `2026-10-18T02:29:23.877903+00:00`. Даты источников не равны времени отчёта.

## Счёт и происхождение результатов

| Показатель | Унаследовано и восстановлено | Реально новое в этом run |
|---|---:|---:|
| Уникальные provider identities |366|0|
| Клинически обработаны |364|0 новых identities;14 известных повторно рассмотрены по15URL|
| Первично не обработаны |2|0 фиктивного processing credit|
| Strict FULL |240:220NEW+20baseline|0|
| NEW |220:211physical+7network+2mobile|0|
| Полевые UPDATE |2|0|
| DUP / EXCL / clinicalUNRES |18 /49 /75|без изменения|
| Поисковые запросы |579 в предыдущем recoveryrun; более ранние324 — только отдельно унаследованная история, не новые посещения|16, все16регионов|
| Actual URL reads |Предыдущие даты16/17Oct сохранены;483legacyretrievalbatchunits не равны визитам/FULL|15:14readable relevant profiles+1tool-not-accessible|

20baseline — уже опубликованные ранее идентичности, не сегодняшние открытия. Полностью восстановлены222эффективных полевых объекта (220NEW+2UP) по001+patches002–019 и revisions001–005. SHA-256 всех55конечных файлов-носителей и канонические SHA-256 всех222объектов проверены. Сборка ledger366 выполнена точной хронологической цепочкой providerpatches/amendments, не возвратом к initial rows. Проверены все5реальных входов:901compiled+893supplemental+977inventory+458ACVIM+64literalASTtele=3293records;220NEW не дали сильных identityduplicates. NeoVetWrocław и existingNeoVetPoznań различны по улице/телефону/домену.

Необязательный email Iława опущен из effective proposal без новогоGET: нет точного retainedcontactlocator. Surgery и основная eligibility не менялись. Другие поля сохраняют старые реальные clinicalsource dates.

## Покрытие16воеводств

Текущий/недатированный слой наследуется из реальных польских query/outcome receipts, включая current-discovery-queries017/queries4–19. Новый18Oct слой —16фактических запросов в current-national-queries001/queries0–15, по одному на строку таблицы;46combined resultrefs сведены к существующим366identities/baseline либо к каталогам/обучению/человеческой медицине/шуму. Ни searchsnippet, ни crawleddate не дали NEW/клиническую свежесть. Все конкретные current independentprofiles из незавершённых75-targetleads дополнительно разобраны15URLreads.

| Регион | Столица/крупные города | Retained NEW physical | Точная coverage proof | Пример primaryURL |
|---|---|---:|---|---|
|Dolnośląskie|Wrocław|19|final-national-coverage.json /regions/0; queries017/4; currentnational/0|[https://ervet.pl/weterynarz-wroclaw/uslugi/onkologia-chemioterapia/](https://ervet.pl/weterynarz-wroclaw/uslugi/onkologia-chemioterapia/)|
|Kujawsko-Pomorskie|Bydgoszcz/Toruń|14|final-national-coverage.json /regions/1; queries017/5; currentnational/1|[https://weterynariakosciuszki.pl/uslugi/chirurgia/](https://weterynariakosciuszki.pl/uslugi/chirurgia/)|
|Lubelskie|Lublin|11|final-national-coverage.json /regions/2; queries017/6; currentnational/2|[https://up.lublin.pl/uslugi/klinika-weterynaryjna/katedra-i-klinika-chirurgii-zwierzat/](https://up.lublin.pl/uslugi/klinika-weterynaryjna/katedra-i-klinika-chirurgii-zwierzat/)|
|Lubuskie|Zielona Góra/Gorzów|6|final-national-coverage.json /regions/3; queries017/7; currentnational/3|[https://animal-doctor.pl/uslugi/chirurgia-miekka/](https://animal-doctor.pl/uslugi/chirurgia-miekka/)|
|Łódzkie|Łódź|6|final-national-coverage.json /regions/4; queries017/8; currentnational/4|[https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-broniewskiego/](https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-broniewskiego/)|
|Małopolskie|Kraków|22|final-national-coverage.json /regions/5; queries017/9; currentnational/5|[https://upw.urk.edu.pl/uslugi?service=oncology](https://upw.urk.edu.pl/uslugi?service=oncology)|
|Mazowieckie|Warszawa|54|final-national-coverage.json /regions/6; queries017/10; currentnational/6|[https://www.vet4pet.pl/specjalizacje/onkologia](https://www.vet4pet.pl/specjalizacje/onkologia)|
|Opolskie|Opole|2|final-national-coverage.json /regions/7; queries017/11; currentnational/7|[https://www.onkolvet.pl/en/oncology/](https://www.onkolvet.pl/en/oncology/)|
|Podkarpackie|Rzeszów|6|final-national-coverage.json /regions/8; queries017/12; currentnational/8|[https://us-wet.pl/uslugi/chirurgia/](https://us-wet.pl/uslugi/chirurgia/)|
|Podlaskie|Białystok|6|final-national-coverage.json /regions/9; queries017/13; currentnational/9|[https://noegoweterynarz.pl/oferta/](https://noegoweterynarz.pl/oferta/)|
|Pomorskie|Gdańsk|12|final-national-coverage.json /regions/10; queries017/14; currentnational/10|[https://animal.med.pl/](https://animal.med.pl/)|
|Śląskie|Katowice|18|final-national-coverage.json /regions/11; queries017/15; currentnational/11|[https://www.almavet.pl/index.php/nasz-zespol/](https://www.almavet.pl/index.php/nasz-zespol/)|
|Świętokrzyskie|Kielce|4|final-national-coverage.json /regions/12; queries017/16; currentnational/12|[https://labrador.ostrowiec.pl/uslugi/onkologia/](https://labrador.ostrowiec.pl/uslugi/onkologia/)|
|Warmińsko-Mazurskie|Olsztyn|6|final-national-coverage.json /regions/13; queries017/17; currentnational/13|[https://lecznica.olsztyn.pl/zakres-swiadczen/](https://lecznica.olsztyn.pl/zakres-swiadczen/)|
|Wielkopolskie|Poznań|17|final-national-coverage.json /regions/14; queries017/18; currentnational/14|[https://www.anicura.pl/znajdz-praktyke/pod-wiezami-przychodnia-weterynaryjna/zabiegi-i-uslugi/](https://www.anicura.pl/znajdz-praktyke/pod-wiezami-przychodnia-weterynaryjna/zabiegi-i-uslugi/)|
|Zachodniopomorskie|Szczecin|8|final-national-coverage.json /regions/15; queries017/19; currentnational/15|[https://przychodniawet-szczecin.pl/](https://przychodniawet-szczecin.pl/)|

В таблице211physicalNEW, не все польские клиники. Остаток по источникам вынесен ниже, в том числе exactmaster gaps; регион не назван «без раковой помощи» из недостаточной страницы. Полная матрица иSHA proof находятся в working/final-national-coverage.json.

## Университеты и сети

| Университет | Фактический outcome | Proof |
|---|---|---|
|SGGW Warszawa|SGGW: подтверждённая Surgery; конкретный хирург/сеанс уточняется при записи|university-matrix-001.json /rows/0; pl-sggw-warszawa|
|UP Lublin|UPLublin: Localoncology; oral/reproductivecancer scope, без неподтверждённых Chemo/RT|university-matrix-001.json /rows/1; pl-up-lublin-kliniki|
|URK Rząska|URKRząska: Localoncology; retainedRomanAleksiewicz role, failedcurrentprofile404 не новая дата/уход|university-matrix-001.json /rows/2; pl-urk-rzaska|
|UMK Toruń|UMKToruń: generalcare/surgery, не canceract; непубликация, не закрытие|university-matrix-001.json /rows/3; pl-umk-torun|
|UWM Olsztyn|UWMOlsztyn: текущая generalsurgery не canceract; oncologycentre2029 — будущее|university-matrix-001.json /rows/4; pl-uwm-olsztyn|
|UP Poznań|UPPoznań: общая работа клиники, currentcancertreatment не установлено|university-matrix-001.json /rows/5; pl-upp-poznan|
|UwB Białystok|UwBBiałystok: запланированная клиника/обучение2027, не нынешний онкологический доступ|university-matrix-001.json /rows/6; pl-uwb-planned-clinic|
|UPWr Wrocław|UPWrWrocław: exactmaster/thoracic403; независимая permitteddiscovery не разрешила currentcare|university-matrix-001.json /rows/7; pl-upwr-clinical-master|

| Сеть/roster | Точный знаменатель и ограничения | Outcome / proof |
|---|---|---|
|LuxVet|57 retained16Oct roster entries =56clinical identities+1PerfectVettrainingreference|All56knownclinical identities reconciled to ledger; currentmasterexact403 held001. Not current18Oct complete57roster; no roster from incidental search snippet. `input/prior/working/frontier-reconciliation-002.json`|
|AniCura|12 actualprehold17Oct branches|All12identities ledger:11qualifying+1Sosnowiecnonpromotion; latermaster403held002, not rebuilt. `input/prior/working/anicura-roster-001.json`|
|EDINA|20 individuallyknown retained clinical identities; unknown full currentmasterdenominator|All20knownIDs ledger; publicmapJSheld003. Currentrosterfullness unproved, not20total asserted. GRABISZYŃSKA primaryidentitygap separate. `input/prior/working/frontier-reconciliation-002.json`|
|SpecVet|2physicalbranches+1separatelytypednetworkcontact|Currentsharedchemo route ONE network; Mokotów/Ursynów branchcare keptindependent, no procedurefanout. `input/prior/working/network-access-001.json`|
|Kochanowskiego|2physicalidentities+1separatelytypednetworkcontact|Kondratowicza physicalLocal; Kochanowskiego23 notphysicaloncopromotion; commonMedical/Chemo/Immunotherapy ONE network. `input/prior/working/network-access-002.json`|
|Maxvet|2Kraków/Michałowicebranches|ONEcurrentnetworkLocal/Surgery; no physicalfanout. Not MAXVETPLUS. `input/prior/working/inherited-revalidated-029.json`|
|MAXVETPLUS|2currentlyidentifiedPułtusk/Przasnysz; old vague6/7 notinvented|Pułtusk known; Przasnysz currentidentity/localcancer gap afteractualroot/treatment/profile/contact/bookingscope. `input/prior/working/fresh-frontier-outcomes-052.json`|
|Zviropolis|4currentidentifiedbranches|Currentroster/localbranchoutcomes ledger; shared grouptext not cloned. `input/prior/working/inherited-revalidated-009.json#/changes/0..3`|
|Teodorowscy|3currentidentifiedbranches|Warszawa independentlyphysicalLocal; Mikołów/Orzesze localallocationgaps; ONEnetworkSurgery via commonclinicalemail. `input/prior/working/roster-outcomes-003.json`|
|Medican|2currentOlsztynbranches|Bothknowncontacts/legalqualifiedhead, noactualoncotherapyclaim;2UNRES not2NEW. `input/prior/working/roster-outcomes-003.json`|
|Amicus|2currentŁódźbranches|ONEcurrentnetworkMedical/Chemo/Surgery via sharedclinicalemail; branchphonesremoved revision005. `input/prior/working/proposal-network-scope-amendment-005.json`|
|Szwarc&Sobik|2Rybnik/Żorybranches|ONEcurrentnetworkSurgery,2physicalallocationgaps; Radlintitle notthirdbranch. `input/prior/working/fresh-frontier-outcomes-031.json`|
|ARS-VETChodzież/Złotów|2currentbranches|ONEcurrentnetworkMedical/Chemo/Surgery via owncommonbookingselector;2physicalallocationgaps, separatefrom Ełk. `input/prior/working/inherited-revalidated-038.json`|

У сетей собственный общий clinicalemail/phone/bookingselector и branchfinder. Все7networkNEW имеют пустые street/city/postcode и nullcoordinates; это7листингов, не7физических адресов. Branchphones Amicus/Maxvet/Teodorowscy удалены revision005; sharedbranchfooter не localdelivery. EDINA20known и LuxVetretained57 не объявлены свежими полными18Octmasterrosters.

## Независимые GP, RT/ECT, visiting/mobile/remote

Прошли отдельные региональные/currentundated/новые сигналы и независимые общие практики. GPchemotherapy допустима без boardoncologist; explicittumourremoval поддерживает Surgery, genericSurgery — нет. Диагностический RTG/радиология/CO2laser/отсылка к внешнему центру не RT. Текущие врачуcredentials не заменяют местный deliveryscope.

RTWet — уже существующий baselineRT; ECT оставлен только при точном собственном подтверждении. Therios Local/Surgery/ECT через physician-authoredIngarden+официальныйMILW qualifiedhead/contact, без Chemo/RT. AMVETKraków Local-only, residency неdiplomate, optionalpostcodeconflict не eligibilitybarrier. GugałaStargardzka Medical сохраняется; Mieszka — отдельный LocalNEW. PRO-VET/Napieraj/HALIVET имеют узкую Surgery; Giszowiec — Local из независимой hematology/currentcontact, без heldSurgery. GoldenVet3branches: explicitownall3surgeryallocation, не Chemo/RT из referral. DAVET — ownserviceindexsuccess до surgicalchallenge; ARWET не получает процедуры из общего physicianprofile. Iława — performedmastectomy для mammarytumours, не диагностическая biopsy и не requirementmalignancyword/board.

Два отдельно типизированных mobileNEW сохранены; обычные homevisits/доставка препаратов не mobilechemo. Нового подтверждённого remoteprovider с базой в Польше0. UKregisteredVOS уже существует отдельно и не становится польским кабинетом/NEWremote. Hippicahorseonly, SowaEgzoticaratsoncology и genericVetDoDomu не dog/catcancerprovider. Все636hostmetadata ранее классифицированы, Wydra и legacyReptilio followups сведены; это не636clinicalvisits.

## Все220NEW — полные эффективные предложения

Все строки ниже retained drafts с исходными источниками16/17Oct, а не сегодняшние открытия. Конкретный branch/session/цена/доступность подтверждаются клиникой; никаких обещаний результата лечения. Поля old/new, credentials, contacts, provenance и supportingURLs полностью находятся в proposed_changes.json.

| Имя | Город/тип | Подтверждённые services | PrimaryURL |
|---|---|---|---|
|Vet4Pet Klinika Weterynaryjna|Warszawa (fixed)|Local oncology care, Surgery|[https://www.vet4pet.pl/specjalizacje/onkologia](https://www.vet4pet.pl/specjalizacje/onkologia)|
|SpecVet Mokotów|Warszawa (fixed)|Local oncology care|[https://specvet.pl/mokotow/](https://specvet.pl/mokotow/)|
|SpecVet Ursynów|Warszawa (fixed)|Local oncology care|[https://specvet.pl/ursynow/](https://specvet.pl/ursynow/)|
|Uniwersytet Przyrodniczy w Lublinie — Klinika Weterynaryjna / Katedra i Klinika Chirurgii Zwierząt|Lublin (fixed)|Local oncology care|[https://up.lublin.pl/uslugi/klinika-weterynaryjna/katedra-i-klinika-chirurgii-zwierzat/](https://up.lublin.pl/uslugi/klinika-weterynaryjna/katedra-i-klinika-chirurgii-zwierzat/)|
|SGGW Klinika Małych Zwierząt|Warszawa (fixed)|Surgery|[https://klinikawet.sggw.edu.pl/klinika/](https://klinikawet.sggw.edu.pl/klinika/)|
|Uniwersytecka Poliklinika Weterynaryjna URK|Rząska (fixed)|Local oncology care|[https://upw.urk.edu.pl/uslugi?service=oncology](https://upw.urk.edu.pl/uslugi?service=oncology)|
|ALMAVET Weterynaryjna Przychodnia Dermatologiczno-Onkologiczna|Sosnowiec (fixed)|Medical oncology, Chemotherapy|[https://www.almavet.pl/index.php/nasz-zespol/](https://www.almavet.pl/index.php/nasz-zespol/)|
|ERVet Specjalistyczna Przychodnia Weterynaryjna|Wrocław (fixed)|Medical oncology, Chemotherapy|[https://ervet.pl/weterynarz-wroclaw/uslugi/onkologia-chemioterapia/](https://ervet.pl/weterynarz-wroclaw/uslugi/onkologia-chemioterapia/)|
|Przychodnia Weterynaryjna OnkolVet|Opole (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy, Immunotherapy|[https://www.onkolvet.pl/en/oncology/](https://www.onkolvet.pl/en/oncology/)|
|SpecVet — oncology network contact|network (network)|Medical oncology, Chemotherapy|[https://specvet.pl/onkologia/](https://specvet.pl/onkologia/)|
|AniCura Animal Broniewskiego Przychodnia Weterynaryjna|Łódź (fixed)|Local oncology care|[https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-broniewskiego/](https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-broniewskiego/)|
|AniCura Gliwicka Przychodnia Weterynaryjna|Gliwice (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Electrochemotherapy, Targeted therapy|[https://wetgliwice.pl/uslugi/onkologia/](https://wetgliwice.pl/uslugi/onkologia/)|
|AniCura ANIMAL.MED Przychodnia Weterynaryjna|Gdańsk (fixed)|Surgical oncology|[https://animal.med.pl/](https://animal.med.pl/)|
|AniCura Molicki Całodobowa Klinika Weterynaryjna|Dąbrowa Górnicza (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://www.anicura.pl/znajdz-praktyke/molicki-klinika-weterynaryjna/](https://www.anicura.pl/znajdz-praktyke/molicki-klinika-weterynaryjna/)|
|AniCura Wróblewscy Przychodnia Weterynaryjna|Dąbrowa Górnicza (fixed)|Local oncology care, Surgical oncology|[https://www.anicura.pl/znajdz-praktyke/wroblewscy-przychodnia-weterynaryjna/zabiegi-i-uslugi/](https://www.anicura.pl/znajdz-praktyke/wroblewscy-przychodnia-weterynaryjna/zabiegi-i-uslugi/)|
|AniCura Legwet Całodobowa Klinika Weterynaryjna|Legionowo (fixed)|Local oncology care, Surgery|[https://www.anicura.pl/znajdz-praktyke/legwet-klinika-weterynaryjna/](https://www.anicura.pl/znajdz-praktyke/legwet-klinika-weterynaryjna/)|
|AniCura Pod Wieżami Przychodnia Weterynaryjna|Poznań (fixed)|Local oncology care|[https://www.anicura.pl/znajdz-praktyke/pod-wiezami-przychodnia-weterynaryjna/zabiegi-i-uslugi/](https://www.anicura.pl/znajdz-praktyke/pod-wiezami-przychodnia-weterynaryjna/zabiegi-i-uslugi/)|
|AniCura Aksvet Przychodnia Weterynaryjna|Oława (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy|[https://weterynarz.olawa.pl/onkologia-weterynaryjna/](https://weterynarz.olawa.pl/onkologia-weterynaryjna/)|
|AniCura Animal Care Center Przychodnia Weterynaryjna|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://animalcarecenter.pl/zakres-uslug/](https://animalcarecenter.pl/zakres-uslug/)|
|AniCura MedicaVet Przychodnia Weterynaryjna|Warszawa (fixed)|Local oncology care|[https://medicavet.pl/home-uslugi/](https://medicavet.pl/home-uslugi/)|
|AniCura Animal Młynarska Przychodnia Weterynaryjna|Łódź (fixed)|Local oncology care|[https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-mlynarska/zabiegi-i-uslugi/](https://www.anicura.pl/znajdz-praktyke/animal-przychodnia-weterynaryjna-mlynarska/zabiegi-i-uslugi/)|
|Przychodnia Weterynaryjna 4 Łapy|Reńska Wieś (fixed)|Local oncology care|[https://4lapywet.pl/uslugi/onkologia/](https://4lapywet.pl/uslugi/onkologia/)|
|Centrum Weterynaryjne Zwierzyniec|Lębork (fixed)|Surgery|[https://centrum-zwierzyniec.pl/uslugi/chirurgia/](https://centrum-zwierzyniec.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Pavet|Warszawa (fixed)|Surgery|[https://pavet.pl/uslugi/zabiegi-chirurgiczne/](https://pavet.pl/uslugi/zabiegi-chirurgiczne/)|
|Animal Doctor Gabinet Weterynaryjny|Gorzów Wielkopolski (fixed)|Surgical oncology|[https://animal-doctor.pl/uslugi/chirurgia-miekka/](https://animal-doctor.pl/uslugi/chirurgia-miekka/)|
|Gdyński Szpital Weterynaryjny|Gdynia (fixed)|Surgery|[https://gswet.pl/uslugi/chirurgia/](https://gswet.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Multivet|Kraków (fixed)|Surgical oncology|[https://multivet.com.pl/uslugi/chirurgia/](https://multivet.com.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Ostródzka|Warszawa (fixed)|Medical oncology|[https://ostrodzka-wet.pl/uslugi/onkologia/](https://ostrodzka-wet.pl/uslugi/onkologia/)|
|Gabinet Weterynaryjny Nesta|Grodzisk Mazowiecki (fixed)|Surgery|[https://nesta-wet.pl/uslugi/chirurgia/](https://nesta-wet.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Orka|Czechowice-Dziedzice (fixed)|Surgical oncology|[https://klinikaorka.pl/uslugi/chirurgia-ogolna/](https://klinikaorka.pl/uslugi/chirurgia-ogolna/)|
|Przychodnia Weterynaryjna Ampułka|Mińsk Mazowiecki (fixed)|Surgery|[https://ampulka.com.pl/uslugi/chirurgia/](https://ampulka.com.pl/uslugi/chirurgia/)|
|Lubelska Poliklinika Weterynaryjna|Lublin (fixed)|Surgical oncology|[https://poliklinikaweterynaryjna.pl/uslugi/chirurgia/](https://poliklinikaweterynaryjna.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Bokserska|Warszawa (fixed)|Surgery|[https://bokserska.waw.pl/uslugi/zabiegi-chirurgiczne/](https://bokserska.waw.pl/uslugi/zabiegi-chirurgiczne/)|
|Przychodnia Weterynaryjna Bytom|Bytom (fixed)|Surgery|[https://weterynariabytom.pl/uslugi/chirurgia/](https://weterynariabytom.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Bajeczna — Bajeczna 1|Kraków (fixed)|Surgery|[https://bajeczna.com.pl/uslugi/chirurgia/](https://bajeczna.com.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Help|Zielona Góra (fixed)|Surgery|[https://help.zgora.pl/uslugi/chirurgia/](https://help.zgora.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Kościuszki|Toruń (fixed)|Surgery|[https://weterynariakosciuszki.pl/uslugi/chirurgia/](https://weterynariakosciuszki.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Tarnowskie Góry|Tarnowskie Góry (fixed)|Surgery|[https://weterynariatarnowskiegory.pl/uslugi/chirurgia-miekka/](https://weterynariatarnowskiegory.pl/uslugi/chirurgia-miekka/)|
|Przychodnia Weterynaryjna US-WET|Szówsko (fixed)|Surgery|[https://us-wet.pl/uslugi/chirurgia/](https://us-wet.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna VET-MED Toruń|Toruń (fixed)|Surgery|[https://vet-med.pl/uslugi/chirurgia/](https://vet-med.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna VETIKA|Grodzisk Mazowiecki (fixed)|Surgical oncology|[https://vetika-grodzisk.pl/uslugi/chirurgia/](https://vetika-grodzisk.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Wesoły Kundelek|Lesko (fixed)|Surgical oncology|[https://przychodniawesolykundelek.pl/uslugi/chirurgia/](https://przychodniawesolykundelek.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna WIBRYS|Płock (fixed)|Surgery|[https://wibrys.pl/zespol/piotr-pawlowski/](https://wibrys.pl/zespol/piotr-pawlowski/)|
|Przychodnia Weterynaryjna Żernicka|Wrocław (fixed)|Surgery|[https://wroclaw-weterynarz.pl/uslugi/chirurgia-weterynaryjna/](https://wroclaw-weterynarz.pl/uslugi/chirurgia-weterynaryjna/)|
|Przychodnia Weterynaryjna Toruń Wyszyńskiego|Toruń (fixed)|Surgery|[https://wyszynskiego.lecznicatorun.pl/uslugi/chirurgia/](https://wyszynskiego.lecznicatorun.pl/uslugi/chirurgia/)|
|Gabinet Weterynaryjny Toruń Migdałowa|Toruń (fixed)|Surgery|[https://migdalowa.lecznicatorun.pl/uslugi/chirurgia-miekka/](https://migdalowa.lecznicatorun.pl/uslugi/chirurgia-miekka/)|
|Gabinet Weterynaryjny Lubicz|Lubicz Górny (fixed)|Surgery|[https://lubicz.lecznicatorun.pl/uslugi/chirurgia/](https://lubicz.lecznicatorun.pl/uslugi/chirurgia/)|
|Lecznica Weterynaryjna VET-MED Brwinów|Brwinów (fixed)|Surgery|[https://brwinow.vetmed.com.pl/uslugi/chirurgia/](https://brwinow.vetmed.com.pl/uslugi/chirurgia/)|
|Gabinet Weterynaryjny MAXVET PLUS Pułtusk|Pułtusk (fixed)|Surgery|[https://maxvetplus.com.pl/uslugi/chirurgia-miekka/](https://maxvetplus.com.pl/uslugi/chirurgia-miekka/)|
|Przychodnia Weterynaryjna VIVOVET|Iwiny (fixed)|Local oncology care, Surgery|[https://vivovet.pl/uslugi/onkologia/](https://vivovet.pl/uslugi/onkologia/)|
|Klinika Weterynaryjna VETS|Warszawa (fixed)|Surgery|[https://vets.pl/uslugi/chirurgia/](https://vets.pl/uslugi/chirurgia/)|
|Vets&Pets Zakładowa|Wrocław (fixed)|Surgery|[https://zakladowa.vetsandpets.pl/uslugi/chirurgia-miekka/](https://zakladowa.vetsandpets.pl/uslugi/chirurgia-miekka/)|
|Vets&Pets Brzozy|Wrocław (fixed)|Surgery|[https://brzozy.vetsandpets.pl/uslugi/chirurgia-miekka/](https://brzozy.vetsandpets.pl/uslugi/chirurgia-miekka/)|
|Vets&Pets Kamienna|Wrocław (fixed)|Surgery|[https://kamienna.vetsandpets.pl/uslugi/chirurgia-miekka/](https://kamienna.vetsandpets.pl/uslugi/chirurgia-miekka/)|
|Przychodnia Weterynaryjna GAJA|Warszawa (fixed)|Surgery|[https://www.przychodniagaja.pl/chirurgia/](https://www.przychodniagaja.pl/chirurgia/)|
|Przychodnia Weterynaryjna HYRAX|Kraków (fixed)|Surgery|[https://www.hyrax.pl/chirurgia-miekka/](https://www.hyrax.pl/chirurgia-miekka/)|
|Lecznica Weterynaryjna LuxVet24|Kraków (fixed)|Local oncology care|[https://luxvet24.pl/team/julia-sliwa/](https://luxvet24.pl/team/julia-sliwa/)|
|Przychodnia Weterynaryjna Na Polance|Poznań (fixed)|Surgery|[https://www.napolance.pl/chirurgia/](https://www.napolance.pl/chirurgia/)|
|Klinika Weterynaryjna NEW VET 24h|Gdynia (fixed)|Surgery|[https://www.newvet24h.pl/chirurgia/](https://www.newvet24h.pl/chirurgia/)|
|Klinika Weterynaryjna MULTIWET|Warszawa (fixed)|Surgical oncology|[https://multiwet.pl/uslugi/chirurgia-miekka/](https://multiwet.pl/uslugi/chirurgia-miekka/)|
|ŻKW Przychodnia Weterynaryjna|Warszawa (fixed)|Local oncology care|[https://weterynaria.waw.pl/stomatologia-weterynaryjna/](https://weterynaria.waw.pl/stomatologia-weterynaryjna/)|
|Klinika Weterynaryjna Marysin|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.wetmarysin.pl/onkologia](https://www.wetmarysin.pl/onkologia)|
|HemaTeamVet|Warszawa (fixed)|Local oncology care|[https://hemateamvet.pl/uslugi/](https://hemateamvet.pl/uslugi/)|
|Zviropolis Klinika Wilanów|Warszawa (fixed)|Surgery|[https://zviropolis.pl/weterynarz-stomatolog-warszawa/](https://zviropolis.pl/weterynarz-stomatolog-warszawa/)|
|Zviropolis Klinika Ochota|Warszawa (fixed)|Surgery|[https://zviropolis.pl/weterynarz-stomatolog-warszawa/](https://zviropolis.pl/weterynarz-stomatolog-warszawa/)|
|Zviropolis Klinika Praga|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgery|[https://zviropolis.pl/weterynarz-stomatolog-warszawa/](https://zviropolis.pl/weterynarz-stomatolog-warszawa/)|
|Zviropolis Klinika Żoliborz|Warszawa (fixed)|Surgery|[https://zviropolis.pl/weterynarz-stomatolog-warszawa/](https://zviropolis.pl/weterynarz-stomatolog-warszawa/)|
|Vet-Service Przychodnia Weterynaryjna|Siedlce (fixed)|Surgical oncology|[https://www.vetservicesiedlce.pl/chirurgia](https://www.vetservicesiedlce.pl/chirurgia)|
|Wetmedic|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://wetmedic.pl/onkologia-2/](https://wetmedic.pl/onkologia-2/)|
|Klinika Teodorowscy Warszawa|Warszawa (fixed)|Local oncology care|[https://www.klinikadlazwierzat.pl/nasz-zespol/](https://www.klinikadlazwierzat.pl/nasz-zespol/)|
|Klinika Weterynaryjna dr n. wet. Dariusz Niedzielski|Wrocław (fixed)|Surgery|[https://www.klinikapsaikota.pl/chirurgia-miekka](https://www.klinikapsaikota.pl/chirurgia-miekka)|
|Przychodnia Weterynaryjna Vetin|Wrocław (fixed)|Surgical oncology|[https://vetin.wroclaw.pl/leczenie-zwierzat](https://vetin.wroclaw.pl/leczenie-zwierzat)|
|Przychodnia Weterynaryjna Strzyża|Gdańsk (fixed)|Local oncology care|[https://przychodniastrzyza.pl/uslugi/onkolog-zwierzecy/](https://przychodniastrzyza.pl/uslugi/onkolog-zwierzecy/)|
|Przychodnia Weterynaryjna Zdrowy Kurczak i Azorek|Siedlce (fixed)|Surgical oncology|[https://weterynarz-siedlce.pl/chirurgia/](https://weterynarz-siedlce.pl/chirurgia/)|
|Przychodnia Weterynaryjna Piotr Dąbrowski|Poznań (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.wet.pl/specjalizacje.html](https://www.wet.pl/specjalizacje.html)|
|Animal Center|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://animal-center.pl/chemioterapia-psow-i-kotow/](https://animal-center.pl/chemioterapia-psow-i-kotow/)|
|KoniczynaVET|Warszawa (fixed)|Medical oncology, Chemotherapy|[https://koniczynavet.pl/konsultacja-onkologiczne](https://koniczynavet.pl/konsultacja-onkologiczne)|
|Lubelskie Centrum Małych Zwierząt|Lublin (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://lcmz.pl/klinika-24h/onkologia](https://lcmz.pl/klinika-24h/onkologia)|
|ArkaNoego Gabinet Weterynaryjny Adam Tymiński|Białystok (fixed)|Local oncology care, Surgical oncology|[https://noegoweterynarz.pl/oferta/](https://noegoweterynarz.pl/oferta/)|
|Przychodnia Weterynaryjna ADA|Rzeszów (fixed)|Surgery|[https://ada.rzeszow.pl/uslugi/chirurgia](https://ada.rzeszow.pl/uslugi/chirurgia)|
|ART VET Gabinet Weterynaryjny|Grębocin (fixed)|Local oncology care, Surgical oncology|[https://www.art-vet.pl/](https://www.art-vet.pl/)|
|Gabinet Weterynaryjny Barbara Szarszewska|Toruń (fixed)|Surgery|[https://weterynarz.torun.pl/chirurgia/](https://weterynarz.torun.pl/chirurgia/)|
|Przychodnia Weterynaryjna Białobrzeska|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy, Immunotherapy|[https://bialobrzeska.waw.pl/uslugi/](https://bialobrzeska.waw.pl/uslugi/)|
|Przychodnia Weterynaryjna z Sercem|Włocławek (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://zsercem.eu/uslugi/onkologia/](https://zsercem.eu/uslugi/onkologia/)|
|Przychodnia Weterynaryjna NeoVet|Wrocław (fixed)|Medical oncology, Chemotherapy, Surgery, Electrochemotherapy, Targeted therapy|[https://www.neovetwroc.pl/elektrochemioterapia/](https://www.neovetwroc.pl/elektrochemioterapia/)|
|Przychodnia Weterynaryjna LABRADOR|Ostrowiec Świętokrzyski (fixed)|Surgery|[https://labrador.ostrowiec.pl/uslugi/onkologia/](https://labrador.ostrowiec.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna PRO-VET|Łódź (fixed)|Medical oncology, Chemotherapy, Surgery, Immunotherapy|[https://provet-lodz.pl/onkologia/](https://provet-lodz.pl/onkologia/)|
|AMVET — Gdańsk|Gdańsk (fixed)|Local oncology care|[https://gdansk.amvet.pl/uslugi/onkologia/](https://gdansk.amvet.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna RYŚ|Piła (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://przychodniarys.pl/uslugi/onkologia/](https://przychodniarys.pl/uslugi/onkologia/)|
|Psychodnia — Przychodnia Weterynaryjna|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgery, Immunotherapy|[https://psychodnia.pl/uslugi/onkologia/](https://psychodnia.pl/uslugi/onkologia/)|
|Klinika Weterynaryjna Bemowo|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgery|[https://bemowo-wet.com.pl/uslugi/onkologia-weterynaryjna/](https://bemowo-wet.com.pl/uslugi/onkologia-weterynaryjna/)|
|Przychodnia Weterynaryjna lek. wet. Marek Pasiak|Siedlce (fixed)|Surgery|[https://lekwet.siedlce.pl/leczenie-profilaktyka-psow-kotow.phtml](https://lekwet.siedlce.pl/leczenie-profilaktyka-psow-kotow.phtml)|
|Veterio — Całodobowa Klinika Weterynaryjna|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy, Immunotherapy|[https://veterio.pl/onkologia-weterynaryjna-warszawa/](https://veterio.pl/onkologia-weterynaryjna-warszawa/)|
|Przychodnia Weterynaryjna LoVeT|Kraków (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://lovet-przychodnia.com/](https://lovet-przychodnia.com/)|
|Klinika Weterynaryjna Szmaragdowa|Lublin (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://klinikaszmaragdowa.pl/uslugi/onkologia-weterynaryjna/](https://klinikaszmaragdowa.pl/uslugi/onkologia-weterynaryjna/)|
|Przychodnia Weterynaryjna REX|Lublin (fixed)|Medical oncology, Chemotherapy, Surgery|[https://lublin-weterynarz.pl/uslugi/onkologia/](https://lublin-weterynarz.pl/uslugi/onkologia/)|
|Trójmiejska Klinika Weterynaryjna|Gdańsk (fixed)|Medical oncology, Chemotherapy, Surgery, Electrochemotherapy|[https://tkw24.pl/uslugi/onkologia/](https://tkw24.pl/uslugi/onkologia/)|
|Ostrowskie Centrum Weterynaryjne|Ostrów Wielkopolski (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://ocw.com.pl/onkologia](https://ocw.com.pl/onkologia)|
|Centrum Weterynaryjne Boliłapka|Białystok (fixed)|Surgical oncology|[https://www.bolilapkabialystok.pl/chirurgia-i-ortopedia](https://www.bolilapkabialystok.pl/chirurgia-i-ortopedia)|
|Przychodnia Weterynaryjna Tropek — Katarzyna Żakiewicz|Białystok (fixed)|Surgical oncology|[https://www.tropek-wet.pl/oferta/chirurgia-miekka](https://www.tropek-wet.pl/oferta/chirurgia-miekka)|
|Vet Premium Kraków — Lux-Vet Premium|Kraków (fixed)|Local oncology care|[https://lux-vet.pl/uslugi/onkologia/](https://lux-vet.pl/uslugi/onkologia/)|
|Specjalistyczna Przychodnia Lux-Vet Premium — Bielsko-Biała|Bielsko-Biała (fixed)|Local oncology care|[https://lux-vet.pl/uslugi/onkologia/](https://lux-vet.pl/uslugi/onkologia/)|
|Vet Clinic — Przychodnia Weterynaryjna|Łódź (fixed)|Medical oncology, Chemotherapy|[https://vetcliniclodz.pl/onkologia](https://vetcliniclodz.pl/onkologia)|
|Przychodnia Weterynaryjna 4PET|Toruń (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://www.przychodnia4pet.pl/uslugi/](https://www.przychodnia4pet.pl/uslugi/)|
|Centrum Zdrowia Małych Zwierząt|Gorzów Wielkopolski (fixed)|Medical oncology, Chemotherapy, Surgery|[https://czmz-gorzow.pl/uslugi/onkologia-zwierzat-onkologia-weterynaryjna/](https://czmz-gorzow.pl/uslugi/onkologia-zwierzat-onkologia-weterynaryjna/)|
|Klinika Weterynaryjna SFORA|Warszawa (fixed)|Medical oncology, Chemotherapy, Electrochemotherapy|[https://klinikasfora.pl/uslugi/onkologia/](https://klinikasfora.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna Jamniczek|Piotrków Trybunalski (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://jamniczek24.pl/uslugi/onkologia/](https://jamniczek24.pl/uslugi/onkologia/)|
|Klinika Weterynaryjna Giszowiec|Katowice (fixed)|Local oncology care|[https://wetklinika.pl/uslugi/hematologia-weterynaryjna/](https://wetklinika.pl/uslugi/hematologia-weterynaryjna/)|
|Przychodnia dla Zwierząt Wnuk|Kraków (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.przychodniawnuk.pl/onkologia](https://www.przychodniawnuk.pl/onkologia)|
|Całodobowa Klinika Weterynaryjna Elwet|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://www.elwet.pl/onkologia](https://www.elwet.pl/onkologia)|
|Klinika Weterynaryjna Arka|Kraków (fixed)|Medical oncology|[https://arka-vet.pl/uslugi/onkologia-weterynaryjna/](https://arka-vet.pl/uslugi/onkologia-weterynaryjna/)|
|Napieraj i Synowie|Radom (fixed)|Medical oncology, Chemotherapy, Surgery|[https://weterynarz.radom.pl/uslugi/onkologia/](https://weterynarz.radom.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna HALIVET|Halinów (fixed)|Surgical oncology|[https://www.halivet.pl/uslugi/](https://www.halivet.pl/uslugi/)|
|Przychodnia Weterynaryjna Kochanowskiego — Kondratowicza|Warszawa (fixed)|Local oncology care|[https://www.kochanowskiegowet.pl/onkologia-weterynaryjna](https://www.kochanowskiegowet.pl/onkologia-weterynaryjna)|
|Przychodnia Weterynaryjna Zalesie|Rzeszów (fixed)|Surgery|[https://przychodniazalesie.pl/uslugi/chirurgia/](https://przychodniazalesie.pl/uslugi/chirurgia/)|
|Przychodnia i Szpital dla Zwierząt Podkarpacka 52|Rzeszów (fixed)|Surgery|[https://weterynarz-rzeszow.pl/chirurgia](https://weterynarz-rzeszow.pl/chirurgia)|
|Przychodnia Weterynaryjna VETKA|Bielsko-Biała (fixed)|Surgery|[https://vetka.pl/uslugi/onkologia/](https://vetka.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna Węgrzyn Weterynaria|Strzelce Krajeńskie (fixed)|Local oncology care|[https://strzelce.wegrzynweterynaria.pl/uslugi/onkologia/](https://strzelce.wegrzynweterynaria.pl/uslugi/onkologia/)|
|Przychodnia Weterynaryjna Zielona Góra|Zielona Góra (fixed)|Surgery|[https://lecznica.zgora.pl/uslugi/chirurgia-ogolna/](https://lecznica.zgora.pl/uslugi/chirurgia-ogolna/)|
|Specjalistyczna Przychodnia Weterynaryjna Tomasz Dmuchała|Gdynia (fixed)|Surgery|[https://dmuchala.pl/uslugi/chirurgia/](https://dmuchala.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Hołdowańscy|Pszenno (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Targeted therapy|[https://weterynarz.swidnica.pl/specjalizacje/onkologia/](https://weterynarz.swidnica.pl/specjalizacje/onkologia/)|
|Specjalistyczna Przychodnia Weterynaryjna Akacjowa|Kiełczów (fixed)|Medical oncology, Chemotherapy, Surgery|[https://weterynarz-akacjowa.pl/onkologia/](https://weterynarz-akacjowa.pl/onkologia/)|
|Przychodnia Weterynaryjna Sanatus|Krosinko (fixed)|Surgery|[https://www.weterynarz-krosinko.pl/neurochirurgia](https://www.weterynarz-krosinko.pl/neurochirurgia)|
|Przychodnia Weterynaryjna Małych Zwierząt Leonard Gugała — Mieszka I|Szczecin (fixed)|Local oncology care|[https://przychodniawet-szczecin.pl/](https://przychodniawet-szczecin.pl/)|
|Lecznica Weterynaryjna MIRAK|Toruń (fixed)|Local oncology care, Surgery|[https://mirak.pl/uslugi/onkologia/](https://mirak.pl/uslugi/onkologia/)|
|Klinika Weterynaryjna TENVET|Kraków (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://kwt24.pl/nasze-specjalizacje-onkologia.html](https://kwt24.pl/nasze-specjalizacje-onkologia.html)|
|AMVET Kraków|Kraków (fixed)|Local oncology care|[https://krakow.amvet.pl/uslugi/onkologia/](https://krakow.amvet.pl/uslugi/onkologia/)|
|Całodobowa Klinika Weterynaryjna PUŁAWSKA|Warszawa (fixed)|Local oncology care|[https://weterynarzpulawska.pl/uslugi-weterynaryjne/onkologia-weterynaryjna/](https://weterynarzpulawska.pl/uslugi-weterynaryjne/onkologia-weterynaryjna/)|
|Przychodnia Weterynaryjna Kochanowskiego — network oncology contact|network (network)|Medical oncology, Chemotherapy, Immunotherapy|[https://www.kochanowskiegowet.pl/chemioterapia](https://www.kochanowskiegowet.pl/chemioterapia)|
|Przychodnia Weterynaryjna Przy Kładce|Bydgoszcz (fixed)|Surgical oncology|[https://weterynarz-przykladce.pl/chirurgia/](https://weterynarz-przykladce.pl/chirurgia/)|
|Przychodnia Weterynaryjna DR HAU|Kraków (fixed)|Surgical oncology|[https://drhau.pl/uslugi/chirurgia](https://drhau.pl/uslugi/chirurgia)|
|Całodobowa Lecznica Weterynaryjna Dobrywet|Bobrowiec (fixed)|Medical oncology, Chemotherapy, Surgical oncology, Electrochemotherapy|[https://dobrywet.com/services/onkologia/](https://dobrywet.com/services/onkologia/)|
|Przychodnia Weterynaryjna VetHome|Długołęka (fixed)|Surgical oncology|[https://vethome.pl/uslugi/chirurgia/](https://vethome.pl/uslugi/chirurgia/)|
|Lecznica Weterynaryjna AS|Olsztyn (fixed)|Local oncology care|[https://lecznica.olsztyn.pl/zakres-swiadczen/](https://lecznica.olsztyn.pl/zakres-swiadczen/)|
|Przychodnia Weterynaryjna Lupus|Kraków (fixed)|Local oncology care|[https://lupusvet.pl/](https://lupusvet.pl/)|
|Biegaławet|Inowrocław (fixed)|Surgical oncology|[https://www.biegalawet.pl/oferta/chirurgia](https://www.biegalawet.pl/oferta/chirurgia)|
|Przychodnia Weterynaryjna Amicus|Chełm (fixed)|Surgery|[https://www.amicus-chelm.pl/chirurgia.html](https://www.amicus-chelm.pl/chirurgia.html)|
|Przychodnia Weterynaryjna NaTuwima|Zamość (fixed)|Surgery|[https://www.natuwima.pl/uslugi/laser-chirurgiczny-co2/](https://www.natuwima.pl/uslugi/laser-chirurgiczny-co2/)|
|Przychodnia Weterynaryjna Royal Vet|Zamość (fixed)|Surgical oncology|[https://royalvet.eu/chirurgia](https://royalvet.eu/chirurgia)|
|Gabinet Weterynaryjny VetMedica|Zamość (fixed)|Surgery, Local oncology care|[https://vetmedica-zamosc.pl/chirurgia/](https://vetmedica-zamosc.pl/chirurgia/)|
|Przychodnia Weterynaryjna Promienna|Tarnów (fixed)|Surgical oncology, Local oncology care|[https://weterynarztarnow.com.pl/](https://weterynarztarnow.com.pl/)|
|Gabinet Weterynaryjny Dobry Weterynarz|Myślenice (fixed)|Surgery, Local oncology care|[https://dobryweterynarz.pl/leczenie](https://dobryweterynarz.pl/leczenie)|
|Animal Centrum|Ostrołęka (fixed)|Surgical oncology|[https://www.animal-centrum.pl/](https://www.animal-centrum.pl/)|
|Przychodnia Weterynaryjna Chiron|Płock (fixed)|Local oncology care|[https://chiron.com.pl/onkologia/](https://chiron.com.pl/onkologia/)|
|Centrum Zdrowia Zwierząt — Radom|Radom (fixed)|Surgical oncology|[https://www.czz.com.pl/oferta-medyczna/onkologia](https://www.czz.com.pl/oferta-medyczna/onkologia)|
|Przychodnia Weterynaryjna Dogtorki — Szczytno|Szczytno (fixed)|Local oncology care|[https://dogtorki.pl/onkologia/](https://dogtorki.pl/onkologia/)|
|Przychodnia Weterynarii Specjalistycznej PRO-WET|Częstochowa (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://pro-wet.pl/zakres-us%C5%82ug-pro-wet.html](https://pro-wet.pl/zakres-us%C5%82ug-pro-wet.html)|
|Przychodnia Weterynaryjna VITA|Częstochowa (fixed)|Surgical oncology, Local oncology care|[https://www.lecznicavita.pl/uslugi/leczenie](https://www.lecznicavita.pl/uslugi/leczenie)|
|Gabinet Weterynaryjny ARGO|Częstochowa (fixed)|Surgery|[https://argowet.pl/chirurgia-weterynaryjna-czestochowa/](https://argowet.pl/chirurgia-weterynaryjna-czestochowa/)|
|Sosken Vet 24h|Gdańsk (fixed)|Local oncology care|[https://sosken.pl/zakres-uslug/onkologia/](https://sosken.pl/zakres-uslug/onkologia/)|
|Gabinet Weterynaryjny FIVET|Zabrze (fixed)|Surgical oncology|[https://fivet.pl/zakres-uslug](https://fivet.pl/zakres-uslug)|
|Centrum Weterynaryjne Ars-Vet|Ełk (fixed)|Surgical oncology|[https://www.arsvet-elk.pl/chirurgia](https://www.arsvet-elk.pl/chirurgia)|
|Klinika Weterynaryjna REHAwet|Piła (fixed)|Medical oncology, Chemotherapy, Surgical oncology|[https://rehawet.pila.pl/uslugi/onkologia](https://rehawet.pila.pl/uslugi/onkologia)|
|Przychodnia Weterynaryjna MILOVET|Konin (fixed)|Medical oncology, Chemotherapy|[https://milovetkonin.pl/](https://milovetkonin.pl/)|
|Gabinety Weterynaryjne Franciszkańska|Koszalin (fixed)|Surgical oncology|[https://lecznica.org/chirurgia/](https://lecznica.org/chirurgia/)|
|Leszczyńskie Centrum Weterynaryjne Misiu|Leszno (fixed)|Surgery, Local oncology care|[https://www.weterynarz-leszno.pl/uslugi/chirurgia/](https://www.weterynarz-leszno.pl/uslugi/chirurgia/)|
|Przychodnia Weterynaryjna Adam Hauke / HAUWET|Konin (fixed)|Surgical oncology|[https://hauwet.pl/](https://hauwet.pl/)|
|Gabinet Weterynaryjny Vet Medica|Świnoujście (fixed)|Surgery|[https://www.e-vetmedica.pl/service](https://www.e-vetmedica.pl/service)|
|Lecznica weterynaryjna Serwin|Nowy Sącz (fixed)|Surgery|[https://www.lecznicaserwin.pl/pl/chirurgia-ogolna.html](https://www.lecznicaserwin.pl/pl/chirurgia-ogolna.html)|
|Przychodnia weterynaryjna VetMania|Gdańsk (fixed)|Local oncology care|[https://vetmania.vet/uslugi.html](https://vetmania.vet/uslugi.html)|
|Przychodnia Weterynaryjna DOG — Remigiusz Cichoń|Skarżysko-Kamienna (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.dog.com.pl/uslugi/szczegolowa-oferta-firmy](https://www.dog.com.pl/uslugi/szczegolowa-oferta-firmy)|
|Przychodnia weterynaryjna Dr.Wet — Karolina Malińska|Warszawa (fixed)|Medical oncology, Chemotherapy, Surgery|[https://dr-wet.pl/onkologia/](https://dr-wet.pl/onkologia/)|
|Przychodnia weterynaryjna Pupilmed|Warszawa (fixed)|Local oncology care|[https://pupilmed.pl/weterynaria/onkologia](https://pupilmed.pl/weterynaria/onkologia)|
|VetGo — mobilna opieka weterynaryjna|Kraków; surrounding towns advertised onhome/areapages but about saysKrakówonly, confirm outside-city reach directly. (mobile)|Local oncology care|[https://www.wizytaweterynarza.pl/oferta/](https://www.wizytaweterynarza.pl/oferta/)|
|Przychodnia Weterynaryjna VET — Wiesław Janiszewski|Lublin (fixed)|Surgery|[https://www.vetlublin.pl/index.php?go=34](https://www.vetlublin.pl/index.php?go=34)|
|Animalia Medica|Nowy Sącz (fixed)|Surgery|[https://www.animaliamedica.pl/chirurgia.html](https://www.animaliamedica.pl/chirurgia.html)|
|Przychodnia Weterynaryjna Thalvet — Wawrzyniec Thal|Chrzanów (fixed)|Surgery|[https://weterynarz-chrzanow.pl/](https://weterynarz-chrzanow.pl/)|
|Przychodnia Weterynaryjna VetMedica|Chojnice (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.vetmedica-chojnice.pl/10_leczenie.html](https://www.vetmedica-chojnice.pl/10_leczenie.html)|
|Przychodnia Weterynaryjna OLWET|Tczew (fixed)|Surgery|[https://olwettczew.pl/zakres-uslug](https://olwettczew.pl/zakres-uslug)|
|Lecznica Weterynaryjna Animals — Piotr Burzyński|Bielsk Podlaski (fixed)|Surgery|[https://animals-wet.pl/](https://animals-wet.pl/)|
|Amicus — sieć placówek weterynaryjnych w Łodzi|Łódź (network)|Medical oncology, Chemotherapy, Surgery|[https://weterynarzlodz.pl/](https://weterynarzlodz.pl/)|
|Maxvet — sieć gabinetów Kraków/Michałowice|Kraków / Michałowice (network)|Local oncology care, Surgery|[https://maxvet.com.pl/zespol/](https://maxvet.com.pl/zespol/)|
|Klinika Teodorowscy — sieć klinik|Mikołów / Orzesze / Warszawa (branch finder; common clinical email confirmed for Mikołów/Orzesze) (network)|Surgery|[https://www.klinikadlazwierzat.pl/uslugi/chirurgia-miekka/usuniecie-guzow/](https://www.klinikadlazwierzat.pl/uslugi/chirurgia-miekka/usuniecie-guzow/)|
|Przychodnia Weterynaryjna TELVET — Szymon Teliński|Koszalin (fixed)|Surgery|[https://www.telvet.pl/oferta/kriochirurgia-wymrazanie](https://www.telvet.pl/oferta/kriochirurgia-wymrazanie)|
|Przychodnia Weterynaryjna NOVA|Nowa Sól (fixed)|Surgery|[https://www.nova-vet.pl/uslugi.php](https://www.nova-vet.pl/uslugi.php)|
|Gabinet Weterynaryjny PUPIL — Marta Jurewicz|Elbląg (fixed)|Surgery|[https://www.pupil.elblag.pl/53,zabiegi-chirurgiczne](https://www.pupil.elblag.pl/53,zabiegi-chirurgiczne)|
|Przychodnia Weterynaryjna Podaj Łapę — Joanna i Artur Różyccy|Brzeg Dolny (fixed)|Surgery|[https://podajlape.az.pl/nasze-uslugi/](https://podajlape.az.pl/nasze-uslugi/)|
|Przychodnia Weterynaryjna Karpacka|Bielsko-Biała (fixed)|Surgery|[https://weterynarz-bielsko.pl/uslugi/onkologia/](https://weterynarz-bielsko.pl/uslugi/onkologia/)|
|Centrum Weterynaryjne 4 Łapy|Jelenia Góra (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.lecznica.4lapy.jgora.pl/oferta/](https://www.lecznica.4lapy.jgora.pl/oferta/)|
|Przychodnia Weterynaryjna ARKA — Jolanta i Adam Kracińscy|Włocławek (fixed)|Surgery|[https://arka.wloclawek.pl/oferta/](https://arka.wloclawek.pl/oferta/)|
|Przychodnia Weterynaryjna im. Piotra Tymienieckiego|Sieradz (fixed)|Surgery|[https://weterynarz-sieradz.pl/nasze-uslugi/chirurgia-weterynaryjna/](https://weterynarz-sieradz.pl/nasze-uslugi/chirurgia-weterynaryjna/)|
|Przychodnia Weterynaryjna CENTRUM — Mateusz Stachowiak|Brodnica (fixed)|Surgery|[https://lecznicacentrum.pl/chirurgia/](https://lecznicacentrum.pl/chirurgia/)|
|Przychodnia Weterynaryjna ARKA — Jacek Zarzecki|Legnica (fixed)|Surgery|[https://www.arkalegnica.pl/](https://www.arkalegnica.pl/)|
|Eyeris Okulistyczna Przychodnia Weterynaryjna|Ciechanów (fixed)|Surgery|[https://www.eyeris.pl/chirurgia](https://www.eyeris.pl/chirurgia)|
|Gabinet Weterynaryjny Dorota Florysiak|Płock (fixed)|Surgery|[https://www.weterynarze-plock.com.pl/](https://www.weterynarze-plock.com.pl/)|
|Przychodnia Weterynaryjna ARKA — Piotr i Franciszek Surma|Bochnia (fixed)|Surgery|[https://www.arka-weterynaria.pl/](https://www.arka-weterynaria.pl/)|
|Gabinet Weterynaryjny ALFA — Sylwia Rutkowska|Łomża (fixed)|Surgery|[https://vetalfa.pl/](https://vetalfa.pl/)|
|Przychodnia Weterynaryjna DONA|Piła (fixed)|Surgery|[https://dona.pila.pl/oferta/leczenie-chirurgiczne/](https://dona.pila.pl/oferta/leczenie-chirurgiczne/)|
|Pet Medica — gabinet weterynaryjny|Kalisz (fixed)|Surgery|[https://petmedica.pl/](https://petmedica.pl/)|
|Przychodnia Weterynaryjna zooVET|Rzęskowo (fixed)|Surgery|[https://zoovet.com.pl/](https://zoovet.com.pl/)|
|Przychodnia Weterynaryjna Dr Ola — Aleksandra Grzeczny|Racibórz (fixed)|Surgery|[https://weterynarzraciborz.pl/uslugi/chirurgia](https://weterynarzraciborz.pl/uslugi/chirurgia)|
|Rodzinna Przychodnia Weterynaryjna|Szczecin (fixed)|Surgery|[https://www.rodzinnawet.pl/index.php/chirurgia-2/](https://www.rodzinnawet.pl/index.php/chirurgia-2/)|
|Przychodnia Weterynaryjna AS — Maciej Skowyra|Piła (fixed)|Surgery|[https://www.weterynarz.pila.pl/nasza-oferta/chirurgia](https://www.weterynarz.pila.pl/nasza-oferta/chirurgia)|
|Gabinet weterynaryjny — Łazienna 4|Augustów (fixed)|Surgery|[https://weterynarz.augustow.pl/uslugi/](https://weterynarz.augustow.pl/uslugi/)|
|Szwarc & Sobik — network cancer-surgery contact|network (network)|Surgery|[https://lecznica.net.pl/chirurgia](https://lecznica.net.pl/chirurgia)|
|Gabinet Weterynaryjny Kameleon|Siedlce (fixed)|Surgery|[https://www.wet-siedlce.pl/uslugi/chirurgia](https://www.wet-siedlce.pl/uslugi/chirurgia)|
|Przychodnia Weterynaryjna nad Lubrzanką / Amigo|Suków (fixed)|Medical oncology, Chemotherapy, Surgery|[https://weterynarzkielce.pl/oferta/](https://weterynarzkielce.pl/oferta/)|
|Gabinet Weterynaryjny Anna i Mateusz Radziwołek|Białogard (fixed)|Medical oncology, Chemotherapy, Surgery|[http://veterynarz.pl/](http://veterynarz.pl/)|
|Gabinet Weterynaryjny Zdrowy Zwierz|Zamość (fixed)|Local oncology care, Surgery|[https://zdrowy-zwierz.pl/weterynarz-uslugi/](https://zdrowy-zwierz.pl/weterynarz-uslugi/)|
|Gabinet Weterynaryjny Sana Animalis — Weronika Rarok|Chybie (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.sanaanimalis.pl/oferta/onkologia](https://www.sanaanimalis.pl/oferta/onkologia)|
|Klinika Weterynaryjna Lancet|Warszawa (fixed)|Local oncology care, Surgery|[https://lancet.waw.pl/uslugi/](https://lancet.waw.pl/uslugi/)|
|Przychodnia Weterynaryjna Wojciech Nowakowski — Gałeczki|Chorzów (fixed)|Surgery|[https://weterynaria.slask.pl/uslugi-weterynaryjne/chirurgia-weterynaryjna-w-chorzowie](https://weterynaria.slask.pl/uslugi-weterynaryjne/chirurgia-weterynaryjna-w-chorzowie)|
|Przychodnia Weterynaryjna Therios|Myślenice (fixed)|Local oncology care, Surgery, Electrochemotherapy|[https://www.znanylekarz.pl/profil/jacek-ingarden](https://www.znanylekarz.pl/profil/jacek-ingarden)|
|Przychodnia Weterynaryjna LABEK|Ostrów Wielkopolski (fixed)|Surgery|[https://www.labek.com.pl/chirurgia.html](https://www.labek.com.pl/chirurgia.html)|
|Przychodnia Weterynaryjna ARS-VET — sieć Chodzież / Złotów|network (network)|Medical oncology, Chemotherapy, Surgery|[https://www.arsvet.pl/onkologia-weterynaryjna](https://www.arsvet.pl/onkologia-weterynaryjna)|
|Przychodnia Weterynaryjna Sanitas|Ełk (fixed)|Surgery|[https://przychodniasanitas.pl/oferta/](https://przychodniasanitas.pl/oferta/)|
|Centrum Weterynaryjne Ossowscy|Leszno (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.klinika.note.pl/klinika-malych-zwierzat.php](https://www.klinika.note.pl/klinika-malych-zwierzat.php)|
|Gabinet Weterynaryjny lek. wet. Dariusz Filipiński|Poznań (fixed)|Medical oncology, Chemotherapy, Surgery|[https://www.wet-poznan.pl/index.php/oferta-1](https://www.wet-poznan.pl/index.php/oferta-1)|
|LABROS Specjalistyczna Przychodnia Weterynaryjna|Warszawa (fixed)|Surgery|[https://labros.pl/nasz-zespol](https://labros.pl/nasz-zespol)|
|Lecznica dla Zwierząt Sławomir Witczak|Kalisz (fixed)|Surgery|[https://weterynarz-witczak.pl/chirurgia/](https://weterynarz-witczak.pl/chirurgia/)|
|Gabinet Weterynaryjny Józef i Błażej Kozar|Białogard (fixed)|Medical, Chemo, Surgery|[https://www.weterynarzbialogard.pl/oferta/](https://www.weterynarzbialogard.pl/oferta/)|
|Gabinet Weterynaryjny ANIMAL — Justyna Maciąg-Kuźma|Busko-Zdrój (fixed)|Surgery|[https://www.weterynarz-busko.pl/uslugi/](https://www.weterynarz-busko.pl/uslugi/)|
|Gabinet Weterynaryjny DOGTOR — Paweł Dadej i Piotr Rabiasz|Bochnia (fixed)|Local oncology care|[https://booksy.com/pl-pl/123262_gabinet-weterynaryjny-dogtor_zwierzaki_10189_bochnia](https://booksy.com/pl-pl/123262_gabinet-weterynaryjny-dogtor_zwierzaki_10189_bochnia)|
|lek. wet. Kacper Kubicki — stomatologia psów i kotów (visiting)|Warszawa–Konstancin-Jeziorna; publishedpartnercliniclocations only. Confirm actualplace/procedure/session withphysician; nothomevisits orcountrywidenetwork. (mobile)|Surgery|[https://psiokociastomatologia.com/zakres-uslug/](https://psiokociastomatologia.com/zakres-uslug/)|
|GoldenVet — Drzewieckiego|Wrocław (fixed)|Surgery|[https://goldenvet.pl/usuwanie-guzow/](https://goldenvet.pl/usuwanie-guzow/)|
|GoldenVet — Jagodno|Wrocław (fixed)|Surgery|[https://goldenvet.pl/usuwanie-guzow/](https://goldenvet.pl/usuwanie-guzow/)|
|GoldenVet — Korzenna|Wrocław (fixed)|Surgery|[https://goldenvet.pl/usuwanie-guzow/](https://goldenvet.pl/usuwanie-guzow/)|
|Lecznica dla Zwierząt ADA — Przemyśl|Przemyśl (fixed)|Surgery|[https://www.lecznica-ada.pl/](https://www.lecznica-ada.pl/)|
|Gabinet Weterynaryjny DAVET — Radłów|Radłów (fixed)|Surgery|[https://davet.pl/zakres-uslug/](https://davet.pl/zakres-uslug/)|
|Gabinet Weterynaryjny — lek. wet. Arkadiusz Szkamelski|Iława (fixed)|Surgery|[https://weterynarz-ilawa.pl/zakres-uslug/](https://weterynarz-ilawa.pl/zakres-uslug/)|

## ДваUPDATE — не новые клиники

| Имя / город | Поле / изменение | PrimaryURL |
|---|---|---|
|Onkovet /Gliwice|access_note: собственный treatmentroster дополнительно называет Stelfonta; suitability/appointment уточняются, без efficacy/universaleligibilityclaim|[https://onkovet.pl/uslugi/](https://onkovet.pl/uslugi/)|
|ZWIERZAK /Rzeszów|clinician_review: JakubSzpunar теперь публикует completedSpecjalistaChirurgiiWeterynaryjnej вместо inprogress; не oncologyboard, не новый ECTfilter|[https://zwierzak.rzeszow.pl/lecznica/](https://zwierzak.rzeszow.pl/lecznica/)|

## Отклонённые49: почему не предложены

EXCLUDED_NONPROMOTION означает недостаточность/несоответствие конкретной прочитанной собственной evidence, не доказательство отсутствия лечения или закрытия. Отзывы/картинки/общие Surgery или Hematology/образование не promoted.

| Имя / город | Причина | Точный outcome |
|---|---|---|
|UMK Toruń /UMK Toruń|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/university-matrix-001.json#/rows/3`|
|UWM Olsztyn /UWM Olsztyn|Текущая generalSurgery; cancercentre2029 ещё будущее|`input/prior/working/university-matrix-001.json#/rows/4`|
|UP Poznań /UP Poznań|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/university-matrix-001.json#/rows/5`|
|UwB Białystok /UwB Białystok|Планируемая клиника/обучение2027, не currentcare|`input/prior/working/university-matrix-001.json#/rows/6`|
|AniCuraMolickiRysia2a /Sosnowiec|Расширенная помощь отнесена к Dąbrowa, не Rysia2a|`input/prior/working/anicura-roster-001.json#/branches/11`|
|ZebrzydowickaWET /Rybnik|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-frontier-outcomes-001.json#/candidates/0`|
|PrzychodniaLux-VetJaworze /Jaworze|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-frontier-outcomes-005.json#/candidates/0`|
|GabinetLux-VetSkoczów /Skoczów|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-frontier-outcomes-005.json#/candidates/1`|
|PrzychodniaLux-VetWilamowice /Wilamowice|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-frontier-outcomes-005.json#/candidates/2`|
|Kochanowskiego23/H6 physical /Warszawa|Онкокоманда назначена Kondratowicza; sharednetwork не physicaldelivery|`input/prior/working/network-frontier-outcomes-004.json#/candidates/0`|
|Przychodnia Weterynaryjna ABA-VET S.C. Wojtaszek /Wieliczka|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/saved-frontier-outcomes-001.json#/candidates/0`|
|iVet Katowice /Katowice|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/saved-frontier-outcomes-002.json#/candidates/0`|
|Duo-Wet /Wrocław|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/saved-frontier-outcomes-002.json#/candidates/1`|
|Jaśminvet /Orzesze-Zgoń|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/saved-frontier-outcomes-002.json#/candidates/2`|
|MultiVet Ołowiana /Wrocław|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/saved-frontier-outcomes-002.json#/candidates/3`|
|Parkowa Słupsk /Słupsk|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/regional-outcomes-002.json#/candidates/4`|
|Opolskie Pogotowie Weterynaryjne /Opole|Emergencyoxygen/supportivecare не противоопухолевое лечение|`input/prior/working/regional-outcomes-003.json#/candidates/0`|
|Przychodnia Centrum Maciej Malec /Tczew|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/regional-outcomes-004.json#/candidates/0`|
|Canisia /Kalisz|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/regional-outcomes-005.json#/candidates/0`|
|Vet Brand /Koszalin|Офтальмология/корнеальный melanosis не подтверждают malignantcancertherapy|`input/prior/working/regional-outcomes-005.json#/candidates/1`|
|Centrum Weterynaryjne OPTIMUM /Nowy Sącz|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-001.json#/candidates/0`|
|Gabinet Weterynaryjny Węgrzyn Weterynaria /Dobiegniew|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-001.json#/candidates/1`|
|Przychodnia Weterynaryjna Felis /Brzeszcze|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-001.json#/candidates/3`|
|Przychodnia Weterynaryjna Kwilcz /Kwilcz|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-001.json#/candidates/4`|
|Przychodnia Weterynaryjna VET-MED VET VITA /Błonie|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-001.json#/candidates/5`|
|BRYNÓW /Katowice|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-002.json#/candidates/0`|
|Folwark Zwierzęcy /Kraków|Generalhematology не explicitbloodcancertherapy|`input/prior/working/network-remainder-outcomes-002.json#/candidates/1`|
|NA NARAMOWICACH /Poznań|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-002.json#/candidates/2`|
|REPTILIO /Siemianowice Śląskie|Currentscope smallmammals/exotics/reptiles, не dog/catcancer|`input/prior/working/regional-outcomes-006.json#/reclassifications/0`|
|TAUZEN WET /Katowice|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/network-remainder-outcomes-002.json#/candidates/3`|
|MultiVet — Lutynia rehabilitation branch /Lutynia|Реабилитационный/гидротерапевтический филиал, не cancerdelivery|`input/prior/working/saved-frontier-outcomes-002.json#/candidates/4`|
|VetDoDomu /Kraków|Generalhomecare/drugdelivery не mobileoncology|`input/prior/working/identity-outcomes-002.json#/candidates/5`|
|Gabinet Weterynaryjny Hippica — Anna Tarczykowska /Toruń/Bydgoszcz region mobile|Только лошади, не dog/catcancer|`input/prior/working/roster-outcomes-003.json#/candidates/4`|
|Przychodnia Weterynaryjna Sowa Egzotica /Bydgoszcz|Явная онкология крыс/экзотов, не dog/catcancer|`input/prior/working/roster-outcomes-003.json#/candidates/5`|
|Lecznica Weterynaryjna Polna /Toruń|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/roster-outcomes-003.json#/candidates/6`|
|Przychodnia Weterynaryjna WALVET /Brzeg|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-029.json#/records/0`|
|Przychodnia Weterynaryjna ALASKA /Brzeg|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-029.json#/records/1`|
|Gabinet Weterynaryjny Radosław Wydra /Kielce|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/host-reconciliation-followup-029.json#/provider_candidates/0`|
|Lecznica weterynaryjna lek. wet. Jerzego Legienia /Legnica|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-030.json#/records/0`|
|Przychodnia Weterynaryjna Zwierzogród /Legnica|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-030.json#/records/1`|
|DogWet Lecznica /Ostrów Wielkopolski|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-036.json#/records/2`|
|Medicus Veterinarius — Piotr Lisiak /Ostrów Wielkopolski|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-036.json#/records/3`|
|OAZA Prywatna Lecznica Dużych i Małych Zwierząt /Łomża|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-036.json#/records/4`|
|Vet Medica /Leszno|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-036.json#/records/5`|
|Gabinet Weterynaryjny CHART /Leszno|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-037.json#/records/0`|
|Przychodnia Weterynaryjna Marek Leończak /Łomża|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-037.json#/records/1`|
|Gabinet Weterynaryjny ZWIERZAK /Łomża|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-037.json#/records/2`|
|Gabinet Weterynaryjny Kocimiętka /Łomża|Полные релевантные собственные service/role/contact не устанавливают explicit local cancer-treatment act; generic surgery/diagnostics/интересы не достаточны|`input/prior/working/fresh-frontier-outcomes-037.json#/records/3`|
|Gabinet weterynaryjny Anna Golec / Marcin Rybski — Marcelińska /Poznań|Generalcare/rehablaser не cancertherapy/RT/ECT; другая Golecidentity|`input/prior/working/fresh-frontier-outcomes-037.json#/added/0`|

## Сохранённые18DUP / baseline

Это уже представленные ранее идентичности, не сегодняшние новые клиники и не пропущенные provider reviews. ДваUPDATE выше входят в baseline20; остальные18 — DUPalreadyapplied.

- RTWet — Polski Ośrodek Radioterapii Weterynaryjnej /Wiskitki — pl-rtwet-wiskitki; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Neo Vet /Poznań — pl-neo-vet-poznan; working/baseline-QA-001.json
- GreenVet Przychodnia Weterynaryjna /Zielona Góra — pl-greenvet-zielona-gora; working/baseline-QA-001.json
- Przychodnia Weterynaryjna VETHOUSE /Lublin — pl-vethouse-lublin; working/baseline-QA-001.json
- Praska — Przychodnia Weterynaryjna /Kraków — pl-praska-krakow; working/baseline-QA-001.json
- Dom-Vet Przychodnia Weterynaryjna / OnkoWet /Warszawa-Wesoła — pl-dom-vet-warszawa-wesola; working/baseline-QA-001.json
- Moonvet — Przychodnia Weterynaryjna Moniki Morawskiej /Łódź — pl-moonvet-lodz; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Żurawiniec /Poznań — pl-zurawiniec-poznan; working/baseline-QA-001.json
- Weterynaryjne Centrum Kliniczne Kurosz /Gorzów Wielkopolski — pl-kurosz-gorzow; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Pobłocki i Miazga /Kosakowo — pl-poblocki-miazga-kosakowo; working/baseline-QA-001.json
- Całodobowa Klinika Weterynaryjna VETKA /Warszawa — pl-vetka-warszawa; working/baseline-QA-001.json
- Mokotowska Klinika Weterynaryjna /Warszawa — pl-mkw-warszawa; working/baseline-QA-001.json
- LEW Weterynaryjne Centrum Zdrowia /Olsztyn — pl-lew-olsztyn; working/baseline-QA-001.json
- Azyl Przychodnia Weterynaryjna /Horodniany — pl-azyl-horodniany; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Bilscy /Kielce — pl-bilscy-kielce; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Krzycka /Wrocław — pl-krzycka-wroclaw; working/baseline-QA-001.json
- Specjalistyczne Centrum Weterynaryjne — Stanisław Firlik /Opole — pl-scw-opole; working/baseline-QA-001.json
- Przychodnia Weterynaryjna Leonard Gugała 24h — Grupa EDINA /Szczecin — pl-gugala-szczecin-stargardzka; working/medical-label-hold-001.json

## Собственный остаток и77внешних вопросов

Собственный доступный документированный остаток:0. Это не blanket«все источники недоступны»: у части открытая страница не публикует нужную clinical/branchallocation, у части точный permissionhold, у части исчерпан обычный transport, а2кандидата не дали первичного маршрута. Все77 source-specific rows содержат exactURLs/actualoutcome pointers+SHA, недостающий факт, разрешённый следующий шаг и recheck_after в remaining.json и working/final-77-gap-review.json. Никакой из75 не клинически FULL;2routing-only не получили primaryreview/processedcredit.

Разрешённый следующий шаг — только действительно новая независимая собственная clinical/branch публикация или явное восстановление/разрешение доступа к heldsource. Даты recheck_after24Oct(retainedonly)/25Oct(currentattempts) — не permissionrelease и не автоматическая задача. Сообщения/формы не отправлялись.

| Имя / город | Точный нерешённый факт и уже выполненная маршрутизация | Класс / proof |
|---|---|---|
|UPWr Wrocław /UPWr Wrocław|Действующие точные master/thoracic403; независимый разрешённый поиск не установил текущий клинический онкологический маршрут, квалифицированную связь и доступ.|external_access_and_information_gap; `input/prior/working/university-matrix-001.json`|
|MAXVETPLUSPrzasnysz /Przasnysz|Текущие разрешённые root/лечение/врач/контакт/booking ведут в Pułtusk. Адрес, клинический контакт и лечение именно в Przasnysz не установлены; хирургическая страница403 остаётся held.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-052.json`|
|MED-VET Pałucka /Wrocław|Квалифицированный зарегистрированный руководитель и работа филиала известны. Общая онкотерапия/паллиация/хирургия не распределена на Pałucka55; email учебного офиса не заменяет clinicalnetwork contact.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/saved-frontier-outcomes-002.json`|
|MED-VET Zachodnia /Wrocław|Работа Zachodnia20 подтверждена, но местная онкотерапия и назначение врача не распределены общей страницей. Программа стерилизации2026 не доказывает онкологию.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/saved-frontier-outcomes-002.json`|
|Vetspec /Czernica/Groblice identity requires current primary|Текущий квалифицированный BartłomiejHutny связан с Odrzańska9Czernica; профессиональный интерес/Oncology label не устанавливает конкретную местную терапию. Собственный root502 исчерпан, VetEdabout403 held; старый Groblice не второй филиал.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-043.json`|
|Elżbieta Turczanik-Suska /Wrocław|Регистрационная квалифицированная личность известна; собственной текущей публикации противоопухолевого лечения/приёма не найдено. Конфликт Grabiszyńska130/Grochowa17 не разрешён как переезд/филиал.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-037.json`|
|Gabinet Golec / Anna Starczewska /Poznań|Недоступный точный прежний собственный сайт held; текущая терапия и связь Golec/Starczewska/двух адресов не установлены. Отдельный AnnaGolecMarcelińska не объединён по фамилии.|external_access_and_information_gap; `input/prior/working/identity-outcomes-001.json`|
|Przychodnia AVET /Olsztyn|Текущая регистрационная связь drMałgorzataKander с Limanowskiego25/4 установлена; actual local cancer therapy/intake не опубликованы в разрешённых прочитанных источниках. Старый websitehold сохранён.|external_access_and_information_gap; `input/prior/working/identity-outcomes-001.json`|
|GiVet /Giżycko|Root/contact502 уже проверены разрешёнными способами; независимые актуальные профили дают контакт, общую хирургию и диагностику, не противоопухолевую терапию.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|ZWIERZAK Lenkiewicz/Zaleski /Białystok|Квалифицированный AdamKołotko и Piastowska11A известны. Его собственный scope общий, опухолевые отзывы/экзотические пациенты не клиническое обещание. Rootheld/bookingloop не повторялись.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-049.json`|
|Zdrowy Zwierzak Szara26 /Kraków|Квалифицированный KarolStąpor/Szara26 известен; bareOncology/Surgery в независимом профиле не описывает текущую терапию. Клинические429 не восстанавливались; Wieliczka не получает услуги автоматически.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-049.json`|
|Zdrowy Zwierzak Modrzewiowa2B /Wieliczka|Отдельный открытый Modrzewiowa2B и контакт известны; actual branch oncology/квалифицированное назначение не распределены общей клинической страницей. Held429 не повторялись.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|AnimalVET /Puławy|Текущие врачи и общий scope известны; интерес к онкологии не подтверждает local cancer act. Ранее рекламировавшийся legacyURL502 исчерпан, не второй адрес.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-040.json`|
|Dr ZOO /Lubsko|Точный собственный источник после Webtimeout/normalTLS502 не дал тела; каталожная онкология не терапия. Независимый текущий клинический первоисточник не установлен.|external_transport_and_information_gap; `input/prior/working/identity-outcomes-001.json`|
|Tymiankowa /Lublin|Текущий maintenance/contact и независимый legacy clinical502 не подтверждают онкотерапию; generic/unclaimedprofile не primary treatment. URL не угадывались.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-039.json`|
|Paluch Marek /Świebodzin|Официальный PIW подтверждает квалифицированное имя/адрес/контакт, но запись обновлена28.12.2023, не2026care. Собственная текущая противоопухолевая практика не установлена; LILWET403 held.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/identity-outcomes-002.json`|
|Provet /Nowy Sącz|Ранее точная хирургическая страница вывела AccountSuspended; hostworkflow held. Независимый currentclinical/cancer intake не установлен, закрытие клиники не утверждается.|external_access_and_information_gap; `input/prior/working/regional-outcomes-003.json`|
|Zapiesek /Myślenice|PETHELP подтверждает партнёрскую routine identity/contact, не clinic-owned oncotherapy. Часыnieczynne не доказательство закрытия, heldroot не повторялся.|external_access_and_information_gap; `input/prior/working/regional-outcomes-003.json`|
|Nowa Huta Wet Weronika Janta /Kraków|RootWeb/native502 и независимый контактный профиль исчерпаны. Текущий профиль Mistrzejowice9/1A не доказывает cancer act; юридический старый адрес WeronikaJanta не новый филиал.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Marcin Kuchciński /Opole|Текущая квалифицированная связь/контакт установлены. Раковая терапия остаётся за heldservice; разрешённый contactredirect завершён, не основание для вывода об отсутствии лечения.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-042.json`|
|Vet-Centrum /Kluczbork|Собственная clinicalURL502 исчерпана; PETHELP подтверждает routine partnercontact, не рак. Старый cachedtumourremoval не принят за текущий доступ; FBworkflow held.|external_transport_and_information_gap; `input/prior/working/regional-outcomes-003.json`|
|Złotorzyńscy /Suwałki|Собственная root502/offer403 и разрешённый независимый bookingprofile обработаны. Текущая противоопухолевая терапия/квалифицированная клиническая связь не установлены из тонкого профиля; старый cache не свежая терапия.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-049.json`|
|Dagmara Dobrzyń /Suwałki|Текущая квалификация/Chopina8D известны. Интерес к хирургии и genericprofile не actualcancer act; offer403 не повторялся.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Centrum Małych Zwierząt /Przemyśl|Mickiewicza28/166782748 подтверждены независимым профилем; общий dogcat/surgery scope не противоопухолевая терапия и не текущая врачебная связь. Heldroot007 не читался.|external_access_and_information_gap; `input/prior/working/regional-outcomes-003.json`|
|VetKa /Stalowa Wola|Партнёрская PETHELP identity/Poniatowskiego19H/1 известна, но не собственная онкотерапия/квалифицированный clinicalrole. Не другие VetKa; часы не закрытие.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/identity-outcomes-002.json`|
|Suszko Lipiński /Białystok|Реестр25.09.2026 подтверждает AnatolSuszko/Zwycięstwa26B/телефон, не текущую онкотерапию. Старое партнёрское имя не отдельный provider; реестр не расширен на чужие строки.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/identity-outcomes-002.json`|
|Alfavet /Rzeszów|Два независимых профиля подтверждают Kotuli92/535803035, genericcare без cancer act/врача. JS-bundle/mixed deniedsession14230 не читались и не повторялись.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Goldi /Starachowice|Точный рекламировавшийся Weeblyroot был недоступен16Oct и held. Текущий собственный clinical/cancer contact не найден; каталог не лечение.|external_access_and_information_gap; `input/prior/working/identity-outcomes-002.json`|
|AS Dariusz Białoń /Starachowice|Квалифицированный DariuszBiałoń/AS/Piłsudskiego35 и общий scope установлены. Cancerprocedure из другого профиля не прочитана; deniedmixed14230 не восстановлен. Homevisits не mobile oncology.|external_access_and_information_gap; `input/prior/working/regional-outcomes-006.json`|
|Boliłapka /Kołobrzeg|Точная собственная aboutURL502 исчерпана; независимый текущий bookingcontact даёт Budowlana4A/MatyldaZielińska, но не actualcancer act/текущую квалифицированную клиническую связь.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Gabinet Weterynaryjny Stargard /Stargard|Точная текущая domestic-animal serviceURL Webtimeout/normalTLS502 не дала тела. Новая собственная cancertherapy/currentrole primaryroute не выявлена.|external_transport_and_information_gap; `input/prior/working/regional-outcomes-005.json`|
|Centrum Zdrowia Zwierząt Iłża /Iłża|Bodzentyńska11/486162130 работает как отдельный филиал, но рак явно распределён на Radom; не клонируем услуги в Iłża.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/regional-outcomes-002.json`|
|Centrum Zdrowia Zwierząt Krzyżanowice /Krzyżanowice|Krzyżanowice180a/483897941 — отдельный филиал с общим GPcontact; localcancer act не распределён с Radom.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/regional-outcomes-002.json`|
|Dogtorki Dźwierzuty /Dźwierzuty|Niepodległości3/2Dźwierzuty/666101280 подтверждены. Онкология Szczytno не является местным назначением/процедурой Dźwierzuty.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/regional-outcomes-002.json`|
|Przychodnia Nasza /Kraków|MajaKoczur квалифицирована и связана с Nasza; её общая bloodcancer helparea при трёх адресах не распределяет лечение на Murarska3b. Rootheld, независимый contactprofile обработан.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-049.json`|
|GRABISZYŃSKA /53-238 Wrocław|Старый EDINAroster даёт Ostrowskiego13c/contact, currentindependent rosterreader-shell и legalmatch не подтверждают текущую собственную clinic/cancer route. Не DuoWet; heldmasterJS не восстановлен.|external_access_and_information_gap; `input/prior/working/identity-outcomes-002.json`|
|Skotnicka24 /Kraków|Текущая SabinaGalganek clinicalassociation известна, но actual dogcat therapeutic scope отсутствует в разрешённых service/platform bodies. Profile/widgetheld не повторялись; дополнительный board не требуется.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|MULTIWET BEMOWO /Warszawa|Текущая DariaJankowska/контакт известны. Genericcare/academiconcologyinterest и platformcontact не treatmentact; surgery/team429held, не равны общей недоступности клиники.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|NEW VET Chełm /Gdańsk|Currentdogcat canceract не установлен: successfulroleprofiles generic/exotics; после039 весь текущий roster/profile/service/contact workflow остановлен. Не было новых запросов/зеркал/heldbody reconstruction.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|PULSVET /02-801 Warszawa|Собственное объявление5OctmoveTaneczna30 конфликтует с platformPuławska403. Actualdogcat canceract/назначение неизвестны; экзотический общий scope не лечит рак, root/services429held.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|WETMEDYKA /05-510 Konstancin-Jeziorna|Текущий контакт и независимый квалифицированный visitingphysician известны. Его общий двухклиничный scope не распределяет онкопроцедуры на Pułaskiego103; genericownindex не canceract, team429held.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-045.json`|
|Vetmedic /Szczecin|Собственный exactroot502 исчерпан. Независимые profiles подтверждают PrzyjaciółŻołnierza80a/телефон/generalcare, не текущую квалифицированную связь и cancer-treatmentact.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|VETKA /Sanok|Собственный root403held. Независимые profiles дают Sadowa6A/телефон/generalcare, не cancertherapy/текущую врачебную связь. Не повторялся heldroot.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Gabinet Weterynaryjny Paweł Łaczek /Tarnów|Квалифицированный PawełŁaczek/контакт/generalcare известны; offerchallenge015 не обходился. Независимый новый cancertherapy source не выявлен.|external_access_and_information_gap; `input/prior/working/followup-outcomes-003.json`|
|Klinika Teodorowscy Mikołów /Mikołów|Действующий OliwierTeodorowski/ŻwirkiiWigury5 известны. Networktumour surgery не распределена на физический филиал; ONE network route сохранён отдельно.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/roster-outcomes-003.json`|
|Klinika Teodorowscy Orzesze /Orzesze|Текущий Powstańców7/contact известен; generalnetwork surgery и общая команда не распределяют местное лечение/врача. Network route не физическая карточка.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/roster-outcomes-003.json`|
|Medican Olsztyn Centrum /Olsztyn|Квалифицированная регистрационная связь drIzabellaBabińska известна. На текущем clinicbody только Oncology label/generalcare, не конкретный противоопухолевый акт; дополнительные credentials не барьер.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/roster-outcomes-003.json`|
|Medican Olsztyn Dajtki /Olsztyn|Квалифицированная регистрационная связь drIwonaBorkowska известна. BareOncology/generalcare не currentcanceract; register/ownphoneconflicts сохранены, новый офис уже открыт, не будущая онкология.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/roster-outcomes-003.json`|
|Centrum Weterynarii Doggy Dream /Opole|Ownclinical502 исчерпан; муниципальная квалификация/адрес из31Mar2023routineprogramme не2026oncotherapy. Новый currentprimaryroute не установлен.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-043.json`|
|Przychodnia Weterynaryjna ARKA — Robert Ratajski /Nysa|Текущие programmeidentity/квалифицированные имена/контакт corroboratebranch, не авторство старого hostedfirstperson treatmentclaim. Clinicalsubdomain403, FBheld, Opoleauthoritygamblinguntrusted; не закрытие/не отсутствие рака.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-053.json`|
|Gabinet Weterynaryjny AS — Gabriela i Bartosz Tuz /Nowa Sól|Собственный rootnotaccessibleheld018; clinicalpartnerprogramme даёт identity/контакт, не собственную противоопухолевую терапию. AS/Tuz не Wlekliński или NOVA.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-029.json`|
|Mariusz Wlekliński — current clinic identity unverified /Nowa Sól|Клинический provider не обработан первично. Сохранённые secondary/authority/publicprofileroutes реально разобраны; Citymenu exact403held042, остальные не дали текущего собственного клинического URL. Это исчерпание маршрутизации, не primary403/EXCL/processed.|external_route_identification_gap; `input/prior/working/fresh-frontier-outcomes-053.json`|
|Weterynaria BP — Łukasz Górniak lead /Biała Podlaska|Собственный advertisedclinical502 исчерпан; currentowned cancertherapy/qualifiedrole/exactbranchcontact не получены. Searchoncologylabel не promotion.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-030.json`|
|MEDICA-VET — Magdalena Błachnio-Baj /Biała Podlaska|Собственный root502 и разрешённые physician/placeprofiles обработаны. Профиль учреждения даёт только genericcare и ещё один конфликтующий адрес JanaPawłaII128; связь с актуальным кабинетом/actualcanceract не установлена.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Lecznica Sobieszów — Ewa Charchut /Jelenia Góra|Точный advertisedredirecttarget недоступен/held034, неHTTP403. Currentowned cancertherapy/contact/qualifiedassociation не подтверждены каталогом; aliases/root не повторялись.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-042.json`|
|Gabinet Weterynaryjny lek. wet. Przemysław Błaszczyk /Sieradz|PETHELPprogramme подтверждает identity/routinecontact, но не clinic-owned currentcancertherapy. Programmehoursне закрытие; собственная клиническая публикация не выявлена.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-032.json`|
|ZWIERZAK — Kamila Kwaśniewicz /Jelenia Góra / Szklarska Poręba identity unresolved|Профессиональное квалифицированное имя известно, адрес JeleniaGóra/SzklarskaPoręba конфликтует; собственная онкотерапия не подтверждена. FacebookDisabledheld024 не восстанавливался.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-032.json`|
|Gabinet Weterynaryjny Tomasz Garbal /Dębica|OwnedcontactOneMoment022 и новый exactprofessionalprofiletool-not-accessible001held. Нет currentcancer act/квалифицированной связи/первичного клинического контакта; HTTPstatus нового отказа неизвестен.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-031.json`|
|Gabinet Weterynaryjny OGONIAŚCI.PL — Małgorzata Bajorek /Dębica|Квалифицированная MałgorzataBajorek/Ogoniasci из собственного профиля известна, но genericconsult/biopsy/USG не терапия. Rzeszowska2/Rzemieślnicza2/Wielopolska45 не разрешены как филиалы; rootheld/FBworkflowstop.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Przychodnia Weterynaryjna Szwarc & Sobik — Rybnik /Rybnik|Текущий Energetyków89/branchbooking известен. Общая cancerSurgery/команда не распределены на Rybnik; ONE networkcontact сохранён, не physicalfanout.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-031.json`|
|Przychodnia Weterynaryjna Szwarc & Sobik — Żory /Żory|Текущий os.PowstańcówŚląskichP20/contact известен. Общая operativecancer page не распределяет услуги/врача на Żory; ONE network route, не secondphysicalcard.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-031.json`|
|Gabinet weterynaryjny Amigo — Morawica /Morawica|Kielecka14/общая регистратура и условные короткие сессии известны. Хирургия/chemo страницы явно Suków, не Morawica; прежняя формулировка о работе не закрытие.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-032.json`|
|Przychodnia Weterynaryjna Uszy do Góry /Kielce|Официальный реестр1Oct2026 даёт квалифицированную AleksandraSemik-Pękalska/Prosta35/1/contact, не текущую cancertherapy. Отдельный provider, не Amigo.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-043.json`|
|Aliland lek. wet. Alina Grzymalska — clinic identity/scope unverified /Świnoujście|Первичная клиническая проверка не состоялась: только business/directory oncologylabel и autogeneratedtext, сохранённые независимые маршруты разобраны. Witosa2B/2 vsretailадреса не отдельные онкоклиники. Directory404 не primaryblocked/processed/EXCL.|external_route_identification_gap; `input/prior/working/fresh-frontier-outcomes-053.json`|
|Gabinet Weterynaryjny dr n. wet. Paweł Kulik /Kalinowice / Zamość|Квалифицированный PawełKulik и старый oncologic scopeSzczebrzeska12 известны; текущий Kalinowice21A/currentbooking не связывает туда противоопухолевые процедуры. Нет fanout/второго врача/клиники по конфликту.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-034.json`|
|Przychodnia Weterynaryjna Rafał Szaluś /Zawada koło Zamościa|Точный advertisedbusiness.site Weberror/normalTLS404 реально проверен; не authdenial. Текущая собственная онкотерапия/qualifiedrole/contact не получены, каталожная oncologylabel недостаточна.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-034.json`|
|Przychodnia Weterynaryjna Dariusz Pfeifer /Zamość|Fullownclinicalpages дают genericguzy/skinchanges/surgery и историю основателя; explicitneoplastictherapy/currentqualifiedclinicalrole не установлены. FBTemporaryBlocked028 не повторялся.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-034.json`|
|BemoVet /Warszawa|Новый независимый профиль врача подтверждает qualifiedcurrentassociation UrszulaGrzesiuk/Człuchowska35. Её dentistry/exotics/generalSurgery не рак; patientoral-tumourreview не первичный акт. Ownedroot/team/oncologyworkflowheld029; второй адрес не онкокарточка.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-035.json`|
|Przychodnia Leśna — Ewa Sumiła /Wrzosówka|Точный advertisedcontactURL Web/native502 исчерпан; currentownedcancertherapy/currentqualifiedrole/branchcontact не получены. Это transportgap, не auth403/закрытие.|external_transport_and_information_gap; `input/prior/working/fresh-frontier-outcomes-042.json`|
|Przychodnia Wojciech Nowakowski — Gwarecka /Chorzów|Gwarecka17/contact известны; sharedoncology page не распределяет терапию/ветеринара. Gałeczki47 имеет отдельное доказательство, не фан-аут на Gwarecka.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-035.json`|
|Gabinet weterynaryjny Kozłowski /Szczecin|PETHELPfullprofile уже прочитан17Oct: qualifiedtitleTomaszKozłowski/Pokoju42A/contact. Не clinic-owned currentcancertherapy; собственные root/oncologypage403held16Oct не реконструировались.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-035.json`|
|Przychodnia Weterynaryjna RYDŁÓWKA /Kraków|QualifiedMajaKoczur/Rydłówka21 установлена, её shared3addressbloodcancer scope не physicaltherapyallocation/contact. Exactservices/team429held; broadsearchrootreference не новый primaryread.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-049.json`|
|Cowet /Gdańsk|Root403held; независимый профиль подтверждает LawendoweWzgórze10/U2/contact, но названиеCancerCenter не actualtherapy/currentvet. Исторический biographymention не currentassignment.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|ARS-VET — Chodzież /Chodzież|Currentbranch Zwycięstwa6/contact и independentbareOncologylabel известны; actualtherapy/qualifiedbranchallocation не опубликованы. ONEnetworkChemo/Surgery сохранён, не physicalfanout.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|ARS-VET — Złotów /Złotów|Currentbranch Norwida13/contact и bareOncologylabel известны; actualtherapy/qualifiedbranchallocation не опубликованы. Общее booking не гарантирует localprocedure.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-048.json`|
|Gabinet Weterynaryjny Jacek Zyzman /Ełk|Точная clinic-hostedclinicalpage403held033; currentownedtherapy/qualifiedrole/contact остаются неустановленными. Каталог не первичный cancercare и не ARS-VETEłk.|external_access_and_information_gap; `input/prior/working/fresh-frontier-outcomes-036.json`|
|Gabinet Weterynaryjny ARWET — Wieliczka /Wieliczka|QualifiedKatarzynaKarmańska/Sienkiewicza25 известна. Её общий двухклиничный oraloncologic scope не распределяет procedure в ARWET; rootWeb/normalTLSshell и platformcontact исчерпаны, DAVET доказан отдельно.|external_unpublished_clinical_or_branch_allocation_gap; `input/prior/working/fresh-frontier-outcomes-050.json`|

## Источники, ограничения, даты и backup

15новыхURLreads перечислены в evidence.json/working/current-primary-outcomes001–002. Garbalprofessionalprofile вернул tool-not-accessible, HTTPstatus неизвестен: новый exacthold001 без fallback/slug/client/cache.14прочих reads дают только relevantprofilecontent; Grzesiukreader имел644строки, показано0–428, полное relevantclinical0–224 прочитано — не заявляется полный644read. FULL0. Sourceattemptдата18Oct относится только к этим15URL, не обновляет retainedeligible16/17Oct и не делает cachedcrawldate currentclinicalproof.

Непреднамеренное попадание heldLuxVetmaster в broadregionalsearch зафиксировано событием/URL/ref/0clinicalcredit. Первый plain-textfilter не удалил search excerpt; он не использован и не сохранялся/не хешировался как тело, не перечитывался/не восстанавливался. Последующие searchвыводы title/URL/refonly. Exactmasterhold не снят, свежий masterroster из него не получен. Отдельные heldRYDŁÓWKA/NewVetmirror references также толькоmetadata, безbodyreconstruction. Запрещённые web079/080/119/120/quarantine/privatepassport/deniedsessions14230/88289 не читались/не хешировались/не poll. Никаких APIcredentials/sourceJSkeys/платныхсервисов/внешнихписем/forms/UI/articles/trialsweep.

Researchbackupbranch `research/europe-recovery-eu6-recovery-20261018T020312Z`; контроллер сообщил начальный прочитанный обратно SHA `5ae3637413c5c09ece4ab68437a34280e0e64e15`, унаследованный remote `a1278262482f56f7571d35b8d2a3e2d5e2edede3`. Immutableblocks1–4 переданы контроллеру, финальный пакет запечатан отдельным ready.json. Никакой последующий remoteSHA/readback/production/deployment не выдуман: финальный readback и parentacceptance отдельно.

Ключевые finalproof: working/effective-proposal-locators.json, working/current-five-input-dedupe.json, working/final-national-coverage.json, working/final-77-gap-review.json, working/final-named-dispositions.json; exact SHA-256 конечных шести файлов находится в финальном checkpoints/block-5/ready.json. Все JSONroots имеют этот новый run/slot3/Poland/baseline, унаследованные source dates/IDs оставлены в самих evidence objects.

Основание research_complete=true: восстановлена полная эффективная222proposalцепочка и366identityledger; реально сверены все77точных gaps, дополнительно завершены15независимых primary/profileURLreads, выполнен freshnative16regionalnewsignallayer, сведены8universities/всеknownnetworkbranches/GP/RT-ECT/mobile-remote и все найденные новые resultreferences. Не осталось документированного разрешённого неисполненного clinicalchild/новой identity для текущего фронта. Остались не переименованные75clinicalinformation/accessquestions+2routinggaps и неполные currentmasterrosters по точным holds. Это исследовательское закрытие доступного фронта, не национальная гарантия полноты, clinicalrecommendation, принятие контроллером или публикация сайта.

## Финальная форматная QA

Проверены все222верхних changeobjects: operation NEW/UPDATE,source_id,field,official_url,supporting_quote,branch_scope,checked_at,old_value,new_value. Для трёхGoldenVet добавлен только supporting_quotealias из реально сохранённого golden-tumor-act/facts0quote, безGET/новойцитаты/смены clinicaldate; amendment отдельно. В5JSONroots coverage_complete=true сопровождается16region/8university/networkproofobjects и exact SHA; rootassigned/processed/fully_verified — integers. Исправлен точный Zviropolisproof на inherited-revalidated009/changes0–3. Final-effective-proposal-audit содержит все222последних objectSHA и исходные retainedlocators; необъяснённых изменений0.
