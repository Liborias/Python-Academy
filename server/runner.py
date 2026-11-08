"""Spouštění studentského kódu v podprocesu s časovým limitem a omezeným výstupem.

Relace běhu (Run): proces běží na pozadí, výstup se sbírá po částech, student může
posílat vstup pro input() a běh zastavit. Okno aplikace (Tkinter, Pygame) se otevře
na počítači studenta, protože proces dědí jeho grafické prostředí.
"""
import codecs
import base64
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

from .lessonfiles import copy_files

MAX_OUTPUT = 200_000          # znaků na jeden běh
MAX_CODE = 200_000            # znaků kódu
DEFAULT_TIMEOUT = 20
MAX_TIMEOUT = 600             # okenní aplikace potřebují delší limit
MAX_ACTIVE = 4
KEEP_FINISHED = 60            # sekund, po které se hotový běh drží pro poslední poll
MAX_IMAGES = 6
MAX_IMAGE_BYTES = 2_000_000
MAX_IMAGES_BYTES = 4_000_000
MAX_IMAGE_PIXELS = 8_000_000


def collect_images(directory: Path) -> tuple[list[dict], str]:
    """Načte malé PNG vytvořené během běhu; server nepotřebuje grafické knihovny."""
    images, total, skipped = [], 0, False
    for path in sorted(directory.rglob('*.png')):
        if path.is_symlink() or not path.is_file():
            continue
        try:
            size = path.stat().st_size
            if len(images) >= MAX_IMAGES or size > MAX_IMAGE_BYTES or total + size > MAX_IMAGES_BYTES:
                skipped = True
                continue
            with path.open('rb') as stream:
                data = stream.read(MAX_IMAGE_BYTES + 1)
            if total + len(data) > MAX_IMAGES_BYTES or len(data) > MAX_IMAGE_BYTES or len(data) < 33 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
                skipped = True
                continue
            width, height = struct.unpack('>II', data[16:24])
            if not width or not height or width * height > MAX_IMAGE_PIXELS:
                skipped = True
                continue
            images.append({'name': path.relative_to(directory).as_posix(),
                           'data': base64.b64encode(data).decode('ascii')})
            total += len(data)
        except OSError:
            skipped = True
    notice = ('Některé náhledy se nezobrazily. Podporujeme nejvýše 6 PNG, 2 MB a 8 milionů pixelů '
              'na obrázek, dohromady 4 MB. Zkuste menší rozměr nebo DPI; soubory lze uložit i v editoru.') if skipped else ''
    return images, notice

# Proměnné prostředí, které podproces smí zdědit (žádná hesla ani klíče).
ENV_ALLOW = {
    "PATH", "HOME", "USERPROFILE", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR",
    "LANG", "LC_ALL", "DISPLAY", "WAYLAND_DISPLAY", "XDG_RUNTIME_DIR", "XAUTHORITY",
    "APPDATA", "LOCALAPPDATA", "COMSPEC", "PATHEXT", "SDL_VIDEODRIVER", "SDL_AUDIODRIVER",
}


def clean_env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if k in ENV_ALLOW}
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1",
                "PYTHONDONTWRITEBYTECODE": "1"})
    if extra:
        env.update(extra)
    return env


