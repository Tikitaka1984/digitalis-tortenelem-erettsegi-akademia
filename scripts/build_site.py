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
SUPPLEMENTAL_LIBRARIES = ROOT / "runtime-libraries" / "lumi-media-libraries.zip"
SITE_SOURCE = ROOT / "site"
PLAYER_SOURCE = ROOT / "node_modules" / "h5p-standalone" / "dist"
OUTPUT = ROOT / "_site"
EXPECTED_LIBRARIES_SHA256 = "fc72aa0b6abb4e7aac3f396182725a26b135d3f24942091517d82a8c2c382a75"
MODULES = (
    {
        "slug": "atheni-demokracia",
        "source": ROOT / "content" / "digitalis-tortenelem-erettsegi-akademia-atheni-demokracia-v2.0-complete.h5p",
        "sha256": "86e932d8545cfdde8a8963dedf6c5afc1cf2820c0e61f6ba6e6029675a4adc7f",
        "pages": 30,
    },
    {
        "slug": "foldrajzi-felfedezesek",
        "source": ROOT / "content" / "digitalis-tortenelem-erettsegi-akademia-foldrajzi-felfedezesek-v1.0.h5p",
        "generated": True,
        "pages": 30,
    },
)
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


def validate_h5p_tree(path: Path, expected_pages: int) -> None:
    manifest_path = path / "h5p.json"
    content_path = path / "content" / "content.json"
    if not manifest_path.is_file() or not content_path.is_file():
        fail("A csomagból hiányzik a h5p.json vagy a content/content.json.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    content = json.loads(content_path.read_text(encoding="utf-8"))
    if manifest.get("mainLibrary") != "H5P.InteractiveBook":
        fail("A forrás nem H5P Interactive Book.")
    chapters = content.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != expected_pages:
        fail(f"A projekt oldalszáma nem {expected_pages}.")

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
    for module in MODULES:
        source = module["source"]
        if not source.is_file():
            fail(f"Nem található a forráscsomag: {source.relative_to(ROOT)}")
        if module.get("sha256") and sha256(source) != module["sha256"]:
            fail(f"A(z) {module['slug']} H5P SHA-256 ellenőrzőösszege eltér; a tananyag megváltozott.")
    if not SUPPLEMENTAL_LIBRARIES.is_file() or sha256(SUPPLEMENTAL_LIBRARIES) != EXPECTED_LIBRARIES_SHA256:
        fail("A kiegészítő Lumi médiakönyvtárak hiányoznak vagy megváltoztak.")
    if not PLAYER_SOURCE.is_dir():
        fail("A h5p-standalone runtime nincs telepítve. Futtasd: npm install")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SITE_SOURCE, OUTPUT)
    shutil.copytree(PLAYER_SOURCE, OUTPUT / "player")
    build_info = []
    for module in MODULES:
        h5p_output = OUTPUT / "h5p" / module["slug"]
        h5p_output.mkdir(parents=True)
        with zipfile.ZipFile(module["source"]) as archive:
            bad_file = archive.testzip()
            if bad_file:
                fail(f"Sérült fájl a(z) {module['slug']} H5P csomagban: {bad_file}")
            safe_extract(archive, h5p_output)

        # Lumi keeps a few dynamic media libraries in its application-level
        # library store instead of embedding them in every exported H5P package.
        with zipfile.ZipFile(SUPPLEMENTAL_LIBRARIES) as archive:
            bad_file = archive.testzip()
            if bad_file:
                fail(f"Sérült fájl a kiegészítő médiakönyvtárakban: {bad_file}")
            safe_extract(archive, h5p_output)

        apply_runtime_compatibility(h5p_output)
        validate_h5p_tree(h5p_output, module["pages"])
        build_info.append({
            "slug": module["slug"],
            "content": module["source"].name,
            "sha256": sha256(module["source"]),
            "generated": module.get("generated", False),
            "pages": module["pages"],
        })
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT / "build-info.json").write_text(
        json.dumps(
            {
                "modules": build_info,
                "runtime": "h5p-standalone@3.8.2",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Built {OUTPUT} ({len(MODULES)} modules, SHA-256 verified).")


if __name__ == "__main__":
    main()
