#!/usr/bin/env python3
"""Build the approved GSI-02 Interactive Book from the repository documentation."""

from __future__ import annotations

import copy
import hashlib
import html
import json
import pathlib
import re
import shutil
import tempfile
import uuid
import zipfile

import build_discoveries_h5p as core


ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "DTEA/06_Master_Scripts/geza-fejedelem-szent-istvan/MASTER_SCRIPT.md"
ATHENS = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p"
ASSET_DIR = ROOT / "assets/h5p/geza-istvan"
OUTPUT = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-geza-fejedelem-szent-istvan-v1.0.h5p"

core.UID_NAMESPACE = uuid.UUID("357775e0-9a37-46d5-93ea-9f12bf4cd90d")
core._uid_counter = 0


VISUALS = {
    10: ("stephen-coronation-pall.jpg", "I. István ábrázolása az 1031-ben készült koronázási paláston."),
    11: ("kingdom-hungary-1000.svg", "A Magyar Királyság területének szemléltető térképe 1000 körül."),
    15: ("pannonhalma-charter.jpg", "A pannonhalmi monostor 1002-re keltezett alapítólevelének képe."),
    22: ("stephen-monogram.svg", "I. István király oklevélben fennmaradt monogramja."),
    28: ("hungary-11th-century.png", "A Magyar Királyság 11. századi területi viszonyait szemléltető térkép."),
}

