# Digitális Történelem Érettségi Akadémia

Statikus, GitHub Pages-kompatibilis webes futtatókörnyezet a **Digitális Történelem Érettségi Akadémia** H5P Interactive Book moduljaihoz.

Publikált modulok: **Athéni demokrácia** és **Földrajzi felfedezések**.

## DTEA Design System v1.0

A platformfelület a tananyag tartalmától különálló, újrafelhasználható design systemre épül. A H5P-csomag, annak kérdései, pontozása, metaadatai és belső struktúrája változatlan marad.

- `site/index.html` – márkaoldal, kiemelt tananyag, működési modell, előnyök és GYIK;
- `site/library.html` – kereshető és korszak szerint szűrhető digitális könyvtár;
- `site/learn.html` – tanulási keret oldalsávval, haladásjelzővel és fókusz móddal;
- `site/assets/app.css` – szemantikus design tokenek, komponensek, reszponzív és sötét téma;
- `site/assets/app.js` – témaváltás, mobilmenü, könyvtárszűrés és fókusz mód;
- `docs/DTEA_DESIGN_SYSTEM.md` – színek, tipográfia, H5P-szabályok és release checklist.

A felület három törésponttal optimalizált asztali, tablet- és mobilhasználatra. A billentyűzetfókusz, a szemantikus régiók, az ARIA-címkék, a csökkentett mozgás és a kontrasztos sötét mód a platformréteg része.

## Működési elv

A böngésző nem tud közvetlenül `.h5p` fájlt futtatni, mert az egy meghatározott szerkezetű ZIP-csomag, amely tartalmi JSON-t, médiafájlokat és H5P-könyvtárakat tartalmaz. A repository az Athéni demokrácia változatlan forráscsomagját és a Földrajzi felfedezések reprodukálható generátorát tárolja. A GitHub Actions minden buildnél:

1. a jóváhagyott Master Scriptből előállítja a Földrajzi felfedezések H5P-csomagját;
2. SHA-256 ellenőrzéssel igazolja, hogy egyik forráscsomag sem változott;
3. biztonságosan kibontja a csomagokat a generált `_site` könyvtárba;
4. ellenőrzi a H5P manifesteket, a 30–30 oldalt, a licencmetaadatokat és a deklarált könyvtárakat;
5. melléteszi a Lumi alkalmazásszintű tárából származó, ellenőrzőösszeggel rögzített dinamikus média-könyvtárakat (`H5P.Audio-1.5`, `H5P.Video-1.6`);
6. bemásolja a rögzített `h5p-standalone@3.8.2` runtime-ot;
7. minden modulra Student Auditot, valamint desktop-, tablet- és mobilteszteket futtat;
8. a kész `_site` könyvtárat GitHub Pages-re telepíti.

A build a történelmi `content.json` tartalmat **nem módosítja**. A publikált H5P-manifesztumba a központi konfigurációból egységes licenc-, szerző- és verziómetaadat kerül.

A webes artifacton egy ellenőrzőösszeggel védett, szűken célzott kompatibilitási javítás fut a `H5P.SortParagraphs-0.11` könyvtáron. Ez kizárólag a standalone lejátszó korai inicializálásakor jelentkező két null-hivatkozást védi ki; a feladat szövegét, válaszait, pontozását, metaadatait és a forrás `.h5p` csomagot nem érinti.

## Architektúra

```text
Athéni .h5p + jóváhagyott Master Script + reprodukálható generátor
       │
       ▼
Földrajzi felfedezések .h5p (CI build artifact)
       │
       ▼
scripts/build_site.py
       │  integritás-ellenőrzés + biztonságos kibontás
       ▼
_site/h5p/{atheni-demokracia,foldrajzi-felfedezesek}
       │
       ├── h5p.json
       ├── content/content.json + média
       └── H5P-könyvtárak

site/ + h5p-standalone/dist
       │
       ▼
_site/ → GitHub Pages artifact
```

Az `learn.html` a `module` URL-paraméter alapján választ a rögzített modulkonfigurációk közül, és relatív útvonalakkal inicializálja a standalone lejátszót. Így ugyanaz a lejátszókeret szolgálja ki mindkét könyvet a GitHub Pages repository-alútvonalán is.

