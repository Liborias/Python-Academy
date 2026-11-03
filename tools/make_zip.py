#!/usr/bin/env python3
"""Zabalí projekt do ZIP (bez .venv, řešení studenta, cache a dočasných souborů).  python tools/make_zip.py [výstup.zip]"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "dilna-pythonu-v0.36.zip"
SKIP_DIRS = {".venv", "__pycache__", "_run", ".git", "node_modules"}
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or f.suffix == ".pyc":
            continue
        if rel.parts[0] == "workspace" and rel.name != ".gitkeep":
            continue
        z.write(f, Path("dilna-pythonu") / rel); n += 1
print(f"{out}  ({n} souborů, {out.stat().st_size // 1024} kB)")
