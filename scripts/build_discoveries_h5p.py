#!/usr/bin/env python3
"""Build the approved Földrajzi felfedezések Master Script as a Lumi-compatible H5P book.

The Athens package is used only as a library/runtime carrier. Its learning content and
media are not copied into the generated book.
"""

from __future__ import annotations

import copy
import html
import json
import pathlib
import re
import shutil
import tempfile
import uuid
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/master-scripts/dtea-foldrajzi-felfedezesek-master-script-v1.0.2.md"
ATHENS = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p"
OUTPUT = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-foldrajzi-felfedezesek-v1.0.h5p"
ASSET_DIR = ROOT / "assets/h5p/discoveries"

EXCLUDED_SECTIONS = {
    "Vizuális brief", "UX", "UX és vizuál", "Elfogadási feltétel",
    "Oldalszintű forrás- és státuszmetaadat", "Média placeholder",
    "Média státusza", "Vizuális és a11y", "Vizuális elv", "Teszt QA",
    "Végleges záróteszt-mátrix", "Tanári megjegyzés", "Akadálymentes alternatíva",
    "Szöveges alternatíva", "Kép- és hotspotterv", "Értékelés", "Pontozás",
    "Visszajelzés", "Oldalvégi visszajelzés", "Mobilalternatíva",
}

HIDDEN_SECTION_HEADINGS = {"Tanulói szöveg", "Megjelenő szöveg", "Bevezető"}
SECTION_TITLES = {
    "Accordion": "Részletek",
    "Dialog Cards": "Fogalomkártyák",
    "Single Choice Set": "Önellenőrzés",
    "Hotspotok": "A hajózás eszközei",
    "Hotspotok és lineáris alternatíva": "Az út állomásai",
    "Mini idővonal": "Az expedíció állomásai",
    "Használati utasítás": "Hogyan használd?",
    "Tágabb témaköri jelzés": "Kitekintés",
    "Szintjelölés": "Kitekintés",
}

VISUALS = {
    1: ("cover-atlantic-routes.webp", "Stilizált atlanti térkép tengeri útvonalakkal és egy 15. századi karavellával."),
    5: ("navigation-tools.svg", "A karavella, az iránytű, az asztrolábium, valamint a térkép és a hajózási tudás sematikus ábrája."),
    7: ("martellus-world-map-1489.jpg", "Henricus Martellus 1489 körül készült világtérképe; Afrika déli partvidéke és a Jóreménység foka térsége."),
    8: ("cantino-planisphere-1502.jpg", "Az 1502-es Cantino-planiszféra; az Afrika megkerülésével Indiába vezető portugál tengeri tér ismerete."),
    9: ("juan-de-la-cosa-map-1500.jpg", "Juan de la Cosa 1500-ban készült világtérképe, amely az európai térképezésben korán ábrázolja Amerikát."),
    10: ("ribero-world-map-1529.jpg", "Diego Ribero 1529-es világtérképe, amely a tordesillasi megállapodás szerinti spanyol és portugál érdekszférákra utal."),
    11: ("agnese-world-map-1544.jpg", "Battista Agnese 1544-es világtérképe, rajta a Magellán–Elcano-expedíció Föld körüli útvonalával."),
    24: ("ribero-world-map-1529.jpg", "Diego Ribero 1529-es világtérképe a nagy földrajzi felfedezések korának új földrajzi ismereteivel."),
}

VISUAL_CREDITS = {
    7: ("Henricus Martellus világtérképe, kb. 1489", "Yale University Library / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:Henricus_Martellus_-_Map_of_the_world_-_1489_-_Yale_archive.jpg"),
    8: ("Cantino-planiszféra, 1502", "Biblioteca Estense, Modena / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:Cantino_planisphere_(1502).jpg"),
    9: ("Juan de la Cosa világtérképe, 1500", "Museo Naval de Madrid / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:1500_map_by_Juan_de_la_Cosa_rotated.jpg"),
    10: ("Diego Ribero: Carta Universal, 1529", "National Library of Australia / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:Map_Diego_Ribero_1529.jpg"),
    11: ("Battista Agnese világtérképe, 1544", "Library of Congress / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:1544_Battista_Agnese_Worldmap.jpg"),
    24: ("Diego Ribero: Carta Universal, 1529", "National Library of Australia / Wikimedia Commons", "Közkincs", "https://commons.wikimedia.org/wiki/File:Map_Diego_Ribero_1529.jpg"),
}

TECHNICAL_LINE = re.compile(
    r"^\s*\*\*(?:Cél|Kognitív művelet|Elsődleges H5P|Javasolt H5P|Tartalék H5P|"
    r"Pontozás|Pont|Retry|Show Solution|Helyes(?: válasz| sorrend)?|Helyes visszajelzés|"
    r"Hibás visszajelzés|Média státusza|Szakmai státusz|Elfogadási feltétel|QA)[^*]*:\*\*",
    re.I,
)


UID_NAMESPACE = uuid.UUID("fa73b259-19cb-4fef-b625-540fa7d6ea45")
_uid_counter = 0


def uid() -> str:
    """Return deterministic H5P sub-content ids for reproducible CI builds."""
    global _uid_counter
    _uid_counter += 1
    return str(uuid.uuid5(UID_NAMESPACE, f"dtea-foldrajzi-felfedezesek-{_uid_counter}"))


def zip_read_normalized(archive: zipfile.ZipFile, name: str) -> bytes:
    """Read ZIP members portably when Lumi used Windows separators."""
    for member in archive.infolist():
        if member.filename.replace("\\", "/") == name:
            return archive.read(member)
    raise KeyError(f"Hiányzó ZIP-bejegyzés: {name}")


