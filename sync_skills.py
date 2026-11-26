#!/usr/bin/env python3
"""Public, dependency-free entry point for shared skill installation/import."""
import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "scripts" / "sync_skills.py"), run_name="__main__")
