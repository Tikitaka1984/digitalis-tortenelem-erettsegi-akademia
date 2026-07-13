# Digitális Történelem Érettségi Akadémia

## DTEA STANDARD v1.0

**Dokumentumtípus:** kötelező tananyag-fejlesztési, H5P-, UX-, vizuális és minőségbiztosítási szabvány  
**Hatály:** minden új DTEA-modul, Master Script, Build Guide, médiaelem és publikált kiadás  
**Státusz:** jóváhagyásra előterjesztett v1.0; a PR merge jelenti a hivatalos elfogadást  
**Első referenciaszint:** középszintű történelemérettségi, NAT 2020  
**Elsődleges futtatási környezet:** H5P Interactive Book, Lumi Desktop, H5P Standalone, GitHub Pages  
**Nyelv:** magyar

---

## 0. A szabvány használata

### 0.1 Cél

A DTEA STANDARD azt biztosítja, hogy az Akadémia különböző témájú moduljai azonos pedagógiai minőségben, felismerhető vizuális nyelven, kiszámítható navigációval és ellenőrizhető forráshűséggel készüljenek. A szabvány nem helyettesíti a témaspecifikus történelmi szakértelmet. Azt határozza meg, hogyan kell a jóváhagyott tartalmat digitális tanulási útvonallá alakítani.

### 0.2 Normatív kifejezések

- **KÖTELEZŐ:** eltérés csak dokumentált, jóváhagyott kivétellel lehetséges.
- **AJÁNLOTT:** alapértelmezett megoldás; eltérés indokolható.
- **MEGENGEDETT:** választható, ha illeszkedik a tanulási célhoz.
- **TILOS:** nem használható kiadásra jelölt modulban.
- **ELLENŐRZÉSI KAPU:** a következő fázis csak sikeres ellenőrzés után kezdhető meg.

### 0.3 Dokumentumhierarchia

1. DTEA STANDARD - minden modulra érvényes szabály.
2. Design System - platform- és komponensszintű vizuális tokenek.
3. Master Script - az adott modul végleges történelmi és pedagógiai tartalma.
4. Build Guide - az adott modul technikai, H5P- és UX-megvalósítása.
5. Asset Register - képek, térképek, ikonok, licencek és alt szövegek.
6. H5P-csomag - a jóváhagyott specifikáció megvalósítása.
7. Fejlesztői jelentés és QA-jegyzőkönyv - eltérések, tesztek, kiadási döntés.

Ütközés esetén a magasabb szintű dokumentum az irányadó. Történelmi állításnál azonban a jóváhagyott Master Script szövege nem írható felül UX- vagy technikai megfontolásból. Az eltérést vissza kell vezetni szakmai felülvizsgálatra.

### 0.4 Kötelező fejlesztési kapuk

| Kapu | Bemenet | Kilépési feltétel |
|---|---|---|
| G0 Forrásbefogadás | forráscsomag | forrásjegyzék, jogállás, verzió, elsődlegesség rögzítve |
| G1 Tartalmi modell | követelmények és források | tématérkép, tanulási célok, lefedettségi mátrix |
| G2 Master Script | tartalmi modell | szakmai és pedagógiai jóváhagyás |
| G3 Build Guide | jóváhagyott Master Script | minden oldal és H5P-elem specifikálva |
| G4 Build | Build Guide és assetek | valid H5P, eltérésnapló elkészült |
| G5 QA | H5P és jelentések | funkcionális, tartalmi, mobil- és a11y-tesztek sikeresek |
| G6 Pilot | kiadásra jelölt build | 5-10 tanuló visszajelzése feldolgozva |
| G7 Release | javított build | verzió, changelog, publikációs ellenőrzés kész |

---

# I. Küldetés és pedagógiai alapelvek

## 1. Küldetés

A DTEA célja nem a tankönyv képernyőre másolása, hanem olyan interaktív tanulási rendszer létrehozása, amelyben a tanuló:

- érti az okokat, folyamatokat és következményeket;
- térben és időben el tudja helyezni az eseményeket;
- forrásból következtet;
- felismeri a fogalmak, személyek és intézmények kapcsolatait;
- érettségi helyzetben alkalmazza a tudását;
- azonnali, magyarázó visszajelzést kap;
- önállóan meg tudja ítélni, mit kell még gyakorolnia.

## 2. Pedagógiai alapelvek

### 2.1 Követelményvezérelt tervezés

Minden modul a hatályos középszintű érettségi követelményekből indul ki. A moduladatlapban kötelező elkülöníteni:

- a középszinthez szükséges törzsanyagot;
- az emelt szintű vagy érdeklődést bővítő kiegészítést;
- a forrásban szereplő, de a modul céljához nem szükséges háttéranyagot.

Egy állítás nem válik kötelezővé pusztán azért, mert szerepel valamelyik forrásban. A követelmény, a tanulási cél és a forráshierarchia együtt határozza meg a státuszát.

### 2.2 Visszafelé tervezés

A sorrend: elvárt teljesítmény -> bizonyíték -> tanulási tevékenység -> média és H5P. TILOS egy látványos H5P-típust választani, majd utólag keresni hozzá tananyagot.

### 2.3 Aktív felidézés

Minden nagyobb tananyagblokk után legyen rövid felidézési pont. A kérdés ne pusztán a közvetlenül előtte álló mondat mechanikus visszamondását kérje, hanem fogalmi megkülönböztetést, sorrendet, kapcsolatot vagy következtetést.

### 2.4 Fokozatos terhelés

A modul három szinten építkezik:

1. **Felismerés:** fogalom, személy, hely, időpont azonosítása.
2. **Kapcsolás:** ok-okozat, személy-intézkedés, tér-idő kapcsolat.
3. **Alkalmazás:** forráselemzés, érettségi feladat, önálló vázlat.

