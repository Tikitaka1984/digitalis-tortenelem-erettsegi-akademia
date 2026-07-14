Exit code: 0
Wall time: 1.6 seconds
Output:
#!/usr/bin/env python3
"""Fail CI when authoring notes leak into any published H5P learner view."""

from __future__ import annotations

import json
import pathlib
import re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / "_site"
BANNED = (
    "Tanulói szöveg", "Megjelenő szöveg", "Retry", "Show Solution",
    "Placeholder", "Accordion", "Multiple Choice", "Single Choice",
    "Kép- és hotspotterv", "Akadálymentes alternatíva", "VIZUÁLIS ELEM",
    "KÉSŐBB CSERÉLENDŐ", "Pontozás", "Helyes válasz", "Hibás válasz",
    "Developer", "Teacher note",
)


class VisibleHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth:
            self.parts.append(data)


def scrub_blanks_solution(text: str) -> str:
    """Remove H5P Blanks answer markup because it is hidden until checking."""
    return re.sub(r"\*[^*]+\*", "______", text)


def visible_entries(value, path="root"):
    """Yield (JSON path, text) pairs that may actually appear to learners."""
    if isinstance(value, dict):
        library = value.get("library", "")
        params = value.get("params", {})
        if library.startswith("H5P.AdvancedText"):
            yield f"{path}.params.text", params.get("text", "")
        elif library.startswith("H5P.MultiChoice"):
            yield f"{path}.params.question", params.get("question", "")
            for index, answer in enumerate(params.get("answers", [])):
                yield f"{path}.params.answers[{index}].text", answer.get("text", "")
        elif library.startswith("H5P.TrueFalse"):
            yield f"{path}.params.question", params.get("question", "")
        elif library.startswith("H5P.Blanks"):
            yield f"{path}.params.text", params.get("text", "")
            for index, question in enumerate(params.get("questions", [])):
                yield f"{path}.params.questions[{index}]", scrub_blanks_solution(question)
        elif library.startswith("H5P.SortParagraphs"):
            yield f"{path}.params.taskDescription", params.get("taskDescription", "")
            for index, paragraph in enumerate(params.get("paragraphs", [])):
                yield f"{path}.params.paragraphs[{index}]", paragraph
        elif library.startswith("H5P.Essay"):
            yield f"{path}.params.taskDescription", params.get("taskDescription", "")
        elif library.startswith("H5P.QuestionSet"):
            intro = params.get("introPage", {})
            yield f"{path}.params.introPage.title", intro.get("title", "")
            yield f"{path}.params.introPage.introduction", intro.get("introduction", "")
        elif library.startswith("H5P.Dialogcards"):
            yield f"{path}.params.title", params.get("title", "")
            yield f"{path}.params.description", params.get("description", "")
            for index, card in enumerate(params.get("dialogs", [])):
                yield f"{path}.params.dialogs[{index}].text", card.get("text", "")
                yield f"{path}.params.dialogs[{index}].answer", card.get("answer", "")
        for key, child in value.items():
            yield from visible_entries(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from visible_entries(child, f"{path}[{index}]")


def matching_contexts(entries, pattern):
    contexts = []
    for path, value in entries:
        if not value:
            continue
        text = str(value)
        found = sorted({match.group(0) for match in pattern.finditer(text)}, key=str.casefold)
        if found:
            compact = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()
            contexts.append((path, found, compact[:180]))
    return contexts


def main() -> None:
    failures: list[str] = []
    roots = sorted((BUILD / "h5p").glob("*/content/content.json"))
    if not roots:
        raise SystemExit("STUDENT AUDIT ERROR: egyetlen publikált H5P-modul sem található.")
    pattern = re.compile("|".join(re.escape(item) for item in BANNED), re.I)
    for content_path in roots:
        module = content_path.parents[1].name
        content = json.loads(content_path.read_text(encoding="utf-8"))
        contexts = matching_contexts(visible_entries(content), pattern)
        if contexts:
            details = "; ".join(
                f"{path}: {', '.join(matches)} [{snippet}]"
                for path, matches, snippet in contexts
            )
            failures.append(f"{module}: {details}")
    for page in ("index.html", "library.html", "learn.html"):
        parser = VisibleHTML()
        parser.feed((BUILD / page).read_text(encoding="utf-8"))
        text = "\n".join(parser.parts)
        matches = sorted({match.group(0) for match in pattern.finditer(text)}, key=str.casefold)
        if matches:
            failures.append(f"{page}: tiltott tanulói kifejezések: {', '.join(matches)}")
    if failures:
        raise SystemExit("STUDENT AUDIT ERROR:\n- " + "\n- ".join(failures))
    print(f"Student audit: PASS ({len(roots)} H5P-modul, {len(BANNED)} tiltott kifejezés).")


if __name__ == "__main__":
    main()