VISUAL_CREDITS = {
    10: ("Portrayal of Stephen I on the coronation pall", "1031-es koronázási palást", "Public Domain", "https://commons.wikimedia.org/wiki/File:Portrayal_of_Stephen_I,_King_of_Hungary_on_the_coronation_pall.jpg"),
    11: ("Kingdom of Hungary 1000", "Alphathon", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Kingdom_of_Hungary_1000.svg"),
    15: ("Pannonhalmi alapítólevél", "Magyar Nemzeti Levéltár", "Public Domain", "https://commons.wikimedia.org/wiki/File:Pannonhalmi_alapítólevél.jpg"),
    22: ("King Saint Stephen signature", "Wikimedia Commons", "Public Domain", "https://commons.wikimedia.org/wiki/File:King_Saint_Stephen_signature.svg"),
    28: ("Hungary 11th cent hu", "Wikimedia Commons", "CC0 1.0", "https://commons.wikimedia.org/wiki/File:Hungary_11th_cent_hu.png"),
}


def choice(question: str, options: list[str], correct: list[int]) -> dict:
    return {"kind": "choice", "question": question, "options": options, "correct": correct}


def pair(task: str, pairs: list[tuple[str, str]]) -> dict:
    return {"kind": "pair", "task": task, "pairs": pairs}


def order(task: str, values: list[str]) -> dict:
    return {"kind": "order", "task": task, "values": values}


def category(task: str, groups: list[tuple[str, list[str]]]) -> dict:
    return {"kind": "category", "task": task, "groups": groups}


INTERACTIONS = {
    1: choice("Jelöld ki a tartósan működő középkori királyság négy közvetlen összetevőjét!", ["adó- és birtokbevétel", "területi igazgatás", "egyházi szervezet", "törvény és fegyveres erő", "kizárólag zsákmányszerző portya", "csak személyes hírnév"], [0, 1, 2, 3]),
    2: category("Rendezd az elemeket a megfelelő csoportba!", [("Korábbi működéshez kapcsolódik", ["zsákmányszerző hadjárat", "személyes hűség", "alkalmi katonai szövetség"]), ("Tartós államszervezéshez szükséges", ["rendszeres bevétel", "területi hivatal", "írott törvény"])]),
    3: order("Tedd logikus sorrendbe az oksági lánc elemeit!", ["nyugati katonai fölény erősödése", "a korábbi portyázó stratégia kockázata nő", "új diplomáciai és hatalmi megoldások keresése", "Géza nyugati kapcsolatfelvétele"]),
    4: pair("Párosítsd a célokat az eszközökkel!", [("nyugati béke és elismerés", "követküldés"), ("fejedelmi hatalom erősítése", "riválisok korlátozása"), ("dinasztikus kapcsolat", "házassági politika"), ("keresztény orientáció", "térítők fogadása")]),
    5: choice("Melyik állítás a legpontosabb?", ["972 és 973 ugyanannak az egyetlen napnak két téves dátuma.", "A kapcsolatfelvétel folyamatában 972-es kezdeményezés és 973-as követjárás különíthető el.", "Quedlinburgban azonnal létrejött a magyar királyság."], [1]),
    6: choice("Válaszd ki a két megalapozott következtetést!", ["a térítés külpolitikai kapcsolatot is erősített", "a nyugati lovagok belpolitikai támaszt is adhattak", "minden magyar azonnal keresztény lett", "a vallásnak nem volt köze a hatalomhoz"], [0, 1]),
    7: choice("A dinasztikus házasság a középkorban nem csupán családi esemény, hanem…", ["politikai kapcsolat és erőforrás", "automatikus területi egyesítés", "vallástól független magánügy"], [0]),
    8: pair("Párosítsd az öröklési elvet a meghatározásával!", [("seniorátus", "a dinasztia legidősebb alkalmas férfitagja"), ("primogenitúra", "az uralkodó elsőszülött fia")]),
    9: choice("Válaszd ki a konfliktus három indokolt tényezőjét!", ["eltérő öröklési elv", "területi hatalmi verseny", "keresztény nyugati kapcsolatok", "kizárólag személyes sértődés", "19. századi nemzetállami program"], [0, 1, 2]),
    10: category("Rendezd az állításokat bizonyíthatóságuk szerint!", [("Biztos mag", ["István királlyá koronázása az ezredfordulón", "a koronázás legitimáló szerepe"]), ("Eltérő vagy ellenőrzendő részlet", ["a pontos nap kettős hagyománya", "a helyszín eltérő megadása"]), ("Nem elfogadható állítás", ["a mai Szent Korona biztos tárgyi azonossága István koronájával"])]),
    11: order("Rendezd a területi hatalom átalakításának lépéseit!", ["regionális hatalmi központ", "fegyveres legyőzés", "királyi tisztségviselők és egyházi szervezet", "rendszeresebb területi ellenőrzés"]),
    12: category("Helyezd el Géza és István politikájának elemeit!", [("Géza", []), ("Közös", ["nyugati kapcsolatok", "térítés támogatása", "dinasztikus politika"]), ("István", ["koronázott királyi rang", "vármegyerendszer"])]),
    13: choice("Melyik magyarázat a legerősebb?", ["A latin kereszténység csak vallási szertartást adott.", "A latin orientáció vallási, diplomáciai, írásbeli és szervezeti kapcsolatokat együtt kínált.", "A választás után minden bizánci kapcsolat megszűnt."], [1]),
    14: pair("Párosítsd az egyházi szintet a szerepével!", [("érsek", "több egyházmegyét összefogó vezető"), ("püspök", "egy egyházmegye vezetője"), ("plébániai templom", "helyi vallási központ")]),
    15: choice("Válaszd ki a monostorok négy történeti funkcióját!", ["vallási közösség", "írásbeliség", "gazdálkodás", "kulturális kapcsolat", "modern parlament", "kizárólag katonai erőd"], [0, 1, 2, 3]),
    16: choice("Melyik következtetés helyes?", ["A törvény bizonyítja, hogy minden faluban azonnal állt templom.", "A törvény megmutatja az uralkodói célt, de a végrehajtást külön bizonyítékokkal kell vizsgálni.", "A tized katonai szolgálat volt."], [1]),
    17: pair("Kösd össze a világi államszervezet elemeit a szerepükkel!", [("király", "legfőbb hatalom"), ("tanács", "döntés-előkészítés"), ("ispán", "területi királyi megbízott"), ("vár", "katonai és gazdasági központ")]),
    18: choice("Jelöld a pontos állítást!", ["A vármegye és a várispánság minden részletében azonos.", "A vármegye területi igazgatási, a várispánság várhoz kötődő katonai-gazdasági szervezet; szorosan összekapcsolódtak.", "Az ispán a pápa megbízottja volt."], [1]),
    19: pair("Párosítsd a fogalmat a szerepével!", [("várjobbágy", "katonai szolgálat és vezető szerep"), ("várnép", "termelő és ellátó szolgáltatás"), ("ispán", "királyi vezető a helyi szervezet élén")]),
    20: choice("Melyik állítás anakronisztikus?", ["A király előkelőkkel tanácskozott.", "A tanács egyházi és világi tagokat fogott össze.", "A tanács általános választójog alapján működő parlament volt."], [2]),
    21: order("Egészítsd ki a királyi birtok működésének láncát!", ["királyi földbirtok", "termény és szolgáltatás", "udvar, vár és hadszervezet fenntartása", "királyi hatalom érvényesítése"]),
    22: category("Csoportosítsd a fogalmakat szerepük szerint!", [("Bevétel", ["vám", "bírság", "pénzverési haszon"]), ("Jogrögzítés és hitelesítés", ["oklevél", "monogram", "pecsét"])]),
    23: choice("Mi a felsorolt törvényi előírások közös célja?", ["a keresztény intézmény és gyakorlat megszilárdítása", "a kalandozások újraindítása", "a vármegyék megszüntetése"], [0]),
    24: {"kind": "truefalse", "question": "A tulajdon és személy elleni erőszak királyi büntetése azt jelzi, hogy a központi hatalom igényt tartott a rend szabályozására.", "correct": True},
    25: category("Döntsd el, mit támogat közvetlenül a törvény szövege!", [("Közvetlenül támogatja", ["a király templomhálózatot akart", "a közösségekre kötelezettséget rótt"]), ("Nem bizonyítja önmagában", ["minden templom azonnal felépült", "minden lakos személyes hite azonos volt"])]),
    26: choice("Melyik leírás pontos?", ["Az Intelmek modern alkotmány.", "Az Intelmek uralkodói erényeket és kormányzási elveket közvetítő királytükör.", "Az Intelmek Koppány hadinaplója."], [1]),
    27: order("Rendezd időrendbe az eseményeket!", ["1031 – Imre halála", "1038 – István halála", "1083 – István szentté avatása"]),
    28: pair("Párosítsd az évszámokat és helyeket a hozzájuk tartozó eseménnyel vagy szereplővel!", [("955", "Augsburg"), ("973", "Quedlinburg"), ("997", "Koppány fellépése"), ("1038", "István halála"), ("1083", "szentté avatás"), ("Gyula", "Erdély"), ("Ajtony", "Maros vidéke"), ("Koppány", "Somogy"), ("monostor", "Pannonhalma")]),
    29: order("Rendezd a felelet tematikus blokkjait!", ["kiinduló helyzet 955 után", "Géza diplomáciája és dinasztikus politikája", "utódlási konfliktus és koronázás", "egyház- és vármegyeszervezet", "törvények és erőforrások", "utódlás és örökség"]),
}


FINAL_QUESTIONS = [
    ("Kronológia", "Válaszd ki a két helyes párt!", ["955 – Augsburg", "973 – Quedlinburg", "997 – István szentté avatása", "1038 – Imre halála"], [0, 1]),
    ("Öröklési elvek", "Válaszd ki a két helyes fogalom-meghatározás párt!", ["seniorátus – a dinasztia legidősebb alkalmas férfitagjának elsőbbsége", "primogenitúra – az uralkodó elsőszülött fiának elsőbbsége", "seniorátus – kizárólag apáról fiúra öröklés", "primogenitúra – az összes felnőtt rokon közös uralma"], [0, 1]),
    ("Géza politikája", "Válaszd ki Géza két jellemző politikai eszközét!", ["nyugati diplomácia", "dinasztikus házasság", "a kész vármegyerendszer teljes kiépítése", "az 1083-as szentté avatás"], [0, 1]),
    ("Koppány konfliktusa", "Válaszd ki Koppány és István küzdelmének két tényezőjét!", ["öröklési elvek ütközése", "területi hatalmi verseny", "modern nemzeti pártok küzdelme", "ipari erőforrások versenye"], [0, 1]),
    ("Koronázás és forráskritika", "Jelöld a két helyes állítást!", ["a koronázás az ezredfordulón történt", "a koronázás legitimálta a királyi rangot", "a helyszín minden vizsgált forrásban azonos", "a mai Szent Korona bizonyosan azonos István koronájával"], [0, 1]),
    ("Egyházszervezet", "Válaszd ki a két helyes fogalom-meghatározás párt!", ["érsekség – több egyházmegyét összefogó központ", "püspökség – egy egyházmegye vezetési egysége", "érsekség – helyi katonai vár", "püspökség – királyi adónem"], [0, 1]),
    ("Világi szervezet", "Válaszd ki az ispán két jellemző szerepét!", ["a király területi képviselete", "helyi bíráskodás és jövedelemszedés", "pápaválasztás", "a szerzetesi regula megalkotása"], [0, 1]),
    ("Várnépek és várjobbágyok", "Válaszd ki a két helyes fogalom-szerep párt!", ["várjobbágy – katonai szolgálat és vezető szerep", "várnép – termelő és ellátó szolgáltatás", "várjobbágy – kizárólag egyházi tisztség", "várnép – királyválasztó testület"], [0, 1]),
    ("Törvény mint forrás", "Válaszd ki a két indokolt következtetést!", ["az uralkodó helyi templomhálózatot akart", "közösségi kötelezettséget írt elő", "minden templom azonnal elkészült", "minden lakos hite azonos volt"], [0, 1]),
    ("Folytonosság és változás", "Válaszd ki a folytonosság és a változás helyes elemét!", ["folytonosság: a nyugati orientáció vagy a központi hatalom erősítése", "változás: a királyi rang és a területi intézményrendszer", "folytonosság: a kalandozások változatlan fenntartása", "változás: a fejedelmi hatalom teljes megszüntetése"], [0, 1]),
]


DIAGRAMS = {
    1: ("Az államszervezés rendszere", ["bevétel", "területi igazgatás", "egyház", "törvény és fegyveres erő"]),
    7: ("Dinasztikus kapcsolatok", ["Sarolt – erdélyi Gyula családja", "Vajk / István – Géza fia", "Gizella – bajor hercegi család"]),
    9: ("A konfliktus tényezői", ["öröklési elv", "területi hatalom", "vallási-politikai orientáció"]),
    12: ("Folytonosság és változás", ["Géza: előkészítés", "közös: nyugati kapcsolatok és centralizáció", "István: királyi rang és intézmények"]),
    13: ("A latin orientáció kapcsolatai", ["egyház", "diplomácia", "írásbeliség", "szervezeti minták"]),
    14: ("Egyházi hierarchia", ["érsek", "püspök", "helyi templom"]),
    17: ("A világi szervezet", ["király", "tanács", "ispán", "vár"]),
    21: ("A királyi birtok működése", ["földbirtok", "termény és szolgáltatás", "udvar, vár, hadszervezet", "hatalomgyakorlás"]),
}


def field(body: str, label: str, default: str = "") -> str:
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\*\*|\n###|$)", body, re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else default


def learner_text(body: str, number: int) -> str:
    heading = "Tanulói instrukció" if number == 30 else "Tanulói szöveg"
    match = re.search(rf"### {heading}\s*(.+?)(?=\n### |\n---|$)", body, re.S)
    if not match:
        raise ValueError(f"Hiányzó tanulói szöveg: pg-{number:03d}")
    return match.group(1).strip()


def page_map(master: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(
        r"^## `geza-fejedelem-szent-istvan--pg-(\d{3})`\s+[–-]\s+(.+)$",
        master,
        re.M,
    ))
    pages = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(master)
        pages.append((int(match.group(1)), match.group(2).strip(), master[match.end():end].strip()))
    return pages


def interaction_block(body: str) -> str:
    match = re.search(r"### Interakció[^\n]*\s*(.+?)(?=\n---|$)", body, re.S)
    return match.group(1).strip() if match else ""


def mark_formative(component: dict, number: int) -> dict:
    component["metadata"]["title"] = f"int-{number:03d}"
    component["metadata"]["dteaFormative"] = True
    return component


def make_choice(templates: dict[str, dict], title: str, spec: dict, correct_feedback: str, wrong_feedback: str, *, formative: bool = True) -> dict:
    component = core.clone_template(templates, "H5P.MultiChoice 1.16", title)
    correct = set(spec["correct"])
    component["params"]["question"] = f"<p>{html.escape(spec['question'])}</p>"
    component["params"]["answers"] = [
        {
            "text": html.escape(option),
            "correct": index in correct,
            "tipsAndFeedback": {
                "tip": "",
                "chosenFeedback": correct_feedback if index in correct else wrong_feedback,
                "notChosenFeedback": "",
            },
        }
        for index, option in enumerate(spec["options"])
    ]
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({
        "enableRetry": True,
        "enableSolutionsButton": True,
        "enableCheckButton": True,
        "type": "multi" if len(correct) > 1 else "single",
        "singlePoint": len(correct) == 1,
        "showSolutionsRequiresInput": True,
        "randomAnswers": False,
    })
    core.localize_multichoice(component)
    if formative:
        component["metadata"]["dteaFormative"] = True
    return component


def make_sort(templates: dict[str, dict], title: str, spec: dict, correct_feedback: str, wrong_feedback: str) -> dict:
    component = core.clone_template(templates, "H5P.SortParagraphs 0.11", title)
    component["params"]["taskDescription"] = f"<p>{html.escape(spec['task'])}</p>"
    component["params"]["paragraphs"] = spec["values"]
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({
        "enableRetry": True,
        "enableSolutionsButton": True,
        "enableCheckButton": True,
        "addButtonsForMovement": True,
    })
    component["params"]["l10n"].update({
        "checkAnswer": "Ellenőrzés", "showSolution": "Megoldás megtekintése", "tryAgain": "Újrapróbálkozás",
        "up": "Fel", "down": "Le", "disabled": "Letiltva", "scoreBarLabel": "Elért pont: :num / :total",
    })
    component["metadata"]["dteaFormative"] = True
    return component


def make_category(templates: dict[str, dict], title: str, spec: dict, correct_feedback: str, wrong_feedback: str) -> dict:
    component = core.clone_template(templates, "H5P.DragQuestion 1.14", title)
    entries: list[tuple[str, int]] = []
    for zone_index, (_, values) in enumerate(spec["groups"]):
        entries.extend((value, zone_index) for value in values)
    elements = []
    for index, (value, zone_index) in enumerate(entries):
        row, col = divmod(index, 3)
        elements.append({
            "type": core.text_component(value, f"<p>{html.escape(value)}</p>", raw_html=True),
            "x": 2 + col * 32.5, "y": 2 + row * 10.5, "height": 9, "width": 30,
            "dropZones": [zone_index], "backgroundOpacity": 100, "multiple": False,
        })
    zone_count = len(spec["groups"])
    zone_width = 94 / zone_count
    zones = []
    for zone_index, (label, _) in enumerate(spec["groups"]):
        zones.append({
            "label": label, "showLabel": True, "x": 2 + zone_index * zone_width, "y": 52,
            "height": 44, "width": zone_width - 2,
            "correctElements": [index for index, (_, target) in enumerate(entries) if target == zone_index],
            "backgroundOpacity": 100, "single": False, "autoAlign": True,
            "tipsAndFeedback": {"feedbackOnCorrect": correct_feedback, "feedbackOnIncorrect": wrong_feedback},
        })
    component["params"]["question"] = {
        "settings": {"size": {"width": 960, "height": max(640, 360 + len(entries) * 42)}},
        "task": {"elements": elements, "dropZones": zones},
    }
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({
        "enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True, "singlePoint": False,
        "applyPenalties": False, "enableScoreExplanation": False, "enableFullScreen": False,
        "showScorePoints": False,
    })
    core.localize_drag(component)
    component["metadata"]["dteaFormative"] = True
    return component


def make_true_false(templates: dict[str, dict], title: str, spec: dict, correct_feedback: str, wrong_feedback: str) -> dict:
    component = core.clone_template(templates, "H5P.TrueFalse 1.8", title)
    component["params"]["question"] = f"<p>{html.escape(spec['question'])}</p>"
    component["params"]["correct"] = "true" if spec["correct"] else "false"
    component["params"]["l10n"].update({
        "correctAnswerMessage": correct_feedback, "wrongAnswerMessage": wrong_feedback,
        "trueText": "Igaz", "falseText": "Hamis", "score": "Elért pont: @score / @total",
        "checkAnswer": "Ellenőrzés", "submitAnswer": "Beküldés",
        "showSolutionButton": "Megoldás megtekintése", "tryAgain": "Újrapróbálkozás",
        "wrongAnswer": "Helytelen válasz", "correctAnswer": "Helyes válasz",
        "scoreBarLabel": "Elért pont: :num / :total", "a11yCheck": "A válasz ellenőrzése.",
        "a11yShowSolution": "A megoldás megtekintése.", "a11yRetry": "A feladat újrapróbálása.",
    })
    component["params"]["behaviour"].update({
        "enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True,
        "feedbackOnCorrect": correct_feedback, "feedbackOnWrong": wrong_feedback,
    })
    component["metadata"]["dteaFormative"] = True
    return component


def make_interaction(templates: dict[str, dict], number: int, body: str) -> dict:
    spec = INTERACTIONS[number]
    block = interaction_block(body)
    feedback = field(block, "Feedback", "Helyes. A kapcsolatokat pontosan azonosítottad.")
    common_error = field(block, "Gyakori hiba", "Nézd át újra az oldal magyarázatát.")
    correct_feedback = f"Helyes. {feedback}"
    wrong_feedback = f"Még nem teljesen helyes. {common_error}"
    title = f"int-{number:03d} – Önellenőrzés"
    if spec["kind"] == "choice":
        component = make_choice(templates, title, spec, correct_feedback, wrong_feedback)
    elif spec["kind"] == "pair":
        component = core.drag_pairs(templates, title, spec["task"], spec["pairs"], correct_feedback, wrong_feedback)
        component["params"]["behaviour"]["enableSolutionsButton"] = True
        component["metadata"]["dteaFormative"] = True
    elif spec["kind"] == "order":
        component = make_sort(templates, title, spec, correct_feedback, wrong_feedback)
    elif spec["kind"] == "category":
        component = make_category(templates, title, spec, correct_feedback, wrong_feedback)
    elif spec["kind"] == "truefalse":
        component = make_true_false(templates, title, spec, correct_feedback, wrong_feedback)
    else:
        raise ValueError(f"Ismeretlen interakciótípus: {spec['kind']}")
    return mark_formative(component, number)


def concept_diagram(number: int) -> dict:
    title, values = DIAGRAMS[number]
    items = "".join(f"<li>{html.escape(value)}</li>" for value in values)
    body = (
        f'<section class="dtea-concept-diagram" aria-label="{html.escape(title)}">'
        f"<h3>{html.escape(title)}</h3><ol>{items}</ol></section>"
    )
    return core.text_component(title, body, raw_html=True)


def visual_credit(number: int) -> dict:
    title, creator, license_name, url = VISUAL_CREDITS[number]
    body = (
        '<p class="dtea-media-credit"><small>Forrás: '
        f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(title)}</a>'
        f" — {html.escape(creator)}. {html.escape(license_name)}.</small></p>"
    )
    return core.text_component("Kép forrása és licence", body, raw_html=True)


