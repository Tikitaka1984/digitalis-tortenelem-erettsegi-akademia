# H5P Build Guide – Géza fejedelem és I. (Szent) István

**Modulazonosító:** `geza-fejedelem-szent-istvan`  
**Dokumentumverzió:** `v0.1.0`  
**Build státusz:** dokumentáció jóváhagyása előtt nem indítható  
**Forrás:** [Master Script](../../../06_Master_Scripts/geza-fejedelem-szent-istvan/MASTER_SCRIPT.md)  
**Oldaltérkép:** [Page Map](PAGE_MAP.md)

## 1. Rögzített runtime és könyvtárak

A build a repository két működő moduljával azonos, már integrált könyvtárkészletet használja: `H5P.InteractiveBook 1.11`, `H5P.Column 1.18`, `H5P.AdvancedText 1.1`, `H5P.Image 1.1`, `H5P.Accordion 1.0`, `H5P.MultiChoice 1.16`, `H5P.SingleChoiceSet 1.11`, `H5P.TrueFalse 1.8`, `H5P.SortParagraphs 0.11`, `H5P.QuestionSet 1.20`, `H5P.DragQuestion 1.14`, `H5P.MarkTheWords 1.11` és függőségeik. Új library csak külön kompatibilitási és licenc-review után adható hozzá.

## 2. Könyvszintű konfiguráció

- A fejezetek sorrendje a `pg-001`–`pg-030` azonosítókat követi; minden `subContentId` egyedi UUID.
- Oldalanként egy `H5P.Column` a gyökér. Blokksorrend: cím → szintcímke → tanulói szöveg → jogtisztázott vizuál vagy szöveges alternatíva → interakció → visszajelzés.
- A 1–29. oldal interakciói formatívak: pontszámuk nem számít bele a könyv eredményébe; `retry=true`, `showSolution=true`, válasz nélkül nincs ellenőrzés.
- A 30. oldali `QuestionSet` adja az egyetlen összesített eredményt, `maxScore=20`, `passPercentage=60`, `retry=true`, `showSolution=true`.
- Magyar UI: `Ellenőrzés`, `Újrapróbálkozás`, `Megoldás mutatása`, `Tovább`, `Vissza`, `Befejezés`, `Eredmény`, `pont`, `helyes`, `nem helyes`. Angol kezelőszöveg nem maradhat.
- Mobil: egyoszlopos elrendezés; képek `max-width:100%`; 44×44 CSS px célterület; 320 px-nél nincs vízszintes görgetés; a húzós feladatokhoz azonos tartalmú kattintásos alternatíva kapcsolható.
- Hozzáférhetőség: logikus H2/H3 rend, billentyűzet, látható fókusz, színfüggetlen visszajelzés, képek alt szövege, összetett ábrák hosszú leírása, mozgás nélkül is teljes funkció.
- Assetek repositoryn belüli relatív úttal kerülnek a csomagba; hotlink tilos. Az [Asset Register](../../../08_Assets/geza-fejedelem-szent-istvan/ASSET_REGISTER.md) `APPROVED_FOR_BUILD` státusza nélkül vizuál nem építhető be.

## 3. Oldalankénti buildspecifikáció

Az „automatika” mező a kötelező gépi ellenőrzés rövid kódja: `ID` egyedi azonosító; `HU` magyar UI; `A11Y` billentyűzet/alt/reflow; `SCORE0` formatív pont kizárása; `SCORE20` pontos zárópont; `ASSET` fájl/licenc/hash; `ORDER` blokksorrend; `FEEDBACK` helyes, hibás és üres állapot.

### `pg-001` – Két nemzedék, egy fordulat

