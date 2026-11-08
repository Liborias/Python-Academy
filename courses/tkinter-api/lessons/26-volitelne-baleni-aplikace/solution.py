from pathlib import Path
import sys
import json


def prikaz_sestaveni(python, skript, vystup, jmeno="KorespondencniDilna"):
    if not isinstance(python, str) or not python.strip():
        raise ValueError("Zadejte interpreter Pythonu.")
    if (not isinstance(jmeno, str) or not 1 <= len(jmeno) <= 40 or not jmeno.isascii()
            or not jmeno[0].isalpha() or not all(c.isalnum() or c in "_-" for c in jmeno)):
        raise ValueError("Název má začínat písmenem ASCII a obsahovat jen písmena, číslice, _ a -.")
    skript = Path(skript).resolve()
    vystup = Path(vystup).resolve()
    if not skript.is_file() or skript.suffix.lower() != ".py":
        raise ValueError("Vstup musí být existující soubor .py.")
    # Seznam uchová cesty s mezerami jako samostatné argumenty, žádný shell.
    prikaz = [python, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--console",
              "--name", jmeno, "--distpath", str(vystup / "dist"),
              "--workpath", str(vystup / "build"), "--specpath", str(vystup / "spec")]
    data = skript.parent / "data"
    if data.is_dir():
        prikaz.extend(["--add-data", str(data) + ":data"])
    prikaz.append(str(skript))
    return prikaz


if __name__ == "__main__":
    # Výuková ukázka příkaz pouze připraví a vypíše, nic nesestavuje.
    skript = Path(__file__).with_name("dilna.py")
    prikaz = prikaz_sestaveni(sys.executable, skript, skript.parent / "sestaveni")
    print("Argumenty pro volitelné sestavení:")
    print(json.dumps(prikaz, ensure_ascii=False, indent=2))
