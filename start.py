#!/usr/bin/env python3
"""Spuštění Dílny Pythonu: zkontroluje verzi Pythonu, spustí místní server a otevře prohlížeč.

Používá jen standardní knihovnu. Server poslouchá výhradně na 127.0.0.1.
Použití:  python start.py [--port 8765] [--no-browser]
"""
import argparse
import sys
import webbrowser
from pathlib import Path

def venv_python(root: Path) -> Path:
    """Python z .venv (cvičení se spouští v něm), pokud existuje."""
    return root / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


MIN_PYTHON = (3, 11)  # kurz je testován na 3.12 až 3.15
ROOT = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Dílna Pythonu")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    if sys.version_info < MIN_PYTHON:
        print(f"Je potřeba Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} nebo novější, "
              f"máte {sys.version.split()[0]}.")
        return 1

    # server/ je balíček v kořeni projektu
    sys.path.insert(0, str(ROOT))
    from server.app import create_server

    py = venv_python(ROOT)
    server = create_server(ROOT, "127.0.0.1", args.port, python=str(py) if py.exists() else None)
    print("Cvičení běží v:", server.runs.python)
    url = f"http://127.0.0.1:{args.port}/?t={server.token}"
    print(f"Dílna Pythonu běží na {url}\n(adresa obsahuje jednorázový token, nesdílejte ji; ukončení: Ctrl+C)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKonec.")
    finally:
        server.runs.stop_all()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
