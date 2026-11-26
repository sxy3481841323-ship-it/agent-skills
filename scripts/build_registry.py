#!/usr/bin/env python3
"""Rebuild the public, portable skill catalog using only the standard library."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://github.com/sxy3481841323-ship-it/agent-skills"
RAW_URL = "https://raw.githubusercontent.com/sxy3481841323-ship-it/agent-skills/main"


def metadata(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    values = {}
    lines = match.group(1).splitlines()
    for index, line in enumerate(lines):
        key, separator, value = line.partition(":")
        if separator and key in {"name", "description"}:
            value = value.strip()
            if value in {">", ">-", ">+", "|", "|-", "|+"}:
                continuation = []
                for following in lines[index + 1:]:
                    if following and not following[0].isspace():
                        break
                    continuation.append(following.strip())
                values[key] = (" " if value.startswith(">") else "\n").join(continuation).strip()
            elif value.startswith('"'):
                values[key] = json.loads(value)
            elif value.startswith("'") and value.endswith("'"):
                values[key] = value[1:-1].replace("''", "'")
            else:
                values[key] = value
    if not values.get("name") or not values.get("description"):
        raise ValueError(f"Missing name/description: {path}")
    return values


def category(name):
    if re.search(r"brainstorm|inventor|product-design|design-thinking|emotion|creative|psychology", name):
        return "创意发散与产品构思"
    if re.search(r"game|phaser|level|camera|input|audio-design|dialogue", name):
        return "游戏玩法、镜头与声效"
    if re.search(r"threejs|3d|spline", name):
        return "3D、材质与交互场景"
    if re.search(r"animat|motion|gesture|choreograph|scroll", name):
        return "动效、手势与空间叙事"
    if re.search(r"art|canvas|poster|image|scientific|slide|brand|theme|logo|color|typograph|font", name):
        return "视觉艺术、品牌与演示"
    return "界面设计与审美打磨"


def build(root=ROOT):
    inventory_path = root / "source-inventory.json"
    inventory = {s["name"]: s for s in json.loads(inventory_path.read_text())} if inventory_path.exists() else {}
    entries = []
    checksums = []
    for skill_dir in sorted((root / "skills").iterdir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        meta = metadata(skill_dir / "SKILL.md")
        if meta["name"] != skill_dir.name:
            raise ValueError(f"Folder/name mismatch: {skill_dir.name} != {meta['name']}")
        manifest = {}
        text = (skill_dir / "SKILL.md").read_text()
        for path in sorted(skill_dir.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Unportable symlink: {path}")
            if not path.is_file() or "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            relative = path.relative_to(root).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest[path.relative_to(skill_dir).as_posix()] = digest
            checksums.append(f"{digest}  {relative}")
        source = inventory.get(skill_dir.name, {})
        entry = {
            "name": meta["name"],
            "aliases": source.get("aliases", []),
            "description": meta["description"],
            "category": category(meta["name"]),
            "path": skill_dir.relative_to(root).as_posix(),
            "skill_md": (skill_dir / "SKILL.md").relative_to(root).as_posix(),
            "read_url": f"{BASE_URL}/blob/main/skills/{meta['name']}/SKILL.md",
            "raw_url": f"{RAW_URL}/skills/{meta['name']}/SKILL.md",
            "invoke": "$" + meta["name"],
            "source_repository": source.get("source_repository"),
            "source_commit": source.get("source_commit"),
            "source_path": source.get("source_path"),
            "external_credentials_mentioned": sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}_(?:API_KEY|TOKEN)\b", text))),
            "file_count": len(manifest),
            "files": manifest,
        }
        entries.append(entry)
    counts = {}
    for entry in entries:
        counts[entry["category"]] = counts.get(entry["category"], 0) + 1
    registry = {
        "schema_version": 1,
        "repository": BASE_URL,
        "skills_root": "skills",
        "total": len(entries),
        "categories": counts,
        "download_zip": BASE_URL + "/archive/refs/heads/main.zip",
        "usage_rule": "Read a SKILL.md remotely for instructions; install the complete skill directory for scripts/assets and automatic discovery. External service availability is separate from installation.",
        "skills": entries,
    }
    (root / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    (root / "checksums.sha256").write_text("\n".join(checksums) + "\n")
    lines = ["# 共享技能目录", "", f"共 {len(entries)} 项；源文件统一位于 `skills/<name>/`。点击名称读取完整说明，所有配套文件均保存在同一目录。", "", "如技能需要第三方 API、软件或账号，需在实际使用时单独满足；保存或安装本库不会调用这些服务。", ""]
    for group in counts:
        lines += ["## " + group, "", "| 技能与调用名 | 用途 |", "| --- | --- |"]
        for item in entries:
            if item["category"] == group:
                desc = item["description"].replace("|", "\\|").replace("\n", " ")
                if len(desc) > 210:
                    desc = desc[:207] + "…"
                lines.append(f"| [{item['name']}]({item['skill_md']}) · `{item['invoke']}` | {desc} |")
        lines.append("")
    (root / "CATALOG.md").write_text("\n".join(lines))
    return registry


if __name__ == "__main__":
    result = build()
    print(json.dumps({"skills": result["total"], "categories": result["categories"]}, ensure_ascii=False))
