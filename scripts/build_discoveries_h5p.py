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

EXCLUDED_SECTIONS = {
    "Vizuális brief", "UX", "UX és vizuál", "Elfogadási feltétel",
    "Oldalszintű forrás- és státuszmetaadat", "Média placeholder",
    "Média státusza", "Vizuális és a11y", "Vizuális elv", "Teszt QA",
    "Végleges záróteszt-mátrix", "Tanári megjegyzés",
}


def uid() -> str:
    return str(uuid.uuid4())


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
    return {"contentType": content_type, "license": "U", "title": title, "authors": [], "changes": []}


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


def clone_template(templates: dict[str, dict], library: str, title: str) -> dict:
    component = reuuid(copy.deepcopy(templates[library]))
    component["metadata"]["title"] = title
    return component


def feedback_pair(body: str) -> tuple[str, str]:
    match = re.search(r"\*\*Visszajelzés:\*\*\s*[„\"](.+?)[”\"]\s*/\s*[„\"](.+?)[”\"]", body, re.S)
    if match:
        return normalize_quotes(match.group(1)), normalize_quotes(match.group(2))
    correct = re.search(r"\*\*Helyes visszajelzés:\*\*\s*[„\"](.+?)[”\"]", body, re.S)
    wrong = re.search(r"\*\*Hibás visszajelzés:\*\*\s*[„\"](.+?)[”\"]", body, re.S)
    return (
        normalize_quotes(correct.group(1)) if correct else "Helyes válasz.",
        normalize_quotes(wrong.group(1)) if wrong else "Nézd át újra az oldal magyarázatát.",
    )


def parse_options(body: str) -> tuple[str, list[str], set[str]] | None:
    question = re.search(r"\*\*(?:Kérdés|Utasítás):\*\*\s*(.+?)(?=\n[A-F]\)|\n\*\*|$)", body, re.S)
    if not question:
        question = re.search(r"\*\*(Multiple Choice[^*]*):\*\*", body, re.I)
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
    component["params"]["scoreExplanation"] = f"A teljes feladat {count} pontot ér."
    component["params"]["overallFeedback"] = {"overallFeedback": [
        {"from": 0, "to": 99, "feedback": wrong_feedback},
        {"from": 100, "to": 100, "feedback": correct_feedback},
    ]}
    component["params"]["behaviour"].update({
        "enableRetry": True, "enableCheckButton": True, "singlePoint": False,
        "applyPenalties": False, "enableScoreExplanation": True, "enableFullScreen": False,
    })
    component["params"]["scoreShow"] = task
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
        ], "Helyes: Dias → Kolumbusz → Tordesillas → Vasco da Gama.", "A portugál előkészítő út megelőzte 1492-t; az indiai út ezután teljesedett ki.")
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
        "showSolutionButton": "Megoldás mutatása",
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
    component["params"]["solution"] = {
        "introduction": "Vesd össze a válaszodat az oldalon szereplő forrásokkal és szempontokkal.",
        "sample": markdown_to_html(body),
    }
    component["params"]["behaviour"].update({"enableRetry": True, "ignoreScoring": True})
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
    return component


def accordion(templates: dict[str, dict], title: str, panel_sections: list[tuple[str, str]]) -> dict:
    component = clone_template(templates, "H5P.Accordion 1.0", title)
    component["params"]["panels"] = []
    for panel_title, body in panel_sections:
        component["params"]["panels"].append({"title": panel_title, "content": text_component(panel_title, body)})
    return component


