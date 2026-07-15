# Új DTEA-modul teljes folyamata

Ez a dokumentum az operatív ellenőrzőlista minden új tananyagmodulhoz. Nem helyettesíti a részletes szabványokat.

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési célra használható.

## Kötelező modul-artefaktumok

- [ ] Source Register elkészült és jóváhagyott.
- [ ] Master Script elkészült és jóváhagyott.
- [ ] Build Guide elkészült és jóváhagyott.
- [ ] Asset Register elkészült és jóváhagyott.
- [ ] Automatikus QA eredménye dokumentált és `PASS`.
- [ ] Kézi QA jegyzőkönyve dokumentált és `PASS`.

## 1. Források

### Feladatok

- [ ] Modulazonosító és module charter létrehozva.
- [ ] Forrásjelöltek összegyűjtve.
- [ ] Bibliográfiai és jogi metaadatok rögzítve.
- [ ] Fájlhash és eredeti hely rögzítve.
- [ ] Forrásminőség és relevancia értékelve.
- [ ] Állítás–forrás térkép elkészítve.
- [ ] Ellentmondások és bizonytalanságok dokumentálva.
- [ ] Source Register elkészítve.

### Kilépési feltétel

Historical Lead jóváhagyás: `G1 SOURCES APPROVED`.

## 2. Elemzés

### Feladatok

- [ ] A modul hatóköre és kizárásai források alapján finomítva.
- [ ] Kötelező fogalmak, személyek, helyek, időpontok és folyamatok azonosítva.
- [ ] Nézőpontok és történeti viták elkülönítve.
- [ ] Előzetes tudás és tipikus tévképzetek listázva.
- [ ] Minden elemzés állításazonosítóval visszakövethető.

### Kilépési feltétel

Az elemzés teljes, belsőleg konzisztens és forrásolt; nyitott kérdéshez tulajdonos és döntési határidő tartozik.

## 3. Master Script

### Feladatok

- [ ] Oldalszám és narratív ív meghatározva.
- [ ] Tanulói szöveg elkészült.
- [ ] Minden tényállítás forrásazonosítóval ellátva.
- [ ] Fogalomhasználat, időrend és tulajdonnevek konzisztenciája ellenőrizve.
- [ ] Interakciós szándék és visszajelzési cél leírva.
- [ ] Szerkesztői instrukció elkülönül a tanulói szövegtől.
- [ ] Historical és editorial review lezárva.

### Kilépési feltétel

`G2 CONTENT APPROVED`; rögzített Master Script verzió.

## 4. Build Guide és Asset Register

### Feladatok

- [ ] A Build Guide rögzíti az oldal- és komponensszerkezetet, a H5P-verziókat, a lokalizációt és a buildeljárást.
- [ ] A Build Guide minden interakcióhoz meghatározza a konfigurációt és az elfogadási feltételeket.
- [ ] Oldalankénti assetigény rögzítve.
- [ ] Minden asset egyedi `asset-id`-t kapott.
- [ ] Forrás, licenc és felhasználási mód tisztázva.
- [ ] Méret, formátum, képarány és fájlméretcél meghatározva.
- [ ] Alt text, caption és szükség esetén transcript megtervezve.
- [ ] Mobil és nagyított megjelenés ellenőrzési terve elkészült.
- [ ] Asset státuszok és felelősök rögzítve.
- [ ] Az Asset Register elkészítve és jóváhagyva.

### Kilépési feltétel

`G4 ASSETS PLANNED`; a Build Guide jóváhagyott, és implementációhoz minden kötelező asset `APPROVED` az Asset Registerben.

## 5. Interactive Book

### Feladatok

- [ ] Támogatott Interactive Book és komponensverziók használata.
- [ ] Oldalazonosítók a Master Scripthez kötve.
- [ ] Magyar UI-feliratok teljes körűek.
- [ ] Helyes válasz és feedback csak tanulói művelet után jelenik meg.
- [ ] Navigáció, progress és mentési viselkedés dokumentált.
- [ ] Billentyűzet, képernyőolvasó és mobil viselkedés megvalósítva.
- [ ] Determinisztikus build és csomagvalidáció sikeres.

### Kilépési feltétel

`G5 BUILD ACCEPTED`; release candidate azonosító és hash rögzítve.

## 6. QA

### Feladatok

- [ ] Historical QA: `PASS`.
- [ ] Instructional QA: `PASS`.
- [ ] UX QA: `PASS`.
- [ ] Accessibility QA: `PASS`.
- [ ] Technical QA: `PASS`.
- [ ] H5P QA: `PASS`.
- [ ] Desktop és mobil vizuális bizonyítékok csatolva.
- [ ] Automatikus build-, audit- és regressziós tesztek sikeresek.
- [ ] A kötelező kézi Historical, Instructional, UX-, Accessibility-, Technical és H5P QA jegyzőkönyve elkészült.
- [ ] Nincs nyitott blokkoló vagy súlyos hiba.

### Kilépési feltétel

`G6 QA PASSED`; QA dossier lezárva.

## 7. Release

### Feladatok

- [ ] Szemantikus verziószám jóváhagyva.
- [ ] Release H5P és manifest létrehozva.
- [ ] SHA-256, dependency lock és buildazonosító rögzítve.
- [ ] Changelog és release notes elkészült.
- [ ] Jóváhagyók, dátum és ismert korlátok rögzítve.
- [ ] Archiválás és visszaállítás tesztelve.
- [ ] Publikálás utáni smoke check sikeres.
- [ ] A GitHub Pages publikáció sikeres és a publikált commit azonosítható.

### Kilépési feltétel

`G7 RELEASED`; a csomag változtathatatlan és visszakereshető.

## Kötelező megállási pontok

A folyamatot meg kell állítani, ha:

- forrás vagy jogi státusz nem tisztázott;
- történelmi állítás nem visszakövethető;
- tanulási cél és interakció nincs összhangban;
- hozzáférhetőségi alternatíva hiányzik;
- a H5P-csomag nem reprodukálható;
- bármely kötelező QA-dimenzió sikertelen;
- a release hash nem egyezik a jóváhagyott artefaktummal.
