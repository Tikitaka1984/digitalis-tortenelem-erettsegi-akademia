# DTEA többszintű QA-szabvány

**Szabványazonosító:** `DTEA-QA-STANDARD`

**Cél:** bizonyítékalapú, reprodukálható és release-kapukhoz kötött minőségbiztosítás

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`. Minden modulhoz külön automatikus QA-riport és kézi QA-jegyzőkönyv kötelező.

## 1. QA-alapelvek

- A QA nem a fejlesztés utolsó lépése, hanem minden fázis része.
- A vizsgált artefaktum verziója és hash-e minden eredmény kötelező része.
- A `PASS` állítás bizonyíték nélkül érvénytelen.
- Automatikus teszt és szakértői review egymást kiegészíti, nem helyettesíti.
- Javítás után célzott retest és kockázatarányos regresszió szükséges.
- A tanulói felületet kezdeti, interakció utáni és visszaállított állapotban is ellenőrizni kell.

## 2. QA-szintek

| Szint | Időpont | Cél |
|---|---|---|
| `L0` Static | minden commit/PR | struktúra, séma, naming, tiltott minták |
| `L1` Component | implementáció közben | egyedi H5P-komponensek működése |
| `L2` Module | release candidate | teljes könyv és tanulói út |
| `L3` Integration | publikáció előtt | futtatókörnyezet, build, navigáció és assetek |
| `L4` Release | kiadás előtt/után | csomagintegritás, publikált verzió és smoke check |
| `L5` Regression | változás után | korábbi működés és nem érintett modulok védelme |

## 3. Hibasúlyosság

| Szint | Definíció | Release-hatás | Célidő |
|---|---|---|---|
| `BLOCKER` | nem tölthető be, adatvesztés, súlyos jogi/történelmi hiba vagy kritikus út teljesen akadályozott | azonnali stop | azonnal |
| `CRITICAL` | alapvető tanulási eredmény, hozzáférhetőség vagy pontozás megbízhatatlan | release tilos | release előtt |
| `MAJOR` | lényeges funkció, tartalom vagy UX hibás, van korlátozott kerülőút | release tilos, kivétel csak governance-döntéssel | release előtt |
| `MINOR` | korlátozott hatás, a fő cél teljesíthető | mérlegelhető dokumentált elfogadással | tervezett javítás |
| `TRIVIAL` | kozmetikai vagy szerkesztési eltérés | nem blokkol | backlog |

Történelmi tévedés, forrás nélküli tény, jogsértő asset és kritikus accessibility-akadály legalább `CRITICAL`.

## 4. Kötelező QA-dimenziók

## 4.1 Historical QA

### Cél

A tananyag történelmi pontosságának, forrásoltságának, kontextusának és értelmezési tisztességének ellenőrzése.

### Kötelező ellenőrzések

- minden tényállítás rendelkezik érvényes `claim_id` és `source_id` kapcsolattal;
- a forráshivatkozás ténylegesen támogatja az állítást;
- dátumok, személyek, helyek, fogalmak és időrend pontosak;
- oksági állítás nem lépi túl a források által indokolható szintet;
- vitatott kérdés és bizonytalanság megfelelően jelölt;
- elsődleges forrás nézőpontja és kontextusa nem tűnik el;
- nincs anakronizmus, hamis idézet vagy kitalált hivatkozás;
- a kép, térkép vagy ábra nem sugall történelmileg hamis pontosságot;
- érzékeny csoportok és erőszakos folyamatok bemutatása kiegyensúlyozott és dehumanizálástól mentes.

### Bizonyíték

Claim map review, tételes eltéréslista, reviewer, dátum és vizsgált Master Script/build verzió.

### PASS-feltétel

Nincs nyitott forráshiány, `BLOCKER`, `CRITICAL` vagy `MAJOR` történelmi eltérés.

## 4.2 Instructional QA

### Cél

A tanulási célok, tartalom, tevékenységek, visszajelzés és értékelés pedagógiai összehangoltságának ellenőrzése.

### Kötelező ellenőrzések

- a tanulási cél mérhető és a célközönséghez illeszkedik;
- minden oldal és feladat célhoz kötött;
- a nehézség fokozatos, az előzetes tudás kezelve van;
- a kognitív terhelés és az oldalsűrűség elfogadható;
- a feladat típusa megfelel a gyakoroltatott gondolkodási műveletnek;
- a distractorok hihetőek, de nem félrevezetők;
- a feedback magyarázza a helyes és hibás gondolkodást;
- a pontozás arányos, egyértelmű és a tanulási célhoz igazodik;
- nincs öncélú interakció, redundáns számonkérés vagy nem tanított tartalom tesztelése;
- a modul lezárása támogatja az összegzést és transzfert.

### Bizonyíték

Cél–oldal–interakció mátrix, szakértői checklist és mintatanulói út.

### PASS-feltétel

Minden kötelező cél legalább egyszer tanított és megfelelően ellenőrzött; nincs súlyos illeszkedési hiba.

## 4.3 UX QA

### Cél

Az érthető, következetes, hatékony és hibabiztos tanulói élmény ellenőrzése.

### Kötelező ellenőrzések

- kezdőlapról a modul egyértelműen elérhető;
- címek, tartalomjegyzék és progress konzisztens;
- a tanuló minden képernyőn érti a következő műveletet;
- feedback csak megfelelő művelet után jelenik meg;
- retry, reset, navigáció és visszatérés előre jelezhető;
- nincs szerkesztői metaadat, technikai próbaszöveg vagy angol UI-maradvány;
- desktop és mobil layout stabil;
- nincs vízszintes túlcsordulás, levágott vezérlő vagy olvashatatlan szöveg;
- hosszú tartalom, sticky elemek, zoom és orientációváltás nem rontja a használhatóságot;
- betöltési, üres, hibás és befejezett állapotok értelmesek.

### Bizonyíték

Előírt viewport-képernyőképek, végigjárási jegyzőkönyv, konzolhiba-lista és szükség esetén videó.

### Minimális viewportok

- desktop: 1440×900;
- laptop: 1280×720;
- mobil: 390×844;
- keskeny mobil/reflow: 320 CSS px;
- 200% böngészőzoom.

## 4.4 Accessibility QA

### Cél

A kritikus tanulói út és minden információ észszerű hozzáférhetősége, WCAG 2.2 AA célértékkel.

### Kötelező ellenőrzések

- szemantikus címsor- és landmarkszerkezet;
- teljes billentyűzetes használat, csapdamentes fókusz;
- látható, logikus fókuszsorrend;
- programozott címkék és hozzáférhető nevek;
- állapot- és hibaüzenetek képernyőolvasó számára érzékelhetők;
- információ nem kizárólag színnel vagy pozícióval közölt;
- kontraszt és szövegméretezés megfelel;
- képek alt textje, komplex vizuálok hosszú alternatívája megfelelő;
- audio/video felirat, transcript és vezérlés rendelkezésre áll;
- drag-and-drop feladathoz billentyűzetes vagy egyenértékű alternatíva tartozik;
- időkorlát elkerülhető vagy szabályozható;
- újrapróbálkozás és feedback nem zavarja a képernyőolvasó fókuszát.

### Tesztkombináció

- automatikus accessibility scan;
- kizárólag billentyűzetes manuális teszt;
- legalább egy támogatott képernyőolvasó-böngésző kombináció;
- 200% zoom és 320 px reflow;
- reduced motion és nagy kontraszt, ahol releváns.

### PASS-feltétel

Nincs kritikus útvonalat blokkoló akadály és nincs nyitott WCAG A/AA `CRITICAL` vagy `MAJOR` eltérés.

## 4.5 Technical QA

### Cél

A build, csomag, runtime, integritás, teljesítmény és biztonság ellenőrzése.

### Kötelező ellenőrzések

- tiszta környezetből reprodukálható build;
- rögzített dependency verziók és licencellenőrzés;
- manifest- és sémavalidáció;
- minden hivatkozott fájl létezik és hash-elhető;
- nincs duplikált vagy instabil azonosító;
- hibamentes böngészőkonzol és nincs sikertelen kritikus hálózati kérés;
- offline vagy statikus hosting elvárásai teljesülnek;
- fájlméret-, betöltési és Lighthouse-kapuk teljesülnek;
- nincs titok, személyes adat vagy tiltott külső kapcsolat;
- támogatott böngészőkön smoke és regressziós teszt sikeres;
- nem érintett modulok hash- vagy regressziós védelme teljesül.

### Ajánlott automatikus kapuk

- naming és repository lint;
- Markdown linkellenőrzés;
- JSON/H5P schema audit;
- dependency és asset audit;
- Playwright desktop/mobil smoke;
- accessibility scan;
- Lighthouse küszöb;
- SHA-256 egyezés és reprodukálhatósági ellenőrzés.

## 4.6 H5P QA

### Cél

A H5P Interactive Book és beágyazott komponensek szabványos, lokalizált és pontozáshelyes működésének ellenőrzése.

### Kötelező ellenőrzések

- helyes main library és teljes preloaded dependency lista;
- pontos oldalszám és egyedi `subContentId` értékek;
- minden komponens támogatott verziójú;
- teljes magyar lokalizáció, beleértve accessibility stringeket;
- helyes válasz, megoldás és feedback nem látható kezdetben;
- check, retry, show solution és reset konfiguráció megfelel a pedagógiai tervnek;
- pontmaximumok, részpontok és summary konzisztens;
- Question Set navigáció és eredményoldal helyes;
- képek és egyéb content assetek hordozható relatív elérési úttal működnek;
- csomag importálható és exportálható a célplatformon;
- állapotmentés és újratöltés nem okoz hibás pontot vagy feedbacket;
- a technikai tartalom nem jelenik meg a tanulói felületen.

### Komponensállapot-mátrix

Minden pontozott komponensnél ellenőrizendő:

1. üres kezdeti állapot;
2. válasz nélküli ellenőrzés;
3. helyes válasz;
4. hibás válasz;
5. részben helyes válasz, ha értelmezett;
6. megoldás megjelenítése;
7. újrapróbálkozás;
8. navigáció el és vissza;
9. oldalfrissítés vagy mentett állapot visszatöltése;
10. billentyűzetes végrehajtás.

## 5. Tesztkörnyezet és böngészőmátrix

Minimálisan:

- aktuális stabil Chromium desktop;
- aktuális stabil Chromium mobil emuláció;
- egy második böngészőmotor kockázat alapján;
- cél H5P-hosting környezet;
- statikus build helyi és CI-környezetben.

A pontos támogatási mátrix verziózott és release-manifesthez kötött.

## 6. QA dossier

Minden release candidate QA-mappája tartalmazza:

- QA-terv és vizsgált hatókör;
- buildazonosító, commit SHA és csomag SHA-256;
- környezet és böngészőverziók;
- lefuttatott ellenőrzőlisták;
- automatikus riportok;
- képernyőképek és vizuális bizonyítékok;
- hibajegyek és retest eredmények;
- elfogadott kockázatok és kivételek;
- dimenziónkénti reviewer és státusz;
- végső release-javaslat.

## 7. Belépési és kilépési feltételek

### QA-ba léphet

- befagyasztott Master Script, Build Guide és Asset Register;
- azonosítható release candidate;
- sikeres build és statikus audit;
- dokumentált tesztkörnyezet;
- nincs ismert build-blokkoló hiba.

### QA-ból kiléphet

- minden kötelező dimenzió `PASS`;
- nulla nyitott `BLOCKER`, `CRITICAL` vagy `MAJOR`;
- elfogadott `MINOR` eltérésekhez tulajdonos és célverzió tartozik;
- a retest és regresszió sikeres;
- a QA dossier teljes és aláírt.

## 8. Regressziós stratégia

- Szövegjavítás: érintett oldal, keresés/lokalizáció, történelmi és vizuális retest.
- Pontozás- vagy interakcióváltozás: teljes komponensállapot-mátrix és eredményregresszió.
- Library-váltás: teljes modul-, accessibility- és böngészőregresszió.
- Assetcsere: betöltés, méret, alt text, licenc, mobil és vizuális regresszió.
- Buildrendszer-váltás: minden modul smoke, hash és reprodukálhatósági ellenőrzés.
- Közös runtime-változás: teljes portfólió regresszió.

## 9. QA-státuszok

`NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `FAILED`, `PASS_WITH_ACCEPTED_RISK`, `PASS`.

A `PASS_WITH_ACCEPTED_RISK` nem használható történelmi pontatlanság, jogi hiány, kritikus accessibility-hiba vagy integritási eltérés elfedésére.
