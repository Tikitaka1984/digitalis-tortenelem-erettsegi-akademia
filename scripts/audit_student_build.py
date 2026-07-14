#!/usr/bin/env python3
"""Fail CI when authoring notes leak into any published H5P learner view."""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / "_site"
BANNED = (
    "Tanulói szöveg", "Megjelenő szöveg", "Retry", "Show Solution",
    "Placeholder", "Accordion", "Multiple Choice", "Single Choice",
    "Kép- és hotspotterv", "Akadálymentes alternatíva", "VIZUÁLIS ELEM",
    "KÉSŐBB CSERÉLENDŐ", "Pontozás", "Helyes válasz", "Hibás válasz",
    "Developer", "Teacher note",
)


def visible_strings(value):
    """Yield strings that can be visible before or while answering."""
    if isinstance(value, dict):
        library = value.get("library", "")
        params = value.get("params", {})
        if library.startswith("H5P.AdvancedText"):
            yield params.get("text", "")
        elif library.startswith("H5P.MultiChoice"):
            yield params.get("question", "")
            for answer in params.get("answers", []):
                yield answer.get("text", "")
        elif library.startswith("H5P.TrueFalse"):
            yield params.get("question", "")
        elif library.startswith("H5P.Blanks"):
            yield params.get("text", "")
            yield from params.get("questions", [])
        elif library.startswith("H5P.SortParagraphs"):
            yield params.get("taskDescription", "")
            yield from params.get("paragraphs", [])
        elif library.startswith("H5P.Essay"):
            yield params.get("taskDescription", "")
        elif library.startswith("H5P.QuestionSet"):
            yield params.get("introPage", {}).get("title", "")
            yield params.get("introPage", {}).get("introduction", "")
        elif library.startswith("H5P.Dialogcards"):
            yield params.get("title", "")
            yield params.get("description", "")
            for card in params.get("dialogs", []):
                yield card.get("text", "")
                yield card.get("answer", "")
        for child in value.values():
            yield from visible_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from visible_strings(child)


def main() -> None:
    failures: list[str] = []
    roots = sorted((BUILD / "h5p").glob("*/content/content.json"))
    if not roots:
        raise SystemExit("STUDENT AUDIT ERROR: egyetlen publikált H5P-modul sem található.")
    pattern = re.compile("|".join(re.escape(item) for item in BANNED), re.I)
    for content_path in roots:
        module = content_path.parents[1].name
        content = json.loads(content_path.read_text(encoding="utf-8"))
        visible = "\n".join(str(item) for item in visible_strings(content) if item)
        matches = sorted({match.group(0) for match in pattern.finditer(visible)}, key=str.casefold)
        if matches:
            failures.append(f"{module}: tiltott tanulói kifejezések: {', '.join(matches)}")
    for page in ("index.html", "library.html", "learn.html"):
        text = (BUILD / page).read_text(encoding="utf-8")
        matches = sorted({match.group(0) for match in pattern.finditer(text)}, key=str.casefold)
        if matches:
            failures.append(f"{page}: tiltott tanulói kifejezések: {', '.join(matches)}")
    if failures:
        raise SystemExit("STUDENT AUDIT ERROR:\n- " + "\n- ".join(failures))
    print(f"Student audit: PASS ({len(roots)} H5P-modul, {len(BANNED)} tiltott kifejezés).")


if __name__ == "__main__":
    main()
