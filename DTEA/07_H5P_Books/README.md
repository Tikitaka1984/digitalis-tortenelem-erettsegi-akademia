# 07 – H5P Books

## Mire szolgál?

A modulonként elkülönített, reprodukálhatóan építhető H5P Interactive Book projektek munkaterülete.

A hivatalos fejlesztési módszer `Work + automatikus QA + GitHub Pages`. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési eszköz; ott készült változtatás csak a Work munkatérben reprodukálva kerülhet a hivatalos buildbe.

## Milyen fájlok kerülnek ide?

- H5P-forrásprojekt és buildkonfiguráció;
- modulmanifest és library-függőségi jegyzék;
- lokalizációs konfiguráció;
- reprodukálható buildszkriptek;
- kiadásra jelölt, de még nem archivált H5P-csomagjelölt.

## Mi nem kerülhet ide?

- szerkesztői ideiglenes fájl vagy cache;
- licenc nélküli library;
- nyers forrás, Master Script vagy forrás nélküli asset;
- végleges release archívum.

## Workflow-kapcsolat

A jóváhagyott Master Script, Build Guide és Asset Register alapján épül; innen kerül automatikus és kézi QA-ra, majd a `10_Releases` területre és GitHub Pages publikációra.
