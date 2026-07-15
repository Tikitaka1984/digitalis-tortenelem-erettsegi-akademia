# DTEA – Digital Teaching Excellence Architecture

A DTEA történelmi digitális tananyagok nagy volumenű, egységes és auditálható fejlesztésének projektarchitektúrája. Ez a könyvtár nem tananyagot, hanem a tananyagfejlesztés irányítási, mérnöki, pedagógiai, forráskezelési, H5P-, minőségbiztosítási és kiadási rendszerét tartalmazza.

**Dokumentációs verzió:** `v0.1.0`

**Hivatalos fejlesztési módszer:** `Work + automatikus QA + GitHub Pages`

A `Work` a kontrollált szerzői és build-munkatér, az automatikus QA a pull requestek és publikációk kötelező kapuja, a GitHub Pages pedig az ellenőrzött tanulói felület publikációs célkörnyezete. A Lumi Desktop kizárólag prototípus-, kompatibilitási és hibakeresési eszköz; nem hivatalos szerzői, build-, QA- vagy publikációs környezet.

## Alapelvek

- egyetlen állítás vagy asset sem kerülhet kiadásba ellenőrizhető eredet nélkül;
- a tartalom, a pedagógiai terv, a technikai implementáció és a QA elkülönülő felelősségi kör;
- minden modul azonos életciklust, azonos kapurendszert és azonos verziózási szabályokat követ;
- a hozzáférhetőség, a tanulói UX és a H5P-kompatibilitás kiadási feltétel;
- a generált vagy automatizált eredmények emberi szakmai jóváhagyás nélkül nem tekinthetők késznek.
- az automatikus merge minden változásnál tilos; merge csak sikeres QA és emberi review után történhet.

## Kötelező modul-artefaktumok

Minden új modulhoz kötelező a Source Register, a Master Script, a Build Guide, az Asset Register, az automatikus QA eredménye és a kézi QA jegyzőkönyve. E hat artefaktum bármelyikének hiánya release-blokkoló eltérés.

## Könyvtártérkép

| Könyvtár | Felelősség |
|---|---|
| `00_Project_Documentation` | Projektarchitektúra, teljes workflow és modul-életciklus |
| `01_Engineering_Standards` | Kötelező mérnöki, elnevezési és repository-szabványok |
| `02_Prompt_System` | Verziózott promptok, bemeneti és kimeneti szerződések |
| `03_H5P_Standards` | H5P-kompatibilitás, komponens- és csomagolási szabványok |
| `04_Instructional_Design` | Pedagógiai tervezési modellek, sablonok és döntési rekordok |
| `05_Source_Library` | Forrásbevételezés, jogi metaadatok és eredetkövetés |
| `06_Master_Scripts` | Jóváhagyott tananyag-forgatókönyvek helye |
| `07_H5P_Books` | Építhető és kiadásra jelölt H5P Interactive Book projektek |
| `08_Assets` | Ellenőrzött képi, hang-, videó- és grafikai assetek |
| `09_QA` | QA-tervek, ellenőrzőlisták, bizonyítékok és hibajegyek |
| `10_Releases` | Kiadási csomagok, jegyzékek, változásnaplók és archiválás |

## Irányító dokumentumok

- [Projektkézikönyv](00_Project_Documentation/PROJECT_README.md)
- [Végponttól végpontig workflow](00_Project_Documentation/WORKFLOW.md)
- [Új modul workflow](00_Project_Documentation/MODULE_WORKFLOW.md)
- [Elnevezési szabvány](01_Engineering_Standards/NAMING_STANDARD.md)
- [Kötelező projektszabályok](01_Engineering_Standards/PROJECT_RULES.md)
- [Forráskönyvtári szabvány](05_Source_Library/SOURCE_LIBRARY_STANDARD.md)
- [QA-szabvány](09_QA/QA_STANDARD.md)
- [Kiadási folyamat](10_Releases/RELEASE_PROCESS.md)

## Használat

Új modul csak jóváhagyott modulazonosítóval és forrásbevételezéssel indítható. A fejlesztés a dokumentált kapukon halad végig; kapu nem hagyható ki. A kiadási csomag kizárólag a `10_Releases` területre kerülhet, miután minden kötelező QA-státusz `PASS`.

## Jelen inicializálás hatóköre

Ez a verzió kizárólag az infrastruktúrát és a szabványrendszert hozza létre. Nem tartalmaz történelmi tananyagot, Master Scriptet, H5P-feladatot vagy kiadható modult.
