# Sprint 4 – Földrajzi felfedezések H5P Interactive Book

## Eredmény

- Kimenet: `content/digitalis-tortenelem-erettsegi-akademia-foldrajzi-felfedezesek-v1.0.h5p`
- Formátum: H5P Interactive Book 1.11
- Oldalszám: 30
- SHA-256: `9848f986c28056466413aadc7def694c4a631adf987a0e5a438e6a93d554c564`
- Forrás: Master Script v1.0.2, Source Register v1.0.2 és Build Guide váz v1.0.2
- Az Athéni demokrácia csomag tartalma nem módosult.
- A Földrajzi felfedezések csomagot a CI reprodukálhatóan előállítja, majd 30 napos letölthető workflow artifactként is feltölti.

## H5P-komponensek

| Típus | Darab |
|---|---:|
| Interactive Book | 1 |
| Column | 30 |
| Advanced Text | 129 |
| Accordion | 13 |
| Multiple Choice | 28 |
| Question Set | 4 |
| Drag and Drop | 4 |
| Dialog Cards | 3 |
| Essay | 6 |
| Fill in the Blanks | 1 |
| Sort the Paragraphs | 1 |
| True/False | 1 |

A záróteszt 12 komponensből áll; a statikusan ellenőrzött maximumpontszám pontosan 20.

## Webes integráció

- A kezdőlap két külön tananyagkártyát jelenít meg.
- A könyvtárban mindkét kész modul kereshető és szűrhető.
- Az egységes `learn.html` a `module` paraméter alapján tölti be a megfelelő könyvet.
- A paraméter nélküli `learn.html` továbbra is az Athéni demokráciát nyitja meg, így a korábbi hivatkozások nem törnek el.
- A build előbb létrehozza a második `.h5p` csomagot, majd mindkét forrást külön SHA-256 értékkel ellenőrzi és külön célkönyvtárba bontja ki.

## Engedélyezett technikai alternatívák

A Build Guide v1.0.2 saját státusza szerint váz, nem mezőszintű végrehajtási specifikáció. Emiatt kizárólag a benne felsorolt típusok és engedélyezett alternatívák kerültek használatba:

- Image Hotspots → számozott/lineáris szöveg + Accordion;
- Timeline → lineáris kronológia + Accordion;
- Summary → hét kulcsállítást tartalmazó Accordion;
- médiahiány → egységes, jól látható placeholder;
- mobilon kockázatos párosítások → billentyűzettel is kezelhető Drag and Drop vagy szöveges alternatíva.

A 20 pontos záróteszt súlyozásának megőrzéséhez a Z4, Z9 és Z11 kétpontos elemei két célmezős Drag and Drop mezőleképezést kaptak. A történelmi állítások, a helyes megoldások és a pontértékek nem változtak. A Z9 három fogalma két vizuális csoportban jelenik meg; ez technikai mezőleképezés, amelyet pilotban manuálisan is ellenőrizni kell.

## Placeholder-ek

Nyolc egységes placeholder maradt a csomagban a végleges, jogtiszta vizuális assetek helyén:

1. borító/hero;
2. hajózási eszközök;
3. Dias útvonala;
4. Vasco da Gama útvonala;
5. Kolumbusz útvonala;
6. Tordesillas térképe;
7. Magellán útvonala;
8. összesített térkép/topográfia.

## Teszteredmények

### Sikeres

- H5P ZIP-integritás;
- pontosan 30, Master Scripttel egyező sorrendű oldalcím;
- 220 egyedi `subContentId`;
- minden deklarált H5P library jelen van;
- 20 pontos záróteszt statikus pontellenőrzése;
- kétmodulos statikus Pages build;
- 60 oldalas build-verifikáció;
- kezdőlap: két elérhető modul;
- könyvtár: két aktív tananyagkártya;
- asztali és 390 × 844 mobil platformnézet: nincs vízszintes túlcsordulás.

### CI-ben ellenőrizendő

A helyi workspace `h5p-standalone` és Playwright csomagjai szerkezeti teszt-placeholder-ek; a valódi csomagokat a GitHub Actions telepíti. Emiatt a teljes H5P iframe, Retry, Show Solution, pontozási esemény és oldalankénti navigáció végső böngészős regressziója a PR CI-ben futtatandó. A helyi H5P-betöltési hiba ebből a placeholder runtime-ból ered, nem a két forráscsomagból.

## Képernyőképek

- `docs/screenshots/sprint-4/homepage-two-modules-desktop.png`
- `docs/screenshots/sprint-4/homepage-two-modules-mobile.png`
- `docs/screenshots/sprint-4/library-two-modules-desktop.png`

## Ismert korlátok

- A statikus GitHub Pages nem tárol tanulói eredményt központilag.
- Nyolc végleges vizuális asset még hiányzik.
- A Build Guide v1.0.2 mezőszintű specifikáció helyett jóváhagyott váz; a pontos mezőleképezést ez a sprint reprodukálható buildscriptben rögzíti.
- A Z9 részpontozásának két vizuális csoportos megoldását a pilot során külön ellenőrizni kell.
- Publikálási ellenőrzés csak a PR elfogadása és későbbi merge után végezhető; ez a sprint nem merge-el automatikusan.

## Publikálási ellenőrzőlista

- [x] Két H5P forrás külön ellenőrzőösszeggel
- [x] Reprodukálható H5P-generálás és letölthető CI artifact
- [x] Két külön runtime-célkönyvtár
- [x] Két kezdőoldali/könyvtári kártya
- [x] Visszafelé kompatibilis Athéni URL
- [x] Reszponzív platformréteg
- [ ] PR CI: teljes Playwright mátrix
- [ ] PR CI: Lighthouse küszöbök
- [ ] Manuális Lumi-import
- [ ] Manuális végigjárás: mind a 30 oldal
- [ ] Merge utáni GitHub Pages smoke teszt
