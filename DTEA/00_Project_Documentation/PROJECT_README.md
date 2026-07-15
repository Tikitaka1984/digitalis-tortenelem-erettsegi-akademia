# DTEA projektkézikönyv

**Dokumentumazonosító:** `DTEA-GOV-PROJECT-README`

**Státusz:** kötelező irányító dokumentum

**Hatókör:** minden DTEA-modul, asset, build és release

**Dokumentációs verzió:** `v0.1.0`

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`

A `Work` az egyetlen hivatalos szerzői és build-munkatér. Az automatikus QA minden pull request és publikáció kötelező kapuja, a GitHub Pages az ellenőrzött tanulói felület publikációs célkörnyezete. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési célra használható; nem helyettesíti a Work munkateret, az automatikus vagy kézi QA-t és a GitHub Pages publikációt.

## 1. Projektcél

A Digital Teaching Excellence Architecture olyan vállalati szintű fejlesztési rendszer, amely több száz történelmi digitális tananyag következetes, mérhető és fenntartható előállítását teszi lehetővé. A rendszer nem egyetlen tananyagot ír le: közös szerződést biztosít a kutatás, a történelmi validáció, az instructional design, az assetgyártás, a H5P-fejlesztés, a QA és a kiadás között.

### Sikerkritériumok

- minden kiadott állítás visszakövethető jóváhagyott forráshoz;
- minden modul ugyanazon kötelező kapukon halad át;
- minden build reprodukálható rögzített bemenetekből;
- minden release technikai és szakmai bizonyítékokkal auditálható;
- a felület egységes, lokalizált, reszponzív és hozzáférhető;
- a rendszer párhuzamos modulfejlesztés mellett is elkerüli a név-, verzió- és assetütközéseket.

## 2. Hatókör és kizárások

### A DTEA része

- governance és repository-architektúra;
- forrás- és jogkezelés;
- Master Script és pedagógiai tervezési szabvány;
- H5P Interactive Book implementációs szabvány;
- asset-életciklus;
- többszintű QA és release management;
- automatizálható validáció és bizonyítékmegőrzés.

### Nem része ennek az inicializálásnak

- konkrét történelmi tananyag;
- H5P-feladat vagy kész H5P-csomag;
- Master Script;
- modul-specifikus forrásanyag vagy médiaasset;
- publikációs környezet telepítése.

## 3. Architektúra

A DTEA elválasztja az irányítást, a bemeneteket, a szerkesztett tartalmat, az implementációt, a bizonyítékokat és a kiadást.

| Réteg | Könyvtárak | Elsődleges felelősség |
|---|---|---|
| Governance | `00`, `01` | szabályok, workflow, verziózás, repository-szerződések |
| Módszertan | `02`, `03`, `04` | AI-támogatás, H5P és pedagógiai tervezés |
| Bemenetek | `05` | források, jogok, provenance és integritás |
| Tartalomterv | `06` | jóváhagyott Master Script |
| Implementáció | `07`, `08` | H5P-projekt és jóváhagyott assetek |
| Bizonyíték | `09` | QA-tervek, eredmények és kapudöntések |
| Kiadás | `10` | változtathatatlan release és archiválás |

### Információáramlási szabály

Az anyag kizárólag előre haladhat a jóváhagyási láncban. Egy későbbi fázisban talált hiba a hiba eredeti forrásrétegében javítandó; kiadási vagy build output kézi foltozása tilos.

## 4. Kötelező workflow

1. **Modulindítás:** egyedi modulazonosító, tulajdonos, célközönség és hatókör.
2. **Forrásbevételezés:** bibliográfia, jogi státusz, integritás és megbízhatósági besorolás.
3. **Forráselemzés:** állításjelöltek, bizonytalanságok és forrástérkép.
4. **Master Script:** tanulói szöveg, oldalterv, hivatkozások és interakciós szándék.
5. **Instructional Design:** cél–tartalom–tevékenység–értékelés összehangolása.
6. **Asset Register és Build Guide:** szükséglet, licenc, alt text, technikai specifikáció, implementációs szerződés és státusz.
7. **H5P implementáció:** a Build Guide szerinti reprodukálható build, magyar lokalizáció és szabványos komponensek.
8. **QA:** kötelező automatikus QA és dokumentált kézi Historical, Instructional, UX-, Accessibility-, Technical és H5P QA.
9. **Release:** szemantikus verzió, manifest, hash, changelog, jóváhagyás és archiválás.

Részletek: [WORKFLOW.md](WORKFLOW.md) és [MODULE_WORKFLOW.md](MODULE_WORKFLOW.md).

## 5. Szerepkörök és felelősségek

Egy személy több szerepet is elláthat, de ugyanazon magas kockázatú változás szerzője és végső jóváhagyója lehetőség szerint ne legyen ugyanaz.

| Szerepkör | Fő felelősség | Kötelező jóváhagyás |
|---|---|---|
| Product/Program Owner | prioritás, hatókör, release-döntés | modulindítás, kiadás |
| Historical Lead | forrásminőség és történelmi hitelesség | forráskapu, Historical QA |
| Instructional Designer | célok, terhelés, értékelési illeszkedés | ID-kapu, Instructional QA |
| LXD/UX Lead | tanulói út, következetesség és érthetőség | UX QA |
| H5P Developer | implementáció, lokalizáció, build | technikai jelölt |
| Accessibility Reviewer | WCAG-alapú hozzáférhetőség | Accessibility QA |
| QA Engineer | tesztterv, regresszió és bizonyíték | QA-kapu |
| Release Manager | verzió, manifest, hash és archiválás | release-kapu |

## 6. Verziókezelés

### Git-modell

- `main`: kizárólag jóváhagyott, integrálható állapot;
- `module/<module-id>/<short-purpose>`: modulfejlesztés;
- `standards/<short-purpose>`: infrastruktúra- és szabványmódosítás;
- `fix/<module-id>/<short-purpose>`: hibajavítás;
- `release/<module-id>/vMAJOR.MINOR.PATCH`: kiadási stabilizáció, ha szükséges.

Közvetlen push a `main` branchre tilos. Minden változás pull requesten, automatikus ellenőrzéseken és kijelölt review-n halad át. Az automatikus merge minden esetben tilos; merge csak sikeres automatikus QA és dokumentált emberi review után, kézi művelettel történhet.

### Commitok

Ajánlott forma: `<type>(<scope>): <imperative summary>`.

Engedélyezett típusok: `docs`, `standards`, `source`, `content`, `assets`, `h5p`, `test`, `fix`, `release`, `chore`.

Példa: `standards(qa): define accessibility release gate`.

## 7. Naming convention

Minden azonosító ASCII, kisbetűs kebab-case, stabil és jelentéshordozó. Ékezet, szóköz, dátum nélküli „final”, „new”, „latest”, „copy” vagy személynév fájlnévben nem használható. A részletes szabvány: [NAMING_STANDARD.md](../01_Engineering_Standards/NAMING_STANDARD.md).

## 8. Release rendszer

A DTEA szemantikus verziózást használ:

- `MAJOR`: tanulási cél, szerkezet, kompatibilitás vagy tartalmi értelmezés jelentős változása;
- `MINOR`: visszafelé kompatibilis tartalmi, pedagógiai vagy funkcionális bővítés;
- `PATCH`: javítás, amely nem változtatja meg a modul célját vagy követelményszintjét.

Minden release tartalmaz H5P-csomagot, manifestet, SHA-256 hash-t, dependency jegyzéket, changelogot, QA-összefoglalót és jóváhagyási rekordot. Részletek: [RELEASE_PROCESS.md](../10_Releases/RELEASE_PROCESS.md).

## 9. Státuszmodell és kapuk

| Státusz | Jelentés |
|---|---|
| `DRAFT` | szerkesztés alatt, downstream használatra nem engedélyezett |
| `IN_REVIEW` | kijelölt szakmai vagy technikai review zajlik |
| `CHANGES_REQUESTED` | blokkoló eltérés javítandó |
| `APPROVED` | a saját fázisában jóváhagyott bemenet |
| `RELEASE_CANDIDATE` | minden tartalmi bemenet rögzített, teljes QA folyamatban |
| `RELEASED` | változtathatatlanul kiadott verzió |
| `DEPRECATED` | támogatott utódra cserélt, új felhasználásra nem ajánlott |
| `WITHDRAWN` | súlyos okból visszavont kiadás |

Kaput csak névvel, dátummal, vizsgált verzióval és bizonyítékhivatkozással lehet jóváhagyni.

## 10. Változáskezelés

- Szabványmódosítás hatáselemzést igényel a meglévő modulokra.
- Kötelező mező vagy formátum törése `MAJOR` szabványverzió-váltás.
- A kivétel időkorlátos, tulajdonossal, kockázattal és megszüntetési tervvel dokumentálandó.
- Súlyos történelmi, jogi, biztonsági vagy accessibility-hiba release-visszavonást indíthat.
- A dokumentáció és az automatizált validátor ugyanabban a változásban frissítendő.

## 11. Definition of Ready

Egy modul implementációra kész, ha:

- modulazonosítója és tulajdonosa rögzített;
- a Source Register `APPROVED`;
- a Master Script történelmi és szerkesztői review-ja sikeres;
- az Instructional Design döntései, a Build Guide és az Asset Register jóváhagyott;
- minden bizonytalanság lezárt vagy kifejezetten dokumentált.

## 12. Definition of Done

Egy modul kiadásra kész, ha:

- reprodukálható H5P-build készült rögzített bemenetekből;
- az automatikus QA és a kézi QA külön bizonyítékkal `PASS`;
- minden kötelező QA-dimenzió `PASS`;
- nincs nyitott blokkoló vagy súlyos hiba;
- a csomag magyar, reszponzív és hozzáférhető;
- a manifest, hash, changelog és release notes elkészült;
- a release manager és a kijelölt szakmai jóváhagyó aláírta a kiadást.
