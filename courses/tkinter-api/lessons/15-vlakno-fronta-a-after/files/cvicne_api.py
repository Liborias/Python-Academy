"""Předvídatelné cvičné HTTP API, pouze 127.0.0.1 na volném portu.

with cvicne_api() as adresa: ...
GET /kurz?mena=EUR (také USD, GBP) vrací smyšlené CZK za jednotku měny.
Prefix /pomalu čeká 0,35 s, /chyba vrátí 503, /neplatny-json poškozený JSON,
/spatna-data záporný kurz. Datum a hodnoty nejsou aktuální tržní data.
"""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
import time
from urllib.parse import parse_qs, urlsplit


class _Obsluha(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        url = urlsplit(self.path)
        casti = url.path.strip('/').split('/')
        rezim = casti[0] if len(casti) == 2 else ''
        mena = parse_qs(url.query).get('mena', [''])[0]
        hodnoty = {'EUR': 25.0, 'USD': 20.0, 'GBP': 30.0}
        status = 200
        data = {'mena': mena, 'czk_za_jednotku': hodnoty.get(mena),
                'datum': '2026-01-15', 'zdroj': 'Cvičné API'}
        if casti[-1] != 'kurz' or len(casti) > 2 or rezim not in ('', 'pomalu', 'chyba', 'neplatny-json', 'spatna-data') or mena not in hodnoty:
            status, data = 404, {'chyba': 'Neznámý endpoint nebo měna.'}
        elif rezim == 'pomalu':
            time.sleep(.35)
        elif rezim == 'chyba':
            status = 503
        elif rezim == 'spatna-data':
            data['czk_za_jednotku'] = -1
        body = '{neplatný JSON' if rezim == 'neplatny-json' else json.dumps(data, ensure_ascii=False)
        body = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except OSError:
            # Klient při nácviku timeoutu může spojení ukončit před odpovědí.
            pass


@contextmanager
def cvicne_api():
    """Spustí server, vrátí základní adresu a při opuštění with jej uklidí."""
    server = ThreadingHTTPServer(('127.0.0.1', 0), _Obsluha)
    server.daemon_threads = True
    vlakno = threading.Thread(target=lambda: server.serve_forever(poll_interval=.02), daemon=True)
    vlakno.start()
    # Jen loopback patří přímo na tento počítač, nikoli do firemní/cloudové proxy.
    puvodni = {key: os.environ.get(key) for key in ('NO_PROXY', 'no_proxy')}
    for key, value in puvodni.items():
        hodnoty = [item.strip() for item in (value or '').split(',') if item.strip()]
        if '127.0.0.1' not in hodnoty:
            hodnoty.append('127.0.0.1')
        os.environ[key] = ','.join(hodnoty)
    try:
        yield f'http://127.0.0.1:{server.server_address[1]}'
    finally:
        server.shutdown()
        server.server_close()
        vlakno.join(timeout=1)
        for key, value in puvodni.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