def final_question_set(templates: dict[str, dict], page_body: str) -> dict:
    test_blocks = re.findall(r"### `test-(\d{2})`[^\n]*\s*(.+?)(?=\n### |\n---|$)", page_body, re.S)
    if len(test_blocks) != 10:
        raise ValueError("A záróteszt nem pontosan 10 feladatot tartalmaz.")
    feedback_by_number = {
        int(number): (field(block, "Feedback"), field(block, "Gyakori hiba"))
        for number, block in test_blocks
    }
    questions = []
    for index, (title, question, options, correct) in enumerate(FINAL_QUESTIONS, start=1):
        feedback, common_error = feedback_by_number[index]
        component = make_choice(
            templates,
            f"test-{index:02d} – {title}",
            choice(question, options, correct),
            f"Helyes. {feedback}",
            f"Még nem teljesen helyes. {common_error}",
            formative=False,
        )
        component["metadata"]["dteaFinalTest"] = True
        questions.append(component)
    question_set = core.clone_template(templates, "H5P.QuestionSet 1.20", "Záróteszt – 20 pont")
    question_set["params"]["questions"] = questions
    question_set["params"]["passPercentage"] = 60
    question_set["params"]["introPage"].update({
        "showIntroPage": True,
        "title": "Záróteszt – 20 pont",
        "introduction": "<p>Válaszolj mind a tíz kérdésre! Minden kérdésben két helyes elem összesen 2 pontot ér. A javasolt teljesítési küszöb 12 pont.</p>",
        "startButtonText": "Kezdés",
    })
    core.localize_question_set(question_set)
    question_set["params"]["override"] = {"checkButton": True, "showSolutionButton": "on", "retryButton": "on"}
    question_set["metadata"]["dteaFinalTest"] = True
    return question_set


