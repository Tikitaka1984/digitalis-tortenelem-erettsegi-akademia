# DTEA Design System v1.0

Állapot: elfogadásra javasolt  
Platformverzió: 1.1.0  
Hatókör: a Digitális Történelem Érettségi Akadémia webes kerete és minden publikált H5P-modul.

## 1. Alapelvek

- A felület a tanulási feladatot segíti; nem versenyez a tartalommal.
- A történelmi tartalom, a fejlesztői specifikáció és a technikai konfiguráció külön réteg.
- A modulok közös taxonómiát, kártyaszerkezetet, borítóarányt és felületi nyelvet használnak.
- A CI-zöld állapot mellett kötelező a tanulói felület vizuális ellenőrzése is.
- Alapkövetelmény a reszponzív, billentyűzettel kezelhető és WCAG 2.2 AA célú működés.

## 2. Színpaletta

| Szerep | Világos mód | Sötét mód | Használat |
|---|---:|---:|---|
| Primer | `#264F3D` | `#B7D9C5` | fő CTA, aktív állapot |
| Primer hover | `#1D3F31` | `#D6ECDF` | interakció |
| Szekunder felület | `#F0EEE7` | `#121914` | szekcióháttér |
| Accent | `#D5FF65` | `#C9F45F` | fókuszált kiemelés |
| Success | `#287A52` | `#75C99A` | sikeres állapot |
| Warning | `#D89058` | `#EFA66E` | figyelmeztetés |
| Error | `#B42318` | `#FF8A80` | hiba |
| Fókusz | `#4169E1` | `#8EACFF` | billentyűzetfókusz |

A szín nem lehet az egyetlen állapotjelző. Szöveg, ikon vagy forma egészítse ki.

## 3. Tipográfia

- Címsor: Manrope, tartalék `Segoe UI`, system-ui.
- Törzsszöveg: DM Sans, tartalék `Segoe UI`, system-ui.
- `h1`: reszponzív 2.7–5.7 rem, maximum 14–16 szavas cím.
- `h2`: 2–3.7 rem; önálló szekciót vezet be.
- `h3`: 1.25–1.4 rem; kártya vagy részfeladat címe.
- Törzsszöveg: legalább 1 rem, 1.5–1.75 sormagasság, legfeljebb 70 karakteres sor.
- Idézet: bal oldali vizuális jel, forrásmegjelöléssel.
- Kiemelés: félkövér vagy accent-háttér; teljes bekezdés nagybetűs írása tilos.

## 4. Kártyák

### Kezdőlap

- Kiemelt modulonként egyetlen fő CTA.
- Kötelező: cím, korszak, szint, oldalszám, időigény, rövid leírás.
- A státusz kizárólag `Elérhető`, `Hamarosan` vagy `Archivált` lehet.

### Könyvtár

- A kártyaadatok a `site/data/modules.json` központi konfigurációból származnak.
- Kézi modulmásolat nem maradhat a HTML-ben.
- A korszak- és szintazonosítók a központi taxonómiát használják.

### Tananyagoldal

- A bal oldali információs kártya csak a tanulót segítő adatokat mutatja.
- A haladás fejezetszintű, nem becsült kattintásszám.
- A fókusz mód elrejtheti a környező navigációt, de nem a H5P kezelőszerveit.

## 5. Borítók

- Minden publikált modulhoz kötelező valódi borítókép.
- Képarány: 16:9; ajánlott 1600×900 px.
- Legnagyobb fájlméret: 350 KB; elsődleges formátum WebP, ábránál optimalizált SVG.
- Kötelező a tartalmi alt szöveg; a pusztán dekoratív kép alt szövege üres.
- Vízjel, AI által hibásan generált felirat és bizonytalan jogállású kép tilos.
- `PLACEHOLDER` vagy „később cserélendő” elem éles buildbe nem kerülhet.

## 6. Ikonrendszer

- Egységes, egyszerű vonalas ikonok; azonos optikai vastagság.
- Az ikon mellé érthető szövegcímke kerül, ha funkciót indít.
- Emoji csak tanulói tartalmi kiemelésben használható, navigációs ikonként nem.
- Az ikonok minimum érintési területe 44×44 px.

