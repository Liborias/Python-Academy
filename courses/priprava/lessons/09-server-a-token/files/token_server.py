"""Místní učební server: ověří token a spustí pouze soubor main.py vedle sebe.

Spusťte Pythonem z .venv. Nejde o server pro veřejné nasazení.
"""
import hmac
import json
import secrets
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        # Token se nesmí objevit v přístupových protokolech.
        pass

    def reply(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.reply(405, {"error": "Použijte POST /run s tokenem v hlavičce."})

    def do_POST(self):
        port = self.server.server_address[1]
        allowed = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if self.headers.get("Host", "").lower() not in allowed:
            return self.reply(403, {"error": "Neplatný Host."})
        origin = self.headers.get("Origin")
        if origin and origin not in {f"http://{host}" for host in allowed}:
            return self.reply(403, {"error": "Cizí původ požadavku."})
        # Token přijímáme pouze v hlavičce, ne v adrese nebo souboru.
        path = urlsplit(self.path)
        if path.path != "/run" or path.query:
            return self.reply(404, {"error": "Cesta nenalezena."})
        supplied = self.headers.get("X-Project-Token", "")
        if not hmac.compare_digest(supplied.encode("utf-8"), self.server.token.encode("utf-8")):
            return self.reply(401, {"error": "Chybějící nebo neplatný token."})
        # Klient nesmí poslat kód, cestu ani příkaz k vykonání.
        if self.headers.get("Transfer-Encoding") or self.headers.get("Content-Length", "0") != "0":
            return self.reply(400, {"error": "Požadavek musí mít prázdné tělo."})
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "main.py")],
                cwd=ROOT, stdin=subprocess.DEVNULL,
                capture_output=True, text=True, encoding="utf-8", timeout=5,
            )
        except subprocess.TimeoutExpired:
            return self.reply(504, {"error": "Program překročil 5 sekund."})
        except OSError:
            return self.reply(500, {"error": "Program se nepodařilo spustit."})
        self.reply(200 if result.returncode == 0 else 500, {
            "exit": result.returncode,
            "stdout": result.stdout[:4000], "stderr": result.stderr[:4000],
        })


def create_server(port=8767):
    server = HTTPServer(("127.0.0.1", port), Handler)
    server.token = secrets.token_urlsafe(32)
    return server


if __name__ == "__main__":
    if sys.prefix == sys.base_prefix:
        raise SystemExit("Spusťte tento server Pythonem z virtuálního prostředí .venv.")
    with create_server() as server:
        print("Server naslouchá jen na tomto počítači, port 8767.", flush=True)
        print("Do klienta zkopírujte tento dočasný token:", server.token, flush=True)
        print("Token nesdílejte. Ukončení: Ctrl+C. Restart vytvoří nový token.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server ukončen.")