def build_page(templates: dict[str, dict], number: int, title: str, body: str) -> dict:
    level = field(body, "Szint", "közép + emelt")
    column = [
        {"content": core.text_component(title, f"<h2>{html.escape(title)}</h2>", raw_html=True), "useSeparator": "never"},
        {"content": core.text_component("Szint", f'<p class="dtea-level"><strong>Szint:</strong> {html.escape(level)}</p>', raw_html=True), "useSeparator": "never"},
        {"content": core.text_component("Tananyag", learner_text(body, number)), "useSeparator": "auto"},
    ]
    if number in DIAGRAMS:
        column.append({"content": concept_diagram(number), "useSeparator": "auto"})
    if number in VISUALS:
        filename, alt_text = VISUALS[number]
        column.append({"content": core.visual_component(filename, alt_text), "useSeparator": "auto"})
        column.append({"content": visual_credit(number), "useSeparator": "never"})
    if number == 30:
        column.append({"content": final_question_set(templates, body), "useSeparator": "auto"})
    else:
        column.append({"content": make_interaction(templates, number, body), "useSeparator": "auto"})
    return {
        "library": "H5P.Column 1.18",
        "params": {"content": column},
        "metadata": {**core.metadata(title, "Oldal"), "extraTitle": title, "dteaPageId": f"geza-fejedelem-szent-istvan--pg-{number:03d}"},
        "subContentId": core.uid(),
    }