Az első harmadban több irányítás és rövidebb feladat, a záró harmadban összetettebb, kevesebb támpontot adó tevékenység szükséges.

### 2.5 Magyarázó visszajelzés

Minden automatikusan javítható feladatnál kötelező:

- helyes válasz után rövid megerősítés és a lényegi összefüggés;
- hibás válasz után javító magyarázat, amely nem árulja el idő előtt a teljes megoldást;
- újrapróbálkozási lehetőség, ha a feladattípus támogatja;
- „Megoldás mutatása” csak ellenőrzés után.

A „Helyes” és „Helytelen” önmagában nem elfogadható visszajelzés.

### 2.6 Tévképzetek kezelése

Minden modulban legyen legalább egy „Gyakori hiba” vagy „Ne keverd össze” rész. A téves állítást vizuálisan el kell választani a korrekciótól. A téves megfogalmazás nem jelenhet meg magyarázat nélküli kiemelt mondatként.

### 2.7 Forrásalapú gondolkodás

Minden modul legalább két forráselemző helyzetet tartalmazzon. Ezek közül legalább az egyik kérjen a forrásból közvetlenül kiolvasható információt, legalább az egyik pedig forrás és háttértudás összekapcsolását. Hosszú jogvédett idézet helyett rövid, jogszerű idézet vagy saját forrásleírás alkalmazandó.

### 2.8 Kognitív terhelés

- Egy képernyőn egy domináns tanulási cél szerepeljen.
- Egy szövegblokk ajánlott hossza 60-120 szó, felső határa 180 szó.
- 180 szónál hosszabb egységet két logikai blokkra kell bontani, a szöveg megváltoztatása nélkül.
- Egy automatikus feladat ajánlott elemszáma mobilon 4-7.
- Egy oldalon legfeljebb két új interakciós mechanika jelenjen meg.
- Dekoratív elem nem versenyezhet az érdemi tartalommal.

### 2.9 Tanulói autonómia

A navigáció legyen szabadon áttekinthető, de a záró összegzés és teszt egyértelmű tanulási végpontként jelenjen meg. A pontszám nem büntető eszköz. A visszajelzés mutassa meg a következő lépést: ismétlés, újrapróbálkozás vagy továbblépés.

### 2.10 Időkeret

Egy teljes középszintű modul ajánlott ideje 35-50 perc. A Build Guide minden oldalhoz becsült időt rendel. A modulnak 10-15 perces ismétlő útvonallal is használhatónak kell lennie: fogalmak, idővonal, érettségi fókusz, záróteszt.

---

# II. Kötelező tananyagstruktúra

## 3. Modulszintű szerkezet

Az alábbi funkciók kötelezőek. Nem mindegyik igényel külön oldalt, de a Build Guide-ban azonosíthatónak kell lennie.

| Rész | Cél | Ajánlott H5P | Idő | Pedagógiai funkció | UX-szabály |
|---|---|---|---:|---|---|
| 1. Motiváció | relevancia és kérdésfelvetés | Text + Image / Course Presentation | 1-2 perc | figyelem, előzetes modell aktiválása | egy fő kérdés, egy hero vizuál |
| 2. Mit fogsz megtanulni? | mérhető célok | Accordion / Text | 1-2 perc | elvárások és önszabályozás | 5-7 cél, közép/emelt jelmagyarázat |
| 3. Előzetes tudás | diagnosztika | Question Set / vegyes rövid elemek | 3-4 perc | előismeret aktiválása | nem számít bele a záró eredménybe |
| 4. Történelmi háttér | tér, idő, előzmény | Text, Timeline, Image Hotspots | 5-8 perc | kontextus kialakítása | rövid blokkok, térkép és kronológia |
| 5. Interaktív feldolgozás | fő folyamat megértése | Interactive Book-oldalak, Accordion, Drag and Drop | 15-22 perc | magyarázat, gyakorlás | blokkonként egy mini feladat |
| 6. Forráselemzés | bizonyítékalapú következtetés | Course Presentation / Column | 5-8 perc | forráskompetencia | forrás, kérdés, kulcs és pontozás együtt |
| 7. Összefüggések | ok-okozat és összehasonlítás | Drag and Drop, Summary, Diagram | 3-5 perc | rendszerezés | 3-6 kapcsolat, nem dekoratív diagram |
| 8. Érettségi fókusz | vizsgaalkalmazás | Accordion, Mark the Words, Essay | 4-6 perc | tétel- és esszéfelkészítés | tipp, tipikus hiba, vázlat |
| 9. Gyakorló teszt | integrált mérés | Question Set | 6-10 perc | önellenőrzés | új kérdések, egyértelmű pontozás |
| 10. Összefoglalás | tanulási zárás | Summary / Text | 2-3 perc | konszolidáció | 8-12 állítás vagy vázlatpont |
| 11. Továbbtanulás | következő lépés | Text + linklista | 1 perc | transzfer és bővítés | csak ellenőrzött, jogszerű célpont |

## 4. Oldalszintű sablon

Minden tartalmi oldal ajánlott sorrendje:

1. oldalcím és 1 mondatos orientáció;
2. rövid tanulói magyarázat;
3. vizuális vagy strukturáló elem;
4. kulcsállítások vagy fogalomkiemelés;
5. egy célzott interakció;
6. magyarázó visszajelzés;
7. szükség szerint „Érettségi tipp” és „Gyakori hiba”.

Nem kötelező minden elemet minden oldalon megjeleníteni. TILOS azonban öt egymást követő, kizárólag szöveget tartalmazó oldal.

## 5. Master Script kötelező mezői

Minden oldalhoz szerepeljen:

