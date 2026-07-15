# DTEA végponttól végpontig workflow

**Folyamat:** Forrás → Master Script → Instructional Design → Build Guide + Asset Register → H5P → automatikus és kézi QA → Release

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`. A Work a szerzői és build-munkatér, a GitHub Pages a publikációs célkörnyezet. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési eszköz.

## 1. Folyamatirányítási elvek

- Minden fázisnak névvel ellátott tulajdonosa, bemenete, kimenete és elfogadási kapuja van.
- Jóváhagyás nélküli kimenet nem használható hivatalos downstream bemenetként.
- A forráskapcsolat az állítástól a release-ig nem szakadhat meg.
- Hiba esetén a legkorábbi hibás artefaktumot kell javítani, majd az érintett downstream eredményeket újragenerálni és regressziózni.
- A workflow-bizonyítékokat modulazonosító és verzió szerint kell megőrizni.

## 2. Áttekintő kapumodell

| Fázis | Kötelező bemenet | Kimenet | Kilépési kapu |
|---|---|---|---|
| 0. Intake | programigény | module charter | `G0 INIT APPROVED` |
| 1. Forrás | charter | Source Register | `G1 SOURCES APPROVED` |
| 2. Master Script | jóváhagyott források | Master Script | `G2 CONTENT APPROVED` |
| 3. Instructional Design | Master Script | ID-specifikáció és Build Guide | `G3 DESIGN APPROVED` |
| 4. Asset Register | ID-specifikáció | Asset Register | `G4 ASSETS PLANNED` |
| 5. H5P | jóváhagyott Master Script, Build Guide és Asset Register | release candidate | `G5 BUILD ACCEPTED` |
| 6. QA | release candidate | automatikus QA-riport és kézi QA-jegyzőkönyv | `G6 QA PASSED` |
| 7. Release | QA dossier | változtathatatlan release | `G7 RELEASED` |

## 3. Fázisok részletesen

### 0. Modulintake

**Tevékenységek**

1. Egyedi `module-id` lefoglalása.
2. Célközönség, oktatási szint, nyelv és tanulási kontextus rögzítése.
3. Témakör, időhatár, földrajzi hatókör és kizárások meghatározása.
4. Tulajdonosok, review-szerepkörök és kockázatok kijelölése.

**Kimenet:** module charter.

**Blokkoló feltétel:** átfedő modulazonosító, nem tisztázott cél vagy hiányzó szakmai tulajdonos.

### 1. Forrásbevételezés és elemzés

**Tevékenységek**

1. Forrásjelöltek gyűjtése prioritási sorrendben.
2. Bibliográfiai, jogi, nyelvi és integritási metaadat rögzítése.
3. Forrásmegbízhatóság, relevancia és felhasználási korlát értékelése.
4. Állításjelöltek forrásazonosítóhoz és pontos helyhez kötése.
5. Ellentmondások, bizonytalanságok és hiányok dokumentálása.

**Kimenet:** jóváhagyott Source Register és claim map.

**Kapu:** minden tervezett lényegi állítás legalább egy elfogadható forrással rendelkezik; vitatott kérdések kezelése dokumentált.

### 2. Master Script

**Tevékenységek**

1. Oldalstruktúra és tartalmi ív megtervezése.
2. Tanulói szöveg forrásazonosítókkal történő megírása.
3. Fogalmak, időrend, térbeli kapcsolatok és nézőpontok explicit kezelése.
4. Interakciós szándék leírása konkrét H5P-implementáció nélkül.
5. Történelmi és szerkesztői review.

**Kimenet:** verziózott, `APPROVED` Master Script.

**Kapu:** nincs forrás nélküli tényállítás, rejtett bizonytalanság, pedagógiailag indokolatlan ismétlés vagy szerkesztői metaadat a tanulói szövegben.

### 3. Instructional Design

**Tevékenységek**

1. Mérhető tanulási célok véglegesítése.
2. Cél–tartalom–tevékenység–értékelés megfeleltetés.
3. Előzetes tudás, scaffolding és kognitív terhelés tervezése.
4. Interakciótípusok, visszajelzések és értékelési pontok meghatározása.
5. Mobil, accessibility és alternatív útvonal tervezése.

**Kimenet:** ID-specifikáció, oldalszintű blueprint és jóváhagyott Build Guide. A Build Guide rögzíti az oldal- és komponensszerkezetet, a konfigurációt, a lokalizációt, a buildeljárást és az elfogadási feltételeket.

**Kapu:** minden interakció tanulási célhoz kötött, nincs dekoratív vagy öncélú feladat.

### 4. Asset Register

**Tevékenységek**

1. Minden szükséges kép, térkép, ábra, hang és videó felsorolása.
2. Assetazonosító, funkció, oldal, forrás/licenc és technikai specifikáció rögzítése.
3. Alt text, felirat, transcript és mobilváltozat megtervezése.
4. Beszerzési, gyártási vagy generálási mód és jóváhagyó kijelölése.
5. Duplikáció- és jogellenőrzés.

**Kimenet:** Asset Register `PLANNED`, majd assetenként `APPROVED` állapottal; a gépi assetmanifest ennek buildszármazéka lehet.

**Kapu:** minden kötelező assetnek van jogi és accessibility-terve.

### 5. H5P implementáció

**Tevékenységek**

1. Befagyasztott Master Script, Build Guide és jóváhagyott Asset Register felhasználása.
2. Támogatott H5P-libraryk és rögzített verziók alkalmazása.
3. Teljes magyar lokalizáció és kezdeti állapotok beállítása.
4. Reszponzív és billentyűzettel használható felület kialakítása.
5. Determinisztikus build, manifest- és függőségvalidáció.

**Kimenet:** verziózott release candidate és buildlog.

**Kapu:** a csomag tisztán újraépíthető, betölthető, és a kötelező smoke tesztek sikeresek.

### 6. Többszintű QA

**Sorrend**

1. Historical QA
2. Instructional QA
3. UX QA
4. Accessibility QA
5. Technical QA
6. H5P QA
7. Regresszió és release-candidate retest

**Kimenet:** külön automatikus QA-riport és kézi QA-jegyzőkönyv, hibajegyekkel, bizonyítékokkal és aláírásokkal.

**Kapu:** nulla nyitott blokkoló vagy súlyos eltérés; az automatikus QA és minden kötelező kézi QA-dimenzió `PASS`.

### 7. Release

**Tevékenységek**

1. Verziószám és változáskategória ellenőrzése.
2. Végleges H5P, manifest, hash, dependency lock és changelog létrehozása.
3. Release notes, ismert korlátok és visszaállítási információ rögzítése.
4. Kiadási jóváhagyás és változtathatatlan archiválás.
5. GitHub Pages publikálás utáni automatikus és kézi smoke check, valamint monitorozási rekord.

**Kimenet:** `RELEASED` csomag.

**Kapu:** a publikált hash egyezik a jóváhagyott release hash-ével.

## 4. Visszalépési szabályok

- Forráshiba: vissza az 1. fázisba; Master Script és minden downstream artefaktum újraértékelendő.
- Pedagógiai hiba: vissza a 3. fázisba; H5P és kapcsolódó QA újrafuttatandó.
- Assetjogi hiba: asset karanténba, vissza a 4. fázisba; érintett build visszavonandó.
- Technikai/H5P hiba: javítás az 5. fázisban; teljes technikai és célzott regressziós QA szükséges.
- Release utáni súlyos hiba: incidens, visszavonás vagy hotfix a release-folyamat szerint.

## 5. Kötelező nyomkövetési lánc

`source-id → claim-id → master-script section → learning-objective-id → page-id/interaction-id → asset-id → build-id → qa-evidence-id → release-id`

A lánc bármely hiánya release-blokkoló eltérés.
