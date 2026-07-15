# 10 – Releases

## Mire szolgál?

A jóváhagyott, változtathatatlan kiadási csomagok, manifestek, változásnaplók és archivált QA-bizonyítékok helye.

A hivatalos fejlesztési módszer `Work + automatikus QA + GitHub Pages`. A publikáció kézi jóváhagyást követ; az automatikus merge minden esetben tilos.

## Milyen fájlok kerülnek ide?

- verziózott H5P release-csomagok;
- release manifest, SHA-256 és dependency lock;
- changelog, release notes és jóváhagyási rekord;
- QA-összefoglaló és visszaállítási információ;
- hosszú távú archiválási metaadat.

## Mi nem kerülhet ide?

- munkapéldány, draft vagy sikertelen build;
- felülírható „latest” fájl egyedi verzió nélkül;
- QA nélküli vagy nem reprodukálható csomag;
- nyers forrás vagy szerkesztői asset.

## Workflow-kapcsolat

A sikeres automatikus és kézi QA-kapu után jön létre. A release innen GitHub Pagesre publikálható, archiválható vagy visszaállítható; a fájlok utólag nem módosíthatók.

## Fő dokumentum

- [RELEASE_PROCESS.md](RELEASE_PROCESS.md)
