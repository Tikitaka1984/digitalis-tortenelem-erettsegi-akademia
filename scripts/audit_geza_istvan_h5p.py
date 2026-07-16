#!/usr/bin/env python3
"""Static implementation QA for the GSI-02 H5P package."""

from __future__ import annotations

import collections
import json
import pathlib
import re
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-geza-fejedelem-szent-istvan-v1.0.h5p"
MASTER = ROOT / "DTEA/06_Master_Scripts/geza-fejedelem-szent-istvan/MASTER_SCRIPT.md"
REQUIRED_ASSETS = {
    "content/images/kingdom-hungary-1000.svg",
    "content/images/hungary-11th-century.png",
    "content/images/stephen-coronation-pall.jpg",
    "content/images/pannonhalma-charter.jpg",
    "content/images/stephen-monogram.svg",
}
EXPECTED_FORMATIVE_TYPES = {
    1: "H5P.MultiChoice 1.16", 2: "H5P.DragQuestion 1.14", 3: "H5P.SortParagraphs 0.11",
    4: "H5P.DragQuestion 1.14", 5: "H5P.MultiChoice 1.16", 6: "H5P.MultiChoice 1.16",
    7: "H5P.MultiChoice 1.16", 8: "H5P.DragQuestion 1.14", 9: "H5P.MultiChoice 1.16",
    10: "H5P.DragQuestion 1.14", 11: "H5P.SortParagraphs 0.11", 12: "H5P.DragQuestion 1.14",
    13: "H5P.MultiChoice 1.16", 14: "H5P.DragQuestion 1.14", 15: "H5P.MultiChoice 1.16",
    16: "H5P.MultiChoice 1.16", 17: "H5P.DragQuestion 1.14", 18: "H5P.MultiChoice 1.16",
    19: "H5P.DragQuestion 1.14", 20: "H5P.MultiChoice 1.16", 21: "H5P.SortParagraphs 0.11",
    22: "H5P.DragQuestion 1.14", 23: "H5P.MultiChoice 1.16", 24: "H5P.TrueFalse 1.8",
    25: "H5P.DragQuestion 1.14", 26: "H5P.MultiChoice 1.16", 27: "H5P.SortParagraphs 0.11",
    28: "H5P.DragQuestion 1.14", 29: "H5P.SortParagraphs 0.11",
}
BANNED_VISIBLE = [
    r"\bCheck\b", r"\bRetry\b", r"Show Solution", r"\bSubmit\b", r"\bPrevious\b", r"\bNext\b",
    r"\bFinish\b", r"Your result", r"Summary\s*&", r"\bPLACEHOLDER\b", r"\bTODO\b", r"\bFIXME\b",
    r"Tanulói szöveg", r"Forrásnyom", r"Helyes válasz:", r"Gyakori hiba:", r"MS-hivatkozás",
]


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def visible_strings(value):
    if isinstance(value, dict):
        library = value.get("library", "")
        params = value.get("params", {})
        if library == "H5P.AdvancedText 1.1":
            yield params.get("text", "")
        elif library == "H5P.MultiChoice 1.16":
            yield params.get("question", "")
            yield from (answer.get("text", "") for answer in params.get("answers", []))
        elif library == "H5P.TrueFalse 1.8":
            yield params.get("question", "")
        elif library == "H5P.SortParagraphs 0.11":
            yield params.get("taskDescription", "")
            yield from params.get("paragraphs", [])
        elif library == "H5P.QuestionSet 1.20":
            yield params.get("introPage", {}).get("title", "")
            yield params.get("introPage", {}).get("introduction", "")
        for child in value.values():
            yield from visible_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from visible_strings(child)
def max_score(component: dict) -> int:
    library = component.get("library", "")
    params = component.get("params", {})
    if library.startswith("H5P.MultiChoice"):
        if params.get("behaviour", {}).get("singlePoint"):
            return 1
        return sum(1 for answer in params.get("answers", []) if answer.get("correct"))
    if library.startswith("H5P.DragQuestion"):
        if params.get("behaviour", {}).get("singlePoint"):
            return 1
        return len(params.get("question", {}).get("task", {}).get("elements", []))
    if library.startswith("H5P.SortParagraphs"):
        return max(len(params.get("paragraphs", [])) - 1, 1)
    if library.startswith("H5P.TrueFalse"):
        return 1
    return 0


