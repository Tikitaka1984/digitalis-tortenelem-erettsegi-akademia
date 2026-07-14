#!/usr/bin/env python3
"""Remove legacy authoring notes from the published artifact, not source H5P files."""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / "_site" / "h5p"
PLACEHOLDER = re.compile(r"PLACEHOLDER|KÉSŐBB CSERÉLENDŐ", re.I)
ANSWER_LABEL = re.compile(r"Helyes válasz\s*:?", re.I)
TEACHER_NOTE = re.compile(r"\bA tanár\b|Tanári megjegyzés", re.I)


def advanced_text(item):
    if not isinstance(item, dict):
        return None
    candidate = item.get("content", item)
    if not isinstance(candidate, dict) or not str(candidate.get("library", "")).startswith("H5P.AdvancedText"):
        return None
    return candidate.get("params", {}).get("text", "")


def sanitize(value):
    """Clean learner-visible authoring residue while preserving facts and structure."""
    if isinstance(value, list):
        cleaned = []
        for item in value:
            text = advanced_text(item)
            if text is not None and PLACEHOLDER.search(text):
                continue
            cleaned.append(sanitize(item))
        return cleaned
    if not isinstance(value, dict):
        return value

    result = {key: sanitize(child) for key, child in value.items()}
    library = str(result.get("library", ""))
    params = result.get("params", {})

    if library.startswith("H5P.AdvancedText") and isinstance(params.get("text"), str):
        params["text"] = ANSWER_LABEL.sub("Magyarázat:", params["text"])

    if library.startswith("H5P.QuestionSet"):
        intro = params.get("introPage", {})
        introduction = intro.get("introduction", "")
        if isinstance(introduction, str) and TEACHER_NOTE.search(introduction):
            intro["introduction"] = (
                "<p>Gyakorold a témakört, ellenőrizd a válaszaidat, "
                "majd próbáld újra azokat a részeket, amelyek még bizonytalanok.</p>"
            )
        elif isinstance(introduction, str):
            intro["introduction"] = ANSWER_LABEL.sub("Megoldási magyarázat", introduction)
    return result


def main():
    changed = []
    for content_path in sorted(BUILD.glob("*/content/content.json")):
        original = json.loads(content_path.read_text(encoding="utf-8"))
        cleaned = sanitize(original)
        if cleaned != original:
            content_path.write_text(
                json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
            changed.append(content_path.parents[1].name)
    print("Published learner artifact sanitized: " + (", ".join(changed) or "no changes"))


if __name__ == "__main__":
    main()

