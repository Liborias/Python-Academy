from pathlib import Path
import sys
import json


def prikaz_sestaveni(python, skript, vystup, jmeno="KorespondencniDilna"):
    # TODO: ověřte vstup a vraťte celý seznam argumentů, PyInstaller zde nespouštějte.
    return []


if __name__ == "__main__":
    # Výuková ukázka příkaz pouze připraví a vypíše, nic nesestavuje.
    skript = Path(__file__).with_name("dilna.py")
    prikaz = prikaz_sestaveni(sys.executable, skript, skript.parent / "sestaveni")
    print("Argumenty pro volitelné sestavení:")
    print(json.dumps(prikaz, ensure_ascii=False, indent=2))
