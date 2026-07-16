# GSI-02 implementációs QA-jelentés

**Modul:** Géza fejedelem és I. (Szent) István  
**Modulazonosító:** `geza-fejedelem-szent-istvan`  
**Csomagverzió:** `v1.0.0`  
**Ellenőrzés dátuma:** 2026-07-16  
**Eredmény:** **PASS**

## Ellenőrzött implementáció

- 30 oldalas H5P Interactive Book a jóváhagyott Master Script, Build Guide és Page Map alapján;
- 29 formatív interakció, amelyek nem számítanak bele a könyv végeredményébe;
- 10 kérdéses, 20 pontos záróteszt 60%-os teljesítési küszöbbel;
- magyar kezelőszövegek, visszajelzések, pontozás és navigáció;
- öt helyi, licenc- és forrásadattal bevételezett történelmi asset;
- magyar alt szövegek, billentyűzetes feladatmozgatás és reszponzív megjelenés;
- kezdőlapi és könyvtári modulkártya, borítókép és közvetlen tananyagútvonal;
- az Athéni demokrácia és a Földrajzi felfedezések meglévő H5P-tartalmának regressziós védelme.

## Forrásdokumentum integritása

A merge-elt Master Script 9–30. oldala binárisan sérült volt. Az implementáció előtt a fájl teljes, korábban már repositoryba rögzített változata lett visszaállítva a `b06c514` commitból. Új történelmi tartalom vagy újratervezés nem történt; az implementáció a jóváhagyott repository-forrást követi.

## Automatikus ellenőrzések

| Ellenőrzés | Eredmény | Bizonyíték |
|---|---:|---|
| GSI-02 statikus H5P-audit | PASS | 30 oldal; 29 formatív interakció; 10 zárókérdés; 20 pont; 5 helyi asset; 229 egyedi `subContentId` |
| Földrajzi felfedezések regressziós H5P-audit | PASS | 30 oldal; 20 pontos záróteszt; minden vizuális elem helyi |
| Webhely build-ellenőrzés | PASS | 3 modul; 90 oldal; 63 deklarált H5P-függőség; 13 hivatkozott tartalmi asset |
| Student Audit | PASS | 3 H5P-modul; tiltott szerkesztői és placeholder-szövegek nélkül |
| Teljes Playwright regresszió | PASS | 55 sikeres, 10 kihagyott; 1 meglévő Sprint 4.1 vizuális teszt elsőre ingadozott, ismétlésre sikeres; a GSI-02 tesztjei nem hibáztak |
| Végleges GSI-02 Playwright | PASS | 12/12: desktop, tablet és mobil |
| Lighthouse desktop quality gate | PASS | Performance 100; Accessibility 95; Best Practices 100; SEO 100 |
| Törött link, hiányzó kép és hiányzó asset ellenőrzése | PASS | a build és a böngészős tesztek minden helyi útvonalat sikeresen betöltöttek |

## Asset- és jogi ellenőrzés

Az öt történelmi vizuális elem Wikimedia Commons-leíróoldalhoz, szerzőhöz vagy őrzőhelyhez, licenchez és SHA-256 ellenőrzőösszeghez kötötten szerepel az [Asset Registerben](../DTEA/08_Assets/geza-fejedelem-szent-istvan/ASSET_REGISTER.md). A csomag nem hotlinkel, és nem tartalmaz AI-generált történelmi térképet, portrét, oklevelet, koronát vagy dokumentumot.

## Képernyőképek

- [Kezdőlapi modulkártya – desktop](screenshots/gsi-02/01-home-module-card-desktop.png)
- [Első tanulói oldal – desktop](screenshots/gsi-02/02-book-first-page-desktop.png)
- [Záróteszt – desktop](screenshots/gsi-02/03-final-test-desktop.png)
- [Első tanulói oldal – mobil](screenshots/gsi-02/04-book-first-page-mobile.png)

## Ismert korlátok

Funkcionális vagy tartalmi release-blokkoló korlát nem ismert. A helyi Windows-környezetben a Lighthouse a kész jelentés után időnként zárolt ideiglenes Chrome-profilt jelez; a jelentés elkészül, és a repositoryban használt quality gate ettől függetlenül PASS. A GitHub Actions eredményét a Draft Pull Request publikálása után kell véglegesen rögzíteni.

## Végső minősítés

**PASS – a GSI-02 implementáció helyi release QA-ja sikeres.**
