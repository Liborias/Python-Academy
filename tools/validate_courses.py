#!/usr/bin/env python3
"""Ověří obsah podkurzů.   python tools/validate_courses.py [--course ID] [--courses-dir DIR]

Pro každou lekci zkontroluje: soubory, course.json, kvíz, komentáře v ukázce, zakázaná témata,
že se ukázka spustí, že vzorové řešení projde kontrolou a že výchozí šablona NEPROJDE.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import ID_RE, run_check  # noqa: E402

REQUIRED = ["lesson.json", "lesson.md", "example.py", "exercise.py", "check.py", "solution.py"]
BANNED = re.compile(r"harry|potter|hogwarts|mozkomor|bradavic|voldemort", re.I)   # zadání: žádný Harry Potter
errors: list[str] = []
warns: list[str] = []


def err(where, msg): errors.append(f"{where}: {msg}")


def run_example(d: Path, kind: str):
    ex = d / "example.py"
    try:
        compile(ex.read_text("utf-8"), str(ex), "exec")
    except SyntaxError as e:
        return err(d.name, f"example.py má syntaktickou chybu: {e}")
    if kind == "gui":
        return run_gui_example(d, ex)
    stdin = (d / "example.stdin").read_text("utf-8") if (d / "example.stdin").is_file() else ""
    run_dir = Path(tempfile.mkdtemp(prefix="ex-"))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from server.lessonfiles import copy_files
    copy_files(d / "files", run_dir)
    (run_dir / "main.py").write_text(ex.read_text("utf-8"), encoding="utf-8")   # jako ve skutečném runneru
    try:
        p = subprocess.run([sys.executable, "-X", "utf8", "main.py"], input=stdin.encode(), capture_output=True, timeout=15, cwd=run_dir)
    except subprocess.TimeoutExpired:
        return err(d.name, "example.py běžel déle než 15 s (chybí example.stdin?)")
    if p.returncode:
        err(d.name, "example.py skončil chybou: " + (p.stderr.decode("utf-8", "replace").strip().splitlines() or ["?"])[-1])



def validate_extra_examples(d: Path):
    """Zkontroluje metadata i skutečný běh všech přepínatelných konzolových ukázek."""
    path = d / "examples.json"
    if not path.is_file():
        return
    try:
        examples = json.loads(path.read_text("utf-8"))
    except ValueError as exc:
        return err(d.name, f"examples.json není platný JSON: {exc}")
    if not isinstance(examples, list) or not examples:
        return err(d.name, "examples.json musí být neprázdný seznam")
    seen = {"original"}
    for i, example in enumerate(examples):
        label = f"{d.name}/examples.json[{i}]"
        if not isinstance(example, dict) or any(
            not isinstance(example.get(key), str) or not example[key].strip()
            for key in ("id", "title", "description", "code")
        ):
            err(label, "chybí neprázdné id/title/description/code")
            continue
        if not ID_RE.fullmatch(example["id"]) or example["id"] in seen:
            err(label, "neplatné nebo duplicitní id")
        seen.add(example["id"])
        code = example["code"]
        if not isinstance(example.get("stdin", ""), str):
            err(label, "stdin musí být text")
            continue
        if sum(line.lstrip().startswith("#") for line in code.splitlines()) < 2:
            err(label, "ukázka má málo vysvětlujících komentářů (min. 2)")
        if BANNED.search(json.dumps(example, ensure_ascii=False)):
            err(label, "zakázané téma")
        from server.lessonfiles import copy_files
        with tempfile.TemporaryDirectory(prefix="extra-ex-") as temp:
            work = Path(temp)
            copy_files(d / "files", work)
            (work / "main.py").write_text(code, encoding="utf-8")
            try:
                result = subprocess.run([sys.executable, "-X", "utf8", "main.py"],
                                        input=example.get("stdin", ""), capture_output=True,
                                        text=True, timeout=15, cwd=work)
                if result.returncode:
                    err(label, "ukázka skončila chybou: " + result.stderr.strip())
            except subprocess.TimeoutExpired:
                err(label, "ukázka běžela déle než 15 s (chybí stdin?)")


def run_turtle_example(d: Path, ex: Path, code: str):
    """Želví příklad se spustí bez okna přes turtlerun (náhrada modulu turtle, která si pamatuje kreslení)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from server.lessonfiles import copy_files
    run_dir = Path(tempfile.mkdtemp(prefix="ttex-"))
    copy_files(d / "files", run_dir)
    (run_dir / "main.py").write_text(code, encoding="utf-8")
    (run_dir / "spec.json").write_text("{}", encoding="utf-8")
    runner = Path(__file__).resolve().parent.parent / "lib" / "dilna_check" / "turtlerun.py"
    try:
        p = subprocess.run([sys.executable, "-X", "utf8", str(runner), "main.py", "spec.json", "out.json"], capture_output=True,
                           timeout=30, cwd=run_dir)
    except subprocess.TimeoutExpired:
        return err(d.name, "example.py (turtle) běžel déle než 30 s")
    out = run_dir / "out.json"
    if not out.is_file():
        return err(d.name, "example.py (turtle) nešel spustit: " + (p.stderr.decode("utf-8", "replace").strip().splitlines() or ["?"])[-1])
    import json as _json
    res = _json.loads(out.read_text("utf-8"))
    if res.get("error"):
        err(d.name, f"example.py (turtle) skončil chybou {res['error']['type']}: {res['error']['msg']}")
    elif not (res.get("segments") or res.get("dots") or res.get("texts") or res.get("stamps")):
        err(d.name, "example.py (turtle) nic nenakreslil")


