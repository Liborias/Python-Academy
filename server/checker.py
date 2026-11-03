"""Spuštění kontroly lekce (check.py) nad kódem studenta v samostatném podprocesu."""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .lessonfiles import copy_files
from .runner import MAX_CODE, clean_env

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
CHECK_TIMEOUT = 30


def lesson_dir(courses_dir: Path, course: str, lesson: str, task: str | None = None) -> Path | None:
    if not (ID_RE.match(course or "") and ID_RE.match(lesson or "")):
        return None
    d = Path(courses_dir) / course / "lessons" / lesson
    if task not in (None, "", "task-1"):
        if not isinstance(task, str) or task not in {"task-2", "task-3", "task-4", "task-5"}:
            return None
        d = d / "tasks" / task
    return d if (d / "check.py").is_file() else None


def run_check(lesson: Path, code: str, lib_dir: Path, workdir: Path, python: str | None = None,
              timeout: float = CHECK_TIMEOUT) -> dict:
    """Vrací {"ok": bool, "results": [...]} nebo {"ok": False, "error": "..."}."""
    if not isinstance(code, str) or len(code) > MAX_CODE:
        return {"ok": False, "error": "Kód je neplatný nebo příliš dlouhý."}
    workdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="check-", dir=workdir) as tmp:
        tmp = Path(tmp)
        copy_files(lesson / "files", tmp)
        student = tmp / "reseni.py"
        student.write_text(code, encoding="utf-8")
        result = tmp / "result.json"
        env = clean_env({
            "DILNA_STUDENT": str(student), "DILNA_RESULT": str(result),
            "DILNA_DATA": str(lesson.parent.parent / "data"),
            "PYTHONPATH": str(lib_dir),
            "SDL_VIDEODRIVER": "dummy", "SDL_AUDIODRIVER": "dummy",
        })
        try:
            p = subprocess.run([python or sys.executable, "-X", "utf8", str(lesson / "check.py")],
                               cwd=tmp, env=env, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Kontrola trvala příliš dlouho. Nemáte v kódu nekonečný cyklus?"}
        if result.is_file():
            try:
                return json.loads(result.read_text(encoding="utf-8"))
            except ValueError:
                pass
        tail = p.stderr.decode("utf-8", "replace").strip().splitlines()[-3:]
        return {"ok": False, "error": "Kontrola selhala: " + " | ".join(tail)}
