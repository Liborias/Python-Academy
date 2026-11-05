import io
import json
import os
import sys
import urllib.request
from pathlib import Path
sys.path.insert(0, os.getcwd())
from dilna_check import check
from kviz_model import Otazka

c = check()
active = {"payload": b"{}", "error": None}
opened = []
original = urllib.request.urlopen
class Response:
    def __init__(self, payload):
        self.stream = io.BytesIO(payload)
        self.reads = []
        self.closed = False
    def read(self, count=-1):
        self.reads.append(count)
        return self.stream.read(count)
    def close(self):
        self.closed = True
        self.stream.close()
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()
def opener(url, *args, **kwargs):
    timeout = kwargs.get("timeout", args[1] if len(args) > 1 else None)
    response = Response(active["payload"])
    opened.append((getattr(url, "full_url", url), timeout, response))
    if active["error"] is not None:
        raise active["error"]
    return response
urllib.request.urlopen = opener
ns = c.load()
try:
    if ns is not None:
        url = "http://127.0.0.1:1/kontrola"
        payload = {"řeka": "žlutá", "hodnoty": [True, False, None]}
        for raw, expected, error_type in [
            (json.dumps(payload, ensure_ascii=False).encode("utf-8"), payload, None),
            (b" " * 65_534 + b"{}", {}, None),
            (b" " * 65_535 + b"{}", None, ValueError),
            (b"{}" + b" " * 65_535, None, ValueError),
            (b"{chyba}", None, ValueError), (b"\xff", None, ValueError),
        ]:
            active["payload"], active["error"] = raw, None
            opened.clear()
            ok, value = c.call(ns, "stahni_json", (url,))
            c.add("Přenos, UTF-8 a JSON", (ok and value == expected) if error_type is None else (not ok and isinstance(value, error_type)),
                  "Přijměte nejvýš 64 KiB a dekódujte UTF-8 i JSON; vadná data odmítněte.")
            valid = len(opened) == 1 and opened[0][0] == url and opened[0][1] == 5
            c.add("Předané URL a timeout", valid, "Otevřete zadané URL s timeoutem 5 sekund.")
            if opened:
                response = opened[0][2]
                c.add("Omezené čtení a zavřená odpověď", response.closed and bool(response.reads)
                      and all(isinstance(n, int) and 0 < n <= 65_537 for n in response.reads),
                      "Čtěte omezený počet bajtů a odpověď zavřete i po chybě.")
        active["error"] = OSError("Výpadek testovacího přenosu")
        c.raises(ns, "stahni_json", (url,), OSError)
        active["error"] = None
        backup = {"response_code": 0, "results": [
            {"type": "boolean", "question": "Záloha &amp; test", "correct_answer": "False"}]}
        Path("vlastni-zaloha.json").write_text(json.dumps(backup, ensure_ascii=False), encoding="utf-8")
        remote = {"response_code": 0, "results": [
            {"type": "boolean", "question": "Remote &quot;OK&quot;", "correct_answer": "True"}]}
        calls = []
        def fetch(url):
            calls.append(url)
            return remote
        def verify(value, text, answer, source, message):
            return isinstance(value, tuple) and len(value) == 3 and isinstance(value[0], list) and len(value[0]) == 1 \
                and isinstance(value[0][0], Otazka) and (value[0][0].text, value[0][0].spravne) == (text, answer) \
                and value[1] == source and isinstance(value[2], str) and (bool(value[2]) if message else value[2] == "")
        ok, value = c.call(ns, "ziskej_otazky", (False, "vlastni-zaloha.json", fetch))
        c.add("Offline bez sítě", ok and verify(value, "Záloha & test", False, "offline", False) and calls == [],
              "Offline použije zadaný soubor a vůbec nevolá stahni.")
        ok, value = c.call(ns, "ziskej_otazky", (True, "neexistujici-zaloha.json", fetch))
        c.add("API úspěch nepotřebuje zálohu", ok and verify(value, 'Remote "OK"', True, "API", False)
              and calls == [ns.get("API_URL")], "Úspěšná data převeďte a vraťte bez čtení zálohy.")
        for failure in [OSError("síť"), TimeoutError("čekání"), ValueError("JSON")]:
            calls.clear()
            def fail(url):
                calls.append(url)
                raise failure
            ok, value = c.call(ns, "ziskej_otazky", (True, "vlastni-zaloha.json", fail))
            c.add("Výpadek přizná použitou zálohu", ok and verify(value, "Záloha & test", False, "záloha", True)
                  and calls == [ns.get("API_URL")], "Použijte soubor a neprázdnou zprávu při OSError nebo ValueError.")
        for bad in [{"response_code": 5, "results": []}, {"response_code": 0, "results": []}, {"response_code": 0, "results": [None]}]:
            ok, value = c.call(ns, "ziskej_otazky", (True, "vlastni-zaloha.json", lambda url: bad))
            c.add("Nepoužitelná API data také spustí zálohu", ok and verify(value, "Záloha & test", False, "záloha", True),
                  "Přijatý JSON musí projít převodem a validací.")
        def broken(url):
            raise RuntimeError("Programátorská chyba")
        c.raises(ns, "ziskej_otazky", (True, "vlastni-zaloha.json", broken), RuntimeError)
        c.raises(ns, "ziskej_otazky", (False, "chybajici.json", fetch), OSError)
        Path("rozbita-zaloha.json").write_text("{chyba}", encoding="utf-8")
        c.raises(ns, "ziskej_otazky", (False, "rozbita-zaloha.json", fetch), ValueError)
        c.raises(ns, "ziskej_otazky", (True, "chybajici.json", fail), OSError)
        c.raises(ns, "ziskej_otazky", (True, "rozbita-zaloha.json", fail), ValueError)
except BaseException as exc:
    c.add("API a zálohu lze ověřit", False, f"{type(exc).__name__}: {exc}")
finally:
    urllib.request.urlopen = original
c.done()
