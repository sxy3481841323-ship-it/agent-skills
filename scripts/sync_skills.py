#!/usr/bin/env python3
"""Install complete skills without overwriting local work; import into the master."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REPOSITORY = "https://github.com/sxy3481841323-ship-it/agent-skills"
IGNORED = {".git", "node_modules", "__pycache__", ".DS_Store", ".venv", ".shared-skill.json"}
AGENTS = {
    "codex": ".agents/skills",
    "claude-code": ".claude/skills",
    "antigravity": ".gemini/config/skills",
    "gemini-cli": ".gemini/skills",
}
SECRET = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-(?:ant-api\d+-)?[A-Za-z0-9_-]{35,})")


def skill_name(path):
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    match = re.search(r"^name:\s*([^\r\n]+)", front.group(1), re.M) if front else None
    if not match:
        raise ValueError(f"Missing skill name: {path}")
    name = match.group(1).strip().strip("\"'")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError(f"Invalid skill name in {path}")
    return name


def discover(base):
    result = {}
    if not base.is_dir():
        return result
    for path in sorted(base.iterdir()):
        if path.is_dir() and (path / "SKILL.md").is_file():
            name = skill_name(path)
            if name in result:
                raise ValueError(f"Duplicate declared skill name: {name}")
            result[name] = path
    return result


def files(path):
    result = []
    for item in sorted(path.rglob("*")):
        relative = item.relative_to(path)
        if any(p in IGNORED or p.startswith(".env") for p in relative.parts):
            continue
        if item.is_symlink():
            raise ValueError(f"Symlinks must be resolved before import/install: {item}")
        if item.is_file():
            result.append((item, relative.as_posix()))
    return result


def hashes(path):
    return {rel: hashlib.sha256(p.read_bytes()).hexdigest() for p, rel in files(path)}


def check_secrets(path):
    for item, relative in files(path):
        if item.stat().st_size <= 2 * 1024 * 1024:
            content = item.read_bytes()
            if b"\0" in content:
                continue
            if SECRET.search(content.decode("utf-8", errors="ignore")):
                raise ValueError(f"Possible credential; refusing import: {relative}")


def copy_complete(source, target):
    target.mkdir(parents=True)
    for item, relative in files(source):
        dest = target / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)


def sync_one(source, target_root, *, dry_run=False, update=False, importing=False):
    name = skill_name(source)
    existing = discover(target_root).get(name)
    dest = existing or target_root / name
    desired = hashes(source)
    if dest.exists():
        if hashes(dest) == desired:
            return "unchanged", name
        if not update:
            return "conflict", name
        marker = dest / ".shared-skill.json"
        if importing or not marker.is_file():
            return "conflict", name
        saved = json.loads(marker.read_text())
        if saved.get("repository") != REPOSITORY or saved.get("files") != hashes(dest):
            return "conflict", name
    if dry_run:
        return "would-update" if dest.exists() else "would-install", name
    target_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".skill-stage-", dir=target_root))
    staged = temporary / name
    backup = temporary / "previous"
    try:
        copy_complete(source, staged)
        assert hashes(staged) == desired
        if not importing:
            (staged / ".shared-skill.json").write_text(json.dumps({"repository": REPOSITORY, "name": name, "files": desired}, indent=2) + "\n")
        if dest.exists():
            dest.rename(backup)
        try:
            staged.rename(dest)
        except BaseException:
            if backup.exists():
                backup.rename(dest)
            raise
        return "updated" if backup.exists() else "installed", name
    finally:
        shutil.rmtree(temporary)


def install_workspace_rule(workspace, dry_run=False):
    rule = (ROOT / "PROJECT_RULES.md").read_text()
    path = workspace / "AGENTS.md"
    old = path.read_text() if path.is_file() else ""
    pattern = r"<!-- shared-agent-skills:start -->.*?<!-- shared-agent-skills:end -->"
    new = re.sub(pattern, lambda _: rule.strip(), old, flags=re.S) if re.search(pattern, old, re.S) else old.rstrip() + "\n\n" + rule
    if not dry_run:
        workspace.mkdir(parents=True, exist_ok=True)
        path.write_text(new.lstrip())
    print(("would-write " if dry_run else "wrote ") + str(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append", choices=[*AGENTS, "all"], help="Agent global directory; repeat to install for multiple agents")
    parser.add_argument("--target", action="append", type=Path, help="Explicit custom skill directory")
    parser.add_argument("--skills", nargs="+", help="Install only these declared skill names")
    parser.add_argument("--list", action="store_true", help="List available skills, without writing anything")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update", action="store_true", help="Update only unchanged copies previously managed by this script")
    parser.add_argument("--import", "--push", dest="imports", nargs="+", help="Import complete local skills into the master; does not publish automatically")
    parser.add_argument("--source", action="append", type=Path, help="Local skill root to import from; repeatable")
    parser.add_argument("--workspace", type=Path, help="Install shared AGENTS rule in the common projects parent")
    args = parser.parse_args(argv)
    available = discover(SKILLS)
    if args.list:
        for name in sorted(available):
            print(name)
        print(f"Total: {len(available)}")
        return 0
    if args.workspace:
        install_workspace_rule(args.workspace.expanduser().resolve(), args.dry_run)
        if not (args.agent or args.target or args.imports):
            return 0
    if args.imports:
        candidates = {}
        sources = args.source or [Path.home() / suffix for suffix in AGENTS.values()]
        for base in sources:
            for name, path in discover(base.expanduser().resolve()).items():
                if name in candidates and hashes(candidates[name]) != hashes(path):
                    raise ValueError(f"Multiple different local versions of {name}; pass one --source")
                candidates[name] = path
        missing = set(args.imports) - candidates.keys()
        if missing:
            parser.error("Local skills not found: " + ", ".join(sorted(missing)))
        conflicts = 0
        for name in args.imports:
            check_secrets(candidates[name])
            state, _ = sync_one(candidates[name], SKILLS, dry_run=args.dry_run, importing=True)
            print(f"{state}: {name}")
            conflicts += state == "conflict"
        if not args.dry_run:
            print("Next: python3 scripts/build_registry.py && python3 scripts/validate_library.py; then commit and push only your skill changes.")
        return 2 if conflicts else 0
    aliases = {}
    registry_path = ROOT / "registry.json"
    if registry_path.is_file():
        for item in json.loads(registry_path.read_text()).get("skills", []):
            for alias in item.get("aliases", []):
                if alias in aliases and aliases[alias] != item["name"]:
                    raise ValueError(f"Ambiguous skill alias: {alias}")
                aliases[alias] = item["name"]
    selected = list(dict.fromkeys(aliases.get(name, name) for name in args.skills or []))
    missing = set(selected) - available.keys()
    if missing:
        parser.error("Unknown skills: " + ", ".join(sorted(missing)))
    names = selected or sorted(available)
    agents = args.agent or []
    if "all" in agents:
        agents = list(AGENTS)
    targets = [p.expanduser().resolve() for p in args.target or []]
    targets += [Path.home() / AGENTS[a] for a in agents]
    if not targets:
        targets = [Path.home() / suffix for suffix in AGENTS.values() if (Path.home() / suffix).is_dir()]
    if not targets:
        parser.error("Choose --agent codex/antigravity/claude-code/gemini-cli or --target DIR; use --list to inspect first.")
    conflicts = 0
    totals = {}
    for target in dict.fromkeys(targets):
        # Managed ChatGPT installations have a separate synchronization protocol.
        if target == Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" and (target / "remote-skills" / ".git").exists():
            raise ValueError("Use the ChatGPT personal-skills installation workflow, or select a standalone CLI directory.")
        for name in names:
            state, _ = sync_one(available[name], target, dry_run=args.dry_run, update=args.update)
            print(f"{state}: {name} -> {target / name}")
            totals[state] = totals.get(state, 0) + 1
            conflicts += state == "conflict"
    print(json.dumps(totals, sort_keys=True))
    return 2 if conflicts else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
