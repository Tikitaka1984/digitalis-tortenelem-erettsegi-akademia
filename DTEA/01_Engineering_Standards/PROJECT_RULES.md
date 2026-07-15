# DTEA kötelező projektszabályok

**Szabványazonosító:** `DTEA-GOV-RULES`

**Érvényesség:** eltérés csak dokumentált, időkorlátos kivétellel lehetséges

## 0. Hivatalos fejlesztési módszer és kötelező artefaktumok

1. A DTEA hivatalos fejlesztési módszere: `Work + automatikus QA + GitHub Pages`.
2. A `Work` az egyetlen hivatalos szerzői és build-munkatér; a GitHub Pages az ellenőrzött tanulói felület publikációs célkörnyezete.
3. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési eszköz. Nem lehet forrás-of-truth, hivatalos build-, QA-, release- vagy publikációs környezet.
4. Minden új modul kötelező artefaktuma: Source Register, Master Script, Build Guide, Asset Register, automatikus QA-riport és kézi QA-jegyzőkönyv.
5. Bármely kötelező artefaktum hiánya release-blokkoló eltérés.

## 1. Történelmi hitelesség

1. Minden történelmi tényállításnak állításazonosítóval és jóváhagyott forráshivatkozással kell rendelkeznie.
2. Elsődleges és másodlagos forrást egyértelműen meg kell különböztetni.
3. Vitatott értelmezést nem szabad bizonyított tényként megjeleníteni.
4. Idő-, hely-, személy- és fogalomhasználatnak a forrásokkal és a projektszótárral konzisztensnek kell lennie.
5. Anakronizmus, hamis okság és indokolatlan leegyszerűsítés release-blokkoló hiba.

## 2. Forráshasználat és visszakövethetőség

1. Ismeretlen eredetű vagy nem ellenőrizhető anyag nem használható.
2. Minden forráshoz bibliográfiai, jogi, integritási és bevételezési metaadat szükséges.
3. Webes forrásnál hozzáférési dátum és tartós hivatkozás vagy archivált rekord szükséges.
4. Kép, hang és videó csak dokumentált licenccel vagy bizonyítható saját előállítással használható.
5. A teljes provenance láncot release-ig fenn kell tartani.
6. Történelmi térkép, valós történelmi személy portréja és történelmi dokumentum kizárólag hiteles őrzőhelyről vagy azonosítható alkotótól származó Public Domain vagy Creative Commons forrásként használható, pontos forrás-, jogosultság- és licencadattal.

## 3. Hallucinációtilalom és AI-használat

1. AI-kimenet nem forrás és nem szakmai jóváhagyás.
2. Generált állítás csak független forrásellenőrzés után kerülhet munkadokumentumba.
3. Nem létező idézet, személy, esemény, mű, URL vagy bibliográfiai adat súlyos hiba.
4. Bizonytalanság esetén a rendszernek meg kell állnia és ellenőrzést kell kérnie; tilos valószínűnek tűnő adattal kitölteni a hiányt.
5. AI-generált kép kizárólag borítóként, hangulatképként vagy dekoratív illusztrációként használható; eredetét, promptkategóriáját, előállítási módját és emberi review-ját dokumentálni kell.
6. AI-generált kép nem használható történelmi térképként, valós történelmi személy portréjaként, történelmi dokumentumként, forrásrekonstrukcióként vagy bizonyító erejű vizuálként.

## 4. Tartalmi és pedagógiai minőség

1. Minden oldal és interakció legalább egy mérhető tanulási célhoz kapcsolódik.
2. A tanulói szöveg elkülönül a szerkesztői, fejlesztői és QA-metaadatoktól.
3. Interakció nem használható pusztán változatosság kedvéért.
4. A visszajelzés magyaráz, nem csak minősít.
5. A helyes válasz és a megoldás kezdeti állapotban nem látható, kivéve dokumentált pedagógiai indokkal.
6. A nyelvezet pontos, életkornak megfelelő és diszkriminációmentes.
7. Az erőszakos, traumatikus vagy érzékeny tartalmak kezelése arányos és kontextualizált.

## 5. H5P-kompatibilitás

