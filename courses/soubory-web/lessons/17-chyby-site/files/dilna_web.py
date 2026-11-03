"""Malý místní web server pro lekce o stahování dat.

Běží jen na adrese 127.0.0.1 (váš počítač), takže lekce fungují bez internetu a nic nezatěžují.
Použití:

    from dilna_web import spust
    adresa = spust()                    # například "http://127.0.0.1:50321"
    # requests.get(adresa + "/index.html")

Server vydává soubory ze složky "web" (vedle programu). Navíc umí zvláštní adresy:

    /_status/404         odpoví zadaným stavovým kódem
    /_pomalu/3           odpoví až za 3 sekundy (max. 10)
    /_nestabilni/abc     poprvé a podruhé selže (500), potom odpoví správně (pro každé jméno zvlášť)
    /_presmerovani       přesměruje na /index.html
    /_hlavicky           vrátí JSON s hlavičkami, které přišly od klienta
"""
import functools
import http.server
import json
import os
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit

__all__ = ["spust"]


def _povol_mistni_adresu():
    """Požadavky na 127.0.0.1 nesmějí jít přes proxy z nastavení počítače."""
    for jmeno in ("NO_PROXY", "no_proxy"):
        hodnoty = [h for h in os.environ.get(jmeno, "").split(",") if h]
        if "127.0.0.1" not in hodnoty:
            hodnoty.append("127.0.0.1")
        os.environ[jmeno] = ",".join(hodnoty)


class _Obsluha(http.server.SimpleHTTPRequestHandler):
    pocitadla: dict = {}

    def log_message(self, format, *args):      # server nic nevypisuje
        pass

    def guess_type(self, path):
        typ = super().guess_type(path)
        if typ.startswith("text/") or typ in ("application/json", "application/javascript"):
            typ += "; charset=utf-8"
        return typ

    def _odpoved(self, kod, text="", typ="text/plain; charset=utf-8", hlavicky=None):
        data = text.encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (hlavicky or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_GET(self):
        cesta = urlsplit(self.path).path
        if cesta.startswith("/_status/"):
            try:
                kod = int(cesta.split("/")[2])
            except (ValueError, IndexError):
                return self._odpoved(400, "Neplatný kód")
            if not 200 <= kod <= 599:
                return self._odpoved(400, "Neplatný kód")
            return self._odpoved(kod, f"Stavový kód {kod}")
        if cesta.startswith("/_pomalu/"):
            try:
                time.sleep(min(float(cesta.split("/")[2]), 10))
            except (ValueError, IndexError):
                return self._odpoved(400, "Neplatný čas")
            return self._odpoved(200, "Hotovo po čekání")
        if cesta.startswith("/_nestabilni/"):
            klic = cesta.split("/", 2)[2]
            self.pocitadla[klic] = self.pocitadla.get(klic, 0) + 1
            if self.pocitadla[klic] <= 2:
                return self._odpoved(500, "Server má chvilku potíže")
            return self._odpoved(200, "Povedlo se")
        if cesta == "/_presmerovani":
            return self._odpoved(302, "Přesměrováno", hlavicky={"Location": "/index.html"})
        if cesta == "/_hlavicky":
            hlavicky = {k.lower(): v for k, v in self.headers.items()}
            return self._odpoved(200, json.dumps(hlavicky, ensure_ascii=False), "application/json; charset=utf-8")
        return super().do_GET()


def spust(slozka="web"):
    """Spustí server na volném portu a vrátí jeho adresu, např. "http://127.0.0.1:50321"."""
    _povol_mistni_adresu()
    obsluha = type("Obsluha", (_Obsluha,), {"pocitadla": {}})
    obsluha = functools.partial(obsluha, directory=str(Path(slozka).resolve()))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), obsluha)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}"
