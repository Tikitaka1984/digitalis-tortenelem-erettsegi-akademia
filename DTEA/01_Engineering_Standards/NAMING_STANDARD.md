# DTEA elnevezési és verziózási szabvány

**Szabványazonosító:** `DTEA-ENG-NAMING`

**Alkalmazás:** kötelező minden új fájlra, azonosítóra, assetre és release-re

## 1. Általános szabályok

- Azonosítókban és fájlnevekben kizárólag kisbetűs ASCII karakter, szám és kötőjel használható.
- Szóköz, ékezet, aláhúzás és zárójel nem megengedett, kivéve a szabvány által rögzített dokumentumneveket.
- A név jelentést ír le, nem állapotot vagy személyt.
- Tilos: `final`, `latest`, `new`, `copy`, `fixed`, `végleges`, dátum mint egyetlen verziójel, szerző neve.
- A kiterjesztés kisbetűs.
- Az azonosító létrehozás után nem változik; átnevezéshez migrációs rekord szükséges.

## 2. Modulazonosító

Forma:

```text
<tantargy>-<korszak>-<tema>
```

Regex:

```text
^[a-z0-9]+(?:-[a-z0-9]+){2,7}$
```

Követelmények:

- 3–8 jelentéshordozó szegmens;
- időtálló, tantervi vagy szerkezeti fogalom;
- nem tartalmaz évfolyamot, verziót vagy fájltípust;
- a központi module registryben egyedi.

Semleges minta: `tortenelem-korszak-temakor`.

## 3. Szemantikus verzió

Forma: `vMAJOR.MINOR.PATCH`, például `v1.0.0`.

| Elem | Növelés oka |
|---|---|
| `MAJOR` | inkompatibilis szerkezet-, cél-, követelmény- vagy jelentésváltozás |
| `MINOR` | visszafelé kompatibilis tartalmi vagy funkcionális bővítés |
| `PATCH` | tény-, szöveg-, accessibility-, UX- vagy technikai hibajavítás |

Pre-release forma: `v1.0.0-rc.1`. A `rc` csomag nem publikálható végleges release-ként.

## 4. Dokumentumfájlok

Központi szabványoknál a kért, stabil felsőházas név használható, például:

```text
PROJECT_RULES.md
QA_STANDARD.md
```

Modulspecifikus dokumentum:

```text
<module-id>--<document-type>--v<major>.<minor>.<patch>.md
```

Engedélyezett dokumentumtípusok többek között:

- `module-charter`
- `source-register`
- `claim-map`
- `master-script`
- `instructional-design`
- `build-guide`
- `asset-register`
- `asset-manifest`
- `automated-qa-report`
- `manual-qa-report`
- `qa-report`
- `release-notes`

## 5. Master Script

```text
<module-id>--master-script--v<major>.<minor>.<patch>.md
```

A Master Script verziója önálló; nem szükséges azonosnak lennie a H5P release-verzióval. A release manifest rögzíti, mely Master Script verzióból készült.

## 6. H5P-fájl

```text
<module-id>--interactive-book--v<major>.<minor>.<patch>.h5p
```

Release candidate:

```text
<module-id>--interactive-book--v<major>.<minor>.<patch>-rc.<n>.h5p
```

Tilos ugyanazzal a névvel eltérő tartalmú H5P-t kiadni.

## 7. Assetazonosító és fájlnév

Assetazonosító:

```text
<module-id>--ast-<type>-<nnn>
```

Fájlnév:

```text
<asset-id>--<short-description>--v<major>.<minor>.<patch>.<ext>
```

Típuskódok:

| Kód | Típus |
|---|---|
| `img` | fotó vagy raszterkép |
| `map` | térkép |
| `ill` | illusztráció |
| `dia` | diagram vagy folyamatábra |
| `aud` | hang |
| `vid` | videó |
| `ico` | ikon |
| `doc` | tanulói dokumentumasset |

Példaséma:

```text
tortenelem-korszak-temakor--ast-map-003--regionalis-attekintes--v1.0.0.svg
```

## 8. Képek és grafikai változatok

Opcionális, szabványos származékjelzők:

- `--desktop`
- `--mobile`
- `--thumbnail`
- `--dark`
- `--light`
- `--print`

Példaforma:

```text
<asset-id>--<description>--mobile--v1.0.0.webp
```

A vizuális jelentés változása verziónövelés; puszta veszteségmentes optimalizálás új buildhash-t, de nem feltétlen új tartalmi verziót igényel.

## 9. Videó és hang

```text
<asset-id>--<description>--<lang>--v<version>.<ext>
```

Nyelvkód ISO 639-1, például `hu`. A felirat és transcript ugyanazt az assetazonosítót használja:

```text
<asset-id>--captions--hu--v1.0.0.vtt
<asset-id>--transcript--hu--v1.0.0.md
```

## 10. Oldal-, cél-, állítás- és interakcióazonosítók

| Entitás | Forma |
|---|---|
| Tanulási cél | `<module-id>--lo-<nnn>` |
| Állítás | `<module-id>--clm-<nnnn>` |
| Oldal | `<module-id>--pg-<nnn>` |
| Interakció | `<module-id>--int-<nnn>` |
| QA-bizonyíték | `<module-id>--qa-<dimension>-<nnn>` |
| Build | `<module-id>--build-<utc-timestamp>-<short-sha>` |

Sorszámok nullával feltöltöttek és újra nem oszthatók.

## 11. Branch- és tagnevek

```text
module/<module-id>/<short-purpose>
fix/<module-id>/<short-purpose>
standards/<short-purpose>
release/<module-id>/v<version>
```

Release tag:

```text
<module-id>/v<major>.<minor>.<patch>
```

## 12. Release-könyvtár

```text
10_Releases/<module-id>/v<major>.<minor>.<patch>/
```

Kötelező fájlok:

```text
<module-id>--interactive-book--vX.Y.Z.h5p
<module-id>--release-manifest--vX.Y.Z.json
<module-id>--release-notes--vX.Y.Z.md
<module-id>--qa-summary--vX.Y.Z.md
SHA256SUMS
```

## 13. Időbélyeg és dátum

- Emberi dokumentumban: `YYYY-MM-DD`.
- Gépi időbélyeg: UTC ISO 8601, például `2030-01-15T13:45:22Z`.
- Dátum nem helyettesítheti a szemantikus verziót.