- **MS-hivatkozás:** `pg-001`, `int-001`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** `MarkTheWords 1.11`.
- **Blokkok:** cím; bevezető szöveg; négy elemet összekötő saját sematikus rendszerábra; hatopciós, négyhelyes MultiChoice.
- **Pontozás/feedback:** formatív 4 nyers pont, könyvbe 0; minden opcióhoz magyarázat; közös hibaüzenet a koronázás kizárólagosságáról.
- **Mobil/A11Y:** az ábra alatt teljes szöveges kapcsolatlista; opciók függőlegesek.
- **Asset:** `ast-dia-001`.
- **Elfogadás:** pontosan négy helyes opció; kezdetben nincs megoldás; retry visszaállít; 320 px reflow hibamentes.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-002` – Előzetes tudás

- **MS-hivatkozás:** `pg-002`, `int-002`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16` két egymást követő kérdésben.
- **Blokkok:** szöveg; két kategóriás, hat kártyás rendezés; összegző feedback.
- **Pontozás/feedback:** formatív 6 nyers pont, könyvbe 0; részpont; minden téves kártyához kategóriamagyarázat.
- **Mobil/A11Y:** kattintásos alternatíva kötelező; a kártyák fókuszsorrendje forrássorrend.
- **Asset:** nincs.
- **Elfogadás:** mind a hat elem egyértelmű célterületet kap; billentyűzettel az alternatíva teljesíthető.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-003` – 955-ös fordulat

- **MS-hivatkozás:** `pg-003`, `int-003`.
- **Elsődleges H5P:** `SortParagraphs 0.11`; **fallback:** `SingleChoiceSet 1.11`.
- **Blokkok:** magyarázat; négyelemű oksági sorrend; többtényezős figyelmeztetés.
- **Pontozás/feedback:** formatív, könyvbe 0; csak teljes helyes sorrend után pozitív feedback; hibánál első hibás kapcsolat magyarázata.
- **Mobil/A11Y:** mozgatógombok és sorszámos szöveg; húzás nem lehet kizárólagos.
- **Asset:** nincs.
- **Elfogadás:** sorrend pontosan az MS szerint; null-őr regresszióteszt a standalone playerben.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-004` – Géza céljai

- **MS-hivatkozás:** `pg-004`, `int-004`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** szöveg; négy cél–eszköz pár; eredményösszegzés.
- **Pontozás/feedback:** 4 nyers pont, könyvbe 0; részpont és páronkénti feedback.
- **Mobil/A11Y:** kattintásos fallback; célmezők neve programozottan elérhető.
- **Asset:** nincs.
- **Elfogadás:** nincs többértelmű pár; a „csak vallási” téves keret magyarázata megjelenik.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-005` – Quedlinburg

- **MS-hivatkozás:** `pg-005`, `int-005`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; háromopciós egyhelyes kérdés; dátumfolyamat-feedback.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; A, B és C saját magyarázatot kap.
- **Mobil/A11Y:** függőleges opciók, évszámok képernyőolvasó-barát mondatokban.
- **Asset:** nincs.
- **Elfogadás:** B az egyetlen helyes; 972 és 973 nem olvad össze.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-006` – Térítés és kíséret

- **MS-hivatkozás:** `pg-006`, `int-006`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; négyopciós kéthelyes kérdés; többmotívumú feedback.
- **Pontozás/feedback:** 2 nyers pont, könyvbe 0; téves opció kijelölése nem ad negatív pontot, de blokkolja a teljes helyességet.
- **Mobil/A11Y:** opciók tördelhetők; feedbacket aria-live udvarias mód jelzi.
- **Asset:** nincs.
- **Elfogadás:** első két opció helyes; vallás és politika nem kizárólagosként jelenik meg.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-007` – Dinasztikus kapcsolatok

- **MS-hivatkozás:** `pg-007`, `int-007`.
- **Elsődleges H5P:** `SingleChoiceSet 1.11`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** dinasztikus kapcsolatot mutató saját, nem portrés diagram; szöveg; mondatkiegészítés.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; mindhárom válasz külön feedback.
- **Mobil/A11Y:** diagram hosszú leírással; 995/996 nem jelenik meg pontozott mezőként.
- **Asset:** `ast-dia-002`.
- **Elfogadás:** csak „politikai kapcsolat és erőforrás” helyes; a diagram nem sugall biztos házassági évet.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-008` – Öröklési elvek