def validate_feedback_and_controls(number: int, component: dict) -> None:
    library = component.get("library", "")
    params = component.get("params", {})
    behaviour = params.get("behaviour", {})
    if not behaviour.get("enableRetry") or not behaviour.get("enableCheckButton"):
        raise SystemExit(f"A(z) int-{number:03d} retry/check vezérlése hiányos.")
    if library.startswith("H5P.MultiChoice"):
        feedback = params.get("overallFeedback", {}).get("overallFeedback", [])
        if len(feedback) < 2 or any(not item.get("feedback") for item in feedback):
            raise SystemExit(f"A(z) int-{number:03d} összesített feedbackje hiányos.")
        if any(not answer.get("tipsAndFeedback", {}).get("chosenFeedback") for answer in params.get("answers", [])):
            raise SystemExit(f"A(z) int-{number:03d} opciófeedbackje hiányos.")
        if params.get("UI", {}).get("checkAnswerButton") != "Ellenőrzés":
            raise SystemExit(f"A(z) int-{number:03d} kezelőszövege nem magyar.")
    elif library.startswith("H5P.DragQuestion"):
        feedback = params.get("overallFeedback", {}).get("overallFeedback", [])
        zones = params.get("question", {}).get("task", {}).get("dropZones", [])
        if len(feedback) < 2 or not zones:
            raise SystemExit(f"A(z) int-{number:03d} húzós feladata vagy feedbackje hiányos.")
        for zone in zones:
            zone_feedback = zone.get("tipsAndFeedback", {})
            if not zone_feedback.get("feedbackOnCorrect") or not zone_feedback.get("feedbackOnIncorrect"):
                raise SystemExit(f"A(z) int-{number:03d} célmezőfeedbackje hiányos.")
    elif library.startswith("H5P.SortParagraphs"):
        feedback = params.get("overallFeedback", {}).get("overallFeedback", [])
        if len(feedback) < 2 or not behaviour.get("addButtonsForMovement"):
            raise SystemExit(f"A(z) int-{number:03d} sorrendi feedbackje vagy billentyűzetes mozgatása hiányos.")
    elif library.startswith("H5P.TrueFalse"):
        if not behaviour.get("feedbackOnCorrect") or not behaviour.get("feedbackOnWrong"):
            raise SystemExit(f"A(z) int-{number:03d} igaz–hamis feedbackje hiányos.")


