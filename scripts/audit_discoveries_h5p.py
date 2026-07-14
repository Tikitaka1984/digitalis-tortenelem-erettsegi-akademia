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


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


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
    placeholders = json.dumps(content, ensure_ascii=False).count("KÉSŐBB CSERÉLENDŐ")
    if manifest.get("mainLibrary") != "H5P.InteractiveBook" or len(actual_titles) != 30:
        raise SystemExit("Hibás H5P főkönyvtár vagy oldalszám.")

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
    print(f"Placeholders: {placeholders}")
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