- **MS-hivatkozás:** `pg-008`, `int-008`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** két fogalomkártya; két definíció; feedback.
- **Pontozás/feedback:** 2 nyers pont, könyvbe 0; részpont és definíciós javítás.
- **Mobil/A11Y:** kattintásos alternatíva; a fogalmak nem csak színnel különülnek el.
- **Asset:** nincs.
- **Elfogadás:** fogalom–definíció párok pontosak; retry mindkét kártyát visszateszi.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-009` – Koppány és István

- **MS-hivatkozás:** `pg-009`, `int-009`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; ötopciós háromhelyes kérdés; anakronizmus-feedback.
- **Pontozás/feedback:** 3 nyers pont, könyvbe 0; teljes helyességhez a két téves opció jelöletlen.
- **Mobil/A11Y:** nincs Koppány-portré; konfliktusdiagram csak szöveges címkékkel.
- **Asset:** `ast-dia-003`.
- **Elfogadás:** „nagybácsi” nem szerepel helyes vagy sugallt tényként; három tényező helyes.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-010` – Koronázás

- **MS-hivatkozás:** `pg-010`, `int-010`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16` három csoportkérdéssel.
- **Blokkok:** szöveg; 1031-es palástrészlet; biztos/eltérő/nem elfogadható kategorizálás; feedback.
- **Pontozás/feedback:** 5 nyers pont, könyvbe 0; a mai korona azonossága „nem elfogadható”.
- **Mobil/A11Y:** kép alt szöveg és hosszú tárgyleírás; kattintásos fallback.
- **Asset:** `ast-img-001`.
- **Elfogadás:** kettős dátum megmarad; helyszín nem pontozott; képaláírás közli: 1031-es palást, történeti reprezentáció.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-011` – Gyula és Ajtony

- **MS-hivatkozás:** `pg-011`, `int-011`.
- **Elsődleges H5P:** `SortParagraphs 0.11`; **fallback:** `SingleChoiceSet 1.11`.
- **Blokkok:** szöveg; négylépéses folyamat; dátumbizonytalansági megjegyzés.
- **Pontozás/feedback:** formatív, könyvbe 0; hibánál „győzelem nem azonos intézménnyel” magyarázat.
- **Mobil/A11Y:** gombos sorrendezés; Ajtony pontos éve nem kérdés.
- **Asset:** `ast-map-001` csak szakmai jóváhagyás után.
- **Elfogadás:** Erdély és Maros vidéke szöveges alternatívában is megjelenik; vitatott év nincs pontozva.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-012` – Géza és István

- **MS-hivatkozás:** `pg-012`, `int-012`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** összehasonlító szöveg; hárommezős Venn-elrendezés; öt kártya.
- **Pontozás/feedback:** 5 nyers pont, könyvbe 0; páronkénti indoklás.
- **Mobil/A11Y:** Venn-ábra helyett mobilon három címkézett lista; kattintásos alternatíva.
- **Asset:** `ast-dia-004`.
- **Elfogadás:** nyugati kapcsolat, térítés és dinasztikus politika közös; koronázott rang és vármegye István.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-013` – Latin kereszténység

- **MS-hivatkozás:** `pg-013`, `int-013`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; háromopciós magyarázatválasztás; térségi sematikus diagram.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; mindhárom opció indokolt.
- **Mobil/A11Y:** diagram hosszú leírása felsorolja a kapcsolatokat, nem állít éles civilizációs határt.
- **Asset:** `ast-dia-005`.
- **Elfogadás:** B az egyetlen helyes; „minden bizánci kapcsolat megszűnt” elutasítva.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-014` – Egyházi hierarchia

- **MS-hivatkozás:** `pg-014`, `int-014`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** háromszintű saját hierarchiaábra; szöveg; három párosítás.
- **Pontozás/feedback:** 3 nyers pont, könyvbe 0; részpont.
- **Mobil/A11Y:** kattintásos alternatíva; faábra szöveges listával.
- **Asset:** `ast-dia-006`.
- **Elfogadás:** teljes püspökségi lista/sorrend nincs; Esztergom és Kalocsa érseki központként szerepel.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-015` – Pannonhalma

