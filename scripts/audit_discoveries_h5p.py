#!/usr/bin/env python3
"""Static QA for the generated Földrajzi felfedezések H5P package."""

from __future__ import annotations

import collections
import json
import pathlib
import re
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "content/digitalis-tortenelem-erettsegi-akademia-foldrajzi-felfedezesek-v1.0.h5p"
MASTER = ROOT / "docs/master-scripts/dtea-foldrajzi-felfedezesek-master-script-v1.0.2.md"

REQUIRED_ASSETS = {
    "content/images/cover-atlantic-routes.webp",
    "content/images/navigation-tools.svg",
    "content/images/dias-route.svg",
    "content/images/da-gama-route.svg",
    "content/images/columbus-route.svg",
    "content/images/tordesillas.svg",
    "content/images/magellan-route.svg",
    "content/images/route-overview.svg",
}

BANNED_STUDENT_PATTERNS = [
    r"\bCheck\b", r"\bRetry\b", r"Show Solution", r"\bSubmit\b", r"\bPrevious\b",
    r"\bNext\b", r"\bFinish\b", r"Your result", r"Summary\s*&", r"Multiple Choice",
    r"Single Choice", r"Question Set", r"Course Presentation", r"Image Hotspots",
    r"Tanulói szöveg", r"Megjelenő szöveg", r"Kép- és hotspotterv",
    r"Akadálymentes alternatíva", r"VIZUÁLIS ELEM", r"KÉSŐBB CSERÉLENDŐ",
    r"\bPLACEHOLDER\b", r"Pontozás:", r"Helyes:", r"Helyes válasz:",
    r"Helyes visszajelzés:", r"Hibás visszajelzés:", r"Média státusza",
    r"Szakmai státusz", r"Kognitív művelet", r"Elfogadási feltétel",
]


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def visible_initial_strings(value):
    """Yield text visible before a learner checks an answer."""
    if isinstance(value, dict):
        library = value.get("library", "")
        params = value.get("params", {})
        if library == "H5P.AdvancedText 1.1":
            yield params.get("text", "")
        elif library == "H5P.MultiChoice 1.16":
            yield params.get("question", "")
            for answer in params.get("answers", []):
                yield answer.get("text", "")
        elif library == "H5P.TrueFalse 1.8":
            yield params.get("question", "")
        elif library == "H5P.Blanks 1.14":
            yield params.get("text", "")
            for question in params.get("questions", []):
                yield re.sub(r"\*[^*]+\*", "______", question)
        elif library == "H5P.SortParagraphs 0.11":
            yield params.get("taskDescription", "")
            yield from params.get("paragraphs", [])
        elif library == "H5P.Essay 1.5":
            yield params.get("taskDescription", "")
        elif library == "H5P.QuestionSet 1.20":
            yield params.get("introPage", {}).get("title", "")
            yield params.get("introPage", {}).get("introduction", "")
        elif library == "H5P.Dialogcards 1.9":
            yield params.get("title", "")
            yield params.get("description", "")
            for card in params.get("dialogs", []):
                yield card.get("text", "")
                yield card.get("answer", "")
        for child in value.values():
            yield from visible_initial_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from visible_initial_strings(child)


def main() -> None:
    with zipfile.ZipFile(PACKAGE) as archive:
        bad = archive.testzip()
        if bad:
            raise SystemExit(f"Sérült ZIP-tag: {bad}")
        manifest = json.loads(archive.read("h5p.json"))
        content = json.loads(archive.read("content/content.json"))
        names = set(archive.namelist())

    master = MASTER.read_text(encoding="utf-8")
    expected_titles = [match.group(1).strip() for match in re.finditer(r"^##\s+\d+\.\s+oldal\s+[–-]\s+(.+)$", master, re.M)]
    actual_titles = [chapter.get("metadata", {}).get("title") for chapter in content.get("chapters", [])]
    if expected_titles != actual_titles:
        raise SystemExit("Az oldalcímek vagy a sorrend eltér a Master Scripttől.")

    ids = [node["subContentId"] for node in walk(content) if isinstance(node, dict) and "subContentId" in node]
    if len(ids) != len(set(ids)):
        raise SystemExit("Ismétlődő subContentId található.")

    libraries = collections.Counter(node["library"] for node in walk(content) if isinstance(node, dict) and "library" in node)
    if manifest.get("mainLibrary") != "H5P.InteractiveBook" or len(actual_titles) != 30:
        raise SystemExit("Hibás H5P főkönyvtár vagy oldalszám.")
    if content.get("showCoverPage") or content.get("behaviour", {}).get("displaySummary"):
        raise SystemExit("A technikai borító vagy az automatikus összegző oldal 31. oldalt hozna létre.")
    if not REQUIRED_ASSETS.issubset(names):
        raise SystemExit("Hiányzó tanulói vizuális assetek: " + ", ".join(sorted(REQUIRED_ASSETS - names)))

    missing_dependencies = []
    for dependency in manifest.get("preloadedDependencies", []):
        folder = f"{dependency['machineName']}-{dependency['majorVersion']}.{dependency['minorVersion']}/library.json"
        if folder not in names:
            missing_dependencies.append(folder)
    if missing_dependencies:
        raise SystemExit("Hiányzó library-k: " + ", ".join(missing_dependencies))

    print("Static H5P audit: PASS")
    print(f"Pages: {len(actual_titles)}")
    print(f"Unique subContentIds: {len(ids)}")
    print(f"Student visuals: {len(REQUIRED_ASSETS)}")

    initial_text = "\n".join(text for text in visible_initial_strings(content) if isinstance(text, str))
    violations = [pattern for pattern in BANNED_STUDENT_PATTERNS if re.search(pattern, initial_text, re.I)]
    if violations:
        raise SystemExit("Tiltott tanulói felületi kifejezések: " + ", ".join(violations))
    if any(label not in json.dumps(content, ensure_ascii=False) for label in ("Ellenőrzés", "Újrapróbálkozás", "Megoldás megtekintése", "Beküldés", "Előző", "Következő", "Befejezés", "Pontszám", "Eredményed", "Összegzés")):
        raise SystemExit("Hiányos magyar H5P-lokalizáció.")
    print("Student-facing content audit: PASS")
    final_children = []
    for node in walk(content["chapters"][28]):
        if isinstance(node, dict) and node.get("library") == "H5P.QuestionSet 1.20":
            final_children = node.get("params", {}).get("questions", [])
            break
    print("Final test components:", [child.get("library") for child in final_children])
    print("Final test component count:", len(final_children))
    def max_score(component):
        library = component.get("library", "")
        params = component.get("params", {})
        if library.startswith("H5P.MultiChoice"):
            if params.get("behaviour", {}).get("singlePoint"):
                return 1
            return sum(1 for answer in params.get("answers", []) if answer.get("correct"))
        if library.startswith("H5P.DragQuestion"):
            return 1 if params.get("behaviour", {}).get("singlePoint") else len(params.get("question", {}).get("task", {}).get("elements", []))
        if library.startswith("H5P.Blanks"):
            return sum(question.count("*") // 2 for question in params.get("questions", []))
        if library.startswith("H5P.TrueFalse"):
            return 1
        return 0
    final_max = sum(max_score(child) for child in final_children)
    print("Final test component max scores:", [max_score(child) for child in final_children])
    if final_max != 20:
        raise SystemExit(f"A záróteszt statikus maximumpontja nem 20, hanem {final_max}.")
    print("Final test static max score:", final_max)
    for library, count in sorted(libraries.items()):
        print(f"{library}: {count}")


if __name__ == "__main__":
    main()
