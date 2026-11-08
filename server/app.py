"""Místní server Dílny Pythonu (jen standardní knihovna, jen 127.0.0.1).

GET  /                    statické soubory z web/
GET  /api/catalog         seznam podkurzů
POST /api/run             {code, timeout?, stdin?} -> {id}          (vyžaduje token)
GET  /api/run/poll?id=&since=                                        (vyžaduje token)
POST /api/run/input       {id, text}                                 (vyžaduje token)
POST /api/run/stop        {id}                                       (vyžaduje token)
POST /api/check           {course, lesson, code} -> {ok, results[]}  (vyžaduje token)
Token se posílá v hlavičce X-Dilna-Token; aplikace ho dostane v adrese (?t=...).
"""
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from . import security
from . import checker
from .checker import lesson_dir, run_check
from . import content
from .preparation import course_preparation
from .runner import RunManager

MAX_BODY = 300_000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, root: Path, **kw):
        self.root = root
        super().__init__(*a, directory=str(root / "web"), **kw)

    # --- pomocné ---
    @property
    def srv(self):
        return self.server  # type: ignore[return-value]

    def _json(self, status: int, obj) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _guard(self, need_token: bool) -> bool:
        port = self.srv.server_address[1]
        if not security.host_ok(self.headers.get("Host"), port):
            self._json(403, {"error": "Neplatná hlavička Host."})
            return False
        if not security.origin_ok(self.headers.get("Origin"), port):
            self._json(403, {"error": "Neplatný původ požadavku."})
            return False
        if need_token and not security.token_ok(self.headers.get("X-Dilna-Token"), self.srv.token):
            self._json(401, {"error": "Chybí nebo je neplatný token."})
            return False
        return True

    def _body(self) -> dict | None:
        try:
            n = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            n = -1
        if n < 0 or n > MAX_BODY:
            self._json(413, {"error": "Požadavek je příliš velký."})
            return None
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
            if not isinstance(data, dict):
                raise ValueError
            return data
        except ValueError:
            self._json(400, {"error": "Neplatný JSON."})
            return None

    # --- metody ---
    def do_GET(self):
        u = urlsplit(self.path)
        if u.path == "/api/catalog":
            if self._guard(False):
                self._json(200, json.loads((self.srv.courses_dir / "catalog.json").read_text("utf-8")))
            return
        if u.path == "/api/preparation":
            if not self._guard(False):
                return
            profile = course_preparation((parse_qs(u.query).get("course") or [""])[0])
            return self._json(200, profile) if profile else self._json(404, {"error": "Příprava kurzu nenalezena."})
        if u.path == "/api/course":
            if self._guard(False):
                self._json(200, content.course_view(self.srv.courses_dir, (parse_qs(u.query).get("id") or [""])[0]))
            return
        if u.path == "/api/doc":
            if not self._guard(False):
                return
            name = (parse_qs(u.query).get("name") or [""])[0]
            if name not in ("instalace", "vscodium", "vscode", "pycharm", "reseni-problemu"):
                return self._json(404, {"error": "Dokument neexistuje."})
            return self._json(200, {"name": name, "md": content._read(self.root / "docs" / f"{name}.md")})
        if u.path == "/api/lesson":
            if not self._guard(False):
                return
            q = parse_qs(u.query)
            v = content.lesson_view(self.srv.courses_dir, (q.get("course") or [""])[0], (q.get("lesson") or [""])[0])
            return self._json(200, v) if v else self._json(404, {"error": "Lekce nenalezena."})
        if u.path == "/api/solution":
            if not self._guard(False):
                return
            q = parse_qs(u.query)
            value = content.solution_view(self.srv.courses_dir, (q.get("course") or [""])[0],
                                          (q.get("lesson") or [""])[0], (q.get("task") or [None])[0])
            return self._json(200, value) if value else self._json(404, {"error": "Řešení pro tento úkol není dostupné."})
        if u.path == "/api/workspace":
            if not self._guard(True):
                return
            q = parse_qs(u.query)
            f = content.workspace_file(self.root, (q.get("course") or [""])[0], (q.get("lesson") or [""])[0], (q.get("task") or [None])[0])
            if f is None:
                return self._json(404, {"error": "Neplatná lekce."})
            return self._json(200, {"exists": f.is_file(), "code": content._read(f), "path": str(f)})
        if u.path == "/api/run/poll":
            if not self._guard(True):
                return
            q = parse_qs(u.query)
            run = self.srv.runs.get((q.get("id") or [""])[0])
            if not run:
                return self._json(404, {"error": "Běh nenalezen."})
            try:
                since = max(0, int((q.get("since") or ["0"])[0]))
            except ValueError:
                since = 0
            return self._json(200, run.poll(since))
        if not self._guard(False):
            return
        super().do_GET()

    def do_POST(self):
        u = urlsplit(self.path)
        if not (u.path.startswith("/api/run") or u.path in ("/api/check", "/api/workspace/save", "/api/workspace/open")):
            return self._json(404, {"error": "Neznámá adresa."})
        if not self._guard(True):
            return
        body = self._body()
        if body is None:
            return
        if u.path in ("/api/workspace/save", "/api/workspace/open"):
            if content.workspace_file(self.root, str(body.get("course", "")), str(body.get("lesson", "")), body.get("task")) is None:
                return self._json(400, {"error": "Neplatná lekce nebo úkol."})
            ld = lesson_dir(self.srv.courses_dir, str(body.get("course", "")), str(body.get("lesson", "")), body.get("task"))
            if ld is None:
                return self._json(404, {"error": "Úkol neexistuje."})
            f = content.save_workspace(self.root, str(body.get("course", "")), str(body.get("lesson", "")), body.get("code", ""),
                                       ld / "files" if ld else None, task=body.get("task"))
            if f is None:
                return self._json(400, {"error": "Neplatná lekce nebo kód."})
            res = {"path": str(f), "saved": True}
            if u.path.endswith("open"):
                res.update(content.open_in_editor(f))
            return self._json(200, res)
        if u.path == "/api/check":
            d = lesson_dir(self.srv.courses_dir, str(body.get("course", "")), str(body.get("lesson", "")), body.get("task"))
            if d is None:
                return self._json(404, {"error": "Lekce nebo její kontrola neexistuje."})
            with self.srv.check_sem:
                res = run_check(d, body.get("code", ""), self.root / "lib", self.root / "workspace" / "_run", self.srv.runs.python)
            return self._json(200, res)
        if u.path == "/api/run":
            try:
                ld = lesson_dir(self.srv.courses_dir, str(body.get("course", "")), str(body.get("lesson", "")), body.get("task"))
                if body.get("task") not in (None, "") and ld is None:
                    return self._json(404, {"error": "Úkol neexistuje."})
                main_lesson = lesson_dir(self.srv.courses_dir, str(body.get("course", "")), str(body.get("lesson", "")))
                meta = content._json(main_lesson / 'lesson.json', {}) if main_lesson else {}
                run = self.srv.runs.start(body.get("code", ""), body.get("timeout", 20), body.get("stdin", ""),
                                          ld / "files" if ld else None, preview_images=meta.get('preview_images') is True,
                                          download_files=meta.get('download_files') is True)
            except ValueError as e:
                return self._json(400, {"error": str(e)})
            except RuntimeError as e:
                return self._json(429, {"error": str(e)})
            return self._json(200, {"id": run.id})
        run = self.srv.runs.get(str(body.get("id", "")))
        if not run:
            return self._json(404, {"error": "Běh nenalezen."})
        if u.path == "/api/run/input":
            return self._json(200, {"ok": run.send_input(str(body.get("text", "")))})
        if u.path == "/api/run/stop":
            run.stop()
            return self._json(200, {"ok": True})
        self._json(404, {"error": "Neznámá adresa."})

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class DilnaServer(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        import sys
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError)):
            return  # prohlížeč zavřel spojení, nic se neděje
        super().handle_error(request, client_address)
    token: str
    runs: RunManager
    courses_dir: Path
    check_sem: threading.Semaphore


def create_server(root: Path, host: str, port: int, python: str | None = None,
                  courses_dir: Path | None = None) -> DilnaServer:
    if host != "127.0.0.1":
        raise ValueError("Server smí poslouchat jen na 127.0.0.1")
    srv = DilnaServer((host, port), partial(Handler, root=Path(root)))
    srv.token = security.new_token()
    srv.courses_dir = Path(courses_dir) if courses_dir else Path(root) / "courses"
    srv.check_sem = threading.Semaphore(2)
    srv.runs = RunManager(Path(root) / "workspace" / "_run", python)
    return srv