- **MS-hivatkozás:** `pg-015`, `int-015`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** Pannonhalma CC-fotó; oklevél PD-részlet; szöveg; hatopciós négyhelyes kérdés.
- **Pontozás/feedback:** 4 nyers pont, könyvbe 0; modern parlament és kizárólagos erőd külön feedback.
- **Mobil/A11Y:** két kép nem lehet egymás mellett 600 px alatt; külön alt és forrásmegjelölés.
- **Asset:** `ast-img-002`, `ast-doc-001`.
- **Elfogadás:** licencek, attribúciók és hashek az assetregisterben; dokumentum forrásjellegként, nem díszként jelenik meg.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-016` – Tized és templom

- **MS-hivatkozás:** `pg-016`, `int-016`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; háromopciós norma–valóság kérdés; feedback.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; minden opció magyarázata.
- **Mobil/A11Y:** egyszerű szöveges komponens; `tized` fogalommagyarázata közvetlenül előtte.
- **Asset:** nincs.
- **Elfogadás:** B az egyetlen helyes; a törvény nem bizonyít teljes végrehajtást.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-017` – Világi szervezet

- **MS-hivatkozás:** `pg-017`, `int-017`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** rendszerábra; szöveg; négy kapcsolat párosítása.
- **Pontozás/feedback:** 4 nyers pont, könyvbe 0; részpont.
- **Mobil/A11Y:** kattintásos alternatíva és hosszú ábraleírás.
- **Asset:** `ast-dia-007`.
- **Elfogadás:** király, tanács, ispán és vár feladata egyértelmű; nincs modern minisztériumi analógia.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-018` – Vármegye és várispánság

- **MS-hivatkozás:** `pg-018`, `int-018`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** fogalmi összevetés; háromopciós kérdés; bizonytalansági kártya.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; A–C opció saját feedback.
- **Mobil/A11Y:** táblázat helyett mobilon címkézett blokkok.
- **Asset:** nincs.
- **Elfogadás:** B helyes; első megye és megyeszám nincs pontozva.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-019` – Várjobbágyok és várnépek

- **MS-hivatkozás:** `pg-019`, `int-019`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** szöveg; három fogalom–szerep pár; jelentésváltozási figyelmeztetés.
- **Pontozás/feedback:** 3 nyers pont, könyvbe 0; részpont.
- **Mobil/A11Y:** kattintásos alternatíva.
- **Asset:** nincs.
- **Elfogadás:** várjobbágy nem „későbbi jobbágy”; minden fogalomhoz pontos szerep.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-020` – Tanács és nádor

- **MS-hivatkozás:** `pg-020`, `int-020`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; háromopciós anakronizmus-kérdés; korszakolási feedback.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0.
- **Mobil/A11Y:** függőleges opciók; az „anakronizmus” fogalma kifejtve.
- **Asset:** nincs.
- **Elfogadás:** C helyes; későbbi nádori jogkör nincs visszavetítve.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-021` – Földbirtok