class Run:
    def __init__(self, code: str, workdir: Path, python: str, timeout: float, stdin: str = "", files: Path | None = None,
                 preview_images: bool = False):
        self.id = uuid.uuid4().hex
        self.chunks: list[tuple[str, str]] = []     # (kanál, text)
        self.size = 0
        self.truncated = False
        self.timed_out = False
        self.stopped = False
        self.exit_code: int | None = None
        self.finished_at: float | None = None
        self.lock = threading.Lock()
        self.preview_images = preview_images
        self.images: list[dict] = []
        self.image_notice = ''
        self.dir = Path(tempfile.mkdtemp(prefix="run-", dir=workdir))
        copy_files(files, self.dir)
        (self.dir / "main.py").write_text(code, encoding="utf-8")
        extra_env = None
        if preview_images:
            cache = workdir / '_matplotlib'
            cache.mkdir(exist_ok=True)
            extra_env = {'MPLBACKEND': 'Agg', 'MPLCONFIGDIR': str(cache.resolve())}
        self.proc = subprocess.Popen(
            [python, "-u", "-X", "utf8", "main.py"],
            cwd=self.dir, env=clean_env(extra_env),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            **({"creationflags": 0x08000000} if sys.platform == "win32" else {}),
        )
        self.deadline = time.monotonic() + timeout
        self.threads = [
            threading.Thread(target=self._pump, args=(self.proc.stdout, "out"), daemon=True),
            threading.Thread(target=self._pump, args=(self.proc.stderr, "err"), daemon=True),
            threading.Thread(target=self._watch, daemon=True),
        ]
        for t in self.threads:
            t.start()
        if stdin:
            self.send_input(stdin)

    # --- vlákna ---
    def _add(self, channel: str, text: str):
        if not text:
            return
        if channel == "err":      # cesta k dočasné složce studenta nezajímá
            text = text.replace(str(self.dir) + os.sep, "")
        with self.lock:
            room = MAX_OUTPUT - self.size
            if room <= 0:
                self.truncated = True
                return
            if len(text) > room:
                text, self.truncated = text[:room], True
            self.size += len(text)
            self.chunks.append((channel, text))

    def _pump(self, pipe, channel):
        dec = codecs.getincrementaldecoder("utf-8")(errors="replace")
        try:
            while True:
                data = pipe.read1(4096) if hasattr(pipe, "read1") else pipe.read(4096)
                if not data:
                    break
                self._add(channel, dec.decode(data))
            self._add(channel, dec.decode(b"", final=True))
        except (OSError, ValueError):
            pass

    def _watch(self):
        while self.proc.poll() is None:
            if time.monotonic() > self.deadline:
                self.timed_out = True
                self._kill()
                break
            if self.truncated and not self.stopped:
                self._kill()           # nekonečný výpis nechceme
                break
            time.sleep(0.05)
        self.proc.wait()
        for t in self.threads[:2]:
            t.join(timeout=1)
        self.exit_code = self.proc.returncode
        if self.preview_images:
            self.images, self.image_notice = collect_images(self.dir)
        shutil.rmtree(self.dir, ignore_errors=True)
        self.finished_at = time.monotonic()

    def _kill(self):
        try:
            self.proc.kill()
        except OSError:
            pass

    # --- ovládání ---
    def send_input(self, text: str):
        if self.proc.poll() is not None:
            return False
        try:
            self.proc.stdin.write(text.encode("utf-8"))
            self.proc.stdin.flush()
            return True
        except (OSError, ValueError):
            return False

    def stop(self):
        self.stopped = True
        self._kill()

    def poll(self, since: int) -> dict:
        with self.lock:
            new = [{"ch": c, "text": t} for c, t in self.chunks[since:]]
            n = len(self.chunks)
        result = {"chunks": new, "next": n, "done": self.finished_at is not None,
                "exit": self.exit_code, "timed_out": self.timed_out,
                "truncated": self.truncated, "stopped": self.stopped}
        if result['done'] and self.preview_images:
            result.update(images=self.images, image_notice=self.image_notice)
        return result


class RunManager:
    def __init__(self, workdir: Path, python: str | None = None):
        self.workdir = Path(workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.python = python or sys.executable
        self.runs: dict[str, Run] = {}
        self.lock = threading.Lock()

    def _gc(self):
        now = time.monotonic()
        for rid in [r for r, run in self.runs.items()
                    if run.finished_at and now - run.finished_at > KEEP_FINISHED]:
            del self.runs[rid]

    def start(self, code: str, timeout=DEFAULT_TIMEOUT, stdin: str = "", files: Path | None = None,
              preview_images: bool = False) -> Run:
        if not isinstance(code, str) or len(code) > MAX_CODE:
            raise ValueError("Kód je neplatný nebo příliš dlouhý.")
        try:
            timeout = max(1.0, min(float(timeout), MAX_TIMEOUT))
        except (TypeError, ValueError):
            timeout = DEFAULT_TIMEOUT
        with self.lock:
            self._gc()
            if sum(1 for r in self.runs.values() if r.finished_at is None) >= MAX_ACTIVE:
                raise RuntimeError("Běží příliš mnoho programů, počkejte na dokončení.")
            run = Run(code, self.workdir, self.python, timeout, stdin if isinstance(stdin, str) else "", files, preview_images)
            self.runs[run.id] = run
            return run

    def get(self, rid: str) -> Run | None:
        return self.runs.get(rid)

    def stop_all(self):
        for r in list(self.runs.values()):
            r.stop()