- oldalszám és végleges cím;
- tanulási cél;
- közép- vagy emelt szint jelölése;
- képernyőn megjelenő teljes szöveg;
- kulcsállítások;
- H5P-típus és alternatíva;
- feladatutasítás;
- válaszlehetőségek és helyes válasz;
- pontérték és részpont szabálya;
- helyes és hibás visszajelzés;
- Retry és Show Solution beállítás;
- médiaigény, képarány, alt szöveg és jogállás;
- UX- és mobilmegjegyzés;
- forráshivatkozás;
- tanári ellenőrzést igénylő pont.

## 6. Build Guide kötelező mezői

A Build Guide nem írhat új történelmi tartalmat. Tartalmazza:

- modul- és verzióadatok;
- pontos oldaltérkép;
- oldalanként komponenssorrend;
- H5P-könyvtár és verzió;
- mezőszintű konfiguráció;
- pontozás, viselkedés és visszajelzés;
- desktop-, tablet- és mobilviselkedés;
- akadálymentes alternatíva;
- médiafájl és placeholder szabály;
- elfogadási kritérium;
- várható építési idő és nehézség;
- Lumi-korlát esetére engedélyezett alternatíva;
- eltérésnapló.

---

# III. H5P STANDARD

## 7. Általános szabályok

### 7.1 Keret

Komplex, több szakaszból álló DTEA-modul elsődleges kerete az **Interactive Book**. Különálló mikrotananyag akkor megengedett, ha a tanulási cél egyetlen interakcióval teljesíthető.

### 7.2 Stabilitás

- Csak a cél-Lumi környezetben ténylegesen elérhető és próbaexporttal validált könyvtár használható.
- Kísérleti vagy ritkán karbantartott tartalomtípushoz kötelező alternatíva.
- A csomag nem támaszkodhat futásidőben nem garantált külső bővítményre.
- Minden verzióban meg kell őrizni a forrás `.h5p` SHA-256 lenyomatát és a deklarált függőségek listáját.

## 8. Tartalomtípus-döntési mátrix

### 8.1 Interactive Book

**Ajánlott:** többféle tartalmi és feladattípusból álló, 20-50 perces modulhoz; fejezetes navigációhoz; összesített haladásjelzéshez.  
**Nem ajánlott:** egyetlen kvízhez vagy 5 perces mikrotananyaghoz.  
**Kerülendő:** ha a célrendszer nem támogatja a szükséges beágyazott könyvtárakat.  
**Kötelező:** rövid, informatív oldalcímek; logikai sorrend; 18-32 oldal ajánlott, 35 felett külön indoklás.

### 8.2 Image Hotspots

**Ajánlott:** történelmi térkép, épület, tárgy vagy képi forrás részleteinek felfedezéséhez.  
**Nem ajánlott:** lineáris kronológia vagy hosszú magyarázat megjelenítésére.  
**Kerülendő:** túl sűrű térképen, apró érintési célokkal vagy szöveges alternatíva nélkül.  
**Szabály:** legalább 44×44 CSS-pixel érintési cél; 3-8 hotspot; mobilon tesztelt nagyítás; minden információ szövegesen is hozzáférhető.

### 8.3 Timeline

**Ajánlott:** 5-12 egymást követő eseményhez, amikor az időbeli távolság vagy folyamat számít.  
**Nem ajánlott:** két dátumhoz vagy összetett párhuzamos folyamatokhoz.  
**Kerülendő:** nagyon hosszú leírásokkal, nem reszponzív médiával.  
**Alternatíva:** Accordion dátumos címekkel vagy Course Presentation.

### 8.4 Accordion

**Ajánlott:** célok, személyek, intézmények, közép/emelt bontás, kiegészítő magyarázat.  
**Nem ajánlott:** a teljes törzsanyag elrejtésére.  
**Kerülendő:** egymásba ágyazott accordion vagy 8-nál több panel.  
**Szabály:** panelcím önmagában is jelentést hordozzon; alapállapotban legfeljebb egy panel nyitott.

### 8.5 Quiz / Question Set

**Ajánlott:** előzetes méréshez és záróteszthez, vegyes kérdéstípusokkal.  
**Nem ajánlott:** hosszú tananyagszöveg kereteként.  
**Kerülendő:** szó szerint ismételt mini feladatok, indokolatlan negatív pontozás.  
**Szabály:** egyértelmű pontösszeg; teljesítményszintek; minden kérdéshez visszajelzés.

### 8.6 Drag and Drop

**Ajánlott:** személy-intézkedés, fogalom-kategória, térképi hely vagy folyamat párosítására.  
**Nem ajánlott:** hosszú mondatok vagy 8-nál több mozgatható elem esetén.  
**Kerülendő:** kizárólagos értékelési formaként, billentyűzetes/szöveges alternatíva nélkül.  
**Mobil:** nagy célterület, rövid címke, függőleges elrendezés; alternatíva Matching vagy Multiple Choice.

### 8.7 Image Pair

**Ajánlott:** két vizuális forrás, előtte-utána állapot, stílus vagy technológia összevetésére.  
**Nem ajánlott:** puszta dekorációra vagy ha a különbség csak színnel érzékelhető.  
**Kerülendő:** eltérő arányú, rosszul feliratozott képekkel.  
**Szabály:** mindkét kép alt szövege és összehasonlítási szempontja kötelező.

### 8.8 Interactive Video

**Ajánlott:** 3-8 perces, jogszerűen használt videóhoz, 2-5 értelmes megállási ponttal.  
**Nem ajánlott:** hosszú előadáshoz, gyenge hanghoz vagy felirat nélkül.  
**Kerülendő:** külső videó, amelynek elérhetősége nem garantálható.  
**Szabály:** felirat/átirat, időbélyegek, nem túl sűrű interakció, letöltési alternatíva ahol jogszerű.

