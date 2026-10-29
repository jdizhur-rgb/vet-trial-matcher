# Массачусетс: систематический поиск онкологической помощи — 28 октября 2026

В подготовленной локальной версии каталога **80 физических мест и 2 сетевых контакта**. Добавлены **61 физическое место и 2 сетевых контакта**, перепроверены 17 прежних записей. У двух прежних записей сохранена предыдущая успешная дата из-за ограничений доступа.

Химиотерапия указана у **18 физических мест**, дополнительно есть один сетевой контакт South Coastal с уточнением филиала. Новые физические места с местной химиотерапией: Acoaxet в Westport и Countryside в Wrentham. Общая клиника с удалением опухолей не названа специализированным онкологическим центром.

## Охват

100 сохранённых точных запросов охватывают все 14 округов, медицинскую и хирургическую онкологию, местную химиотерапию, ЭХТ, облучение, выездные услуги, отдельные филиалы и доступную по стоимости помощь. Исходный каталог: 188 городских страниц с 709 пронумерованными строками плюс 93 одиночных населённых пункта — 802 исходные записи по 281 обозначению населённого пункта. Независимый исторический AnimalShelter: девять страниц, 405 строк с MA ZIP. Официальный национальный sitemap VCA привёл к MA sitemap с 2815 URL, включая 52 хирургические страницы 31 филиала.

**Это систематический discovery-проход штата с перечисленными исключениями, а не 802 независимые первичные проверки действующих клиник.** Исходные списки содержат дубли врачей, старые адреса, вакцинационные точки, не-клинические организации и географические ошибки. Ни одному учреждению сообщения не отправлялись.

## Существенные решения

- South Coastal публикует химиотерапию, но имеет Weymouth и Rockland: одна общая запись, без приписывания услуги обоим филиалам.
- MSPCA community clinics: одна программа срочной льготной хирургии с раздельными формами по филиалам. Удаление масс — при влиянии на качество жизни, с финансовой и клинической оценкой; это не полноценная бесплатная онкология.
- Love Is Life Veterinary Clinic во Franklin открыта всем, без проверки дохода. Диагностику проводят заранее у направившего врача; ночной госпитализации нет.
- Angell West, Bulger, BluePearl Charlestown, Cape Cod Buzzards Bay, Boston West и другие хирургические места добавлены по явным локальным предложениям. Медицинская онкология или лучевая терапия не перенесены из других филиалов.
- NEAMC Primary Care — 20 Pleasant Street, отдельно от Westbridge на 595 West Center Street.
- Исправлено ложное объединение VCA Lynnfield by the Lake и VCA Wakefield: разные адреса и телефоны в одном ZIP. Исключение касается только этой подтверждённой пары.
- Добавлены 58 публичных ZIP-центроидов. Расстояния приблизительные; точки не названы координатами зданий.

## Ограничения источников

32 индивидуальных пункта с конкретными причинами сохранены в remaining.json. Они включают как неподтверждённые услуги/филиалы и доступ к источникам, так и исключённые не-клинические или иногородние результаты. Это не 32 подтверждённых отсутствия лечения.

Integrity сохранила прежние услуги и успешную дату после текущих 403. ACCS сохранён без обхода прежнего точного ограничения доступа. У VCA Weymouth доступна текущая страница медицинской онкологии с двумя врачами и контактами; прямые страницы ЭХТ, иммунотерапии и хирургической онкологии дали 403, поэтому прежние доказательства этих услуг не представлены как новые полные чтения. JS-оболочки Thrive, South Dennis и другие конкретные пробелы не превращены в новые услуги. Ссылки Revere/Lynn ведут на постороннее игровое содержимое или продажу домена; это не доказательство закрытия клиник.

## Проверки

Полная production-сборка PASS. Проверки данных, уникальности и раздельных филиалов, фильтров страны/штата/услуг, сетевых контактов, matcher-регрессий и сохранения других стран/штатов PASS. Исторические hash-assertions сохранены через точную обратную проекцию принятых строк. Исправление не меняет trials_base.json, пользовательский интерфейс и страницы штатов.

