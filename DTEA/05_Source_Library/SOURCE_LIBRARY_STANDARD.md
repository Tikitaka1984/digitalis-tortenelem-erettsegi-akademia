# DTEA Source Library Standard

**Szabványazonosító:** `DTEA-SRC-STANDARD`

**Cél:** jogszerű, ellenőrizhető és állításszinten visszakövethető forrásbázis

## 1. Alapelvek

- A Source Library kontrollált bevételezési rendszer, nem általános fájlmegosztó.
- A forrásrekord és a tárolt fájl két külön entitás; rekord fájl nélkül is létezhet, fájl rekord nélkül nem.
- A fizikai tárolás joga nem azonos a tananyagban történő felhasználás jogával.
- Generált tartalom nem minősül történelmi forrásnak.
- A forrás eredeti példányát és a feldolgozott származékot el kell különíteni.

## 2. Forráskategóriák

| Kód | Kategória | Példa jelleg |
|---|---|---|
| `PRI` | elsődleges forrás | korabeli dokumentum, tárgy, kép vagy felvétel |
| `SEC` | tudományos másodlagos forrás | monográfia, lektorált tanulmány |
| `TER` | megbízható összefoglaló | lexikon, intézményi áttekintés |
| `EDU` | oktatási forrás | jóváhagyott tankönyv, tanári kézikönyv |
| `DAT` | strukturált adat | adatbázis, katalógus, kronológia |
| `VIS` | vizuális forrás | kép, térkép, ábra |
| `AUD` | hangforrás | interjú, archív hang |
| `VID` | videóforrás | dokumentumfilm, intézményi felvétel |
| `WEB` | webes forrás | tartós, azonosítható weboldal |

## 3. Forrásazonosító

Forma:

```text
src-<category>-<year>-<nnnnn>
```

A `year` a bevételezés éve, nem a mű megjelenési éve. Példaforma: `src-sec-2030-00042`.

Az azonosító stabil, törlés után nem osztható újra.

## 4. Kötelező metaadatok

Minden rekord tartalmazza:

| Mező | Követelmény |
|---|---|
| `source_id` | egyedi, stabil azonosító |
| `category` | szabványos kategóriakód |
| `title` | a forrás hivatalos címe |
| `creator` | szerző, alkotó vagy felelős intézmény |
| `publication` | kiadó, folyóirat, gyűjtemény vagy platform |
| `published_at` | ismert megjelenési dátum vagy időintervallum |
| `language` | ISO 639-1 vagy indokolt bővebb kód |
| `identifier` | ISBN, DOI, katalógusszám, stabil URL vagy más azonosító |
| `accessed_at` | webes vagy külső digitális forrás elérési dátuma |
| `rights_holder` | ismert jogosult |
| `license` | licenc vagy jogi státusz |
| `storage_permission` | tárolható-e a repositoryban |
| `reuse_permission` | hogyan használható tananyagban |
| `original_location` | eredeti vagy hiteles elérési hely |
| `file_sha256` | tárolt fájl esetén kötelező |
| `reliability` | minőségi besorolás és indoklás |
| `scope_notes` | mire használható, milyen korlátokkal |
| `status` | `QUARANTINED`, `IN_REVIEW`, `APPROVED`, `REJECTED`, `RETIRED` |
| `reviewer` | szakmai jóváhagyó |
| `reviewed_at` | jóváhagyás dátuma |

## 5. Bevételezési folyamat

### 5.1 Előszűrés

1. Azonosítható szerző vagy intézmény ellenőrzése.
2. A forrás relevanciájának és várható felhasználásának rögzítése.
3. Jogi és adatvédelmi kockázat előzetes értékelése.
4. Duplikátumkeresés azonosító és hash alapján.

Nem tisztázott fájl `QUARANTINED` státuszba kerül, és downstream használata tilos.

### 5.2 Technikai bevételezés

1. Eredeti fájl változtatás nélküli megőrzése, ha jogszerű.
2. SHA-256 kiszámítása.
3. Fájltípus és tényleges MIME ellenőrzése.
4. Malware- és integritásellenőrzés.
5. OCR vagy konverzió külön származékként, saját hash-sel.

### 5.3 Szakmai review

- szerzőség és keletkezési kontextus;
- elsődleges/másodlagos jelleg;
- módszertan és szakmai megbízhatóság;
- elfogultság, nézőpont és korlátozás;
- más forrásokkal való összhang vagy ellentmondás;
- a tervezett állításokhoz való relevancia.

### 5.4 Jogi review

- copyright és közkincs státusz;
- licencfeltételek, attribúció és módosíthatóság;
- területi, időbeli vagy platformkorlátozás;
- oktatási felhasználás és újraterjesztés különbsége;
- személyiségi jog, adatvédelem és érzékeny tartalom.

## 6. Forrástípus-specifikus szabályok

### Tankönyvek