- **MS-hivatkozás:** `pg-021`, `int-021`.
- **Elsődleges H5P:** `SortParagraphs 0.11`; **fallback:** `SingleChoiceSet 1.11`.
- **Blokkok:** szöveg; négylépéses oksági lánc; aránybizonytalanság.
- **Pontozás/feedback:** formatív, könyvbe 0; pontos százalék nem része a válasznak.
- **Mobil/A11Y:** gombos rendezés; lánc sima listaként is olvasható.
- **Asset:** `ast-dia-008`.
- **Elfogadás:** „nagyobb rész” szerepel; kétharmad/háromnegyed nem pontozott.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-022` – Bevételek és írásbeliség

- **MS-hivatkozás:** `pg-022`, `int-022`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** monogram PD-kép; szöveg; hat kártya két kategóriába.
- **Pontozás/feedback:** 6 nyers pont, könyvbe 0; részpont.
- **Mobil/A11Y:** kattintásos alternatíva; monogram alt leírja a funkciót, nem olvas ki betűt bizonytalanul.
- **Asset:** `ast-doc-002`.
- **Elfogadás:** vám/bírság/pénzverés és oklevél/monogram/pecsét kategóriák hibamentesek.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-023` – Törvények: keresztény rend

- **MS-hivatkozás:** `pg-023`, `int-023`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** négy rendelkezéskártya; szöveg; háromopciós közös-cél kérdés.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0.
- **Mobil/A11Y:** kártyák olvasási sorrendje fix; nincs dekoratív kéziratkép jogtisztázás nélkül.
- **Asset:** nincs.
- **Elfogadás:** keresztény intézmény és gyakorlat az egyetlen helyes cél.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-024` – Törvények: tulajdon és béke

- **MS-hivatkozás:** `pg-024`, `int-024`.
- **Elsődleges H5P:** `TrueFalse 1.8`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** szöveg; egy igaz-hamis állítás; magyarázó feedback.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0; helytelen válasznál központi bíráskodás magyarázata.
- **Mobil/A11Y:** igaz/hamis mellett teljes állítás; állapot nem csak szín.
- **Asset:** nincs.
- **Elfogadás:** „igaz” a helyes; modern jogegyenlőség nem következik belőle.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-025` – Törvény mint forrás

- **MS-hivatkozás:** `pg-025`, `int-025`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16`.
- **Blokkok:** saját megfogalmazású forráskivonat; négy állítás két bizonyíthatósági kategóriába; feedback.
- **Pontozás/feedback:** 4 nyers pont, könyvbe 0; részpont és forrásműfaji magyarázat.
- **Mobil/A11Y:** kattintásos alternatíva; a kivonat nem idézőjelben és nem szó szerinti forrásként jelenik meg.
- **Asset:** nincs.
- **Elfogadás:** első két állítás támogatott, utolsó kettő nem; nincs hosszú jogvédett idézet.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-026` – Imre és az Intelmek

- **MS-hivatkozás:** `pg-026`, `int-026`.
- **Elsődleges H5P:** `MultiChoice 1.16`; **fallback:** nincs.
- **Blokkok:** szöveg; háromopciós műfajkérdés; ideális norma–gyakorlat feedback.
- **Pontozás/feedback:** 1 nyers pont, könyvbe 0.
- **Mobil/A11Y:** dőlt cím programozottan is érthető; opciók függőlegesek.
- **Asset:** nincs; kézirat csak későbbi asset-review után.
- **Elfogadás:** B helyes; modern alkotmány és hadinapló elutasítva.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-027` – Utódlás és kultusz

- **MS-hivatkozás:** `pg-027`, `int-027`.
- **Elsődleges H5P:** `SortParagraphs 0.11`; **fallback:** `SingleChoiceSet 1.11`.
- **Blokkok:** szöveg; három dátumozott esemény rendezése; szarkofágkép.
- **Pontozás/feedback:** formatív, könyvbe 0; eseményenkénti javítás.
- **Mobil/A11Y:** gombos rendezés; kép alt és mai őrzési kontextus.
- **Asset:** `ast-img-003`.
- **Elfogadás:** 1031–1038–1083 sorrend; kultusz és koronázás nem mosódik össze.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-028` – Idő és tér

