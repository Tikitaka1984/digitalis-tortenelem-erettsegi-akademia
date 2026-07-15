# Documentation QA Report – Géza fejedelem és I. (Szent) István

**Modulazonosító:** `geza-fejedelem-szent-istvan`  
**Dokumentációverzió:** `v0.1.0`  
**Ellenőrzés dátuma:** `2026-07-15`  
**QA-hatókör:** Source Register, Source Conflict Log, Master Script, metadata, nyitott szakmai döntések, changelog, Build Guide, Page Map, Asset Register, Visual Requirements és ez a riport  
**Végeredmény:** **PASS**

## 1. Eredmény összefoglalása

A dokumentáció teljesíti a sprint dokumentációs Definition of Done követelményeit. A 30 Master Script-oldal, a Build Guide 30 oldalspecifikációja és a Page Map 30 sora azonos oldalhalmazt és sorrendet használ. Minden tanulói feladat megoldást, magyarázó visszajelzést és gyakori hibát tartalmaz. A záróteszt 10 kérdésből, kérdésenként 2 pontból, összesen pontosan 20 pontból áll.

A tizenkét nyitott történészi és forráskezelési döntés szabályosan elkülönül a tanulói biztos állításoktól. Emiatt a dokumentációs QA eredménye PASS, de H5P-build, publikálás és Ready for review állapot nem engedélyezett a szakmai lezárásig.

## 2. Automatikus dokumentációs ellenőrzés

| Ellenőrzés | Mért eredmény | Státusz |
|---|---:|---|
| előírt Markdown-fájlok | 11/11 létezik | PASS |
| nem üres Markdown-fájlok | 11/11 | PASS |
| relatív Markdown-hivatkozások | 23, hibás: 0 | PASS |
| tiltott szerkesztői jelölők | 0 találat | PASS |
| Master Script-oldalak | 30 | PASS |
| Build Guide-oldalspecifikációk | 30 | PASS |
| Page Map-oldalsorok | 30 | PASS |
| MS–Build Guide–Page Map oldalazonosító-egyezés | 30/30 | PASS |
| forrásnyommal rendelkező tanulói oldalak | 30/30; a dokumentumszintű összesítővel 31 jelölés | PASS |
| formatív interakciók | 29 | PASS |
| záróteszt-elemek | 10 | PASS |
| megoldás/helyes válasz blokkok | 39/39 | PASS |
| magyarázó feedback blokkok | 39/39 | PASS |
| gyakori hiba blokkok | 39/39 | PASS |
| záróteszt pontmaximum | 20 | PASS |
| nyitott szakmai döntések | 12, mind `OPEN` és oldalhoz kötött | PASS |
| létrehozott H5P-csomag | 0 | PASS |

## 3. Manuális tartalmi ellenőrzés

### Historical QA

- A modulhatár 955-től az 1083-as szentté avatásig tart; a későbbi Árpád-kor nincs részletesen kibontva.
- A koronázási dátum, koronázási hely, uralkodási jelölés, Gizella házassága, Koppány rokonsága, Gyula és Ajtony dátumai, koronaeredet, püspökségi sorrend, korai vármegyék, királyi földarány és a 972/973-as eseménypár külön konfliktusrekordot kapott.
- A tanulói szöveg a stabil magot használja; vitás részlet nem szerepel kizárólagos pontozott tényként.
- A mai Szent Korona nincs István koronájaként azonosítva.
- Géza és Koppány esetében a kortárs portré hiánya dokumentált, AI-portré nem engedélyezett.

**Státusz:** a dokumentáció konfliktuskezelése PASS; a végleges történészi sign-off a Draft PR szakmai auditjának kapuja.

### Instructional QA

- A tanulási ív 30 oldalból és legalább 21 elkülöníthető tanulási fázisból áll: motiváció, előzetes tudás, probléma, kronológia, diplomácia, vallás, dinasztia, öröklés, konfliktus, legitimáció, egységesítés, összehasonlítás, egyházi rendszer, monostor, vallási gyakorlat, világi rendszer, társadalmi csoportok, erőforrások, törvény, forráskritika, utódlás, összegzés, transzfer és értékelés.
- A közép- és emelt szint elkülönül, de közös történeti gerincre épül.
- Az interakciótípusok változatosak: többválasztás, egyválasztás, igaz-hamis, párosítás/kategorizálás, sorrendezés és kérdéssor.
- A formatív feladatok nem torzítják a 20 pontos záróeredményt.

