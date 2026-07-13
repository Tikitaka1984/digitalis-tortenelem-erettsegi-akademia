# Digitális Történelem Érettségi Akadémia

Statikus, GitHub Pages-kompatibilis webes futtatókörnyezet a **Digitális Történelem Érettségi Akadémia** H5P Interactive Book moduljaihoz.

Az első publikált modul: **Athéni demokrácia**.

## Működési elv

A böngésző nem tud közvetlenül `.h5p` fájlt futtatni, mert az egy meghatározott szerkezetű ZIP-csomag, amely tartalmi JSON-t, médiafájlokat és H5P-könyvtárakat tartalmaz. A repository ezért a változatlan `.h5p` forráscsomagot tárolja, a GitHub Actions pedig minden buildnél:

1. SHA-256 ellenőrzéssel igazolja, hogy a forráscsomag nem változott;
2. biztonságosan kibontja a csomagot a generált `_site` könyvtárba;
3. ellenőrzi a H5P manifestet, a 30 oldalt és a deklarált könyvtárakat;
4. melléteszi a Lumi alkalmazásszintű tárából származó, ellenőrzőösszeggel rögzített dinamikus média-könyvtárakat (`H5P.Audio-1.5`, `H5P.Video-1.6`);
5. bemásolja a rögzített `h5p-standalone@3.8.2` runtime-ot;
6. statikus és böngészős teszteket futtat;
7. a kész `_site` könyvtárat GitHub Pages-re telepíti.

A H5P tananyag tartalmát a build **nem módosítja**. A kibontott fájlok kizárólag a webes telepítési artifact részei.

A webes artifacton egy ellenőrzőösszeggel védett, szűken célzott kompatibilitási javítás fut a `H5P.SortParagraphs-0.11` könyvtáron. Ez kizárólag a standalone lejátszó korai inicializálásakor jelentkező két null-hivatkozást védi ki; a feladat szövegét, válaszait, pontozását, metaadatait és a forrás `.h5p` csomagot nem érinti.

## Architektúra

```text
content/*.h5p
       │
       ▼
scripts/build_site.py
       │  integritás-ellenőrzés + biztonságos kibontás
       ▼
_site/h5p/atheni-demokracia
       │
       ├── h5p.json
       ├── content/content.json + média
       └── H5P-könyvtárak

site/ + h5p-standalone/dist
       │
       ▼
_site/ → GitHub Pages artifact
```

Az `learn.html` a standalone lejátszót relatív útvonalakkal inicializálja, ezért a webhely a GitHub Pages repository-alútvonalán is működik.

## Fájlszerkezet

```text
.
├── .github/workflows/pages.yml
├── content/
│   └── digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p
├── runtime-libraries/
│   └── lumi-media-libraries.zip
├── scripts/
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

