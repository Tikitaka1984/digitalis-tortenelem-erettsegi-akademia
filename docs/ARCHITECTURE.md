# DTEA platformarchitektúra

## Áttekintés

A DTEA statikus GitHub Pages platform. A tananyagok H5P Interactive Book csomagok, amelyeket a `h5p-standalone` futtat. Backend és központi tanulói fiók nincs.

## Adatáramlás

1. A `site/data/modules.json` a taxonómia és modulmetaadat egyetlen forrása.
2. A build a konfigurációból választja ki az elérhető H5P-csomagokat.
3. A `build_site.py` biztonságosan kibontja és validálja a csomagokat, majd egységes licencmetaadatot ad a publikált manifeszthez.
4. A böngésző ugyanebből a konfigurációból építi a könyvtárat és a tananyag keretét.
5. A haladás helyben, modulonként a `localStorage` területén tárolódik.

## Fő komponensek

- `site/assets/app.js`: közös UI, könyvtár, URL-szűrés.
- `site/assets/player.js`: H5P betöltés, runtime retry, fejezetszintű haladás.
- `site/data/modules.json`: modulok, korszakok, szintek, licenc és buildforrás.
- `scripts/build_site.py`: statikus publikációs artifact.
- `scripts/audit_student_build.py`: általános tanulói tartalomaudit.
- `scripts/verify-build.mjs`: csomag-, függőség- és metaadat-ellenőrzés.
- Playwright: desktop, tablet és mobil regresszió.

## Stabilitási elvek

- A történelmi csomagok ellenőrzőösszege védi a tartalmat.
- A Student Audit blokkolja a szerkesztői szövegek publikálását.
- A runtime első hibánál újratöltődik; ismételt hibánál teljes oldalfrissítés ajánlott.
- A haladás az aktuális H5P-fejezetből származik, nem becsült kattintásokból.
- Minden módosítás PR-ben, automatikus merge nélkül készül.