### 8.9 Branching Scenario

**Ajánlott:** történelmi döntési helyzet, forráskritika vagy több következménnyel járó választás modellezésére.  
**Nem ajánlott:** tényszerű eseménysor tanítására.  
**Kerülendő:** ha a fikció és történelmi tény nem különül el; ha egy „helyes” döntést utólag történelmi szükségszerűségként állít be.  
**Szabály:** minden ág jelölje, mi dokumentált és mi didaktikai modell.

### 8.10 Course Presentation

**Ajánlott:** vizuális forráselemzéshez, intézményi folyamatábrához, lépésenként feltárt térképhez.  
**Nem ajánlott:** teljes könyv helyettesítésére vagy PowerPoint-szerű passzív diáksorra.  
**Kerülendő:** apró abszolút pozicionált elemekkel mobilon.  
**Szabály:** egy dia egy gondolat; nagy érintési célok; szöveges alternatíva.

## 9. Feladatszabvány

### 9.1 Kérdésminőség

- A kérdés pontosan egy tudáselemet vagy világosan jelölt többes választ mérjen.
- A disztraktor legyen hihető, de egyértelműen hibás a jóváhagyott források alapján.
- TILOS nyelvtani vagy formai jelzéssel elárulni a választ.
- Negatív kérdés csak indokolt esetben használható, a „NEM” szó vizuális kiemelésével.
- A kérdés nem alapulhat nem tanított részleten.

### 9.2 Pontozás

- Alapértelmezés: 1 pont / önálló tudáselem.
- Több helyes válasz esetén a részpont és hibás jelölés hatása előre rögzítendő.
- Drag and Drop esetén a pontozási egység az egyes helyes párosítás.
- A záróteszt pontösszege legyen egyszerűen értelmezhető, ajánlott 20 pont.
- A teljesítményszintekhez konkrét tanulói következő lépés tartozzon.

### 9.3 Újrapróbálkozás és megoldás

Automatikus feladatnál Retry alapértelmezetten bekapcsolt. Show Solution csak válaszellenőrzés után jelenhet meg. Diagnosztikus előtesztben a megoldás megmutatható, de az eredmény nem adódhat hozzá a záró pontszámhoz.

---

# IV. UX ÉS AKADÁLYMENTESSÉG

## 10. Információs architektúra

- A címek legyenek 2-7 szavasak és megkülönböztethetők.
- A tanuló mindig lássa a modul címét, az aktuális fejezetet és a továbblépés módját.
- A navigáció sorrendje a Build Guide oldaltérképét kövesse.
- TILOS oldalt átnevezni vagy átrendezni dokumentált verzióváltás nélkül.
- A 30 oldal körüli könyvet tematikus szakaszokkal és következetes ikonokkal kell tagolni.

## 11. Reszponzív viselkedés

Kötelező célméretek:

- mobil: 360-430 CSS-pixel;
- tablet: 768-1024 CSS-pixel;
- desktop: 1280-1920 CSS-pixel.

Mobilon:

- nincs vízszintes görgetés, kivéve indokolt, hozzáférhető adatvizualizáció;
- a szöveg nem kisebb 16 CSS-pixel törzsméretnél;
- a gombok és célterületek legalább 44×44 CSS-pixelesek;
- a többoszlopos tartalom egy oszlopra törik;
- a drag-and-drop alternatívája dokumentált;
- a térképek nagyíthatók vagy külön teljes képernyős nézetet kapnak.

## 12. WCAG-alapelvek

- Cél: WCAG 2.2 AA.
- Normál szöveg kontrasztja legalább 4,5:1, nagy szövegé 3:1.
- A fókuszjelző látható, nem takart és legalább 3:1 kontrasztú.
- A jelentés nem támaszkodhat csak színre.
- Minden érdemi képhez kontextusfüggő alt szöveg tartozik.
- Dekoratív kép alt értéke üres.
- Videóhoz felirat vagy teljes átirat szükséges.
- Animáció tiszteletben tartja a `prefers-reduced-motion` beállítást.
- Billentyűzettel elérhető sorrendnek követnie kell a vizuális sorrendet.
- Automatikus időkorlát csak kikapcsolható vagy hosszabbítható formában használható.

## 13. Állapotok

Minden interaktív felülethez tervezendő:

- alapállapot;
- hover, ha van mutatóeszköz;
- billentyűzetfókusz;
- aktív/kiválasztott;
- helyes és hibás;
- letiltott;
- betöltés;
- üres állapot;
- kulturált hibaállapot.

---

# V. VIZUÁLIS ÉS DESIGN SYSTEM STANDARD

## 14. Márkaalapelvek

A vizuális nyelv modern, nyugodt, tudományos és tanulóbarát. Nem utánoz régi pergament, nem alkalmaz folyamatos „történelmi” textúrát, és nem használ dekoratív betűtípust törzsszöveghez. A korszakot a képi tartalom és az akcentus jelzi, nem a használhatóság rovására menő díszítés.

## 15. Színpaletta

Az aktuális platform tokenjei az irányadók:

| Szerep | Világos mód | Használat |
|---|---|---|
| Canvas | `#F7F5EF` | oldalháttér |
| Surface | `#FFFFFF` | kártya, panel |
| Ink | `#172018` | törzsszöveg |
| Brand | `#264F3D` | elsődleges gomb, fejléc |
| Accent | `#D5FF65` | fókuszált kiemelés, haladás |
| Success | `#287A52` | helyes állapot |
| Error | `#B42318` | hibás állapot |
| Focus | `#4169E1` | billentyűzetfókusz |

Sötét módban csak a Design Systemben rögzített tokenpárok használhatók. Új modul nem vezethet be önálló, ellenőrizetlen színkódokat. Korszakjelölő szín csak címkén, illusztráción vagy finom akcentusként jelenhet meg.

