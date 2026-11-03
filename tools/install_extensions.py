#!/usr/bin/env python3
"""Nainstaluje doporučená rozšíření do VSCodium (z .vscode/extensions.json) a vypíše, co se povedlo.

  python tools/install_extensions.py [--dry-run]
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dry = "--dry-run" in sys.argv
exts = json.loads((ROOT / ".vscode" / "extensions.json").read_text(encoding="utf-8"))["recommendations"]
exe = shutil.which("codium") or shutil.which("vscodium")
if not exe and not dry:
    print("Příkaz codium nebyl nalezen v PATH.\nVe VSCodium: Ctrl+Shift+P → „Shell Command: Install 'codium' command in PATH“ (macOS),\n"
          "nebo rozšíření hledejte ručně v panelu Rozšíření (Ctrl+Shift+X) podle těchto identifikátorů:")
    for e in exts: print("  ", e)
    sys.exit(1)
bad = []
for e in exts:
    if dry:
        print("codium --install-extension", e); continue
    r = subprocess.run([exe, "--install-extension", e], capture_output=True, text=True)
    ok = r.returncode == 0 and "successfully" in (r.stdout + r.stderr).lower()
    print(("[ OK ] " if ok else "[CHYBA] ") + e + ("" if ok else "  " + (r.stdout + r.stderr).strip().splitlines()[-1:][0] if (r.stdout + r.stderr).strip() else ""))
    if not ok: bad.append(e)
if bad:
    print("\nNepodařilo se:", ", ".join(bad), "\nPostup při potížích: docs/reseni-problemu.md (aplikace funguje i bez rozšíření).")
sys.exit(1 if bad else 0)
