"""Pomocné soubory lekce (složka lessons/<lekce>/files/): kopírují se vedle kódu studenta."""
import shutil
from pathlib import Path

MAX_FILES = 40
MAX_FILE_BYTES = 2_000_000


def copy_files(src: Path | None, dst: Path, overwrite: bool = True) -> int:
    """Zkopíruje běžné soubory (i v podsložkách) ze `src` do `dst`. Symbolické odkazy se přeskakují."""
    if not src or not Path(src).is_dir():
        return 0
    src = Path(src).resolve()
    n = 0
    for f in sorted(src.rglob("*")):
        if n >= MAX_FILES:
            break
        if f.is_symlink() or not f.is_file() or f.stat().st_size > MAX_FILE_BYTES:
            continue
        rel = f.relative_to(src)
        if ".." in rel.parts:
            continue
        target = Path(dst) / rel
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, target)
        n += 1
    return n