## 16. Szemantikus infoboxok

| Komponens | Szerep | Ikon | Szabály |
|…12684 tokens truncated…l méri a befejezést, időt, hibapontokat, érthetőséget és motivációt. A pilot megfigyelés nem automatikusan jelent tartalmi változtatást; döntési jegyzőkönyv szükséges.

### 60.8 7. fázis – release

A jóváhagyott javítások új verzióba kerülnek. CI, secret scan, assetellenőrzés és GitHub Pages smoke test után külön merge- és publikálási jóváhagyás történik. A projekt archiválja a forrás buildet és a kiadott csomagot.

---

## Függelék D – Master Script minimális fejezetsablon

1. Dokumentum-metaadat és státusz.
2. Moduladatlap.
3. Forrás- és követelményhatár.
4. Mérhető célok és lefedettségi mátrix.
5. Oldaltérkép és időbudget.
6. Oldalankénti teljes specifikáció.
7. Kronológia.
8. Kulcsszemélyek és intézmények.
9. Fogalmak.
10. Topográfia és térképbrief.
11. Forráselemzések.
12. Interaktív feladatbank.
13. Szóbeli tétel- és esszéfelkészítés.
14. Záróteszt és értékelési szintek.
15. Tanári megjegyzések és differenciálás.
16. Média- és assetigény.
17. Forrásjegyzék és nyomonkövetési mátrix.
18. Tartalmi QA.

## Függelék E – Build Guide minimális fejezetsablon

1. Kapcsolódó Master Script verzió.
2. Platform- és library-környezet.
3. Teljes oldaltérkép.
4. Globális navigáció és viselkedés.
5. Oldalankénti H5P-konfiguráció.
6. Pontozási és visszajelzési mátrix.
7. Média- és Asset Register.
8. Reszponzív szabályok.
9. Akadálymentes alternatívák.
10. Teljesítmény- és fájlméret-budget.
11. Engedélyezett technikai alternatívák.
12. Build- és regressziós checklist.
13. Elfogadási kritériumok.
14. Eltérésnapló.
15. Várható fejlesztési idő és kockázatok.

## Függelék F – PR review kérdéssor

### Tartalom

- Minden állítás visszavezethető a jóváhagyott forrásokra?
- Megfelel a deklarált vizsgaszintnek?
- Világos az ok-okozati és tér-időbeli szerkezet?
- A fogalomdefiníciók és névalakok következetesek?
- Nincs-e modern fogalom kritikátlan visszavetítése?

### Pedagógia

- Minden cél gyakorolt és értékelt?
- A feladat valóban a kijelölt kognitív műveletet méri?
- A visszajelzés segít kijavítani a tévképzetet?
- Reális a tanulási idő és a terhelés?
- Az opcionális kitekintés nem terheli a törzsutat?

### Technika és UX

- A H5P-típus a legstabilabb megfelelő megoldás?
- Billentyűzettel és mobilon is használható?
- A média betöltődik és van alternatív szövege?
- Egyezik a pontozás és működik a Retry/Show Solution?
- Van dokumentált alternatíva minden ismert korlátra?

### Kiadás

- A változás hatóköre tiszta és elkülönített?
- A CI és a kézi teszt eredménye dokumentált?
- Nincs érzékeny adat vagy jogilag bizonytalan asset?
- A verzió és changelog helyes?
- A merge külön jóváhagyásra vár?

## Függelék G – A szabvány terjedelmi és renderelési profilja

A DTEA STANDARD forrásformátuma Markdown. Hivatalos kézikönyvként A4-es oldalra, 11 pontos törzsszöveggel, 1,15–1,25-ös sorközzel, 20–25 mm margóval, tartalomjegyzékkel és oldaltörésekkel renderelendő. A célterjedelem 40–60 oldal; a tényleges oldalszám a Markdown-renderelő, a betűkészlet és a táblázatok tördelése szerint változhat. A forrásfájl a normatív változat, a PDF csak kiadási nézet.

A kézikönyv nagyobb változtatásakor ellenőrizni kell:

- a fejezetszámozást és belső hivatkozásokat;
- a táblázatok A4-es tördelhetőségét;
- a checklisták nyomtathatóságát;
- az ékezetes magyar szöveg helyes kódolását;
- a forrás Markdown és a kiadott PDF verzióazonosságát.

---

# XII. OPERATÍV REFERENCIA

## 61. Szemantikus komponenskönyvtár

### 61.1 Fogalomdoboz

**Funkció:** új vagy vizsgán kötelező fogalom pontos bevezetése.  
**Kötelező részek:** „Fogalom” címke, fogalom neve, egy mondatos definíció, egy témabeli példa.  
**Opcionális:** „Ne keverd össze” sor.  
**Tilos:** körkörös definíció, újabb meg nem magyarázott szakkifejezés, kizárólag színnel történő jelölés.

Javasolt elrendezés: bal oldali 4 px-es kék jelzővonal, egyszerű könyv vagy címke ikon, világos háttér, 16–18 px törzsszöveg. Mobilon teljes szélességű. Egy oldalon legfeljebb három fogalomdoboz ajánlott; több fogalom esetén Dialog Cards vagy külön fogalomoldal használata indokolt.

### 61.2 Érettségi tipp

**Funkció:** megmutatja, hogyan használható a tanult elem vizsgahelyzetben. Nem ismétli meg a teljes tananyagot. Konkrét cselekvést kér: hasonlítsd össze, kapcsold össze, nevezd meg a szempontot, kerüld a túlzó állítást.

