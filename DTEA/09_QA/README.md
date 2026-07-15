# 09 – QA

## Mire szolgál?

A történelmi, pedagógiai, UX-, accessibility-, technikai és H5P-minőségbiztosítás tervezésének és bizonyítékainak központi helye.

A hivatalos fejlesztési módszer `Work + automatikus QA + GitHub Pages`. Az automatikus QA és a dokumentált kézi QA külön-külön kötelező; egyik sem helyettesíti a másikat.

## Milyen fájlok kerülnek ide?

- QA-tervek és verziózott ellenőrzőlisták;
- tesztjegyzőkönyvek és automatikus riportok;
- képernyőképek, hibajegyek és reprodukciós lépések;
- jóváhagyási rekordok és kapudöntések;
- regressziós baseline-ok.

## Mi nem kerülhet ide?

- forrásanyag vagy kész release-csomag;
- bizonyíték nélküli `PASS` nyilatkozat;
- személyes adatot vagy titkot tartalmazó napló;
- javításként kezelt, de a forrásfájlokba vissza nem vezetett kézi módosítás.

## Workflow-kapcsolat

Minden fejlesztési kapuhoz tartozik QA. Release és GitHub Pages publikáció csak akkor készülhet, ha az automatikus QA és minden kötelező kézi QA-dimenzió eredménye `PASS`.

## Fő dokumentum

- [QA_STANDARD.md](QA_STANDARD.md)
