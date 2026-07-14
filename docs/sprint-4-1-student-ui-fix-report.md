# Sprint 4.1 – Földrajzi felfedezések tanulói felület javítása

## Eredmény

A Földrajzi felfedezések H5P Interactive Book tanulói felülete 30 oldalas, teljesen magyar, és nem jelenít meg szerkesztői vagy fejlesztői metaadatokat. A helyes válaszok és visszajelzések csak az Ellenőrzés művelet után láthatók. Az Athéni demokrácia H5P-csomag nem változott.

## Javított alapproblémák

- A korábbi, megengedő feldolgozás szerkesztői sorokat és beállítási táblázatokat is átengedhetett a tanulói tartalomba.
- Több H5P-típus alapértelmezett angol kezelőfeliratokat használt.
- A technikai összegzőoldal miatt a könyv 31 oldalnak látszhatott.
- A vizuális helyőrzők nem valódi, hordozható H5P-képekként jelentek meg.
- Egyes többkérdéses blokkok nem önálló, valódi H5P-feladatokként épültek fel.

## Megoldás

- Szigorú engedélyező és tiltó szabályokra épülő tartalomfeldolgozás készült.
- Minden használt H5P-feladattípus és az Interactive Book kezelőfeliratai magyar lokalizációt kaptak.
- A technikai összegzőoldal ki van kapcsolva; a könyv pontosan 30 oldalas.
- Nyolc valódi `H5P.Image` vizuális elem került a csomagba, magyar alternatív szöveggel.
- A többkérdéses részek önálló H5P-komponensekre bomlanak; a záróteszt 12 komponensből és 20 pontból áll.
- Az automatikus audit ellenőrzi a 30 oldalt, a tiltott tanulói szövegeket, a magyar feliratokat, a képeket, az egyedi azonosítókat, a függőségeket és a záróteszt pontértékét.

## Vizuális elemek

A borítókép a beépített OpenAI képgenerálással készült, új kép létrehozási módban. A prompt történelmileg hiteles, felirat és vízjel nélküli, 16:9 arányú atlanti térképet, 15. századi karavellát és finom útvonaljelöléseket kért. A további hét sematikus oktatási ábra determinisztikus SVG.

## QA

- Statikus H5P-audit: PASS
- Tanulói tartalomaudit: PASS
- Oldalszám: 30
- Vizuális elemek: 8
- Záróteszt: 12 komponens, 20 pont
- Webhely build: 2 modul, 60 oldal, SHA-256 ellenőrzés sikeres
- Playwright: 19 sikeres, 3 projektfüggő kihagyás
- Desktop Chromium: sikeres
- Mobil Chromium, 390×844: sikeres, vízszintes túlcsordulás nélkül
- Lighthouse: teljesítmény 100, akadálymentesség 95, bevált gyakorlatok 100, SEO 100
- Athéni H5P SHA-1 egyezés az `origin/main` verzióval: `49a446f2e3e02810c3a05c5f951cf6d60b8afc11`

## Képernyőképek

1. [Valódi borítókép, desktop](screenshots/sprint-4-1/01-cover-real-image-desktop.png)
2. [Tiszta tanulói szöveg](screenshots/sprint-4-1/02-clean-student-text.png)
3. [Feladat ellenőrzés előtt](screenshots/sprint-4-1/03-task-before-check.png)
4. [Feladat ellenőrzés után](screenshots/sprint-4-1/04-task-after-check.png)
5. [Tordesillasi megállapodás oldal](screenshots/sprint-4-1/05-tordesillas-page.png)
6. [Mobilnézet, 390×844](screenshots/sprint-4-1/06-mobile-390x844.png)
7. [Tartalomjegyzék](screenshots/sprint-4-1/07-table-of-contents.png)
8. [Záróteszt](screenshots/sprint-4-1/08-final-test.png)
