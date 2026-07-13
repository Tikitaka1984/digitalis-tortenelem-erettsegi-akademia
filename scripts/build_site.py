#!/usr/bin/env python3
"""Build the static GitHub Pages artifact without modifying the source H5P."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SOURCE_H5P = ROOT / "content" / "digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p"
SUPPLEMENTAL_LIBRARIES = ROOT / "runtime-libraries" / "lumi-media-libraries.zip"
SITE_SOURCE = ROOT / "site"
PLAYER_SOURCE = ROOT / "node_modules" / "h5p-standalone" / "dist"
OUTPUT = ROOT / "_site"
H5P_OUTPUT = OUTPUT / "h5p" / "atheni-demokracia"

EXPECTED_SHA256 = "86e932d8545cfdde8a8963dedf6c5afc1cf2820c0e61f6ba6e6029675a4adc7f"
EXPECTED_LIBRARIES_SHA256 = "fc72aa0b6abb4e7aac3f396182725a26b135d3f24942091517d82a8c2c382a75"
EXPECTED_PAGES = 30
SORT_PARAGRAPHS_SOURCE_SHA256 = "d80ca762ab322cd199dbae363a6bd13a613b77511c881124799373eeadf46bf3"
SORT_PARAGRAPHS_PATCHED_SHA256 = "c685200e429a3832014b38e654ece7894171ecc90c7b9ad5bdff8b28ab78fa21"


def fail(message: str) -> None:
    raise SystemExit(f"BUILD ERROR: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    """Extract portably while rejecting traversal paths.

    Lumi packages created on Windows may contain backslashes in ZIP member
    names. ZIP formally uses forward slashes, so normalize those separators
    explicitly before extracting on Linux-based GitHub Actions runners.
    """
    root = destination.resolve()
    for member in archive.infolist():
        normalized = member.filename.replace("\\", "/")
        parts = PurePosixPath(normalized).parts
        if not parts or normalized.startswith("/") or ".." in parts:
            fail(f"Tiltott útvonal a H5P csomagban: {member.filename}")
        target = (destination / Path(*parts)).resolve()
        if root not in target.parents and target != root:
            fail(f"Tiltott útvonal a H5P csomagban: {member.filename}")
        if member.is_dir() or normalized.endswith("/"):
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(member) as source, target.open("wb") as output:
            shutil.copyfileobj(source, output)


def validate_h5p_tree(path: Path) -> None:
    manifest_path = path / "h5p.json"
    content_path = path / "content" / "content.json"
    if not manifest_path.is_file() or not content_path.is_file():
        fail("A csomagból hiányzik a h5p.json vagy a content/content.json.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    content = json.loads(content_path.read_text(encoding="utf-8"))
    if manifest.get("mainLibrary") != "H5P.InteractiveBook":
        fail("A forrás nem H5P Interactive Book.")
    chapters = content.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != EXPECTED_PAGES:
        fail(f"A projekt oldalszáma nem {EXPECTED_PAGES}.")

    missing = []
    dependencies = manifest.get("preloadedDependencies", []) + manifest.get("dynamicDependencies", [])
    for dependency in dependencies:
        folder = f"{dependency['machineName']}-{dependency['majorVersion']}.{dependency['minorVersion']}"
        if not (path / folder / "library.json").is_file():
            missing.append(folder)
    if missing:
        fail("Hiányzó H5P-könyvtárak: " + ", ".join(missing))


def apply_runtime_compatibility(path: Path) -> None:
    """Apply a narrowly scoped player compatibility fix outside the source H5P.

    Sort Paragraphs 0.11 asks its not-yet-created content object whether an
    answer exists while the Interactive Book eagerly initializes chapters.
    Lumi loads this differently, but the standalone player exposes the null
    access. Guard those two lifecycle lookups and verify both file versions
    by SHA-256.
    """
    target = path / "H5P.SortParagraphs-0.11" / "dist" / "h5p-sort-paragraphs.js"
    if not target.is_file() or sha256(target) != SORT_PARAGRAPHS_SOURCE_SHA256:
        fail("A Sort Paragraphs kompatibilitási javítás forrása hiányzik vagy ismeretlen verziójú.")
    old = b"o.getAnswerGiven=function(){return this.content.isAnswerGiven()}"
    new = b"o.getAnswerGiven=function(){return!!this.content&&this.content.isAnswerGiven()}"
    data = target.read_bytes()
    if data.count(old) != 1:
        fail("A Sort Paragraphs kompatibilitási javítás nem alkalmazható egyértelműen.")
    data = data.replace(old, new)

    old_state = b"this.getAnswerGiven()||this.previousState.order"
    new_state = b"this.getAnswerGiven()||this.previousState?.order"
    if data.count(old_state) != 2:
        fail("A Sort Paragraphs állapotkezelési javítása nem alkalmazható egyértelműen.")
    target.write_bytes(data.replace(old_state, new_state))
    if sha256(target) != SORT_PARAGRAPHS_PATCHED_SHA256:
        fail("A Sort Paragraphs kompatibilitási javítás ellenőrzése sikertelen.")


def main() -> None:
    if not SOURCE_H5P.is_file():
        fail(f"Nem található a forráscsomag: {SOURCE_H5P.relative_to(ROOT)}")
    if sha256(SOURCE_H5P) != EXPECTED_SHA256:
        fail("A H5P SHA-256 ellenőrzőösszege eltér; a tananyag megváltozott.")
    if not SUPPLEMENTAL_LIBRARIES.is_file() or sha256(SUPPLEMENTAL_LIBRARIES) != EXPECTED_LIBRARIES_SHA256:
        fail("A kiegészítő Lumi médiakönyvtárak hiányoznak vagy megváltoztak.")
    if not PLAYER_SOURCE.is_dir():
        fail("A h5p-standalone runtime nincs telepítve. Futtasd: npm install")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SITE_SOURCE, OUTPUT)
    shutil.copytree(PLAYER_SOURCE, OUTPUT / "player")
    H5P_OUTPUT.mkdir(parents=True)

    with zipfile.ZipFile(SOURCE_H5P) as archive:
        bad_file = archive.testzip()
        if bad_file:
            fail(f"Sérült fájl a H5P csomagban: {bad_file}")
        safe_extract(archive, H5P_OUTPUT)

    # Lumi keeps a few dynamic media libraries in its application-level
    # library store instead of embedding them in every exported H5P package.
    # Supply exact copies alongside the extracted package without changing it.
    with zipfile.ZipFile(SUPPLEMENTAL_LIBRARIES) as archive:
        bad_file = archive.testzip()
        if bad_file:
            fail(f"Sérült fájl a kiegészítő médiakönyvtárakban: {bad_file}")
        safe_extract(archive, H5P_OUTPUT)

    apply_runtime_compatibility(H5P_OUTPUT)
    validate_h5p_tree(H5P_OUTPUT)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT / "build-info.json").write_text(
        json.dumps(
            {
                "content": SOURCE_H5P.name,
                "sha256": EXPECTED_SHA256,
                "pages": EXPECTED_PAGES,
                "runtime": "h5p-standalone@3.8.2",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Built {OUTPUT} ({EXPECTED_PAGES} H5P pages, SHA-256 verified).")


if __name__ == "__main__":
    main()