def run_gui_example(d: Path, ex: Path):
    """Okenní příklad se spustí bez okna přes pgrun (pro pygame); Tkinter se jen zkompiluje."""
    code = ex.read_text("utf-8")
    if "import turtle" in code or "from turtle" in code:
        return run_turtle_example(d, ex, code)
    if "pygame" not in code:
        return
    try:
        import pygame  # noqa: F401
    except ImportError:
        warns.append(f"{d.name}: pygame-ce není nainstalován, příklad nebyl spuštěn bez okna")
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from server.lessonfiles import copy_files
    run_dir = Path(tempfile.mkdtemp(prefix="pgex-"))
    copy_files(d / "files", run_dir)
    (run_dir / "main.py").write_text(code, encoding="utf-8")
    (run_dir / "spec.json").write_text('{"frames": 5}', encoding="utf-8")
    runner = Path(__file__).resolve().parent.parent / "lib" / "dilna_check" / "pgrun.py"
    try:
        p = subprocess.run([sys.executable, "-X", "utf8", str(runner), "main.py", "spec.json", "out.json"], capture_output=True,
                           timeout=30, cwd=run_dir)
    except subprocess.TimeoutExpired:
        return err(d.name, "example.py (pygame) neprovedl během 30 s žádný snímek (chybí display.flip?)")
    out = run_dir / "out.json"
    if not out.is_file():
        return err(d.name, "example.py (pygame) nešel spustit: " + (p.stderr.decode("utf-8", "replace").strip().splitlines() or ["?"])[-1])
    import json as _json
    res = _json.loads(out.read_text("utf-8"))
    if res.get("error"):
        err(d.name, f"example.py (pygame) skončil chybou {res['error']['type']}: {res['error']['msg']}")
    elif not res.get("frames") and not res.get("ended"):
        err(d.name, "example.py (pygame) nic nenakreslil")


def validate_tasks(d: Path, work: Path):
    manifest = d / "tasks.json"
    if not manifest.exists():
        return
    try:
        tasks = json.loads(manifest.read_text("utf-8"))
    except ValueError:
        return err(d.name, "tasks.json není platný JSON")
    if not isinstance(tasks, list):
        return err(d.name, "tasks.json musí být seznam")
    ids = set()
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str) or task.get("id") not in {"task-2", "task-3", "task-4", "task-5"} or not task.get("title"):
            err(d.name, "neplatná metadata úkolu")
            continue
        tid = task["id"]
        if tid in ids:
            err(d.name, "duplicitní úkol")
        ids.add(tid)
        directory = d / "tasks" / tid
        label = f"{d.name}/{tid}"
        if any(not (directory / name).is_file() for name in ("exercise.md", "exercise.py", "solution.py", "check.py")):
            err(label, "chybí zadání, šablona, řešení nebo kontrola")
            continue
        if not (directory / "exercise.md").read_text("utf-8").strip():
            err(label, "prázdné zadání")
        for name, expected in (("solution.py", True), ("exercise.py", False)):
            result = run_check(directory, (directory / name).read_text("utf-8"), ROOT / "lib", work)
            if bool(result.get("ok")) != expected or result.get("error"):
                err(label, f"{name}: " + str(result))


