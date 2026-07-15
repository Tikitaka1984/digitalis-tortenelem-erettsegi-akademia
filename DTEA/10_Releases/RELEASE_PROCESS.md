# DTEA release-folyamat

**Szabványazonosító:** `DTEA-REL-PROCESS`

**Cél:** változtathatatlan, reprodukálható és visszaállítható tananyagkiadások

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`. Az automatikus merge minden esetben tilos; publikáció és merge csak sikeres automatikus QA, kézi QA és emberi jóváhagyás után történhet.

## 1. Szemantikus verziózás

A modulverzió formája `vMAJOR.MINOR.PATCH`.

### `v1.0.0`

Az első éles kiadás. Feltétele a teljes workflow, minden kötelező QA-dimenzió és a teljes release-dokumentáció sikeres lezárása.

### `v1.1.0`

Visszafelé kompatibilis bővítés, például új tanulástámogató oldal, új – már tanított célhoz kötött – interakció, javított assetkészlet vagy új, opcionális funkcionalitás.

### `v1.0.1`

Javító kiadás: tény-, szöveg-, fordítás-, accessibility-, UX-, pontozási vagy technikai hiba javítása a modul alapvető céljának és szerkezetének megváltoztatása nélkül.

### `v2.0.0`

Jelentős, inkompatibilis változás, például:

- tanulási célok vagy célközönség érdemi módosítása;
- oldalszerkezet és értékelési modell áttervezése;
- H5P fő library vagy működési szerződés inkompatibilis cseréje;
- tartalmi értelmezés vagy modulhatókör jelentős változása;
- korábbi mentett tanulói állapotok inkompatibilissé válása.

## 2. Release-típusok

| Típus | Verzió | Folyamat |
|---|---|---|
| Initial | `v1.0.0` | teljes QA és teljes jóváhagyás |
| Minor | `vX.Y.0` | hatáselemzés + teljes érintett QA + regresszió |
| Patch | `vX.Y.Z` | célzott QA + kockázatarányos regresszió |
| Hotfix | patch | gyorsított, de nem kihagyott review és QA |
| Major | `vX.0.0` | új baseline, migrációs és kompatibilitási terv |
| Withdrawal | változatlan release-id | visszavonási rekord, nem új tartalomverzió |

## 3. Release-előkészítés

### 3.1 Verziójavaslat

A változásgazda dokumentálja:

- előző release;
- változások listája;
- szemantikus verziójavaslat és indoklás;
- érintett tanulási célok, oldalak, interakciók, assetek és libraryk;
- adat-, jogi, történelmi, accessibility- és kompatibilitási kockázat;
- szükséges regressziós kör.

### 3.2 Bemenetbefagyasztás

Rögzítendő:

- Source Register verzió;
- Master Script verzió;
- Instructional Design verzió;
- Build Guide verzió;
- Asset Register verzió;
- assethash-ek;
- buildszkript és dependency lock;
- commit SHA.

A befagyasztás után tartalmi változás új release candidate-et hoz létre.

### 3.3 Release candidate

Forma: `vX.Y.Z-rc.N`.

Minden RC egyedi buildazonosítót és SHA-256-ot kap. Sikertelen RC nem írható felül; a következő `rc.N+1`.

## 4. Kötelező release QA

Release előtt:

- automatikus QA: `PASS`;
- kézi QA-jegyzőkönyv teljes;
- Historical QA: `PASS`;
- Instructional QA: `PASS`;
- UX QA: `PASS`;
- Accessibility QA: `PASS`;
- Technical QA: `PASS`;
- H5P QA: `PASS`;
- release build tiszta környezetből reprodukálva;
- nem érintett modulok regressziója a változás kockázata szerint;
- dependency és licenc audit sikeres;
- végleges csomaghash rögzítve.

## 5. Release-csomag

Könyvtár:

```text
10_Releases/<module-id>/vX.Y.Z/
```

Kötelező tartalom:

| Fájl | Tartalom |
|---|---|
| `...interactive-book...h5p` | végleges, importálható H5P |
| `...release-manifest...json` | teljes gépi provenance és buildadat |
| `...release-notes...md` | felhasználói és üzemeltetői változásleírás |
| `...qa-summary...md` | QA-kapuk és bizonyítékhivatkozások |
| `CHANGELOG.md` | verziótörténet |
| `SHA256SUMS` | csomag- és dokumentumhash-ek |
| `LICENSES.md` | asset- és dependency-licencek |

## 6. Release manifest kötelező mezői

- `release_id`;
- `module_id`;
- `version`;
- `status`;
- `created_at_utc`;
- `commit_sha`;
- `build_id`;
- `package_file` és `package_sha256`;
- `master_script_version`;
- `instructional_design_version`;
- `source_register_version`;
- `asset_manifest_version`;
- `dependencies` névvel és verzióval;
- `qa_dossier`;
- `approvers`;
- `known_limitations`;
- `supersedes`, ha van;
- `rollback_target`, ha van.

## 7. Changelog-szabály

Kategóriák:

- `Added`
- `Changed`
- `Fixed`
- `Accessibility`
- `Historical corrections`
- `Security`
- `Deprecated`
- `Removed`

Minden tétel hatást ír le, és szükség esetén hiba-, claim-, asset- vagy PR-azonosítóra hivatkozik.

## 8. Jóváhagyás

Minimum jóváhagyók:

- Historical Lead, ha történelmi tartalom érintett;
- Instructional Design vagy LXD felelős, ha tanulói út érintett;
- QA Engineer;
- Release Manager;
- Product/Program Owner.

Az author nem lehet az egyetlen jóváhagyó. A jóváhagyás a konkrét package hash-re vonatkozik.

## 9. Publikálás

1. A release-csomag a Work munkatérből a GitHub Pages publikációs folyamatába kerül.
2. A publikált fájl hash-e összehasonlítandó a manifesttel.
3. A modulindex vagy kezdőlap a pontos release-verzióra frissül.
4. Publikálás utáni smoke check fut desktop és mobil nézetben.
5. Elérhetőség, fő navigáció, H5P-betöltés és kritikus interakció ellenőrzendő.
6. A GitHub Pages publikáció ideje, commit SHA-ja és eredménye a release rekordba kerül.

## 10. Hotfix

Hotfix csak éles, jelentős hiba gyors javítására használható. Nem engedélyez QA-kihagyást.

Folyamat:

1. incidens és súlyosság rögzítése;
2. patch branch a kiadott tagből;
3. legkorábbi hibás forrásartefaktum javítása;
4. célzott Historical/Instructional/Accessibility/Technical/H5P QA;
5. kötelező kritikus út regresszió;
6. új patch verzió és új hash;
7. publikálás és post-release ellenőrzés.

## 11. Visszaállítás és visszavonás

### Rollback

Technikai vagy működési hiba esetén a legutóbbi jóváhagyott release állítható vissza. A korábbi csomag nem építhető újra módosított dependencykből; az archivált byte-azonos artefaktumot kell használni.

### Withdrawal

Kötelezően mérlegelendő, ha:

- súlyos történelmi hamisítás vagy forráshiány derül ki;
- jogsértő asset vagy licencprobléma van;
- kritikus biztonsági/adatvédelmi hiba található;
- a kritikus tanulói út jelentős csoport számára nem hozzáférhető;
- a kiadott csomag hash-e nem igazolható.

A visszavont release nem törlendő nyomtalanul; `WITHDRAWN` státusz, indok, dátum és helyettesítő verzió szükséges.

## 12. Deprecation

- A `DEPRECATED` release továbbra is azonosítható és archivált.
- Meg kell jelölni az ajánlott utódot és a támogatás végének dátumát.
- Ha migráció szükséges, kompatibilitási és adat/állapot-kezelési útmutató készül.
- Deprecated release új telepítése nem ajánlott.

## 13. Megőrzés és audit

- A release-csomag, manifest, hash, QA-összefoglaló és licencek tartósan megőrzendők.
- A build és jóváhagyás audit trailje nem módosítható.
- Évente vagy szabványváltáskor ellenőrizendő a csomag importálhatósága és az archívum integritása.
- Az audit nem változtatja meg az eredeti release-t; megállapításai új rekordba kerülnek.