def patch_book_score_to_final_chapter(temp: pathlib.Path) -> None:
    """Keep formative raw points, but expose only the 20-point final test as book score."""
    path = temp / "H5P.InteractiveBook-1.11/dist/h5p-interactive-book.js"
    source = path.read_text(encoding="utf-8")
    old_score = 'c.getScore=function(){return c.chapters.length>0?c.chapters.reduce((function(t,e){return"function"==typeof e.instance.getScore?t+e.instance.getScore():t}),0):c.previousState&&c.previousState.score||0}'
    new_score = 'c.getScore=function(){var t=c.chapters[c.chapters.length-1];return t&&"function"==typeof t.instance.getScore?t.instance.getScore():c.previousState&&c.previousState.score||0}'
    old_max = 'c.getMaxScore=function(){return c.chapters.length>0?c.chapters.reduce((function(t,e){return"function"==typeof e.instance.getMaxScore?t+e.instance.getMaxScore():t}),0):c.previousState&&c.previousState.maxScore||0}'
    new_max = 'c.getMaxScore=function(){var t=c.chapters[c.chapters.length-1];return t&&"function"==typeof t.instance.getMaxScore?t.instance.getMaxScore():c.previousState&&c.previousState.maxScore||0}'
    if source.count(old_score) != 1 or source.count(old_max) != 1:
        raise ValueError("Az Interactive Book pontozási illesztési pontja megváltozott.")
    source = source.replace(old_score, new_score).replace(old_max, new_max)
    source += "\n/* DTEA GSI-02: book score is the final chapter QuestionSet only. */\n"
    path.write_text(source, encoding="utf-8")