- kiadás, év, szerzők, kiadó, ISBN és oldalszám kötelező;
- egy teljes, jogvédett könyv repositoryba csak kifejezett engedéllyel kerülhet;
- állításhivatkozás pontos oldalra vagy fejezetre mutat;
- a tankönyv önmagában nem zárja ki tudományos kontrollforrás szükségességét.

### PDF-ek

- eredeti letöltési URL és hozzáférési dátum;
- SHA-256 és oldalszám;
- OCR-szöveg nem helyettesíti az eredeti PDF-et;
- OCR-hibákból származó idézet csak vizuális ellenőrzés után használható;
- beágyazott képek joga külön is vizsgálandó.

### Jegyzetek

- szerző, dátum és keletkezési kontextus kötelező;
- magánjegyzet nem válik hiteles forrássá pusztán tárolástól;
- kutatási jegyzet csak pointerként használható az eredeti forrás felé;
- jóváhagyott tényállítás végső hivatkozása nem mutathat kizárólag belső jegyzetre.

### Képek és térképek

- alkotó, cím/leírás, dátum, gyűjtemény és katalógusazonosító;
- történelmi térkép, valós történelmi személy portréja és történelmi dokumentum csak hiteles Public Domain vagy Creative Commons forrásból használható;
- a Public Domain vagy Creative Commons státuszhoz a hiteles őrzőhelyet, alkotót, pontos licencet, forrás-URL-t és az előírt attribúciót rögzíteni kell;
- Creative Commons forrásnál a tervezett újrafelhasználásnak és módosításnak meg kell felelnie a licencfeltételeknek;
- eredeti kép és szerkesztett származék külön rekord vagy egyértelmű derivációs kapcsolat;
- manipuláció, kivágás, színezés vagy annotáció dokumentálandó;
- alt text nem bibliográfiai leírás, hanem a tanulási funkció szöveges alternatívája;
- AI-generált kép kizárólag borítóhoz, hangulatképhez vagy dekoratív illusztrációhoz használható;
- AI-generált kép nem használható történelmi térképként, valós történelmi személy portréjaként, történelmi dokumentumként, forrásrekonstrukcióként vagy bizonyító erejű vizuálként.

### Videók

- készítő, cím, megjelenés, platform, időtartam és stabil URL;
- releváns időkódok állításhivatkozásnál;
- felirat, transcript és nyelv rögzítése;
- streamingelérhetőség nem jelent beágyazási vagy újraterjesztési jogot;
- megszűnési kockázat és alternatíva dokumentálandó.

### Webforrások

- intézmény/szerző és publikációs vagy frissítési dátum;
- hozzáférési dátum;
- lehetőség szerint DOI, permalink vagy webarchív hivatkozás;
- dinamikus, névtelen vagy reklámvezérelt oldal csak erős indoklással;
- keresési találati oldal nem forrás.

## 7. Megbízhatósági besorolás

| Szint | Jelentés | Felhasználás |
|---|---|---|
| `A` | elsődleges hiteles őrzőhely vagy magas minőségű tudományos forrás | fő állítás alátámasztására alkalmas |
| `B` | megbízható, szerkesztett intézményi vagy oktatási forrás | kontrollal használható |
| `C` | korlátozott, nézőpontfüggő vagy részlegesen dokumentált | kiegészítő, nem kizárólagos |
| `D` | nem ellenőrizhető vagy nem megfelelő | nem használható, `REJECTED` |

A besorolás nem presztízslista; az adott állításhoz való megfelelőség külön értékelendő.

## 8. Állítás–forrás kapcsolat

Minden claim rekord tartalmazza:

- `claim_id`;
- normalizált állításszöveg;
- `source_id`;
- pontos hely: oldal, fejezet, időkód vagy rekordazonosító;
- támogatás típusa: `DIRECT`, `INFERRED`, `CONTEXT`, `CONTRADICTS`;
- bizonyossági szint;
- reviewer és dátum.

Az inference jellegét egyértelműen jelezni kell; az értelmezés nem írható a forrás szájába.

## 9. Tárolási zónák

| Zóna | Tartalom | Használhatóság |
|---|---|---|
| `quarantine` | ellenőrizetlen bevitel | tilos |
| `originals` | jogszerűen tárolható eredetik | csak kontrollált |
| `derivatives` | OCR, tömörített vagy szerkesztett származék | derivációval |
| `registers` | metaadat és claim map | hivatalos |
| `licenses` | licencek, engedélyek, attribúció | hivatalos |

## 10. Frissítés, visszavonás és megőrzés

- Megváltozott webforrás rekordja új ellenőrzési dátumot és szükség esetén új snapshotot kap.
- Hibás vagy jogilag visszavont forrás `RETIRED`; fizikai törlés csak megőrzési és jogi szabály szerint.
- Érintett claim, modul és release hatáselemzése kötelező.
- A release-ben használt metaadatot a release élettartamáig meg kell őrizni.
- A forrásrekord története nem írható felül; a státuszváltozás auditálható.