1. Csak a támogatott és rögzített H5P-library verziók használhatók.
2. A csomagnak érvényes manifestet, teljes függőségi készletet és egyedi komponensazonosítókat kell tartalmaznia.
3. A build reprodukálható; kézi változtatás a generált csomagban tilos.
4. Minden felirat és vezérlő a célközönség nyelvén jelenik meg.
5. A komponensek kezdeti, megoldott, hibás, újrapróbálkozási és visszaállított állapotát tesztelni kell.
6. Nem támogatott egyedi script vagy távoli futásidejű függőség csak architekturális jóváhagyással használható.

## 6. UX-szabvány

1. A navigáció, a progress, a feladatvezérlők és a visszajelzés modulok között következetes.
2. A tanuló mindig érti, hol tart, mit kell tennie és mi történt a művelete után.
3. Mobilon nincs vízszintes túlcsordulás vagy csak hoverrel elérhető funkció.
4. A tartalom nem támaszkodhat kizárólag színre, hangra vagy vizuális pozícióra.
5. A kognitív terhelést felesleges ismétlés, túl hosszú oldalak és zsúfolt interakciók nem növelhetik.
6. Destruktív vagy állapotvesztő művelethez egyértelmű figyelmeztetés szükséges.

## 7. Accessibility

1. Cél: WCAG 2.2 AA, a használt platform lehetőségein belül.
2. Minden információhordozó képhez érdemi alt text, dekoratív képhez üres alternatíva szükséges.
3. Videóhoz felirat, hanghoz transcript, összetett vizuálhoz szöveges alternatíva szükséges.
4. A teljes kritikus út billentyűzettel használható.
5. Fókuszjelzés látható, logikus és nem takart.
6. Címsorhierarchia, címkék, állapotüzenetek és olvasási sorrend szemantikailag helyes.
7. Kontraszt, nagyítás, reflow és képernyőolvasó-viselkedés kötelező QA-terület.

## 8. Adatvédelem és biztonság

1. Személyes adat, tanulói válasz vagy analitika csak dokumentált jogalappal és adatminimalizálással kezelhető.
2. Titok, token, jelszó vagy személyes adat repositoryba nem commitolható.
3. Harmadik féltől származó függőség verziója rögzített és licencelt.
4. Külső link és beágyazás biztonsági, adatvédelmi és tartóssági ellenőrzést igényel.
5. Buildlog és képernyőkép nem tartalmazhat érzékeny adatot.

## 9. Repository- és változáskezelés

1. Közvetlen `main` push tilos.
2. Minden változás külön branchen és pull requesten készül.
3. A PR leírja a hatókört, kockázatot, QA-t és érintett modulokat.
4. A munkapéldány, cache, lokális build és titok gitignore-olt.
5. Generált output csak akkor verziózható, ha az audit vagy a kiadási folyamat kifejezetten megköveteli.
6. Meglévő release utólag nem írható felül.
7. Az automatikus merge minden változásnál tilos; merge kizárólag sikeres automatikus QA és dokumentált emberi review után, kézi művelettel történhet.

## 10. QA és release

1. Saját manuális kipróbálás nem helyettesíti a dokumentált QA-t.
2. `PASS` csak konkrét vizsgált verzióhoz és bizonyítékhoz rendelhető.
3. Nyitott blokkoló vagy súlyos hiba mellett release nem készülhet.
4. A historical, instructional, UX, accessibility, technical és H5P QA egyaránt kötelező.
5. A release hash-ének egyeznie kell a jóváhagyott és publikált csomaggal.
6. Minden kiadáshoz rollback vagy visszavonási eljárás tartozik.

## 11. Tiltott gyakorlatok

- forrás nélküli tény kitöltése „józan ész” alapján;
- szerkesztői megjegyzés megjelenítése a tanulói felületen;
- licenc nélküli kép vagy videó ideiglenes használata kiadásban;
- accessibility későbbi feladatként való elhalasztása;
- H5P-csomag közvetlen kézi javítása a forrásprojekt módosítása nélkül;
- QA-eredmény más buildre történő újrafelhasználása;
- release-fájl felülírása változatlan verziószámmal;
- automatikus merge bármely branchen vagy pull requesten.

## 12. Kivételkezelés

Kivétel csak írásban, az alábbi mezőkkel engedélyezhető:

- érintett szabály;
- üzleti vagy technikai indok;
- kockázat és érintett modulok;
- kompenzáló kontroll;
- felelős és jóváhagyó;
- lejárati dátum;
- megszüntetési vagy migrációs terv.

Lejárt kivétel automatikusan blokkolja a következő release-t.