def extract_normalized(archive: zipfile.ZipFile, destination: pathlib.Path) -> None:
    """Extract Lumi packages with POSIX paths on every build platform."""
    for member in archive.infolist():
        normalized = member.filename.replace("\\", "/")
        parts = pathlib.PurePosixPath(normalized).parts
        if not parts or normalized.startswith("/") or ".." in parts:
            raise SystemExit(f"Tiltott ZIP-útvonal: {member.filename}")
        target = destination.joinpath(*parts)
        if member.is_dir() or normalized.endswith("/"):
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(member))


def normalize_quotes(value: str) -> str:
    return value.replace("„", '"').replace("”", '"').strip()


def inline_md(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
    return value


def markdown_to_html(value: str) -> str:
    """Convert the Master Script's limited Markdown subset to safe H5P HTML."""
    lines = value.strip().splitlines()
    out: list[str] = []
    list_tag: str | None = None
    table_rows: list[list[str]] = []

    def close_list() -> None:
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        rows = [row for row in table_rows if not all(re.fullmatch(r":?-+:?", c.strip()) for c in row)]
        if rows:
            out.append("<table><tbody>")
            for row_index, row in enumerate(rows):
                tag = "th" if row_index == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{inline_md(cell.strip())}</{tag}>" for cell in row) + "</tr>")
            out.append("</tbody></table>")
        table_rows = []

    for raw in lines + [""]:
        line = raw.rstrip()
        if line.startswith("|") and line.endswith("|"):
            close_list()
            table_rows.append(line.strip("|").split("|"))
            continue
        flush_table()
        if not line.strip():
            close_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            close_list()
            level = min(4, len(heading.group(1)) + 1)
            out.append(f"<h{level}>{inline_md(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if bullet or numbered:
            tag = "ul" if bullet else "ol"
            if list_tag != tag:
                close_list()
                list_tag = tag
                out.append(f"<{tag}>")
            item = (bullet or numbered).group(1)
            item = re.sub(r"^\[([ xX])\]\s*", lambda m: "☑ " if m.group(1).lower() == "x" else "☐ ", item)
            out.append(f"<li>{inline_md(item)}</li>")
            continue
        close_list()
        if line.startswith(">"):
            out.append(f"<blockquote><p>{inline_md(line.lstrip('> ').strip())}</p></blockquote>")
        else:
            out.append(f"<p>{inline_md(line)}</p>")
    return "".join(out)


def metadata(title: str, content_type: str) -> dict:
    return {
        "contentType": content_type,
        "license": "U",
        "title": title,
        "authors": [],
        "changes": [],
        "defaultLanguage": "hu",
    }


def reuuid(value):
    if isinstance(value, dict):
        result = {key: reuuid(child) for key, child in value.items()}
        if "subContentId" in result:
            result["subContentId"] = uid()
        return result
    if isinstance(value, list):
        return [reuuid(child) for child in value]
    return value


def text_component(title: str, body: str, *, raw_html: bool = False) -> dict:
    return {
        "library": "H5P.AdvancedText 1.1",
        "params": {"text": body if raw_html else markdown_to_html(body)},
        "metadata": metadata(title, "Text"),
        "subContentId": uid(),
    }


def visual_component(filename: str, alt_text: str) -> dict:
    """Embed a portable H5P.Image component with Hungarian controls and alt text."""
    suffix = pathlib.Path(filename).suffix.lower()
    mime = {
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }.get(suffix)
    if mime is None:
        raise ValueError(f"Nem támogatott képformátum: {filename}")
    return {
        "library": "H5P.Image 1.1",
        "params": {
            "file": {"path": f"images/{filename}", "mime": mime},
            "decorative": False,
            "alt": alt_text,
            "title": alt_text,
            "contentName": "Kép",
            "expandImage": "Kép nagyítása",
            "minimizeImage": "Kép kicsinyítése",
        },
        "metadata": metadata("Tanulást segítő ábra", "Kép"),
        "subContentId": uid(),
    }


def visual_credit_component(page_number: int) -> dict:
    """Render the authentic map's source and rights statement below the image."""
    title, collection, license_name, source_url = VISUAL_CREDITS[page_number]
    body = (
        '<p class="dtea-map-credit"><small>'
        f'Forrás: <a href="{html.escape(source_url, quote=True)}" target="_blank" rel="noopener noreferrer">'
        f'{html.escape(title)}</a> — {html.escape(collection)}. {html.escape(license_name)}.'
        '</small></p>'
    )
    return text_component("Térkép forrása és licence", body, raw_html=True)


def clean_student_body(body: str) -> str:
    """Remove authoring/configuration lines from text that can be rendered to learners."""
    lines: list[str] = []
    skipping_table = False
    for raw in body.splitlines():
        line = raw.rstrip()
        if TECHNICAL_LINE.match(line):
            continue
        if re.search(r"\b(?:PLACEHOLDER|KÉSŐBB CSERÉLENDŐ|VIZUÁLIS ELEM)\b", line, re.I):
            continue
        if line.startswith("|") and any(token in line for token in ("Retry", "Show Solution", "Max. pont", "Helyes válasz")):
            skipping_table = True
            continue
        if skipping_table and line.startswith("|"):
            continue
        skipping_table = False
        lines.append(line)
    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"[^.!?\n]*\btanulói szöveg\b[^.!?\n]*[.!?]", "", cleaned, flags=re.I)
    return re.sub(r"[ \t]{2,}", " ", cleaned).strip()


def clone_template(templates: dict[str, dict], library: str, title: str) -> dict:
    component = reuuid(copy.deepcopy(templates[library]))
    component["metadata"]["title"] = title
    component["metadata"]["defaultLanguage"] = "hu"
    component["metadata"]["contentType"] = {
        "H5P.Accordion 1.0": "Részletek",
        "H5P.Blanks 1.14": "Hiányos szöveg",
        "H5P.Dialogcards 1.9": "Fogalomkártyák",
        "H5P.DragQuestion 1.14": "Párosító feladat",
        "H5P.Essay 1.5": "Szöveges válasz",
        "H5P.MultiChoice 1.16": "Feleletválasztás",
        "H5P.QuestionSet 1.20": "Feladatsor",
        "H5P.SortParagraphs 0.11": "Sorrendbe rendezés",
        "H5P.TrueFalse 1.8": "Igaz–hamis feladat",
    }.get(library, component["metadata"].get("contentType", "Feladat"))
    return component


def feedback_pair(body: str) -> tuple[str, str]:
    def clean_feedback(value: str) -> str:
        value = normalize_quotes(value)
        return re.sub(r"^Helyes:\s*", "Helyes. ", value)

    match = re.search(r"\*\*Visszajelzés:\*\*\s*[„\"](.+?)[”\"]\s*/\s*[„\"](.+?)[”\"]", body, re.S)
    if match:
        return clean_feedback(match.group(1)), clean_feedback(match.group(2))
    correct = re.search(r"\*\*Helyes visszajelzés:\*\*\s*[„\"](.+?)[”\"]", body, re.S)
    wrong = re.search(r"\*\*Hibás visszajelzés:\*\*\s*[„\"](.+?)[”\"]", body, re.S)
    return (
        clean_feedback(correct.group(1)) if correct else "Helyes válasz.",
        clean_feedback(wrong.group(1)) if wrong else "Nézd át újra az oldal magyarázatát.",
    )


def localize_multichoice(component: dict) -> None:
    component["params"]["UI"] = {
        "checkAnswerButton": "Ellenőrzés",
        "submitAnswerButton": "Beküldés",
        "showSolutionButton": "Megoldás megtekintése",
        "tryAgainButton": "Újrapróbálkozás",
        "tipsLabel": "Tipp megtekintése",
        "scoreBarLabel": "Elért pont: :num / :total",
        "tipAvailable": "Tipp érhető el",
        "feedbackAvailable": "Visszajelzés érhető el",
        "readFeedback": "Visszajelzés felolvasása",
        "wrongAnswer": "Helytelen válasz",
        "correctAnswer": "Helyes válasz",
        "shouldCheck": "Ezt kellett volna megjelölni",
        "shouldNotCheck": "Ezt nem kellett volna megjelölni",
        "noInput": "A megoldás előtt válaszolj a kérdésre!",
        "a11yCheck": "A válasz ellenőrzése.",
        "a11yShowSolution": "A megoldás megtekintése.",
        "a11yRetry": "A feladat újrapróbálása.",
    }
    component["params"]["confirmCheck"] = {
        "header": "Ellenőrzöd a választ?", "body": "Biztosan ellenőrzöd a választ?",
        "cancelLabel": "Mégse", "confirmLabel": "Ellenőrzés",
    }
    component["params"]["confirmRetry"] = {
        "header": "Újrakezded?", "body": "Biztosan újrakezded a feladatot?",
        "cancelLabel": "Mégse", "confirmLabel": "Újrapróbálkozás",
    }


def localize_drag(component: dict) -> None:
    component["params"].update({
        "scoreShow": "Ellenőrzés", "submit": "Beküldés", "tryAgain": "Újrapróbálkozás",
        "localize": {"fullscreen": "Teljes képernyő", "exitFullscreen": "Kilépés a teljes képernyőből"},
        "grabbablePrefix": "Húzható elem {num} / {total}.",
        "grabbableSuffix": "A(z) {num}. célmezőben.",
        "dropzonePrefix": "Célmező {num} / {total}.", "noDropzone": "Nincs kiválasztott célmező.",
        "tipLabel": "Tipp megtekintése.", "tipAvailable": "Tipp érhető el",
        "correctAnswer": "Helyes válasz", "wrongAnswer": "Helytelen válasz",
        "feedbackHeader": "Visszajelzés", "scoreBarLabel": "Elért pont: :num / :total",
        "scoreExplanationButtonLabel": "Pontszám magyarázata",
        "a11yCheck": "A válaszok ellenőrzése.", "a11yRetry": "A feladat újrapróbálása.",
    })


def localize_essay(component: dict) -> None:
    component["params"].update({
        "checkAnswer": "Ellenőrzés", "submitAnswer": "Beküldés",
        "tryAgain": "Újrapróbálkozás", "showSolution": "Megoldás megtekintése",
        "feedbackHeader": "Visszajelzés", "solutionTitle": "Mintamegoldás",
        "remainingChars": "Hátralévő karakterek: @chars",
        "notEnoughChars": "Írj legalább @chars karaktert!", "messageSave": "elmentve",
        "ariaYourResult": "Elért pont: @score / @total",
        "ariaNavigatedToSolution": "A mintamegoldás megjelent.",
        "ariaCheck": "A válasz ellenőrzése.", "ariaShowSolution": "A mintamegoldás megtekintése.",
        "ariaRetry": "A feladat újrapróbálása.",
    })


def localize_dialogcards(component: dict) -> None:
    component["params"].update({
        "answer": "Megfordítás", "next": "Következő", "prev": "Előző",
        "retry": "Újrakezdés", "correctAnswer": "Tudtam", "incorrectAnswer": "Nem tudtam",
        "round": "@round. kör", "cardsLeft": "Hátralévő kártyák: @number",
        "nextRound": "Tovább a(z) @round. körre", "startOver": "Újrakezdés",
        "showSummary": "Összegzés", "summary": "Összegzés",
        "summaryCardsRight": "Helyesen megválaszolt kártyák:",
        "summaryCardsWrong": "Hibásan megválaszolt kártyák:",
        "summaryCardsNotShown": "Nem megjelenített kártyák:", "summaryOverallScore": "Összesített eredmény",
        "summaryCardsCompleted": "Megtanult kártyák:", "summaryCompletedRounds": "Befejezett körök:",
        "summaryAllDone": "Nagyszerű! Mind a(z) @cards kártyát megtanultad.",
        "progressText": "Kártya @card / @total", "cardFrontLabel": "Kártya eleje",
        "cardBackLabel": "Kártya hátoldala", "tipButtonLabel": "Tipp",
        "audioNotSupported": "A böngésződ nem támogatja a hang lejátszását.",
        "confirmStartingOver": {"header": "Újrakezded?", "body": "Az eddigi haladás elvész. Biztosan újrakezded?", "cancelLabel": "Mégse", "confirmLabel": "Újrakezdés"},
    })


def parse_options(body: str) -> tuple[str, list[str], set[str]] | None:
    question = re.search(r"\*\*(?:Kérdés|Utasítás):\*\*\s*(.+?)(?=\n[A-F]\)|\n\*\*|$)", body, re.S)
    if not question:
        technical_question = re.search(r"\*\*(Multiple Choice[^*]*):\*\*", body, re.I)
        if technical_question:
            question_text = "Jelöld meg a helyes állításokat!"
            question = re.match(r"(.+)", question_text)
    options = re.findall(r"^([A-F])\)\s*(.+)$", body, re.M)
    correct = re.search(r"\*\*Helyes(?: válasz| sorrend)?:\*\*\s*(.+?)(?=\n\*\*|\n###|$)", body, re.S)
    if not question or len(options) < 2 or not correct:
        return None
    correct_text = correct.group(1)
    letters = set(re.findall(r"\b([A-F])\b", correct_text))
    if not letters:
        for letter, option in options:
            if option.strip().rstrip(".") in correct_text:
                letters.add(letter)
    return question.group(1).strip(), [f"{letter}) {option.strip()}" for letter, option in options], letters


def multi_choice(templates: dict[str, dict], title: str, body: str) -> dict | None:
    parsed = parse_options(body)
    if not parsed:
        return None
    question, options, correct_letters = parsed
    correct_feedback, wrong_feedback = feedback_pair(body)
    component = clone_template(templates, "H5P.MultiChoice 1.16", title)
    component["params"]["question"] = markdown_to_html(question)
    component["params"]["answers"] = []
    for option in options:
        letter = option[0]
        is_correct = letter in correct_letters
        component["params"]["answers"].append({
            "text": html.escape(option),
            "correct": is_correct,
            "tipsAndFeedback": {
                "tip": "",
                "chosenFeedback": correct_feedback if is_correct else wrong_feedback,
                "notChosenFeedback": "",
            },
        })
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    behaviour = component["params"]["behaviour"]
    behaviour.update({
        "enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True,
        "type": "multi" if len(correct_letters) > 1 else "single",
        "singlePoint": len(correct_letters) <= 1,
        "showSolutionsRequiresInput": True, "randomAnswers": False,
    })
    localize_multichoice(component)
    return component


def drag_pairs(templates: dict[str, dict], title: str, task: str, pairs: list[tuple[str, str]], correct_feedback: str, wrong_feedback: str) -> dict:
    component = clone_template(templates, "H5P.DragQuestion 1.14", title)
    count = len(pairs)
    row_height = 90 / count
    elements = []
    zones = []
    for index, (label, target) in enumerate(pairs):
        y = 5 + index * row_height
        elements.append({
            "type": text_component(label, f"<p>{html.escape(label)}</p>", raw_html=True),
            "x": 2, "y": y, "height": row_height - 3, "width": 46,
            "dropZones": [index], "backgroundOpacity": 100, "multiple": False,
        })
        zones.append({
            "label": target, "showLabel": True, "x": 53, "y": y,
            "height": row_height - 3, "width": 44, "correctElements": [index],
            "backgroundOpacity": 100, "single": True, "autoAlign": True,
            "tipsAndFeedback": {"feedbackOnCorrect": correct_feedback, "feedbackOnIncorrect": wrong_feedback},
        })
    component["params"]["question"] = {
        "settings": {"size": {"width": 720, "height": max(315, count * 120)}},
        "task": {"elements": elements, "dropZones": zones},
    }
    component["params"]["scoreExplanation"] = "A helyes párosítások növelik az eredményt."
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({
        "enableRetry": True, "enableCheckButton": True, "singlePoint": False,
        "applyPenalties": False, "enableScoreExplanation": False, "enableFullScreen": False,
    })
    localize_drag(component)
    return component


def final_test_special(templates: dict[str, dict], section_title: str, body: str) -> dict | None:
    if section_title.startswith("Z2"):
        return drag_pairs(templates, section_title, "Párosítsd a személyeket az útvonalukkal!", [
            ("Vasco da Gama", "Afrika megkerülésével India"),
            ("Kolumbusz", "nyugat felé a Karib-tenger térsége"),
        ], "A két személyhez a megfelelő útvonal került.", "A személyt mindig az út irányával és céljával együtt idézd fel.")
    if section_title.startswith("Z4"):
        return drag_pairs(templates, section_title, "Rendezd időrendbe a két eseménypárt!", [
            ("Dias → Kolumbusz", "1–2. hely"),
            ("Tordesillas → Vasco da Gama", "3–4. hely"),
        ], "A helyes sorrend: Dias → Kolumbusz → Tordesillas → Vasco da Gama.", "A portugál előkészítő út megelőzte 1492-t; az indiai út ezután teljesedett ki.")
    if section_title.startswith("Z9"):
        return drag_pairs(templates, section_title, "Párosítsd a pénzügyi fogalmakat a meghatározásokkal!", [
            ("bank", "pénzügyi műveleteket végző intézmény"),
            ("tőzsde · részvény", "szervezett piac · tulajdonrészt megtestesítő értékpapír"),
        ], "Helyes. A bank intézmény, a tőzsde szervezett piac, a részvény pedig tulajdonrészt megtestesítő értékpapír.", "Különítsd el az intézményt, a szervezett piacot és a tulajdonrészt megtestesítő értékpapírt.")
    if section_title.startswith("Z11"):
        return drag_pairs(templates, section_title, "Párosítsd a régiókat a helyes folyamattal!", [
            ("Nyugat", "kötöttségek lazulása"),
            ("Kelet", "robot és személyi kötöttség erősödése"),
        ], "Nyugaton lazuló, keleten erősödő jobbágyi kötöttségek kapcsolódtak az eltérő agrárfejlődéshez.", "Hasonlítsd össze ugyanazon szempontból a jobbágyi kötöttségek változását.")
    return None


def true_false(templates: dict[str, dict], title: str, body: str) -> dict | None:
    statement = re.search(r"\*\*(?:Állítás|Kérdés):\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    correct = re.search(r"\*\*Helyes:\*\*\s*(igaz|hamis)", body, re.I)
    if not statement or not correct:
        return None
    correct_feedback, wrong_feedback = feedback_pair(body)
    component = clone_template(templates, "H5P.TrueFalse 1.8", title)
    component["params"]["question"] = markdown_to_html(statement.group(1).strip())
    component["params"]["correct"] = "true" if correct.group(1).lower() == "igaz" else "false"
    component["params"]["l10n"].update({
        "correctAnswerMessage": correct_feedback, "wrongAnswerMessage": wrong_feedback,
        "trueText": "Igaz", "falseText": "Hamis", "score": "Elért pont: @score / @total",
        "checkAnswer": "Ellenőrzés", "submitAnswer": "Beküldés",
        "showSolutionButton": "Megoldás megtekintése", "tryAgain": "Újrapróbálkozás",
        "wrongAnswer": "Helytelen válasz", "correctAnswer": "Helyes válasz",
        "scoreBarLabel": "Elért pont: :num / :total",
        "a11yCheck": "A válasz ellenőrzése.", "a11yShowSolution": "A megoldás megtekintése.",
        "a11yRetry": "A feladat újrapróbálása.",
    })
    component["params"]["behaviour"].update({
        "enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True,
        "feedbackOnCorrect": correct_feedback, "feedbackOnWrong": wrong_feedback,
    })
    return component


def essay(templates: dict[str, dict], title: str, body: str) -> dict:
    component = clone_template(templates, "H5P.Essay 1.5", title)
    question = re.search(r"\*\*(?:Kérdés|Utasítás):\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    component["params"]["taskDescription"] = markdown_to_html(question.group(1).strip() if question else body)
    correct = re.search(r"\*\*Helyes(?: válasz)?:\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    sample = correct.group(1).strip() if correct else "Vesd össze a válaszodat az oldalon szereplő forrásokkal és szempontokkal."
    component["params"]["solution"] = {
        "introduction": "A válaszod ellenőrzése után hasonlítsd össze a mintával.",
        "sample": markdown_to_html(sample),
    }
    component["params"]["behaviour"].update({"enableRetry": True, "ignoreScoring": True})
    localize_essay(component)
    return component


def sort_paragraphs(templates: dict[str, dict], title: str, body: str) -> dict | None:
    order = re.search(r"\*\*Helyes sorrend:\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    if not order:
        return None
    values = [item.strip().rstrip(".") for item in re.split(r"\s*(?:→|–|—)\s*", order.group(1)) if item.strip()]
    if len(values) < 2:
        return None
    correct_feedback, wrong_feedback = feedback_pair(body)
    component = clone_template(templates, "H5P.SortParagraphs 0.11", title)
    component["params"]["taskDescription"] = markdown_to_html(re.search(r"\*\*Utasítás:\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S).group(1) if "**Utasítás:**" in body else title)
    component["params"]["paragraphs"] = values
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({"enableRetry": True, "enableSolutionsButton": True, "addButtonsForMovement": True})
    component["params"]["l10n"].update({"checkAnswer": "Ellenőrzés", "showSolution": "Megoldás megtekintése", "tryAgain": "Újrapróbálkozás", "up": "Fel", "down": "Le", "disabled": "Letiltva"})
    return component


def blanks(templates: dict[str, dict], title: str, body: str) -> dict | None:
    if "Hiányos lánc" not in body and "hiány" not in title.lower():
        return None
    sentence = re.search(r"\*\*Hiányos lánc:\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    correct = re.search(r"\*\*Helyes:\*\*\s*(.+?)(?=\n\*\*|$)", body, re.S)
    if not sentence or not correct:
        return None
    answers = [part.strip() for part in re.split(r";", correct.group(1))]
    value = sentence.group(1)
    for answer in answers:
        alternatives = [item.strip() for item in answer.split("/") if item.strip()]
        token = "*" + "/".join(alternatives) + "*"
        value = value.replace("______", token, 1)
    correct_feedback, wrong_feedback = feedback_pair(body)
    component = clone_template(templates, "H5P.Blanks 1.14", title)
    component["params"]["text"] = "<p>Egészítsd ki a hiányzó részeket!</p>"
    component["params"]["questions"] = [f"<p>{html.escape(value, quote=False)}</p>"]
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({"enableRetry": True, "enableSolutionsButton": True, "showSolutionsRequiresInput": True})
    component["params"]["l10n"].update({
        "checkAnswer": "Ellenőrzés", "submitAnswer": "Beküldés", "showSolutionButton": "Megoldás megtekintése",
        "tryAgain": "Újrapróbálkozás", "notFilledOut": "Töltsd ki az összes üres helyet!",
        "answerIsCorrect": ":ans helyes.", "answerIsWrong": ":ans helytelen.",
        "answeredCorrectly": "Helyes válasz", "answeredIncorrectly": "Helytelen válasz",
        "solutionLabel": "Megoldás:", "inputLabel": "Üres hely @num / @total",
    })
    return component


def sections(page_body: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^###\s+(.+)$", page_body, re.M))
    result = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(page_body)
        result.append((match.group(1).strip(), page_body[match.end():end].strip()))
    return result


def page_map(master: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(r"^##\s+(\d+)\.\s+oldal\s+[–-]\s+(.+)$", master, re.M))
    pages = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else master.find("\n---\n\n# 3.", match.end())
        if end < 0:
            end = len(master)
        pages.append((int(match.group(1)), match.group(2).strip(), master[match.end():end].strip()))
    return pages


def bold_panels(body: str) -> list[tuple[str, str]]:
    panels: list[tuple[str, str]] = []
    for line in body.splitlines():
        match = re.match(r"^\s*\*\*([^*]+)\*\*[:\s]*(.+?)\s*$", line)
        if match:
            panels.append((match.group(1).strip().rstrip(":"), match.group(2).strip()))
    return panels


def interaction_blocks(section_title: str, body: str) -> list[tuple[str, str]]:
    """Split sections that contain several authored questions into real H5P items."""
    pattern = re.compile(
        r"^\*\*((?:\d+\.\s*kérdés|F\d+-\d+|Q\d+-\d+)[^*]*):\*\*\s*(.+?)"
        r"(?=^\*\*(?:\d+\.\s*kérdés|F\d+-\d+|Q\d+-\d+)[^*]*:\*\*|\Z)",
        re.M | re.S | re.I,
    )
    matches = list(pattern.finditer(body))
    if not matches:
        return [(section_title, body)]
    shared_feedback = "\n".join(
        line for line in body.splitlines()
        if re.match(r"^\*\*(?:Helyes visszajelzés|Hibás visszajelzés|Visszajelzés):\*\*", line)
    )
    blocks = []
    for index, match in enumerate(matches, start=1):
        block = clean_student_body(match.group(2))
        # Keep answer and feedback configuration inside the H5P component, never as page text.
        answer_lines = re.findall(
            r"^\*\*(?:Helyes(?: válasz)?|Visszajelzés|Helyes visszajelzés|Hibás visszajelzés):\*\*.*$",
            match.group(2), re.M,
        )
        options = "\n".join(line for line in match.group(2).splitlines() if re.match(r"^[A-F]\)\s+", line))
        question_text = match.group(2).splitlines()[0].strip()
        rebuilt = f"**Kérdés:** {question_text}\n{options}\n" + "\n".join(answer_lines)
        if shared_feedback and "visszajelzés" not in rebuilt.lower():
            rebuilt += "\n" + shared_feedback
        blocks.append((f"{index}. kérdés", rebuilt.strip()))
    return blocks


def student_interaction_title(title: str) -> str:
    title = re.sub(
        r"\s*[–-]\s*(?:Multiple Choice|Single Choice Set|Question Set|Course Presentation|Image Hotspots|Accordion).*$",
        "", title, flags=re.I,
    )
    title = re.sub(r"\b(?:Multiple Choice|Single Choice Set|Question Set|Course Presentation|Image Hotspots|Accordion)\b", "", title, flags=re.I)
    return re.sub(r"\s{2,}", " ", title).strip(" –-") or "Önellenőrzés"


def localize_question_set(component: dict) -> None:
    component["params"].update({
        "progressType": "textual",
        "texts": {
            "prevButton": "Előző", "nextButton": "Következő", "finishButton": "Befejezés",
            "submitButton": "Beküldés", "textualProgress": "Kérdés: @current / @total",
            "jumpToQuestion": "Kérdés %d / %total", "questionLabel": "Kérdés",
            "readSpeakerProgress": "Kérdés @current / @total", "unansweredText": "Megválaszolatlan",
            "answeredText": "Megválaszolva", "currentQuestionText": "Jelenlegi kérdés",
            "navigationLabel": "Kérdések",
        },
    })
    component["params"]["introPage"].update({"startButtonText": "Kezdés"})
    component["params"]["endGame"].update({
        "showResultPage": True, "showSolutionButton": True, "showRetryButton": True,
        "noResultMessage": "Befejezve", "message": "Eredményed",
        "scoreBarLabel": "Elért pont: @finals / @totals",
        "solutionButtonText": "Megoldás megtekintése", "retryButtonText": "Újrapróbálkozás",
        "finishButtonText": "Befejezés", "submitButtonText": "Beküldés", "skipButtonText": "Tovább",
    })


def category_drag(templates: dict[str, dict], body: str) -> dict:
    """Turn the approved page-27 categorisation into one real drag interaction."""
    categories = bold_panels(body)
    component = clone_template(templates, "H5P.DragQuestion 1.14", "Okok és következmények rendszerezése")
    elements: list[dict] = []
    zones: list[dict] = []
    for zone_index, (category, values) in enumerate(categories):
        entries = [value.strip().rstrip(".") for value in values.split(";") if value.strip()]
        for entry in entries:
            index = len(elements)
            row, col = divmod(index, 4)
            elements.append({
                "type": text_component(entry, f"<p>{html.escape(entry)}</p>", raw_html=True),
                "x": 2 + col * 24.5, "y": 2 + row * 10.5, "height": 9, "width": 22.5,
                "dropZones": [zone_index], "backgroundOpacity": 100, "multiple": False,
            })
        zones.append({
            "label": category, "showLabel": True, "x": 2 + zone_index * 24.5, "y": 50,
            "height": 46, "width": 22.5, "correctElements": list(range(zone_index * 4, zone_index * 4 + len(entries))),
            "backgroundOpacity": 100, "single": False, "autoAlign": True,
            "tipsAndFeedback": {"feedbackOnCorrect": "Jó helyre került.", "feedbackOnIncorrect": "Gondold át, hogy okról, eseményről vagy következményről van-e szó."},
        })
    component["params"]["question"] = {"settings": {"size": {"width": 960, "height": 720}}, "task": {"elements": elements, "dropZones": zones}}
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": "Vizsgáld meg újra az okok, az események és a következmények kapcsolatát."},
        {"from": 100, "to": 100, "feedback": "Kiváló. Egyetlen folyamatban látod az ösztönzőket, az utakat és a következményeket."},
    ]}
    component["params"]["behaviour"].update({"enableRetry": True, "enableCheckButton": True, "singlePoint": False, "applyPenalties": False, "enableScoreExplanation": False, "enableFullScreen": False, "showScorePoints": False})
    localize_drag(component)
    return component


def dialog_cards(templates: dict[str, dict], title: str, body: str) -> dict:
    component = clone_template(templates, "H5P.Dialogcards 1.9", title)
    dialogs = []
    # Card entries are consistently led by bold terms/names in the approved script.
    chunks = re.split(r"(?=^[-*]?\s*\*\*[^*]+\*\*)", body, flags=re.M)
    for chunk in chunks:
        match = re.match(r"^[-*]?\s*\*\*([^*]+)\*\*[:\s]*(.*)$", chunk.strip(), re.S)
        if match and len(match.group(1)) < 100:
            dialogs.append({
                "text": f"<p style=\"text-align:center\"><strong>{html.escape(match.group(1).strip())}</strong></p>",
                "answer": markdown_to_html(match.group(2).strip()),
                "tips": {"front": "", "back": ""},
            })
    if not dialogs:
        dialogs = [{"text": f"<p><strong>{html.escape(title)}</strong></p>", "answer": markdown_to_html(body), "tips": {"front": "", "back": ""}}]
    component["params"].update({"title": title, "description": "<p>Fordítsd meg a kártyákat, majd lapozz tovább!</p>", "dialogs": dialogs})
    component["params"]["behaviour"]["enableRetry"] = True
    localize_dialogcards(component)
    return component


def accordion(templates: dict[str, dict], title: str, panel_sections: list[tuple[str, str]]) -> dict:
    component = clone_template(templates, "H5P.Accordion 1.0", title)
    component["params"]["panels"] = []
    for panel_title, body in panel_sections:
        cleaned = clean_student_body(body)
        if cleaned:
            component["params"]["panels"].append({"title": panel_title, "content": text_component(panel_title, cleaned)})
    return component


def build_page(templates: dict[str, dict], number: int, title: str, body: str) -> dict:
    page_sections = sections(body)
    column: list[dict] = []
    column.append({"content": text_component(title, f"<h2>{html.escape(title)}</h2>", raw_html=True), "useSeparator": "never"})

    if number in VISUALS and number != 1:
        filename, alt_text = VISUALS[number]
        column.append({"content": visual_component(filename, alt_text), "useSeparator": "never"})
        if number in VISUAL_CREDITS:
            column.append({"content": visual_credit_component(number), "useSeparator": "never"})

    dialog_pages = {18, 22, 23}
    interaction_sections: list[tuple[str, str]] = []
    content_sections: list[tuple[str, str]] = []
    for section_title, section_body in page_sections:
        if section_title in EXCLUDED_SECTIONS:
            continue
        if number == 27 and section_title == "Kategóriák és elemek":
            continue
        is_interaction = bool(re.search(
            r"(^[DQZ]\d|Mini feladat|Önellenőrz|^Q24|^Kérdések$|Rövid esszégyakorlat|Single Choice Set)",
            section_title, re.I,
        ))
        (interaction_sections if is_interaction else content_sections).append((section_title, section_body))

    if number in dialog_pages:
        target = next((item for item in content_sections if item[0] in {"Dialog Cards", "Kártyák", "Kötelező kártyák"}), content_sections[0] if content_sections else (title, body))
        column.append({"content": dialog_cards(templates, SECTION_TITLES.get(target[0], target[0]), clean_student_body(target[1])), "useSeparator": "auto"})
        content_sections = [item for item in content_sections if item != target]

    if number == 2:
        panel_sections = []
        for item in content_sections[:]:
            if re.match(r"^\d+\. panel", item[0], re.I):
                panel_title = re.sub(r"^\d+\. panel\s*[–-]\s*", "", item[0]).strip()
                panel_sections.append((panel_title, item[1]))
                content_sections.remove(item)
        if panel_sections:
            column.append({"content": accordion(templates, "Tanulási célok", panel_sections), "useSeparator": "auto"})

    accordion_sections = [item for item in content_sections if item[0] == "Accordion"]
    for _, section_body in accordion_sections:
        panels = bold_panels(section_body)
        if panels:
            column.append({"content": accordion(templates, "Részletek", panels), "useSeparator": "auto"})
        content_sections = [item for item in content_sections if item[0] != "Accordion"]

    for section_title, section_body in content_sections:
        cleaned = clean_student_body(section_body)
        if not cleaned:
            continue
        display_title = SECTION_TITLES.get(section_title, section_title)
        rendered = cleaned if section_title in HIDDEN_SECTION_HEADINGS else f"### {display_title}\n\n{cleaned}"
        column.append({"content": text_component(display_title, rendered), "useSeparator": "auto"})
        if number == 1 and section_title == "Megjelenő szöveg":
            filename, alt_text = VISUALS[1]
            column.append({"content": visual_component(filename, alt_text), "useSeparator": "never"})

    children: list[dict] = []
    for section_title, section_body in interaction_sections:
        for item_title, item_body in interaction_blocks(section_title, section_body):
            item_title = student_interaction_title(item_title)
            component = final_test_special(templates, section_title, item_body) if number == 29 else None
            component = component or blanks(templates, item_title, item_body)
            component = component or true_false(templates, item_title, item_body)
            component = component or sort_paragraphs(templates, item_title, item_body)
            component = component or multi_choice(templates, item_title, item_body)
            component = component or essay(templates, item_title, item_body)
            children.append(component)

    if number == 27:
        categories_body = next(section_body for section_title, section_body in page_sections if section_title == "Kategóriák és elemek")
        column.append({"content": category_drag(templates, categories_body), "useSeparator": "auto"})

    if number in {3, 25, 26, 29} and children:
        question_set = clone_template(templates, "H5P.QuestionSet 1.20", title)
        question_set["params"]["questions"] = children
        question_set["params"]["introPage"].update({"showIntroPage": True, "title": title, "introduction": "<p>Válaszolj a kérdésekre, majd ellenőrizd a megoldást!</p>"})
        localize_question_set(question_set)
        question_set["params"]["override"] = {"checkButton": True, "showSolutionButton": "on", "retryButton": "on"}
        column.append({"content": question_set, "useSeparator": "auto"})
    else:
        for component in children:
            column.append({"content": component, "useSeparator": "auto"})

    return {
        "library": "H5P.Column 1.18",
        "params": {"content": column},
        "metadata": {**metadata(title, "Oldal"), "extraTitle": title},
        "subContentId": uid(),
    }


def main() -> None:
    master = MASTER.read_text(encoding="utf-8")
    pages = page_map(master)
    if len(pages) != 30 or [number for number, _, _ in pages] != list(range(1, 31)):
        raise SystemExit("A Master Script oldaltérképe nem pontosan 1–30.")

    with zipfile.ZipFile(ATHENS) as source:
        manifest = json.loads(zip_read_normalized(source, "h5p.json"))
        athens_content = json.loads(zip_read_normalized(source, "content/content.json"))
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
        required = {"H5P.Accordion 1.0", "H5P.AdvancedText 1.1", "H5P.Blanks 1.14", "H5P.Column 1.18", "H5P.Dialogcards 1.9", "H5P.DragQuestion 1.14", "H5P.Essay 1.5", "H5P.Image 1.1", "H5P.MultiChoice 1.16", "H5P.QuestionSet 1.20", "H5P.SortParagraphs 0.11", "H5P.TrueFalse 1.8"}
        missing = required - set(templates)
        if missing:
            raise SystemExit(f"Hiányzó sablonlibrary: {sorted(missing)}")

        content = {
            "showCoverPage": False,
            "cover": None,
            "chapters": [build_page(templates, number, title, body) for number, title, body in pages],
            "behaviour": copy.deepcopy(athens_content.get("behaviour", {})),
            "read": "Megnyitás",
            "displayTOC": "Tartalomjegyzék megjelenítése",
            "hideTOC": "Tartalomjegyzék elrejtése",
            "nextPage": "Következő",
            "previousPage": "Előző",
            "chapterCompleted": "Oldal teljesítve!",
            "partCompleted": "@pages / @total oldal teljesítve",
            "incompleteChapter": "Befejezetlen oldal",
            "navigateToTop": "Vissza az oldal tetejére",
            "markAsFinished": "Befejeztem ezt az oldalt",
            "fullscreen": "Teljes képernyő",
            "exitFullscreen": "Kilépés a teljes képernyőből",
            "bookProgressSubtext": "@count / @total oldal",
            "interactionsProgressSubtext": "@count / @total feladat",
            "submitReport": "Beküldés",
            "restartLabel": "Újrakezdés",
            "summaryHeader": "Összegzés",
            "allInteractions": "Minden feladat",
            "unansweredInteractions": "Megválaszolatlan feladatok",
            "scoreText": "@score / @maxscore",
            "leftOutOfTotalCompleted": "@left / @max feladat teljesítve",
            "noInteractions": "Nincs feladat",
            "score": "Pontszám",
            "summaryAndSubmit": "Összegzés és beküldés",
            "noChapterInteractionBoldText": "Még nem oldottál meg feladatot.",
            "noChapterInteractionText": "Az összegzéshez előbb oldj meg legalább egy feladatot.",
            "yourAnswersAreSubmittedForReview": "A válaszaid beküldve.",
            "bookProgress": "Haladás a könyvben",
            "interactionsProgress": "Haladás a feladatokban",
            "totalScoreLabel": "Összpontszám",
            "a11y": {"progress": "@page. oldal / @total.", "menu": "Navigációs menü megnyitása vagy bezárása"},
        }
        content["behaviour"].update({"displaySummary": False, "defaultTableOfContents": True})
        manifest.update({
            "title": "Földrajzi felfedezések",
            "language": "hu",
            "authors": [{"name": "Digitális Történelem Érettségi Akadémia", "role": "Author"}],
            "license": "CC BY-NC-SA",
            "version": "1.1.0",
        })

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = pathlib.Path(temp_dir)
            extract_normalized(source, temp)
            shutil.rmtree(temp / "content", ignore_errors=True)
            (temp / "content").mkdir()
            image_dir = temp / "content/images"
            image_dir.mkdir()
            for filename, _ in VISUALS.values():
                source_asset = ASSET_DIR / filename
                if not source_asset.is_file():
                    raise SystemExit(f"Hiányzó tanulói vizuális asset: {source_asset}")
                shutil.copy2(source_asset, image_dir / filename)
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

    print(f"Elkészült: {OUTPUT}")
    print(f"Oldalak: {len(pages)}")


if __name__ == "__main__":
    main()