## Даты проверки источников

82 итоговые записи: 80 успешных текущих core-review, одна текущая неуспешная попытка Integrity, одна сохранённая ограниченная ACCS без новой попытки. 776 native receipts включают discovery, клинические страницы и ZIP-запросы; это не 776 завершённых проверок клиник. У успешных записей дата 2026-10-28 и фактический timezone-aware timestamp исходного запроса. Previous/new значения находятся в baseline-projection.json и evidence.json. Публикация в main остановлена автоматической проверкой разрешений: требуется явное подтверждение пользователя. Live-сайт и remote SHA не объявлены обновлёнными; статус сохранён в publication-proof.json.

## Текущий каталог MA

| Клиника / служба | Город или территория | Услуги | Дата |
|---|---|---|---|
| [MSPCA-Angell community clinics — urgent surgical care](https://www.mspca.org/veterinarycare/low-cost-clinics-all-locations/low-cost-clinics/) | Massachusetts; Boston, Centerville and Methuen community-clinic program | Surgery | 2026-10-28 |
| [South Coastal Animal Health — oncology contact](https://www.southcoastalah.com/services) | Massachusetts; Weymouth and Rockland branch allocation to confirm | Local oncology care, Chemotherapy | 2026-10-28 |
| [Agawam Animal Hospital](https://agawamanimalhospital.com/conditions-treated) | Agawam | Surgery | 2026-10-28 |
| [VCA City Cats Hospital](https://vcahospitals.com/city-cats/services/primary-care/general-surgery) | Arlington | Surgery | 2026-10-28 |
| [Ashland Animal Hospital](https://ashlandanimalhospital.com/services/pet-soft-tissue-surgery) | Ashland | Surgery | 2026-10-28 |
| [VCA Adams Animal Hospital](https://vcahospitals.com/adams/services/primary-care/general-surgery) | Athol | Surgery | 2026-10-28 |
| [VCA Auburn Animal Hospital](https://vcahospitals.com/auburn/services/primary-care/general-surgery) | Auburn | Surgery | 2026-10-28 |
| [Back Bay Veterinary Clinic](https://www.backbayvet.com/services/surgery-services) | Boston | Surgery | 2026-10-28 |
| [BluePearl Pet Hospital — Charlestown](https://bluepearlvet.com/hospital/charlestown-ma/specialties-services/surgery/) | Boston | Surgery | 2026-10-28 |
| [MSPCA-Angell Animal Medical Center](https://www.mspca.org/veterinarycare/hospital-locations/oncology/) | Boston | Medical oncology, Surgical oncology, Radiation oncology, Chemotherapy, Immunotherapy, Targeted therapy, IMRT, VMAT, SRT | 2026-10-28 |
| [Shepherd Veterinary Clinic](https://www.shepherdvet.com/meet-the-team) | Boxborough | Surgery | 2026-10-28 |
| [VCA North Main Street Veterinary Clinic](https://vcahospitals.com/north-main-street/services/primary-care/general-surgery) | Brockton | Surgery | 2026-10-28 |
| [VCA Brookline Animal Hospital](https://vcahospitals.com/brookline/services/primary-care/general-surgery) | Brookline | Surgery | 2026-10-28 |
| [Burlington Veterinary Hospital](https://burlingtonvet.com/services/pet-soft-tissue-surgery) | Burlington | Surgery | 2026-10-28 |
| [Cape Cod Veterinary Specialists — Buzzards Bay](https://capecodvetspecialists.com/pet-surgery-buzzards-bay-ma/) | Buzzards Bay | Surgery | 2026-10-28 |
| [Veterinary Cancer Specialists of New England](https://www.vcsnewengland.com/) | Buzzards Bay | Medical oncology, ECT, Immunotherapy, Chemotherapy | 2026-10-28 |
| [Countryside Veterinary Hospital](https://countrysideveterinaryhospital.com/services/pet-soft-tissue-surgery) | Chelmsford | Surgery | 2026-10-28 |
| [Boston Veterinary Specialists](https://bostonvetspecialists.com/pet-soft-tissue-abdominal-surgery-dedham-ma/) | Dedham | Surgery | 2026-10-28 |
| [Falmouth Animal Hospital](https://falmouthanimalhospital.com/services/pet-soft-tissue-surgery) | East Falmouth | Surgery | 2026-10-28 |
| [VCA Pleasant Bay Animal Hospital](https://vcahospitals.com/pleasant-bay/services/primary-care/general-surgery) | East Harwich | Surgery | 2026-10-28 |
| [VCA Shaker Road Animal Hospital](https://vcahospitals.com/shaker-road/services/primary-care/general-surgery) | East Longmeadow | Surgery | 2026-10-28 |
| [VCA Everett Animal Hospital](https://vcahospitals.com/everett/services/primary-care/general-surgery) | Everett | Surgery | 2026-10-28 |
| [VCA Capeway Animal Hospital](https://vcahospitals.com/capeway/services/primary-care/general-surgery) | Fairhaven | Surgery | 2026-10-28 |
| [BluePearl Pet Hospital — Framingham](https://bluepearlvet.com/hospital/framingham-ma/) | Framingham | Medical oncology, Chemotherapy, Surgery | 2026-10-28 |
| [Love Is Life Veterinary Clinic](https://lilvc.org/) | Franklin | Surgery | 2026-10-28 |
| [VCA All Caring Animal Hospital](https://vcahospitals.com/all-caring/services/primary-care/general-surgery) | Great Barrington | Surgery | 2026-10-28 |
| [Compassionate Care Veterinary Services](https://www.ccvsgroton.com/surgery) | Groton | Surgery | 2026-10-28 |
| [Valley Veterinary Hospital](https://valleyvethospital.com/services/pet-soft-tissue-surgery) | Hadley | Surgery | 2026-10-28 |
| [VCA Roberts Animal Hospital](https://vcahospitals.com/roberts/services/primary-care/general-surgery) | Hanover | Chemotherapy, Surgery | 2026-10-28 |
| [VCA Hanson Animal Hospital](https://vcahospitals.com/hanson/services/primary-care/general-surgery) | Hanson | Chemotherapy, Surgery | 2026-10-28 |
| [Hingham Animal Clinic](https://hinghamanimalclinic.com/services/pet-chemotherapy) | Hingham | Local oncology care, Chemotherapy | 2026-10-28 |
| [VCA Lancaster Animal Hospital](https://vcahospitals.com/lancaster/services/primary-care/general-surgery) | Lancaster | Surgery | 2026-10-28 |
| [Bulger Veterinary Hospital](https://www.bulgervet.com/services/surgery) | Lawrence | Surgery | 2026-10-28 |
| [Lexington-Bedford Veterinary Hospital](https://lexingtonbedfordvet.com/services/pet-soft-tissue-surgery) | Lexington | Surgery | 2026-10-28 |
| [Ally Veterinary Speciality Center](https://www.allyvetspecialist.com/) | Lincoln | Medical oncology, Chemotherapy, Immunotherapy, Targeted therapy | 2026-10-28 |
| [Animal Cancer Care Specialists](https://accsvets.com/services/) | Littleton | Medical oncology, Chemotherapy, Immunotherapy, Targeted therapy | 2026-10-11 |
| [Linwood Animal Hospital](https://linwoodah.com/services/pet-soft-tissue-surgery) | Lowell | Surgery | 2026-10-28 |
| [North Shore Animal Hospital](https://www.nshoreanimalhospital.com/vet-services/) | Lynn | Surgery | 2026-10-28 |
| [Boston West Veterinary Emergency & Specialty](https://www.bostonwestvet.com/services/surgery) | Natick | Surgery | 2026-10-28 |
| [VCA Rotherwood Animal Hospital](https://vcahospitals.com/rotherwood/services/primary-care/general-surgery) | Newton | Surgery | 2026-10-28 |
| [Greylock Animal Hospital](https://greylockanimalhospital.com/services/pet-soft-tissue-surgery) | North Adams | Surgery | 2026-10-28 |
| [Tufts — Foster Hospital for Small Animals](https://vet.tufts.edu/foster-hospital-small-animals/specialty-services/oncology) | North Grafton | Medical oncology, Chemotherapy, Radiation oncology, IMRT, Immunotherapy, Surgery | 2026-10-28 |
| [Integrity Veterinary Center](https://integrityvetcenter.com/services/oncology/) | Northampton | Medical oncology, Chemotherapy, Palliative care | 2026-10-11 |
| [VCA Northboro Animal Hospital](https://vcahospitals.com/northboro/services/primary-care/general-surgery) | Northborough | Surgery | 2026-10-28 |
| [Norton Animal Hospital](https://nortonanimalhospital.com/services/vet-surgery) | Norton | Surgery | 2026-10-28 |
| [Norwell Veterinary Hospital](https://norwellveterinaryhospital.com/services/pet-soft-tissue-surgery) | Norwell | Surgery | 2026-10-28 |
| [VCA Palmer Animal Hospital](https://vcahospitals.com/palmer/services/primary-care/general-surgery) | Palmer | Surgery | 2026-10-28 |
| [Borash Veterinary Clinic](https://www.borashvet.com/peabody-ma/veterinary-pet-surgery/) | Peabody | Surgery | 2026-10-28 |
| [Pittsfield Veterinary Hospital](https://pittsfieldvet.com/services/pet-soft-tissue-surgery) | Pittsfield | Surgery | 2026-10-28 |
| [VCA Plymouth Animal Hospital and Pet Resort](https://vcahospitals.com/plymouth/services/primary-care/general-surgery) | Plymouth | Surgery | 2026-10-28 |
| [Rowley Animal Hospital](https://www.rowleyanimalhospital.com/surgery.pml) | Rowley | Surgery | 2026-10-28 |
| [New England Veterinary Clinic & Pet Resort](https://newenglandveterinaryclinic.com/services/pet-soft-tissue-surgery) | Salem | Surgery | 2026-10-28 |
| [Veterinary Emergency & Specialty Hospital – South Deerfield](https://www.veshmass.com/locations/south-deerfield) | South Deerfield | Surgery | 2026-10-28 |
| [VCA South Hadley Animal Hospital](https://vcahospitals.com/south-hadley/services/primary-care/general-surgery) | South Hadley | Surgery | 2026-10-28 |
| [VCA South Shore (Weymouth) Animal Hospital](https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology) | South Weymouth | Medical oncology, Chemotherapy, ECT, Immunotherapy, ONCEPT, Surgical oncology | 2026-10-28 |
| [VCA Southwick Animal Hospital](https://vcahospitals.com/southwick/services/primary-care/general-surgery) | Southwick | Surgery | 2026-10-28 |
| [VCA Sterling Animal Hospital](https://vcahospitals.com/sterling/services/primary-care/general-surgery) | Sterling | Surgery | 2026-10-28 |
| [VCA Lloyd Animal Hospital](https://vcahospitals.com/lloyd/services/primary-care/general-surgery) | Stoughton | Surgery | 2026-10-28 |
| [Sturbridge Veterinary Hospital](https://sturbridgeveterinaryhospital.com/services/pet-soft-tissue-surgery) | Sturbridge | Surgery | 2026-10-28 |
| [Sunderland Animal Hospital](https://sunderlandvet.com/dog-services.pml) | Sunderland | Local oncology care | 2026-10-28 |
| [Bay State Veterinary Emergency and Specialty Services](https://www.bsvess.com/) | Swansea | Medical oncology, Chemotherapy, Radiation oncology, Immunotherapy, Melanoma vaccine | 2026-10-28 |
| [Taunton Cat Hospital](https://tauntoncathospital.com/services/pet-soft-tissue-surgery) | Taunton | Surgery | 2026-10-28 |
| [VCA Blackstone Valley Animal Hospital](https://vcahospitals.com/blackstone-valley/services/primary-care/general-surgery) | Uxbridge | Surgery | 2026-10-28 |
| [VCA Lynnfield by the Lake Animal Hospital](https://vcahospitals.com/lynnfield/services/primary-care/general-surgery) | Wakefield | Surgery | 2026-10-28 |
| [VCA Wakefield Animal Hospital](https://vcahospitals.com/wakefield/services/primary-care/general-surgery) | Wakefield | Surgery | 2026-10-28 |
| [Advanced Veterinary Specialty Center of New England](https://www.avscvets.com/) | Walpole | Medical oncology, Radiation oncology, Chemotherapy, Electrochemotherapy, Immunotherapy, Radiation therapy, IMRT, SRT | 2026-10-28 |
| [Norfolk County Veterinary Service](https://www.norfolkcountyvet.com/your-pets-surgery.html) | Walpole | Surgery | 2026-10-28 |
| [Tufts VETS](https://tuftsvets.org/services/walpole-pet-oncology-services.php) | Walpole | Medical oncology, ECT, Immunotherapy, ONCEPT, Chemotherapy | 2026-10-28 |
| [MSPCA-Angell West](https://www.mspca.org/veterinarycare/hospital-locations/waltham/surgery-in-waltham/) | Waltham | Surgery | 2026-10-28 |
| [New England Animal Medical Center Primary Care](https://www.neamcpc.com/services/general-surgery) | West Bridgewater | Surgery | 2026-10-28 |
| [Westbridge Veterinary Referral Hospital](https://www.westbridgevets.com/) | West Bridgewater | Surgery | 2026-10-28 |
| [VCA Wickaboag Animal Hospital](https://vcahospitals.com/wickaboag/services/primary-care/general-surgery) | West Brookfield | Surgery | 2026-10-28 |
| [Veterinary Emergency & Specialty Hospital – West Springfield](https://www.veshmass.com/locations/west-springfield) | West Springfield | Medical oncology, Chemotherapy, Targeted therapy, Immunotherapy, Surgery | 2026-10-28 |
| [VCA Hyannis Animal Hospital](https://vcahospitals.com/hyannis/services/primary-care/general-surgery) | West Yarmouth | Surgery | 2026-10-28 |
| [Healthy Paws Veterinary Center](https://www.healthypawsvetcenter.com/surgery) | Westborough | Surgery | 2026-10-28 |
| [VCA Westboro Animal Hospital](https://vcahospitals.com/westboro/services/primary-care/general-surgery) | Westborough | Surgery | 2026-10-28 |
| [VCA Montgomery Road Animal Hospital](https://vcahospitals.com/montgomery-road/services/primary-care/general-surgery) | Westfield | Surgery | 2026-10-28 |
| [Acoaxet Veterinary Clinic](https://www.acoaxetvet.com/services/oncology) | Westport | Local oncology care, Chemotherapy | 2026-10-28 |
| [VCA Whitman Animal Hospital](https://vcahospitals.com/whitman/services/primary-care/general-surgery) | Whitman | Local oncology care, Oncology referral, Surgery | 2026-10-28 |
| [Massachusetts Veterinary Referral Hospital](https://www.massvethospital.com/) | Woburn | Medical oncology, Chemotherapy, Immunotherapy, Targeted therapy, Surgical oncology | 2026-10-28 |
| [VCA Abbott Animal Hospital](https://vcahospitals.com/abbott/services/primary-care/general-surgery) | Worcester | Surgery | 2026-10-28 |
| [Countryside Veterinary Clinic](https://www.csvetclinicma.com/) | Wrentham | Local oncology care, Chemotherapy, Surgery | 2026-10-28 |
