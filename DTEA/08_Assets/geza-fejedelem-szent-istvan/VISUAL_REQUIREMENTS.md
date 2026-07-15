# Visual Requirements – Géza fejedelem és I. (Szent) István

**Cél:** történelmileg tisztességes, jogszerű, tanulást támogató és hozzáférhető vizuális rendszer.

## 1. Vizuális narratíva

1. **Rendszer, nem hőskép:** a nyitó vizuál az államszervezés összetevőit mutatja, nem idealizált uralkodóportrét.
2. **Folyamat:** 955-től Géza politikáján át István intézményépítéséig időbeli ív épül.
3. **Hálózat:** az egyház és a világi igazgatás külön, majd összekapcsolt rendszerként látszik.
4. **Forráskritika:** oklevél, monogram, palást és szarkofág esetében a tárgy kora, műfaja, őrzése és reprezentációs funkciója szerepel.
5. **Tér:** a helyek sematikus, adatalapú, nem AI-generált térképen jelennek meg; a bizonytalan határokat nem ábrázoljuk éles vonallal.
6. **Összegzés:** idővonal és topográfiai áttekintés támogatja az érettségi felidézést.

## 2. Kötelező vizuális témák és megoldásuk

| Téma | Követelmény | Tiltott megoldás |
|---|---|---|
| Géza | kortárs portré hiányának közlése; szöveges/dinasztikus diagram | AI-portré vagy későbbi kép korjelölés nélkül |
| István | 1031-es palást ábrázolása mint reprezentáció; pontos tárgyleírás | fotórealisztikus arcrekonstrukció; mai korona István koronájaként |
| Koppány | nem figuratív konfliktusdiagram; rokonsági óvatosság | AI-portré, romantikus történeti kép tényillusztrációként |
| koronázás | legitimációs folyamatábra és palást; kettős datálás | vitatott helyszín biztos térképpontként; AI-korona |
| korai királyság | saját, reviewer által jóváhagyott sematikus térkép | tankönyvi térkép másolata; mesterségesen generált történelmi térkép |
| vármegyék | hálózati elv, becsült szám és első megye nélkül | pontosnak látszó, forrásolatlan megyehatárok |
| egyházmegyék | hierarchia és biztos központok; vitatott sorrend nélkül | forrásolatlan teljes alapítási térkép |
| Pannonhalma | CC-fotó és PD oklevél, külön funkcióval | képaláírás nélküli hangulatkép |
| Esztergom | mai helyszínfotó, mai épületként jelölve | a mai bazilika István kori épületként |
| Székesfehérvár | szarkofág és emlékezet; koronázási hely nincs lezárva | vitatott helyszín biztos tényként |
| törvény és Intelmek | forrásműfaji kártya; kézirat csak tisztázott reprodukciós joggal | díszítő kéziratkép forrásadat nélkül |
| ereklye és szentté avatás | csak intézményi vagy hiteles CC/PD kép, vallási érzékenységgel | szenzációs, kontextus nélküli tárgykép |

## 3. Stílus és adatvizualizáció

- Saját ábrák SVG-formátumban, 16:9 vagy reszponzív viewBox kialakítással készülnek.
- A szín csak másodlagos jel: minden csomópont szöveges címkét és szükség esetén alakjelölést kap.
- A „biztos”, „eltérő forrás” és „nem elfogadható állítás” három külön ikon- és szövegcímkét kap; piros–zöld pár önmagában nem használható.
- Térképen és idővonalon minden jelmagyarázat a vizuál előtt vagy közvetlenül utána olvasható.
- Nem használunk dekoratív címert, zászlót vagy koronát történeti bizonyítékként.
- Képkivágás nem változtathatja meg a tárgy jelentését; minden kivágás dokumentálandó.

## 4. Hozzáférhetőségi követelmények

- Minden információhordozó képnek tanulási funkciót leíró alt szövege van.
- Összetett diagramhoz hosszú leírás tartozik, amely megnevezi a csomópontokat, kapcsolatokat és a levonható következtetést.
- Díszítő elem üres altot kap, és nem ismétel szöveges információt.
- Minimum 4,5:1 szövegkontraszt, 3:1 nagy szöveg és grafikai vezérlő esetén.
- 200% zoomnál és 320 CSS px szélességnél nincs információvesztés vagy vízszintes görgetés.
- A vizuálra épülő feladatnak teljes értékű szöveges vagy kattintásos alternatívája van.
- A képaláírás tartalmazza a tárgyat, kort, őrzőhelyet, alkotót/fotóst, licencet és azt, ha a kép későbbi reprezentáció.

## 5. Technikai elfogadás

- Raszter: WebP vagy JPEG, legalább 1600 px hosszabb oldal, célméret legfeljebb 500 KB, kivéve indokolt forrásnagyítás.
- Dokumentumrészlet: veszteségmentes PNG/WebP, olvasható nagyítással; teljes dokumentumhoz leírás.
- SVG: beágyazott script, külső font és követőkód nélkül; szöveg Unicode HU; biztonsági tisztítás kötelező.
- Minden asset relatív csomagútvonalon töltődik, nincs hotlink vagy runtime külső kérés.
- Minden forrás- és licencmező, eredeti és származék SHA-256 rendelkezésre áll.
- Vizuális regresszió 1440×900, 1280×720, 390×844, 320 px és 200% zoom nézetben.

## 6. Jóváhagyási sorrend

Történész review → jogi/licenc review → instructional review → accessibility review → technikai optimalizálás → hash és attribúció rögzítése → `APPROVED_FOR_BUILD`. Bármely tartalmi vagy forrásváltozás visszaállítja az érintett assetet review státuszba.