def validate_lesson(cdir: Path, lid: str, work: Path):
    d = cdir / "lessons" / lid
    if not ID_RE.match(lid): return err(lid, "neplatné id lekce")
    if not d.is_dir(): return err(lid, "složka lekce neexistuje")
    meta_path = d / "lesson.json"
    try:
        meta = json.loads(meta_path.read_text("utf-8")) if meta_path.is_file() else {}
    except ValueError as exc:
        return err(lid, f"lesson.json není platný JSON: {exc}")
    if meta.get("kind") == "guide":
        if not meta.get("title"):
            err(lid, "lesson.json nemá title")
        text = (d / "lesson.md").read_text("utf-8") if (d / "lesson.md").is_file() else ""
        for heading in ("## Cíl", "## Praktický krok", "## Vlastní ověření"):
            if heading not in text:
                err(lid, f"průvodci chybí oddíl {heading}")
        if "- [ ]" not in text:
            err(lid, "průvodci chybí vlastní kontrolní seznam")
        if (d / "check.py").exists() or (d / "exercise.py").exists():
            err(lid, "průvodce nesmí předstírat automatickou kontrolu místní instalace")
        return
    for f in REQUIRED:
        if not (d / f).is_file(): err(lid, f"chybí {f}")
    if errors and any(e.startswith(f"{lid}: chybí") for e in errors): return
    meta = json.loads((d / "lesson.json").read_text("utf-8"))
    if not meta.get("title"): err(lid, "lesson.json nemá title")
    if meta.get("kind", "console") not in ("console", "gui", "notebook"): err(lid, "neplatné kind")
    for f in d.iterdir():
        if f.suffix in (".md", ".py", ".json") and BANNED.search(f.read_text("utf-8")): err(lid, f"{f.name}: zakázané téma (Harry Potter apod.)")
    ex = (d / "example.py").read_text("utf-8")
    if sum(1 for l in ex.splitlines() if "#" in l) < 2: err(lid, "ukázka má málo vysvětlujících komentářů (min. 2)")
    if not (d / "lesson.md").read_text("utf-8").strip().startswith("##"): warns.append(f"{lid}: lesson.md nezačíná nadpisem ##")
    if (d / "quiz.json").is_file():
        try:
            for i, q in enumerate(json.loads((d / "quiz.json").read_text("utf-8"))):
                if not (isinstance(q.get("options"), list) and len(q["options"]) >= 2 and isinstance(q.get("answer"), int) and 0 <= q["answer"] < len(q["options"]) and q.get("q") and q.get("why")):
                    err(lid, f"kvíz, otázka {i + 1}: chybí q/options/answer/why nebo je answer mimo rozsah")
        except ValueError as e:
            err(lid, f"quiz.json není platný JSON: {e}")
    run_example(d, meta.get("kind", "console"))
    validate_extra_examples(d)
    validate_tasks(d, work)
    sol = run_check(d, (d / "solution.py").read_text("utf-8"), ROOT / "lib", work)
    if not sol.get("ok"):
        err(lid, "VZOROVÉ ŘEŠENÍ NEPROŠLO: " + (sol.get("error") or "; ".join(f"{r['name']} ({r['msg']})" for r in sol.get("results", []) if not r["ok"])))
    st = run_check(d, (d / "exercise.py").read_text("utf-8"), ROOT / "lib", work)
    if st.get("ok"):
        err(lid, "VÝCHOZÍ ŠABLONA PROŠLA kontrolou (úkol je už splněný)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--course"); ap.add_argument("--courses-dir", default=str(ROOT / "courses"))
    a = ap.parse_args()
    cdir_root = Path(a.courses_dir)
    cat = json.loads((cdir_root / "catalog.json").read_text("utf-8"))["courses"]
    ids = {c["id"] for c in cat}
    n = 0
    with tempfile.TemporaryDirectory() as work:
        for c in cat:
            if a.course and c["id"] != a.course: continue
            cdir = cdir_root / c["id"]
            if not (cdir / "course.json").is_file():
                continue
            cj = json.loads((cdir / "course.json").read_text("utf-8"))
            for r in c["doporuceno"]:
                if r not in ids: err(c["id"], f"doporučený podkurz {r} není v katalogu")
            seen = []
            for m in cj["modules"]:
                for lid in m["lessons"]:
                    if lid in seen: err(c["id"], f"lekce {lid} je dvakrát")
                    seen.append(lid); validate_lesson(cdir, lid, Path(work)); n += 1
            extra = {p.name for p in (cdir / "lessons").iterdir() if p.is_dir()} - set(seen)
            for e in sorted(extra): warns.append(f"{c['id']}: lekce {e} není v course.json")
    for w in warns: print("POZOR:", w)
    for e in errors: print("CHYBA:", e)
    print(f"\nZkontrolováno lekcí: {n}, chyb: {len(errors)}, upozornění: {len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