Kötelező részek: „Érettségi tipp” felirat, egy rövid stratégia, szükség esetén jó mondatkezdet. Sárga/borostyán jelölés mellett villanykörte vagy cél ikon használható. A szöveg legfeljebb 60–80 szó.

### 61.3 Gyakori hiba

**Funkció:** konkrét tévképzet korrekciója. Két részből áll: hibás állítás vagy tévesztés, majd a helyes megkülönböztetés. Piros jelzés nem jelent tanulói büntetést; a hangnem tárgyszerű.

Minta:

> **Gyakori hiba:** „X hozta létre Y-t.”  
> **Pontosítás:** X nem létrehozta, hanem [forrás szerint pontos szerep].

A komponens nem használható általános figyelmeztetésre vagy technikai instrukcióra.

### 61.4 Forráselemzés-doboz

Kötelező részek: forrástípus, keletkezési kontextus, olvasási kérdés, maga a forrás vagy forrásleírás, kérdések, pontozás, megoldás és visszajelzés. A szín lila vagy indigó, de a „Forráselemzés” szöveges címke mindig jelen van.

### 61.5 Kitekintés / emelt szint

A törzsúttól eltérő mélységet világosan jelöli. A panel alapértelmezetten csukott Accordion lehet. Nem rejthet el középszinthez szükséges információt. A cím tartalmazza: „Kitekintés” vagy „Emelt szint”.

### 61.6 Tanári megjegyzés

Nem jelenik meg automatikusan a tanulói nézetben. Tartalmazhat időkeretet, differenciálást, érzékeny tartalom kezelését, alternatív feladatot és megfigyelési szempontot. A tanári instrukciót külön dokumentumréteg vagy jelölt blokk őrizze meg.

## 62. Tipográfiai és elrendezési tokenek

### 62.1 Tipográfiai skála

| Token | Cél | Asztali minimum | Mobil minimum |
|---|---|---:|---:|
| `display` | hero cím | 40 px | 30 px |
| `h1` | moduloldal főcím | 32 px | 26 px |
| `h2` | oldalon belüli szakasz | 26 px | 22 px |
| `h3` | komponenscím | 21 px | 19 px |
| `body` | törzsszöveg | 18 px | 17 px |
| `small` | kredit, metaadat | 14 px | 14 px |

Ajánlott rendszerbetű-család: `Inter`, `Segoe UI`, `Arial`, sans-serif. Hosszú történeti forrásrészlethez külön serif betű csak akkor használható, ha a kontraszt és olvashatóság változatlan. Dőlt szöveg nem hordozhat nagy mennyiségű tartalmat.

### 62.2 Térközskála

Alapegység 4 px. Javasolt tokenek: 4, 8, 12, 16, 24, 32, 48, 64 px. Egy komponensen belül 8–16 px, komponensek között 24–32 px, nagy oldalszakaszok között 40–48 px. A túlzott függőleges térköz mobilon kerülendő.

### 62.3 Szélesség és olvasási sor

Törzsszöveg ideális maximális szélessége 68–75 karakter/sor. Nagy képernyőn a szöveg ne nyúljon teljes viewport-szélességre. Táblázat csak akkor használható, ha mobilon kártyává alakítható vagy vízszintes görgetése világosan jelzett.

### 62.4 Gombok és célterületek

Minimum 44×44 CSS px. A gomb felirata cselekvést ír le: „Válasz ellenőrzése”, „Újrapróbálom”, „Megoldás mutatása”. „OK” vagy „Tovább” csak egyértelmű kontextusban használható. Elsődleges gombból egy vizuális régióban legfeljebb egy legyen.

## 63. Szín- és állapottokenek

### 63.1 Alappaletta

| Funkció | Token | Alapszín | Használat |
|---|---|---|---|
| márka | `brand-primary` | `#1E3A8A` | fejléc, elsődleges gomb |
| információ/fogalom | `info` | `#2563EB` | fogalomdoboz, információ |
| siker | `success` | `#15803D` | helyes állapot |
| figyelem/tipp | `warning` | `#B45309` | érettségi tipp |
| hiba/tévképzet | `danger` | `#B91C1C` | gyakori hiba, hibajelzés |
| forrás | `source` | `#6D28D9` | forráselemzés |
| emelt/kitekintés | `advanced` | `#7E22CE` | opcionális mélység |
| semleges szöveg | `text` | `#172033` | törzsszöveg |
| háttér | `surface` | `#FFFFFF` | kártya |
| halvány háttér | `surface-muted` | `#F4F7FB` | oldalszakasz |

A végleges felületi implementációban minden színpárt WCAG-kontrasztméréssel kell igazolni. A token nem jogosít fel arra, hogy világos háttéren változtatás nélkül használják a hozzá tartozó színt.

### 63.2 Interakciós állapotok

- **default:** jól látható interaktív határ;
- **hover:** finom háttér- vagy keretváltozás, nem tartalmi információ;
- **focus:** minimum 2 px-es kontrasztos fókuszgyűrű;
- **selected:** ikon és szöveges/formaállapot;
- **correct:** zöld mellett pipa és „Helyes” szöveg;
- **incorrect:** piros mellett X és magyarázó szöveg;
- **disabled:** alacsonyabb hangsúly, de olvasható; oka hozzáférhető;
- **loading:** folyamatjelző és szöveg;
- **error:** kulturált hiba, következő teendő és technikai kivétel elrejtése.

## 64. H5P-konfigurációs referencia

### 64.1 Retry

Formáló feladatnál alapértelmezetten engedélyezett. A második próbálkozás ne csökkentse automatikusan a pontot, kivéve ha a Master Script ezt kéri. Zárótesztnél a modul pedagógiai célja dönt: gyakorló mód esetén engedett, vizsgaszimulációnál első eredmény külön rögzíthető.

### 64.2 Show Solution