def main() -> None:
    master = MASTER.read_text(encoding="utf-8")
    pages = page_map(master)
    if len(pages) != 30 or [number for number, _, _ in pages] != list(range(1, 31)):
        raise SystemExit("A Master Script oldaltérképe nem pontosan 1–30.")

    with zipfile.ZipFile(ATHENS) as source:
        manifest = json.loads(core.zip_read_normalized(source, "h5p.json"))
        athens_content = json.loads(core.zip_read_normalized(source, "content/content.json"))
        templates: dict[str, dict] = {}

        def collect(value) -> None:
            if isinstance(value, dict):
                library = value.get("library")
                if library and library not in templates:
                    templates[library] = value
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(athens_content)
        required = {"H5P.AdvancedText 1.1", "H5P.Column 1.18", "H5P.DragQuestion 1.14", "H5P.Image 1.1", "H5P.MultiChoice 1.16", "H5P.QuestionSet 1.20", "H5P.SortParagraphs 0.11", "H5P.TrueFalse 1.8"}
        missing = required - set(templates)
        if missing:
            raise SystemExit(f"Hiányzó sablonlibrary: {sorted(missing)}")

        content = {
            "showCoverPage": False,
            "cover": None,
            "chapters": [build_page(templates, number, title, body) for number, title, body in pages],
            "behaviour": copy.deepcopy(athens_content.get("behaviour", {})),
            "read": "Megnyitás", "displayTOC": "Tartalomjegyzék megjelenítése", "hideTOC": "Tartalomjegyzék elrejtése",
            "nextPage": "Következő", "previousPage": "Előző", "chapterCompleted": "Oldal teljesítve!",
            "partCompleted": "@pages / @total oldal teljesítve", "incompleteChapter": "Befejezetlen oldal",
            "navigateToTop": "Vissza az oldal tetejére", "markAsFinished": "Befejeztem ezt az oldalt",
            "fullscreen": "Teljes képernyő", "exitFullscreen": "Kilépés a teljes képernyőből",
            "bookProgressSubtext": "@count / @total oldal", "interactionsProgressSubtext": "@count / @total feladat",
            "submitReport": "Beküldés", "restartLabel": "Újrakezdés", "summaryHeader": "Összegzés",
            "allInteractions": "Minden feladat", "unansweredInteractions": "Megválaszolatlan feladatok",
            "scoreText": "@score / @maxscore", "leftOutOfTotalCompleted": "@left / @max feladat teljesítve",
            "noInteractions": "Nincs feladat", "score": "Pontszám", "summaryAndSubmit": "Összegzés és beküldés",
            "noChapterInteractionBoldText": "Még nem oldottál meg feladatot.",
            "noChapterInteractionText": "Az összegzéshez előbb oldj meg legalább egy feladatot.",
            "yourAnswersAreSubmittedForReview": "A válaszaid beküldve.", "bookProgress": "Haladás a könyvben",
            "interactionsProgress": "Haladás a feladatokban", "totalScoreLabel": "Összpontszám",
            "a11y": {"progress": "@page. oldal / @total.", "menu": "Navigációs menü megnyitása vagy bezárása"},
        }
        content["behaviour"].update({"displaySummary": False, "defaultTableOfContents": True})
        manifest.update({
            "title": "Géza fejedelem és I. (Szent) István",
            "language": "hu",
            "authors": [{"name": "Digitális Történelem Érettségi Akadémia", "role": "Author"}],
            "license": "CC BY-NC-SA",
            "version": "1.0.0",
        })

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = pathlib.Path(temp_dir)
            core.extract_normalized(source, temp)
            shutil.rmtree(temp / "content", ignore_errors=True)
            (temp / "content/images").mkdir(parents=True)
            for filename, _ in VISUALS.values():
                source_asset = ASSET_DIR / filename
                if not source_asset.is_file():
                    raise SystemExit(f"Hiányzó tanulói vizuális asset: {source_asset}")
                shutil.copy2(source_asset, temp / "content/images" / filename)
            patch_book_score_to_final_chapter(temp)
            (temp / "content/content.json").write_text(json.dumps(content, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            (temp / "h5p.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as target:
                for path in sorted(temp.rglob("*")):
                    if path.is_file():
                        name = path.relative_to(temp).as_posix()
                        info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                        info.compress_type = zipfile.ZIP_DEFLATED
                        info.external_attr = 0o100644 << 16
                        target.writestr(info, path.read_bytes())

    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"Elkészült: {OUTPUT}")
    print(f"Oldalak: {len(pages)}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