```text
learn.html?module=atheni-demokracia
learn.html?module=foldrajzi-felfedezesek
```

## A Földrajzi felfedezések csomag újraépítése

A második könyv reprodukálhatóan készül a jóváhagyott `Master Script v1.0.2` dokumentumból. Az Athéni csomag csak a már ellenőrzött H5P library-k hordozója; annak történelmi tartalma és médiája nem kerül át.

```bash
python scripts/build_discoveries_h5p.py
```

A script pontosan 30 oldalt állít elő, az engedélyezett Lumi-kompatibilis komponensekkel és ellenőrzött vizuális elemekkel. Placeholder vagy fejlesztői metaadat nem kerülhet a tanulói buildbe. A Build Guide v1.0.2 mezőszintű végrehajtási specifikáció helyett jóváhagyott váz; emiatt a megvalósítás a benne felsorolt elsődleges típusokra és engedélyezett alternatívákra korlátozódik.

A modul történelmi térképei hiteles, közkincs gyűjteményi forrásokból származnak. A pontos forrás-, licenc- és képernyőképjegyzék: [Sprint 4.2 történelmi térkép Asset Register](docs/assets/FOLDRAJZI_FELFEDEZESEK_HISTORICAL_MAPS.md).

## Fájlszerkezet

```text
.
├── .github/workflows/pages.yml
├── content/
│   ├── digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p
│   └── digitalis-tortenelem-erettsegi-akademia-foldrajzi-felfedezesek-v1.0.h5p  # generált, gitignore
├── runtime-libraries/
│   └── lumi-media-libraries.zip
├── scripts/
│   ├── build_discoveries_h5p.py
│   ├── build_site.py
│   └── verify-build.mjs
├── site/
│   ├── index.html
│   ├── learn.html
│   ├── 404.html
│   ├── sw.js
│   └── assets/
├── tests/smoke.spec.mjs
├── package.json
├── playwright.config.mjs
└── README.md
```

Az `_site/`, a `node_modules/` és a tesztjelentések generált elemek, ezért nem kerülnek verziókezelésbe.

## Helyi build

Előfeltételek:

- Node.js 20 vagy újabb;
- Python 3.11 vagy újabb;
- Chromium a Playwright tesztekhez.

```bash
npm install --ignore-scripts --no-audit --no-fund
npm run build
npm run verify
npx playwright install chromium
npm test
```

A kész statikus oldal az `_site/` könyvtárban található. Helyi megnyitásához HTTP-szerver szükséges:

```bash
python -m http.server 4173 -d _site
```

Ezután: `http://127.0.0.1:4173/`.

## GitHub Pages

A `.github/workflows/pages.yml` pull request esetén buildet és teszteket futtat, de nem publikál. A `main` ágra kerülő commit vagy a kézzel indított workflow:

1. elkészíti és ellenőrzi a statikus artifactot;
2. feltölti azt a GitHub Pages rendszerébe;
3. a `github-pages` környezeten keresztül telepíti.

A repository **Settings → Pages → Source** beállítása legyen **GitHub Actions**. A várható projekt-URL:

```text
https://tikitaka1984.github.io/digitalis-tortenelem-erettsegi-akademia/
```

Privát repository esetén a GitHub-csomag jogosultságaitól függ, hogy a Pages-publikálás elérhető-e. Ha a Pages csak nyilvános repositoryhoz engedélyezett, a repót publikálás előtt nyilvánossá kell tenni, vagy megfelelő GitHub-csomagra kell váltani.

## Új H5P könyv hozzáadása

1. Másold az új, változatlan `.h5p` fájlt a `content/` könyvtárba.
2. Számíts SHA-256 ellenőrzőösszeget.
3. A `scripts/build_site.py` fájlban vegyél fel új modulkonfigurációt: forrásfájl, célkönyvtár, checksum és várt oldalszám.
4. Készíts külön lejátszóoldalt vagy modulválasztót a `site/` könyvtárban.
5. A lejátszóban minden útvonal legyen relatív.
6. Bővítsd a `verify-build.mjs` és Playwright teszteket.
7. Futtasd a buildet és a teljes tesztcsomagot.