Az első ellenőrzés előtt TILOS megjeleníteni. Formáló feladatnál legalább egy próbálkozás után, lehetőleg a visszajelzés elolvasását követően jelenhet meg. Ha a library csak globális kapcsolót kínál, a Build Guide dokumentálja a tényleges viselkedést.

### 64.3 Visszajelzési tartományok

Question Set esetén legalább három tartomány ajánlott: 0–49%, 50–79%, 80–100%. A szöveg konkrét következő lépést adjon. A százalékhatárok helyett a Master Scriptben rögzített pontsáv az irányadó; a Build Guide számolja át.

### 64.4 Randomizálás

Válaszopciók véletlen sorrendje megengedett, ha nincs „mindegyik”, „fenti”, időrendi vagy betűre hivatkozó megoldás. Kérdések randomizálása csak nagy bankból történhet, és nem bonthatja meg forrásszöveg és kérdései kapcsolatát.

### 64.5 Pontozási részletek

Több helyes válasznál a teljes pont feltétele egyértelmű. Negatív pont alapértelmezetten nem használható. Részpont csak akkor, ha a H5P library megbízhatóan kezeli és a Master Script rögzíti. A vizuális drag feladat pontozása mellett szöveges alternatíva azonos maximális pontot kap.

### 64.6 Adminisztratív címkék

Minden elem admin címe tartalmazza a modulkódot, oldalszámot és elemtípust, például `FFD-P04-Q01-MC`. A tanulói felületen megjelenő cím ettől eltérhet. Ez segíti az auditot, xAPI-események olvasását és hibajelentést.

## 65. Funkcionális tesztesetek

### T-01 Könyv betöltése

**Előfeltétel:** tiszta böngészőcache.  
**Lépés:** nyisd meg a publikus URL-t.  
**Elvárt:** nincs konzolhiba, minden alapasset betölt, cím és első oldal megjelenik, fókusz a logikus kezdőpontra kerül.

### T-02 Oldalnavigáció

Haladj előre és vissza minden oldalon, majd válassz oldalt a tartalomjegyzékből. Az oldalszám, cím és tartalom minden esetben egyezik; nincs üres vagy duplikált oldal; a visszalépés nem nulláz indokolatlanul.

### T-03 Accordion

Nyisd és zárd minden panelt egérrel, érintéssel és billentyűzettel. A panelcím bejelenti a nyitott/zárt állapotot; tartalom nem vágódik le.

### T-04 Multiple Choice

Próbáld ki a helyes és minden hibás opciót. Ellenőrizd a pontot, a visszajelzést, Retry-t és Show Solution feltételét. Újrapróbálás után nincs duplikált visszajelzés.

### T-05 Drag and Drop

Helyes, hibás és részleges elrendezéssel tesztelendő asztali és érintéses nézetben. Célterületek nem fedik egymást, elem visszavehető, pontozás reprodukálható. A billentyűzetes alternatíva ugyanazt méri.

### T-06 Image Hotspots

Minden hotspot megnyílik, bezárható, nem lóg le a képernyőről, és mobilon is megérinthető. A szöveges alternatíva minden hotspot információját tartalmazza.

### T-07 Timeline

Minden esemény elérhető, dátum és sorrend helyes, hosszú magyar szöveg nem vágódik le. A lineáris lista ugyanazt a tartalmat adja.

### T-08 Záróteszt

Egy teljesen helyes, teljesen hibás és vegyes válaszsorral futtatandó. Az összpontszám, százalék és teljesítménysáv egyezik a Master Scripttel. Az újrapróbálás és megoldásmutatás a specifikáció szerint működik.

### T-09 Assethiba

Fejlesztői környezetben szimulálj hiányzó képet. A keret kulturált alternatívát vagy alt szöveget mutat; a modul többi része működőképes, nincs kezeletlen JavaScript-kivétel.

### T-10 Reszponzív regresszió

320, 375, 768, 1024 és 1440 px szélességen ellenőrizendő a hero, táblázat, kérdés, visszajelzés és navigáció. Nincs vízszintes oldal-scroll, levágott gomb vagy egymásra csúszó vezérlő.

## 66. Tartalmi audit eljárása

Az auditor oldalanként három dokumentumot vet össze: Master Script, Build Guide, H5P build. Az audit nem javít, hanem bizonyítékot és eltérést rögzít.

| Mező | Tartalom |
|---|---|
| oldal | szám és cím |
| script elvárás | rövid hivatkozás |
| build tény | mit látott az auditor |
| eltérés | hiány, többlet, módosítás, rossz típus |
| hatás | történelmi, pedagógiai, technikai, UX |
| súlyosság | kritikus, javasolt, esztétikai |
| bizonyíték | képernyőkép, elem ID, szövegrész |
| javasolt következő lépés | javítási sprint, döntés vagy elfogadás |

**Kritikus:** történelmi hiba, hiányzó kötelező tartalom, rossz helyes válasz/pont, működésképtelen navigáció, érzékeny adat, súlyos hozzáférési akadály.  
**Javasolt:** a tanulási célt gyengítő, de használatot nem blokkoló eltérés, mobilkockázat, túlterhelő elrendezés.  
**Esztétikai:** a jelentést és működést nem érintő vizuális következetlenség.

Az auditjelentés végén külön listában szerepel minden kategória és az érintett oldalak. Javítás csak külön jóváhagyott feladatban történhet.

## 67. Pilot teszt protokoll

### 67.1 Minta

Első pilot: 5–10, a célcsoportot képviselő tanuló. Lehetőleg legyen köztük eltérő előzetes tudású és eltérő eszközt használó résztvevő. A pilot nem osztályzat, a tanuló ezt előre tudja.

### 67.2 Mérendő adatok

