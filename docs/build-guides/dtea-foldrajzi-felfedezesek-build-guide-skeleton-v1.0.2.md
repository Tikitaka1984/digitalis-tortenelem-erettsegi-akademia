# Földrajzi felfedezések – H5P Build Guide váz v1.0.2

**Kapcsolódó dokumentum:** `dtea-foldrajzi-felfedezesek-master-script-v1.0.2.md`  
**Szabvány:** DTEA STANDARD v1.0 – jóváhagyása után kötelező  
**Státusz:** javasolt szerkezet; nem végrehajtási Build Guide  
**Cél:** a következő sprintben elkészítendő, mezőszintű technikai specifikáció kerete.

> Ez a dokumentum szándékosan nem konfigurál működő H5P-elemeket. A Master Script és a DTEA Standard elfogadása után kell kitölteni. Történelmi tartalmat nem módosíthat.

## 1. Dokumentumvezérlés

- Master Script pontos verziója és SHA-256-ja
- DTEA Standard verziója
- Lumi Desktop és H5P library verziók
- cél runtime: H5P Standalone / GitHub Pages
- szerző, reviewer, dátum, státusz
- eltérésnapló hivatkozása

## 2. Teljes oldaltérkép

| # | Oldal | Elsődleges funkció | Javasolt H5P | Pontozott |
|---:|---|---|---|:---:|
| 1 | Borító és motiváció | ráhangolás | Text + Image | nem |
| 2 | Mérhető tanulási célok | útvonal | Accordion | nem |
| 3 | Előzetes tudás | diagnosztika | Question Set | nem számít a záróeredménybe |
| 4 | Miért indultak útnak? | okok | Multiple Choice | igen |
| 5 | A hajózás feltételei | eszköz–funkció | Image Hotspots; Accordion alternatíva | igen |
| 6 | Portugál kezdeményezés | folyamat | Accordion | igen |
| 7 | Dias útja | tér-idő | Single Choice Set | igen |
| 8 | Vasco da Gama útja | útvonal | Image Hotspots; Accordion alternatíva | igen |
| 9 | Kolumbusz 1492-es útja | fordulópont | Multiple Choice | igen |
| 10 | Tordesillas | térbeli felosztás | Image Hotspots; Course Presentation alternatíva | igen |
| 11 | Magellán expedíciója | folyamat | Timeline; Accordion alternatíva | igen |
| 12 | További utak | rendszerezés | Accordion | igen |
| 13 | Hódítás és gyarmatosítás | ok-okozat | Text + Multiple Choice | igen |
| 14 | Őslakosság és rabszolgaság | következmény | Multiple Choice | igen |
| 15 | Kontinensek közötti csere | forrásalapú felismerés és következmény | Single Choice Set; Multiple Choice alternatíva | igen |
| 16 | Az atlanti kereskedelem | gazdasági tér | Text + Single Choice | igen |
| 17 | Árforradalom | oksági lánc | Accordion; Course Presentation alternatíva | igen |
| 18 | Bank, tőzsde, részvény | fogalmi rendszer | Dialog Cards + MC | igen |
| 19 | Manufaktúra és kapitalizmus | termelési modell | Accordion + MC | igen |
| 20 | Nyugat és Kelet | összehasonlítás | Accordion + Multiple Choice | igen |
| 21 | Interaktív kronológia | időrend | Timeline + lineáris alternatíva | nem |
| 22 | Kulcsszemélyek | szerepek | Dialog Cards / Accordion | nem |
| 23 | Kulcsfogalmak | felidézés | Dialog Cards | nem |
| 24 | Térkép és topográfia | helyek, útvonalak | Image Hotspots + lista | igen |
| 25 | Forráselemzés: Tordesillas | forráskövetkeztetés | Question Set | igen |
| 26 | Forráselemzés: következmények | forrásösszevetés | Question Set | igen |
| 27 | Ok–következmény háló | szintézis | Drag and Drop + alternatíva | igen |
| 28 | Érettségi fókusz | felkészítés | Accordion + Essay guide | nem |
| 29 | Záróteszt | értékelés | Question Set | 20 pont |
| 30 | Összegzés | önellenőrzés | Summary + Text | nem |

## 3. Globális H5P-beállítások

A végleges Guide itt rögzítse:

- Interactive Book cím és metadata;
- tartalomjegyzék és navigáció;
- felület nyelve;
- eredmény-összesítés;
- Retry és Show Solution globális elve;
- pontozott/nem pontozott elemek kezelése;
- teljesítménysávok;
- betű- és design tokenek runtime-oldali alkalmazása;
- állapotmegőrzés és xAPI viselkedés, ha támogatott.

## 4. Oldalspecifikáció sablon

Minden oldal külön fejezetet kap:

1. oldalszám, cím és funkció;
2. Master Script forrásfejezet;
3. tanulási célkód és kognitív művelet;
4. komponensek sorrendje;
5. teljes szöveg és mezőleképezés;
6. pontos H5P library és verzió;
7. adminisztratív címkék;
8. viselkedési beállítások;
9. helyes válaszok és pontozás;
10. helyes/hibás visszajelzés;
11. Retry és Show Solution;
12. médiafájl, képarány, alt szöveg, kredit;
13. mobil és billentyűzetes viselkedés;
14. engedélyezett alternatíva;
15. elfogadási teszt és várható idő.

## 5. Pontozási mátrix

A végleges Guide egyetlen táblázatban egyeztesse:

| Elem ID | Oldal | Kérdéstípus | Max pont | Retry | Show Solution | Eredménybe számít |
|---|---:|---|---:|:---:|:---:|:---:|
| kitöltendő |  |  |  |  |  |  |

A mátrix összpontszámának egyeznie kell a Master Scripttel. Az előzetes tudásfelmérés külön kezelendő.

## 6. Média- és Asset Register

Külön táblázat szükséges a hero képhez, hajózási eszközökhöz, útvonaltérképekhez, személyábrázolásokhoz, csereinfografikához és gazdasági folyamatábrákhoz. Minden rekord: asset ID, oldal, cél, fájlnév, formátum, képarány, alt szöveg, felirat, jogállás, státusz, placeholder.

## 7. Mobil és akadálymentes alternatívák

Kötelezően specifikálandó:

- Image Hotspots mellett szöveges helylista;
- Timeline mellett lineáris kronológia;
- Drag and Drop mellett billentyűzettel működő párosítás/csoportosítás;
- Interactive Video esetén felirat és átirat;
- minden kép alt szövege;
- 320 px-es elrendezés;
- fókuszsorrend és visszajelzés bejelentése.

## 8. Engedélyezett alternatívák

| Tervezett elem | Korlát | Engedélyezett alternatíva |
|---|---|---|
| Drag and Drop | mobil/billentyűzet | Multiple Choice vagy szöveges csoportosítás |
| Image Hotspots | túl sűrű térkép | számozott kép + Accordion/lista |
| Timeline | runtime vagy mobilhiba | Accordion / számozott kronológia |
| Course Presentation | kis képernyős törés | egymás alatti Text + Image + kérdés |
| Dialog Cards | library hiány | Accordion |

Más helyettesítés E2 eltérés, külön jóváhagyást igényel.

## 9. QA és regresszió

- oldalszám és címek összevetése;
- szöveghűség a Master Scripthez;
- minden H5P-elem jelenléte;
- pontozás és visszajelzés;
- Retry/Show Solution;
- navigáció és eredményösszesítés;
- desktop, tablet, mobil;
- billentyűzet és alt szöveg;
- hiányzó asset és JavaScript-hiba;
- H5P csomag validitása;
- GitHub Pages runtime smoke test.

## 10. Lezárt szakmai döntés – Cabral Timeline-dátumozása

- **Timeline-dátum:** 1500–1501.
- **Tanulói címke:** „Cabral expedíciója”.
- **Rövid leírás:** „Brazília partvidékének elérése, majd továbbhaladás India felé”.
- Az Accordion Cabral miatt nem kötelező; kizárólag általános mobil- vagy kompatibilitási tartalék marad.
- Cabral dátumozása nem blokkolja a végleges Build Guide későbbi elkészítését.

## 11. v1.0.1 módosítási jegyzet

- A hivatalos skeleton a repository egyetlen példánya.
- A Master Script akkori v1.0.1 változatára mutató hivatkozás frissült; a v1.0.2 ezt a hivatkozást ismét aktualizálja.
- Az oldaltérképen az elsődleges H5P-típusok egyértelműsödtek.
- A kockázatos elemekhez egyetlen megengedett alternatíva tartozik.
- Cabral Timeline-dátumozását a v1.0.1 döntés-előkészítő pontként rögzítette; a v1.0.2-ben lezárult.

## 12. v1.0.2 módosítási jegyzet

- Cabral Timeline-dátuma 1500–1501.
- A tanulói címke „Cabral expedíciója”, a rövid leírás „Brazília partvidékének elérése, majd továbbhaladás India felé”.
- Az Accordion már csak általános mobil- vagy kompatibilitási tartalék.
- A Cabral-dátum nem blokkoló szakmai kérdés.

## 13. Kimenetek a következő sprint végén

- teljes, jóváhagyott Build Guide;
- Asset Register;
- eltérésnapló;
- fejlesztési és QA-checklist;
- ötlapos pilot buildterv;
- becsült fejlesztési idő oldalanként;
- kockázati lista;
- külön PR, automatikus merge nélkül.

