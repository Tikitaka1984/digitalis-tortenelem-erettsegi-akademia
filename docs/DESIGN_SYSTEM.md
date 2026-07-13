# Design System v1.0

A Digitális Történelem Érettségi Akadémia platformszintű vizuális és interakciós rendszere. A H5P-tananyagok belső megjelenését nem írja felül; a tananyagokat körülvevő böngészési, könyvtári és tanulási felületet szabványosítja.

## Alapelvek

1. **Fókusz:** egy képernyőn egy elsődleges feladat.
2. **Rendszer:** következetes vizuális hierarchia minden modulnál.
3. **Bizalom:** pontos állapotok, egyértelmű visszajelzések és kiszámítható navigáció.
4. **Hozzáférhetőség:** WCAG AA kontraszt, billentyűzetes használat, látható fókusz és csökkentett mozgás.
5. **Skálázhatóság:** az elemek legalább 100 H5P-modul kiszolgálására készülnek.

## Márka

- **Jel:** klasszikus oszlopcsarnok modern, lekerekített keretben.
- **Elsődleges szín:** mély akadémiai zöld (`#264F3D`).
- **Akcentus:** energikus lime (`#D5FF65`).
- **Világos vászon:** meleg törtfehér (`#F7F5EF`).
- **Sötét vászon:** mély zöldes fekete (`#0D120F`).
- **Display betű:** Manrope.
- **Törzsszöveg:** DM Sans.

## Tokenrendszer

A tokenek a `site/assets/app.css` `:root` és `[data-theme="dark"]` blokkjában találhatók. A rendszer szemantikus neveket használ (`--canvas`, `--surface`, `--ink`, `--muted`, `--brand`, `--accent`), ezért a témaváltás nem komponensenként történik.

Térközök: 4, 8, 12, 16, 24, 32, 48 és 72 px.  
Lekerekítések: 10, 16, 24 és 32 px.  
Árnyékok: `xs`, `sm`, `md`, `lg` emelkedési szintek.

## Komponensek

- gombok: elsődleges, másodlagos, inverz, kis és nagy;
- navigáció: ragadós fejléc, mobilmenü, morzsamenü;
- kártyák: tananyag-, funkció-, lépés- és statisztikakártya;
- jelölők: badge, chip és státuszpont;
- információ: tippdoboz, üres-, betöltési- és hibaállapot;
- interakció: accordion, kereső, szűrőchipek, sötét mód és fókusz mód;
- tanulás: kurzusoldalsáv, kurzusadatok, célok, progress bar és lapozó.

### Kiegészítő komponensek

- `.section-header`: cím, leírás és opcionális művelet egységes szekciófejléce;
- `.alert`, `.alert-warning`, `.alert-error`: ikon + szöveg alapú állapotközlés, amely nem kizárólag színre támaszkodik;
- `.tooltip[data-tooltip]`: rövid, billentyűzetfókusszal is megjelenő súgó;
- natív `<dialog class="modal">`: akadálymentes modális ablak `.modal-header`, `.modal-body` és `.modal-footer` részekkel;
- `.skeleton`: betöltési helyőrző; csökkentett mozgás esetén az animáció automatikusan kikapcsol;
- `.loading-state`: központosított betöltési állapot szöveggel és opcionális spinnerrel.

A modális ablakhoz natív `showModal()` és `close()` használata javasolt. A nyitás után a fókusz kerüljön a párbeszédablak első műveletére, bezáráskor pedig térjen vissza a nyitógombra.

## Reszponzív töréspontok

- 1050 px: kétoszlopos tartalmak összevonása;
- 800 px: mobil navigáció, egysávos tanulási munkatér;
- 600 px: telefonos kártyák, teljes szélességű CTA-k és tömör fejléc.

## Akadálymentesség

- minden interaktív elem billentyűzettel elérhető;
- fókuszjelzés legalább 3 px;
- a szín nem az egyetlen állapotjelző;
- dekoratív képek üres `alt` értékkel szerepelnek;
- `prefers-reduced-motion` esetén az animációk gyakorlatilag kikapcsolnak;
- a sötét mód ugyanolyan szemantikus kontrasztrendszert használ;
- a H5P-tartalomhoz külön skip link vezet.

## Új modul felvétele

Az új modul kapjon könyvtárkártyát, egyedi korszak-illusztrációt, saját lejátszóoldalt vagy konfigurációt, valamint korszak-, szint-, időigény- és terjedelem-metaadatokat. A H5P tartalma és a platformdizájn továbbra is külön réteg marad.