- befejezte-e a modult;
- teljes idő és oldalszakaszok ideje;
- hol kért segítséget;
- mely interakciót próbálta újra;
- záróteszt pontszáma;
- mobil/asztali eszköz;
- technikai hiba;
- 1–5 skálán érthetőség, terhelés, motiváció;
- egy nyitott kérdés: „Mi segített a legtöbbet?”;
- egy nyitott kérdés: „Hol akadtál el?”

Személyes adat csak szükséges mértékben, előzetes tájékoztatással kezelhető. Nyilvános repóba tanulói név vagy egyéni eredmény nem kerülhet.

### 67.3 Megfigyelési küszöbök

- 20%-nál több résztvevő ugyanott elakad: javasolt UX-vizsgálat;
- bármely rosszul pontozott helyes válasz: kritikus;
- célidő 25%-nál nagyobb túllépése a többségnél: tartalmi terhelés review;
- mobilon nem teljesíthető interakció: kritikus;
- 80% alatti befejezési arány technikai okból: kritikus;
- ismétlődő szövegértési panasz: pedagógiai review.

### 67.4 Döntési jegyzőkönyv

Minden visszajelzéshez döntés tartozik: elfogadva, későbbre ütemezve vagy elutasítva, indoklással. A pilot megjegyzése nem módosíthatja közvetlenül a jóváhagyott Master Scriptet; új verzió és review szükséges.

## 68. Karbantartási ciklus

### 68.1 Rendszeres ellenőrzés

- félévente: publikus linkek, runtime és mobil smoke test;
- évente: követelményverzió és forrásjogok ellenőrzése;
- H5P/runtime frissítéskor: teljes regressziós készlet;
- jelentett kritikus hiba után: azonnali vizsgálat és szükség esetén rollback;
- új Design System verziónál: hatáselemzés, nem automatikus migráció.

### 68.2 Elavulásjelzés

Ha a vizsgakövetelmény megváltozik, a modul „review szükséges” státuszt kap. A publikus felületen csak akkor maradhat változatlanul ajánlott, ha szakmai vezető igazolja a kompatibilitást. Régi követelményverzió nem törlendő automatikusan; archivált kiadásként megőrizhető.

### 68.3 Hibajelentés minimuma

Modulverzió, URL, oldal, elem ID, eszköz és böngésző, lépések, várt és tényleges eredmény, képernyőkép vagy konzolrészlet. Történelmi hibánál pontos állítás és jóváhagyott forráshivatkozás szükséges.

## 69. Anti-pattern katalógus

### 69.1 „PDF a képernyőn”

Hosszú, tömör szöveg egymás alatt, interakció nélkül. Javítási elv: célonként rövid blokkok, vizuális szervezés és értelmes felidézés; tartalomvesztés nélkül.

### 69.2 „Interakció mint dísz”

Hotspot, húzás vagy animáció úgy, hogy a tanuló ugyanazt egyszerű olvasással is elérné, és nincs kognitív művelet. Javítás: célhoz rendelt komponens vagy egyszerűbb megoldás.

### 69.3 „Mindent pontozunk”

Fogalomkártya megnyitása, navigáció vagy motivációs kérdés pontot kap. Ez torzítja az eredményt. Csak bizonyítható tudásteljesítmény pontozható.

### 69.4 „A megoldás azonnal látható”

Show Solution első próbálkozás előtt vagy vizuálisan kiemelt helyes opció. Ez megszünteti a felidézést és érvényteleníti a tesztet.

### 69.5 „Szín az egyetlen jel”

Helyes/zöld és hibás/piros szöveges vagy ikonjel nélkül. Nem hozzáférhető. Minden állapot többcsatornás jelzést kap.

### 69.6 „AI mint forrás”

Generált állítás hivatkozás nélkül bekerül a tananyagba. Kritikus folyamat-hiba. Az AI szerkesztői eszköz, a Source Register a bizonyíték.

### 69.7 „Placeholder release-ben”

Végleges kiadásban „később cserélendő” kép vagy üres médiahely marad. Release-blokkoló, kivéve ha a jóváhagyott Design tudatosan semleges, végleges helyettesítőt ír elő.

### 69.8 „Build Guide utólag”

A H5P elkészül, majd dokumentációként visszaírják a döntéseket. Így a Guide nem specifikáció és nem védi a tartalmat. A helyes sorrend: jóváhagyott Script → Guide → build.

## 70. Gyors döntési fák

### 70.1 Kell-e kép?

1. A kép hordoz tanulási információt? Ha nem, csak akkor használható, ha nem növeli a terhelést.  
2. A szövegnél gyorsabban mutat térbeli, vizuális vagy szerkezeti kapcsolatot? Ha igen, indokolt.  
3. Van jogtiszta és hiteles forrás? Ha nincs, sematikus saját ábra vagy placeholder fejlesztői buildben.  
4. Van alt/szöveges alternatíva? Ha nincs, még nem kész.

### 70.2 Kell-e interakció?

1. Van megnevezett kognitív művelet?  
2. Az interakció bizonyítja vagy gyakoroltatja ezt?  
3. Mobilon és billentyűzettel működik?  
4. Egyszerűbb komponens ugyanilyen jól teljesít?  
5. Van visszajelzés és elfogadási teszt?

Ha bármelyik döntő kérdésre nem a válasz, az interakciót újra kell tervezni.

### 70.3 Készen áll-e a tartalom buildre?

- Source Register lezárt;
- követelmény és cél mátrix kész;
- Master Script teljes, nincs nyitott történelmi döntés;
- pontozás ellenőrzött;
- médiaigény briefelve;
- tartalmi review jóváhagyott;
- Build Guide verziózott és mezőszintű.

E feltételek hiányában csak technikai sandbox készíthető, hivatalos modulbuild nem.