## 7. H5P-típusok használata

| Típus | Ajánlott | Kerülendő |
|---|---|---|
| Interactive Book | teljes modul kerete | egyetlen rövid feladathoz |
| Accordion | rövid, opcionális magyarázat | hosszú törzsanyag elrejtésére |
| Timeline | időbeli folyamat | nem kronologikus lista |
| Image Hotspots | térkép, tárgy, épület | mobilon túl sok apró hotspot |
| Interactive Video | célzott videókérdés | hosszú, jogilag bizonytalan videó |
| Branching Scenario | valódi döntési helyzet | történelmi tények átírása |
| Course Presentation | vizuális lépéssor | teljes könyv pótlása |
| Single Choice | egyértelmű egyválaszos kérdés | több helyes válasznál |
| Multiple Choice | többválaszos ellenőrzés | félreérthető instrukcióval |
| Sort Paragraphs | sorrend és folyamat | vitatható sorrend esetén |

Minden kockázatos H5P-típushoz mobilon használható alternatíva szükséges.

## 8. Tiltott tanulói elemek

Nem jelenhet meg: `Tanulói szöveg`, `Megjelenő szöveg`, `Pontozás`, `Retry`, `Show Solution`, `Placeholder`, `Accordion`, `Multiple Choice`, `Single Choice`, `Kép- és hotspotterv`, `Akadálymentes alternatíva`, `VIZUÁLIS ELEM`, `KÉSŐBB CSERÉLENDŐ`, `Developer`, `Teacher note`.

A helyes válasz és magyarázat csak a válasz ellenőrzése után látható. A technikai mezők kizárólag a H5P konfigurációban maradnak.

## 9. Reszponzív szabályok

- Desktop: 1180–1480 px tartalmi keret, oldalsáv és tanulási színpad.
- Tablet: egymás alá törő tananyag-információ és H5P, érintésbarát vezérlés.
- Mobil: egyoszlopos nézet, teljes szélességű H5P, vízszintes túlcsordulás nélkül.
- Kötelező ellenőrzési méretek: desktop 1440×900, tablet 820×1180, mobil 390×844.
- A tartalom 200%-os nagyításnál is használható marad.

## 10. Akadálymentesség

- Cél: WCAG 2.2 AA.
- Logikus heading-hierarchia és egyetlen `main` régió.
- Látható `:focus-visible`, billentyűzetes navigáció és ugrólink.
- Minimum 4.5:1 szövegkontraszt; nagy szövegnél 3:1.
- Minden tartalmi kép alt szöveget kap.
- Animáció esetén `prefers-reduced-motion` támogatás kötelező.
- Állapotváltozásnál `aria-live` csak szükséges, rövid üzenetet közölhet.

## 11. QA checklist merge előtt

- [ ] A történelmi tartalom nem változott jogosulatlanul.
- [ ] Minden modul a központi konfigurációban szerepel.
- [ ] A borítókép valós, optimalizált és rendelkezik alt szöveggel.
- [ ] Nincs angol kezelőszöveg vagy fejlesztői metaadat.
- [ ] A megoldás nem látható ellenőrzés előtt.
- [ ] A haladásjelző követi a H5P fejezeteit.
- [ ] Az oldalszám konzisztens.
- [ ] A desktop, tablet és mobil Playwright-teszt sikeres.
- [ ] A Student Audit sikeres.
- [ ] A H5P licenc-, szerző- és verziómetaadata kitöltött.
- [ ] A korábbi modulok regressziótesztje sikeres.
- [ ] A PR nem engedélyez automatikus merge-et.

## 12. Release checklist

- [ ] A platformverzió és a release notes frissült.
- [ ] A CI minden ellenőrzése zöld.
- [ ] A Pages artifact tartalmazza az összes elérhető modult.
- [ ] A kezdőlapon nincs jelöletlen demó- vagy mockadat.
- [ ] A mélylinkek működnek (`era`, `level`, `module`).
- [ ] A runtime-hiba újrapróbálható, majd teljes oldalfrissítés ajánlható fel.
- [ ] A Lighthouse kapu teljesül vagy az eltérés dokumentált.
- [ ] Merge után az éles GitHub Pages gyors ellenőrzése megtörtént.

