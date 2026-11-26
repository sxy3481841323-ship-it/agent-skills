#!/usr/bin/env python3
"""Validate actual source files against the generated public manifest."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    registry = json.loads((root / "registry.json").read_text())
    names = set()
    declared = set()
    for skill in registry["skills"]:
        name = skill["name"]
        if name in names or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Duplicate or invalid skill name: {name}")
        names.add(name)
        folder = root / skill["path"]
        if folder.resolve().parent != (root / "skills").resolve() or folder.name != name:
            raise ValueError(f"Invalid source path for {name}")
        text = (folder / "SKILL.md").read_text()
        if not text.startswith("---\n") or not re.search(r"^name:\s*" + re.escape(name) + r"\s*$", text, re.M):
            raise ValueError(f"Wrong skill entry point for {name}")
        for relative, expected in skill["files"].items():
            path = folder / relative
            if not path.resolve().is_relative_to(folder.resolve()) or path.is_symlink():
                raise ValueError(f"Unsafe manifest path in {name}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != expected:
                raise ValueError(f"File differs from manifest: {path}")
            declared.add(path.relative_to(root).as_posix())
    actual = {p.relative_to(root).as_posix() for p in (root / "skills").rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store"}
    if actual != declared:
        raise ValueError("Registry files differ from source tree: " + str(sorted(actual ^ declared)[:10]))
    if registry["total"] != len(names):
        raise ValueError("Incorrect skill count")
    print(f"PASS: {len(names)} unique skill entry points and {len(declared)} complete files verified")
    return True


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, OSError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