def build_page(templates: dict[str, dict], number: int, title: str, body: str) -> dict:
    page_sections = sections(body)
    column: list[dict] = []
    column.append({"content": text_component(title, f"<h2>{html.escape(title)}</h2>", raw_html=True), "useSeparator": "never"})

    # Explicit placeholders where the approved Master Script requires a later asset.
    if any(name in title for name in ("Borító", "hajózás feltételei", "Dias", "Vasco", "Kolumbusz", "tordesillasi", "Magellán", "Térkép")):
        column.append({"content": text_component("Média placeholder", "<blockquote><p><strong>VIZUÁLIS ELEM – KÉSŐBB CSERÉLENDŐ</strong></p></blockquote>", raw_html=True), "useSeparator": "never"})

    accordion_pages = {2, 5, 6, 8, 10, 11, 12, 17, 19, 20, 21, 24, 30}
    dialog_pages = {18, 22, 23}
    interaction_sections: list[tuple[str, str]] = []
    content_sections: list[tuple[str, str]] = []
    for section_title, section_body in page_sections:
        if section_title in EXCLUDED_SECTIONS:
            continue
        is_interaction = bool(re.search(r"(^[DQZ]\d|Mini feladat|Önellenőrz|^Q24|^Kérdések$|Rövid esszégyakorlat)", section_title, re.I))
        (interaction_sections if is_interaction else content_sections).append((section_title, section_body))

    if number in dialog_pages:
        target = next((item for item in content_sections if item[0] in {"Dialog Cards", "Kártyák", "Kötelező kártyák"}), content_sections[0] if content_sections else (title, body))
        column.append({"content": dialog_cards(templates, target[0], target[1]), "useSeparator": "auto"})
        content_sections = [item for item in content_sections if item != target]

    if number in accordion_pages and content_sections:
        column.append({"content": accordion(templates, title, content_sections), "useSeparator": "auto"})
        content_sections = []

    for section_title, section_body in content_sections:
        column.append({"content": text_component(section_title, f"### {section_title}\n\n{section_body}"), "useSeparator": "auto"})

    children: list[dict] = []
    for section_title, section_body in interaction_sections:
        component = final_test_special(templates, section_title, section_body) if number == 29 else None
        component = component or blanks(templates, section_title, section_body)
        component = component or true_false(templates, section_title, section_body)
        component = component or sort_paragraphs(templates, section_title, section_body)
        component = component or multi_choice(templates, section_title, section_body)
        component = component or essay(templates, section_title, section_body)
        children.append(component)

    if number in {3, 25, 26, 29} and children:
        question_set = clone_template(templates, "H5P.QuestionSet 1.20", title)
        question_set["params"]["questions"] = children
        question_set["params"]["introPage"].update({"showIntroPage": True, "title": title, "introduction": "<p>Válaszolj a kérdésekre, majd ellenőrizd a megoldást!</p>"})
        question_set["params"]["endGame"].update({"showResultPage": True, "showSolutionButton": True, "showRetryButton": True})
        question_set["params"]["override"] = {"checkButton": True, "showSolutionButton": "on", "retryButton": "on"}
        column.append({"content": question_set, "useSeparator": "auto"})
    else:
        for component in children:
            column.append({"content": component, "useSeparator": "auto"})

    return {
        "library": "H5P.Column 1.18",
        "params": {"content": column},
        "metadata": {**metadata(title, "Column"), "extraTitle": title},
        "subContentId": uid(),
    }


def main() -> None:
    master = MASTER.read_text(encoding="utf-8")
    pages = page_map(master)
    if len(pages) != 30 or [number for number, _, _ in pages] != list(range(1, 31)):
        raise SystemExit("A Master Script oldaltérképe nem pontosan 1–30.")

    with zipfile.ZipFile(ATHENS) as source:
        manifest = json.loads(source.read("h5p.json"))
        athens_content = json.loads(source.read("content/content.json"))
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
        required = {"H5P.Accordion 1.0", "H5P.AdvancedText 1.1", "H5P.Blanks 1.14", "H5P.Column 1.18", "H5P.Dialogcards 1.9", "H5P.DragQuestion 1.14", "H5P.Essay 1.5", "H5P.MultiChoice 1.16", "H5P.QuestionSet 1.20", "H5P.SortParagraphs 0.11", "H5P.TrueFalse 1.8"}
        missing = required - set(templates)
        if missing:
            raise SystemExit(f"Hiányzó sablonlibrary: {sorted(missing)}")

        content = {
            "showCoverPage": True,
            "chapters": [build_page(templates, number, title, body) for number, title, body in pages],
            "behaviour": copy.deepcopy(athens_content.get("behaviour", {})),
        }
        manifest.update({
            "title": "Földrajzi felfedezések",
            "language": "hu",
            "authors": [],
            "license": "U",
        })

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = pathlib.Path(temp_dir)
            source.extractall(temp)
            shutil.rmtree(temp / "content", ignore_errors=True)
            (temp / "content").mkdir()
            (temp / "content/content.json").write_text(json.dumps(content, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            (temp / "h5p.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as target:
                for path in sorted(temp.rglob("*")):
                    if path.is_file():
                        target.write(path, path.relative_to(temp).as_posix())

    print(f"Elkészült: {OUTPUT}")
    print(f"Oldalak: {len(pages)}")


if __name__ == "__main__":
    main()