- **MS-hivatkozás:** `pg-028`, `int-028`.
- **Elsődleges H5P:** `DragQuestion 1.14`; **fallback:** `MultiChoice 1.16` két blokkban.
- **Blokkok:** saját idővonal; saját topográfiai sematikus térkép; öt idő- és négy térpár.
- **Pontozás/feedback:** 9 nyers pont, könyvbe 0; részpont.
- **Mobil/A11Y:** teljes szöveges idővonal és helylista; kattintásos alternatíva.
- **Asset:** `ast-dia-009`, `ast-map-002`.
- **Elfogadás:** csak stabil év–esemény és személy–térség párok; koronázási hely nincs.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK ASSET`.

### `pg-029` – Érettségi műhely

- **MS-hivatkozás:** `pg-029`, `int-029`.
- **Elsődleges H5P:** `SortParagraphs 0.11`; **fallback:** `SingleChoiceSet 1.11`.
- **Blokkok:** feleletminta; hat blokk rendezése; emelt szintű érvelési kártya.
- **Pontozás/feedback:** formatív, könyvbe 0; tematikus felcserélés miatt a rendszer egy kanonikus sorrendet értékel, a feedback közli az elfogadható változatokat.
- **Mobil/A11Y:** gombos rendezés; hosszú címkék tördelhetők.
- **Asset:** nincs.
- **Elfogadás:** mind a hat blokk szerepel; bizonytalan adat nem lesz feleletfőpont.
- **Automatika:** `ID HU A11Y SCORE0 ORDER FEEDBACK`.

### `pg-030` – Záróteszt

- **MS-hivatkozás:** `pg-030`, `test-01`–`test-10`.
- **Elsődleges H5P:** `QuestionSet 1.20` tíz `MultiChoice 1.16` kérdéssel; **fallback:** nincs.
- **Blokkok:** instrukció; 10 kérdés rögzített sorrendben; eredményoldal; sávos fejlesztő feedback.
- **Pontozás/feedback:** minden kérdés pontosan 2 pont; részpont a két helyes elemű kérdéseknél; `maxScore=20`; `passPercentage=60`; kérdésenkénti és összesített feedback az MS szerint.
- **Mobil/A11Y:** egy kérdés/képernyő; előre-hátra navigáció; fókusz az új kérdés címére; eredmény szövegben is közölt.
- **Asset:** nincs.
- **Elfogadás:** automatikusan igazolt 10 kérdés és 20 pont; nincs negatív pont; a vitatott dátumok/helyek nem helyes válaszok; reset/retry és mentett állapot helyes.
- **Automatika:** `ID HU A11Y SCORE20 ORDER FEEDBACK`.

## 4. Build- és QA-parancssor

1. Generáláskor validálni kell a 30 oldalt, az egyedi `subContentId` értékeket és a dependency listát.
2. Statikus audit ellenőrzi a magyar UI-szövegeket, a 20 pontos zárótesztet, a relatív assetutakat és a tiltott külső hivatkozásokat.
3. Helyi standalone player smoke fut 1440×900, 1280×720, 390×844 és 320 px reflow nézetben.
4. Billentyűzetes próba lefedi minden húzós feladat alternatíváját és a teljes zárótesztet.
5. H5P import/export próba után a forráscsomag és a publikált artifact SHA-256 értéke a QA-riportba kerül.
6. GitHub Pages integráció csak sikeres automatikus és kézi QA, jóváhagyott assetek és lezárt szakmai döntések után indulhat.

## 5. Manuális elfogadási kapu

- történész reviewer lezárta az [Open Professional Decisions](../../../06_Master_Scripts/geza-fejedelem-szent-istvan/OPEN_PROFESSIONAL_DECISIONS.md) tételeit;
- instructional reviewer jóváhagyta a 30 oldalas ívet és a 20 pontos tesztet;
- accessibility reviewer ellenőrizte a húzós feladatok alternatíváit;
- jogi/asset reviewer minden beépülő vizuált `APPROVED_FOR_BUILD` státuszra állított;
- a dokumentációs PR merge-elve van; automatikus merge továbbra sem használható.

