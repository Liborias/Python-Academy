"""Čtení obsahu kurzů a práce s pracovní složkou studenta (workspace/<podkurz>/<lekce>/reseni.py)."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from .checker import ID_RE, lesson_dir
from .lessonfiles import copy_files


def _read(p: Path, default=""):
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return default


def _json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _has_solution(directory: Path) -> bool:
    return bool(_read(directory / "solution.py").strip())


def solution_view(courses_dir: Path, cid: str, lid: str, task: str | None = None) -> dict | None:
    """Vzorový kód vybraného úkolu se načítá až při odkrytí řešení."""
    directory = lesson_dir(courses_dir, cid, lid, task)
    if directory is None:
        return None
    code = _read(directory / "solution.py")
    if not code.strip():
        return None
    return {"course": cid, "lesson": lid, "task": task or "task-1", "code": code}


def course_view(courses_dir: Path, cid: str) -> dict:
    """course.json obohacený o názvy lekcí a průběžné číslování."""
    if not ID_RE.match(cid or ""):
        return {"id": cid, "modules": []}
    base = Path(courses_dir) / cid
    c = _json(base / "course.json", None)
    if not isinstance(c, dict):
        return {"id": cid, "modules": []}
    n = 0
    for m in c.get("modules", []):
        out = []
        for lid in m.get("lessons", []):
            if not ID_RE.match(str(lid)):
                continue
            n += 1
            meta = _json(base / "lessons" / lid / "lesson.json", {})
            out.append({"id": lid, "n": n, "title": meta.get("title", lid), "minutes": meta.get("minutes")})
        m["lessons"] = out
    if isinstance(c.get("learning_plan"), dict):
        c["learning_plan"]["md"] = _read(base / "plan.md")
    return c


def lesson_view(courses_dir: Path, cid: str, lid: str) -> dict | None:
    if not (ID_RE.match(cid or "") and ID_RE.match(lid or "")):
        return None
    d = Path(courses_dir) / cid / "lessons" / lid
    if not (d / "lesson.md").is_file():
        return None
    meta = _json(d / "lesson.json", {})
    default_timeout = 600 if meta.get("kind") == "gui" else 20
    run_timeout = meta.get("run_timeout", default_timeout)
    if type(run_timeout) is not int or not 1 <= run_timeout <= 600:
        run_timeout = default_timeout
    return {"id": lid, "course": cid, "title": meta.get("title", lid), "kind": meta.get("kind", "console"),
            "minutes": meta.get("minutes"), "run_timeout": run_timeout, "md": _read(d / "lesson.md"), "example": _read(d / "example.py"),
            "example_title": meta.get("example_title", meta.get("title", lid)),
            "preview_images": meta.get("preview_images") is True,
            "download_files": meta.get("download_files") is True,
            "examples": _json(d / "examples.json", []),
            "exercise": _read(d / "exercise.py"), "quiz": _json(d / "quiz.json", []),
            "has_check": (d / "check.py").is_file(),
            "has_solution": _has_solution(d),
            "tasks": [{"id": task["id"], "title": task["title"],
                       "md": _read(d / "tasks" / task["id"] / "exercise.md"),
                       "exercise": _read(d / "tasks" / task["id"] / "exercise.py"),
                       "has_solution": _has_solution(d / "tasks" / task["id"])}
                      for task in _json(d / "tasks.json", [])]}


def workspace_file(root: Path, cid: str, lid: str, task: str | None = None) -> Path | None:
    if not (ID_RE.match(cid or "") and ID_RE.match(lid or "")):
        return None
    base = Path(root) / "workspace" / cid / lid
    if task not in (None, "", "task-1"):
        if not isinstance(task, str) or task not in {"task-2", "task-3", "task-4", "task-5"}:
            return None
        base = base / "tasks" / task
    return base / "reseni.py"


def save_workspace(root: Path, cid: str, lid: str, code: str, files: Path | None = None, task: str | None = None) -> Path | None:
    f = workspace_file(root, cid, lid, task)
    if f is None or not isinstance(code, str) or len(code) > 200_000:
        return None
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(code, encoding="utf-8")
    copy_files(files, f.parent, overwrite=False)      # pomocné soubory lekce, už upravené se nepřepisují
    return f


def open_in_editor(path: Path) -> dict:
    """Pokusí se otevřít soubor ve VSCodium. Vrací {opened, via, uri}."""
    uri = "vscodium://file/" + str(path.resolve()).replace("\\", "/").lstrip("/")
    for exe in ("codium", "vscodium"):
        found = shutil.which(exe)
        if found:
            try:
                kw = {"creationflags": 0x00000008} if sys.platform == "win32" else {"start_new_session": True}
                subprocess.Popen([found, str(path)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, **kw)
                return {"opened": True, "via": exe, "uri": uri}
            except OSError:
                pass
    return {"opened": False, "via": None, "uri": uri}