Az új modul hozzáadása nem igényli a meglévő H5P csomag módosítását.

## A meglévő könyv frissítése

1. Cseréld le a `content/` könyvtárban lévő `.h5p` fájlt az új, ellenőrzött exporttal.
2. Frissítsd a fájlnevet, az `EXPECTED_SHA256` és – ha változott – az `EXPECTED_PAGES` értéket.
3. Frissítsd a webes verziójelölést és a service worker cache-nevét.
4. Futtasd a teljes buildet és tesztet.
5. Külön pull requestben dokumentáld a forráscsomag verzióját és ellenőrzőösszegét.

## Tesztelés

### Statikus ellenőrzés

- H5P ZIP-integritás;
- SHA-256 egyezés;
- `h5p.json` és `content/content.json` jelenléte;
- `H5P.InteractiveBook` főkönyvtár;
- pontosan 30 oldal;
- minden deklarált preloaded dependency;
- minden, a tartalmi JSON-ban hivatkozott médiafájl.

### Böngészős ellenőrzés

- modern nyitóoldal és indítógomb;
- H5P iframe és Interactive Book betöltése;
- kezdőoldali tartalom megjelenése;
- JavaScript-kivételek hiánya;
- mobilos vízszintes túlcsordulás hiánya.

A teljes manuális release-ellenőrzés során végig kell járni mind a 30 oldalt, legalább egy helyes és hibás választ, a Retry/Show Solution működését, a zárótesztet és a Drag and Drop feladatokat mobilon.

## Teljesítmény és cache

- A nyitóoldal nem tölti be a H5P runtime-ot.
- A H5P csak a `learn.html` oldalon inicializálódik.
- A runtime saját tárhelyről érkezik, rögzített verzióval.
- A service worker a statikus keretet előre gyorsítótárazza, a további saját domainelemeket pedig használat közben cache-eli.
- A GitHub Pages CDN további HTTP-cache-t biztosít.
- A H5P belső kép- és feladatbetöltését nem írjuk át, így a tananyag struktúrája érintetlen marad.

## Hibakezelés

Ha a runtime vagy valamely szükséges tartalmi fájl nem tölthető be, a lejátszóoldal olvasható hibaállapotot és „Újrapróbálás” gombot jelenít meg. A build már publikálás előtt meghiúsul hiányzó manifest, könyvtár vagy média esetén.

## Ismert korlátok

- A GitHub Pages statikus: nincs tanulói bejelentkezés, szerveroldali eredménytárolás vagy tanári riport.
- A H5P pontozás és visszajelzés az aktuális böngészős munkamenetben működik.
- Tartós, többeszközös haladáskövetéshez backend vagy LRS szükséges.
- A böngészőcache nem helyettesíti a tanulói eredménytárolást.
- A projekt nem módosítja és nem javítja a H5P csomag belső tartalmát; a tananyaghibákat a forrás `.h5p` új verziójában kell kezelni.

## Biztonság és integritás

- A build útvonalbejárás ellen védett ZIP-kibontást használ.
- A forrás H5P csak az ismert SHA-256 ellenőrzőösszeggel publikálható.
- A runtime verziója rögzített.
- A generált Pages-artifact nem tartalmaz szerkesztői titkot vagy hitelesítő adatot.

## Licencelés

A webes runtime függősége, a `h5p-standalone`, MIT licencű. A H5P csomag belső tartalmainak és médiáinak jogi státuszát a tananyag saját Rights of Use és forrásadatai határozzák meg.


## Platform v1.2.0 – GSI-02

A platform harmadik teljes tananyaga Géza fejedelem és I. (Szent) István államszervező munkáját dolgozza fel 30 oldalas H5P Interactive Bookban. A könyvtár továbbra is központi modulkonfigurációt, mélylinkeket, fejezetszintű haladást és minden publikált modulra kiterjedő automatikus tartalomauditot használ.

Dokumentáció:

- [DTEA Design System v1.0](docs/DTEA_DESIGN_SYSTEM.md)
- [Architektúra](docs/ARCHITECTURE.md)
- [Release Notes](docs/RELEASE_NOTES.md)
- [Verziótörténet](docs/VERSION_HISTORY.md)