**Státusz:** PASS.

### UX és Accessibility QA

- Oldalanként rögzített a blokksorrend, magyar UI, mobilviselkedés, alternatíva, elfogadási feltétel és automatizálható ellenőrzés.
- A húzós feladatokhoz kattintásos alternatíva van előírva.
- Minden összetett vizuálhoz hosszú leírás szükséges; a szín nem kizárólagos információhordozó.
- A célérték WCAG 2.2 AA, 320 CSS px reflow és 200% zoom.

**Státusz:** dokumentációs szinten PASS; futásidejű bizonyíték a későbbi H5P-build QA-jában készül.

### Technical és H5P QA

- A Build Guide a repositoryban már használt `H5P.InteractiveBook 1.11` és kompatibilis komponensverziókhoz kötött.
- A záróteszt konfigurációja `QuestionSet 1.20`, tíz kérdés és 20 pont.
- A build-, import/export-, böngésző-, állapotmentési és GitHub Pages-próba a megvalósítási sprint kapuja, ebben a sprintben nincs H5P-csomag.

**Státusz:** a végrehajtható dokumentáció PASS; runtime QA nem része a jelen hatókörnek.

## 4. Asset- és jogi ellenőrzés

- A vizuális jelöltek hiteles Public Domain vagy Creative Commons fájlleíró oldalhoz kötöttek.
- Hotlink tiltott; tényleges bevételezéskor eredeti és származék hash, attribúció és módosításnapló kötelező.
- Történelmi térkép, portré, korona, pecsét, oklevél, törvénykönyv, rekonstrukció, címer, zászló és dokumentum nem készíthető AI-val.
- A jelen terv nem igényel AI-assetet.
- A tankönyvi térképek és ábrák nem kerülnek másolásra.

**Státusz:** PASS.

## 5. Talált és javított eltérések

1. A kötelező `OH-TOR10TA__teljes.pdf` nem tartalmazza a Géza–István-témát. A fájlt kötelező forrásként megvizsgáltuk, de csak módszertani referenciára korlátoztuk; a felhasználó által biztosított releváns `OH-TOR09TB__teljes (1).pdf` külön, teljes metaadattal került a registerbe.
2. A források koronázási helyre, házassági évre, rokonsági fokra és több intézményi adatra eltérő állításokat tartalmaznak. Ezeket nem simítottuk össze: tizenegy konfliktusrekord és tizenkét szakmai döntés védi a tanulói tartalmat a túlzott pontosságtól.
3. A vizuális igények közt szereplő portrék és történeti térképek kockázatát reprezentációs és AI-tilalmi szabályokkal kezeltük.
4. A Build Guide pontozását úgy rögzítettük, hogy 29 formatív oldal 0 könyvszintű pontot, a záróteszt pedig pontosan 20 pontot adjon.

## 6. Ismert korlátok és következő kapuk

- Tizenkét szakmai döntés nyitott; a PR Draft marad.
- A vizuális jelöltek fájljai még nincsenek letöltve vagy optimalizálva, ezért nincs assetfájl-hash és `APPROVED_FOR_BUILD` státusz.
- Nincs H5P-csomag, webes integráció, GitHub Pages-változás vagy runtime teszt; ezek szándékosan a következő sprintbe tartoznak.
- A dokumentációs QA nem helyettesíti a középkorász, egyháztörténeti, jogi és accessibility review-t.

## 7. Bizonyítékok

- [Source Register](../../../05_Source_Library/modules/geza-fejedelem-szent-istvan/SOURCE_REGISTER.md)
- [Source Conflict Log](../../../05_Source_Library/modules/geza-fejedelem-szent-istvan/SOURCE_CONFLICT_LOG.md)
- [Master Script](../../../06_Master_Scripts/geza-fejedelem-szent-istvan/MASTER_SCRIPT.md)
- [Build Guide](../../../03_H5P_Standards/modules/geza-fejedelem-szent-istvan/BUILD_GUIDE.md)
- [Asset Register](../../../08_Assets/geza-fejedelem-szent-istvan/ASSET_REGISTER.md)
- [Open Professional Decisions](../../../06_Master_Scripts/geza-fejedelem-szent-istvan/OPEN_PROFESSIONAL_DECISIONS.md)

## 8. Végső döntés

**DOCUMENTATION QA: PASS**  
**H5P BUILD AUTHORIZATION: NOT GRANTED**  
**PR STATE: DRAFT REQUIRED**  
**AUTO-MERGE: FORBIDDEN**