def main() -> None:
    with zipfile.ZipFile(PACKAGE) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise SystemExit(f"Sérült ZIP-tag: {bad_member}")
        names = set(archive.namelist())
        manifest = json.loads(archive.read("h5p.json"))
        content = json.loads(archive.read("content/content.json"))
        book_runtime = archive.read("H5P.InteractiveBook-1.11/dist/h5p-interactive-book.js").decode("utf-8")

    master = MASTER.read_text(encoding="utf-8")
    expected_titles = [match.group(1).strip() for match in re.finditer(
        r"^## `geza-fejedelem-szent-istvan--pg-\d{3}`\s+[–-]\s+(.+)$", master, re.M
    )]
    chapters = content.get("chapters", [])
    actual_titles = [chapter.get("metadata", {}).get("title") for chapter in chapters]
    if expected_titles != actual_titles or len(chapters) != 30:
        raise SystemExit("Az oldalcímek, a sorrend vagy a 30 oldalas terjedelem eltér a Master Scripttől.")
    if manifest.get("mainLibrary") != "H5P.InteractiveBook" or manifest.get("language") != "hu":
        raise SystemExit("Hibás H5P főkönyvtár vagy nyelv.")
    if manifest.get("version") != "1.0.0":
        raise SystemExit("A modulverzió nem 1.0.0.")
    if content.get("showCoverPage") or content.get("behaviour", {}).get("displaySummary"):
        raise SystemExit("A technikai borító vagy összegző oldal megváltoztatná a rögzített oldalszámot.")
    missing_assets = REQUIRED_ASSETS - names
    if missing_assets:
        raise SystemExit("Hiányzó helyi assetek: " + ", ".join(sorted(missing_assets)))

    ids = [node["subContentId"] for node in walk(content) if "subContentId" in node]
    if len(ids) != len(set(ids)):
        raise SystemExit("Ismétlődő subContentId található.")
    missing_dependencies = []
    for dependency in manifest.get("preloadedDependencies", []):
        member = f"{dependency['machineName']}-{dependency['majorVersion']}.{dependency['minorVersion']}/library.json"
        if member not in names:
            missing_dependencies.append(member)
    if missing_dependencies:
        raise SystemExit("Hiányzó library-k: " + ", ".join(missing_dependencies))

    image_nodes = [node for node in walk(content) if node.get("library") == "H5P.Image 1.1"]
    if len(image_nodes) != len(REQUIRED_ASSETS):
        raise SystemExit("A tanulói képek száma eltér az Asset Register implementált készletétől.")
    for image in image_nodes:
        params = image.get("params", {})
        if not params.get("alt") or params.get("decorative"):
            raise SystemExit("Hiányzó vagy dekoratívként jelölt történelmi kép-alt szöveg.")
        referenced = "content/" + params.get("file", {}).get("path", "")
        if referenced not in names:
            raise SystemExit(f"Törött képhivatkozás: {referenced}")

    formative = {}
    for number, chapter in enumerate(chapters[:29], start=1):
        marked = [node for node in walk(chapter) if node.get("metadata", {}).get("dteaFormative")]
        primary = [node for node in marked if node.get("metadata", {}).get("title") == f"int-{number:03d}"]
        if len(primary) != 1:
            raise SystemExit(f"A(z) int-{number:03d} interakció hiányzik vagy többszörös.")
        formative[number] = primary[0]
        expected_type = EXPECTED_FORMATIVE_TYPES[number]
        if primary[0].get("library") != expected_type:
            raise SystemExit(f"A(z) int-{number:03d} típusa hibás: {primary[0].get('library')} != {expected_type}")
        validate_feedback_and_controls(number, primary[0])
    if len(formative) != 29:
        raise SystemExit("Nem pontosan 29 formatív interakció található.")

    final_sets = [node for node in walk(chapters[29]) if node.get("library") == "H5P.QuestionSet 1.20" and node.get("metadata", {}).get("dteaFinalTest")]
    if len(final_sets) != 1:
        raise SystemExit("A 30. oldali záró QuestionSet hiányzik vagy többszörös.")
    final_set = final_sets[0]
    final_questions = final_set.get("params", {}).get("questions", [])
    if len(final_questions) != 10:
        raise SystemExit("A záróteszt nem pontosan 10 kérdéses.")
    scores = [max_score(question) for question in final_questions]
    if scores != [2] * 10 or sum(scores) != 20:
        raise SystemExit(f"A záróteszt maximumpontja hibás: {scores} = {sum(scores)}")
    if final_set.get("params", {}).get("passPercentage") != 60:
        raise SystemExit("A záróteszt teljesítési küszöbe nem 60%.")
    if "DTEA GSI-02: book score is the final chapter QuestionSet only" not in book_runtime:
        raise SystemExit("Hiányzik a formatív pontokat kizáró könyvszintű pontozási javítás.")

    serialized = json.dumps(content, ensure_ascii=False)
    visible_text = "\n".join(text for text in visible_strings(content) if isinstance(text, str))
    violations = [pattern for pattern in BANNED_VISIBLE if re.search(pattern, visible_text, re.I)]
    if violations:
        raise SystemExit("Tiltott tanulói vagy szerkesztői szövegek: " + ", ".join(violations))
    required_labels = ["Ellenőrzés", "Újrapróbálkozás", "Megoldás megtekintése", "Beküldés", "Előző", "Következő", "Befejezés", "Eredményed"]
    if any(label not in serialized for label in required_labels):
        raise SystemExit("Hiányos magyar H5P-lokalizáció.")

    libraries = collections.Counter(node["library"] for node in walk(content) if "library" in node)
    print("GSI-02 static H5P audit: PASS")
    print(f"Pages: {len(chapters)}")
    print(f"Formative interactions excluded from book score: {len(formative)}")
    print(f"Final test questions: {len(final_questions)}")
    print(f"Final test static max score: {sum(scores)}")
    print(f"Local historical assets: {len(REQUIRED_ASSETS)}")
    print(f"Unique subContentIds: {len(ids)}")
    for library, count in sorted(libraries.items()):
        print(f"{library}: {count}")


if __name__ == "__main__":
    main()
