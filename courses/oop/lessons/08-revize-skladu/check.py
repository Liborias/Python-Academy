import ast
import os
import sys
from collections import Counter
sys.path.insert(0, os.getcwd())
from dilna_check import check
import skladova_karta

c = check()
c.defines_class("Sklad")
original = skladova_karta.SkladovaKarta
made, calls = [], []
class VerejnaKarta:
    """Stejné veřejné rozhraní, jiné vnitřní uložení počtů."""
    def __init__(self, nazev, celkem=0):
        if type(celkem) is not int or celkem < 0:
            raise ValueError("Počet")
        self.nazev = nazev
        self._fyzicky_test = celkem
        self._volne_test = celkem
        made.append(self)
    @property
    def celkem(self):
        return self._fyzicky_test
    @property
    def rezervovano(self):
        return self._fyzicky_test - self._volne_test
    @property
    def dostupne(self):
        return self._volne_test
    def rezervuj(self, kolik):
        calls.append((id(self), kolik))
        if type(kolik) is not int or kolik <= 0 or kolik > self.dostupne:
            raise ValueError("Rezervace")
        self._volne_test -= kolik
        return self.dostupne
skladova_karta.SkladovaKarta = VerejnaKarta
ns = c.load()
cls = (ns or {}).get("Sklad")
try:
    if ns is not None and isinstance(cls, type):
        store = cls()
        ok, value = c.call({"prehled": store.prehled}, "prehled")
        c.add("Nový sklad je prázdný", ok and value == {} and isinstance(value, dict), "Každý sklad začíná vlastním prázdným slovníkem.")
        expected = {}
        for code, name, amount in [("KNIHA", "Průvodce", 5), ("OBAL", "Dárkový obal", 2), ("ŽK", "Žlutá krabice", 0)]:
            ok, value = c.call({"pridej": store.pridej}, "pridej", (code, name, amount))
            expected[code] = amount
            c.add("Přidání karty přes veřejné rozhraní", ok and value == amount and store.prehled() == expected and c.last_output == "",
                  "Vytvořte kartu, uložte ji a vraťte její dostupnost.")
        active = list(made)
        def snapshot():
            return (dict(store.prehled()), [(id(card), card.nazev, card.celkem, card.rezervovano, card.dostupne) for card in active])
        for code, name, amount in [("KNIHA", "Přepsaný název", 99), ("NOVÁ", "Nová", -1), ("NOVÁ", "Nová", True), ("NOVÁ", "Nová", "3")]:
            before = snapshot()
            ok, error = c.call({"pridej": store.pridej}, "pridej", (code, name, amount))
            c.add("Neplatné přidání nepoškodí sklad", not ok and isinstance(error, ValueError) and snapshot() == before,
                  "Nezapisujte kartu před úspěšnou konstrukcí a nedovolte přepsat existující kód.")
        bad_requests = [{"KNIHA": 1, "OBAL": 3}, {"OBAL": 1, "KNIHA": 6}, {"KNIHA": 1, "NEZNÁMÁ": 1},
                        {"KNIHA": 1, "OBAL": 0}, {"OBAL": 1, "KNIHA": True}, {"KNIHA": -1}, {"KNIHA": 1.0},
                        {"KNIHA": "1"}, {"KNIHA": None}, {"ŽK": 1}]
        for request in bad_requests:
            before = snapshot()
            original_request = dict(request)
            calls.clear()
            ok, error = c.call({"rezervuj": store.rezervuj}, "rezervuj", (request,))
            c.add("Celý požadavek se odmítne před změnou", not ok and isinstance(error, ValueError) and snapshot() == before
                  and calls == [] and request == original_request,
                  "Nejprve ověřte všechny kódy a množství; rezervaci žádné karty ještě nevolejte.")
        for request in [{}, {"KNIHA": 2, "OBAL": 1}, {"KNIHA": 3, "OBAL": 1}]:
            original_request = dict(request)
            calls.clear()
            for code, amount in request.items():
                expected[code] -= amount
            ok, value = c.call({"rezervuj": store.rezervuj}, "rezervuj", (request,))
            c.add("Úspěch vrátí nový přehled", ok and isinstance(value, dict) and value == expected and store.prehled() == expected
                  and request == original_request and c.last_output == "", "Rezervujte celý platný požadavek a vraťte dostupné počty.")
            by_id = {id(card): card for card in made}
            names = {"KNIHA": "Průvodce", "OBAL": "Dárkový obal", "ŽK": "Žlutá krabice"}
            c.add("Rezervaci provádějí jednotlivé karty", Counter((by_id[identity].nazev, amount) for identity, amount in calls)
                  == Counter((names[code], amount) for code, amount in request.items()),
                  "Využijte veřejné rezervuj každé karty, ne její vnitřní údaje.")
            if ok and isinstance(value, dict):
                value["KNIHA"] = 999
                c.add("Vrácený přehled neovládá sklad", store.prehled() == expected, "Vraťte nový slovník s hodnotami, ne vnitřní karty.")
        a, b = store.prehled(), store.prehled()
        c.add("Přehledy jsou samostatné slovníky", isinstance(a, dict) and isinstance(b, dict) and a is not b
              and all(type(n) is int for n in a.values()), "Každé volání připraví nový slovník dostupných celých počtů.")
        before = snapshot()
        calls.clear()
        ok, error = c.call({"rezervuj": store.rezervuj}, "rezervuj", ({"KNIHA": 1},))
        c.add("Po vyčerpání nelze rezervovat znovu", not ok and isinstance(error, ValueError) and snapshot() == before and calls == [],
              "Dostupnost zjišťujte z aktuálního stavu karet.")
        second = cls()
        second.pridej("KNIHA", "Jiný sklad", 9)
        c.add("Nezávislé sklady", second.prehled() == {"KNIHA": 9} and snapshot() == before,
              "Vnitřní slovník patří instanci, ne společné třídě.")
    else:
        c.add("Sklad je třída", False, "Definujte třídu Sklad.")
except BaseException as exc:
    c.add("Sklad lze ověřit", False, f"{type(exc).__name__}: {exc}")
finally:
    skladova_karta.SkladovaKarta = original
r = c.run()
if c.no_error(r):
    for prefix, expected in [("Po odmítnutí:", {"KNIHA": 5, "OBAL": 2}), ("Skutečný sklad:", {"KNIHA": 3, "OBAL": 1})]:
        line = next((line[len(prefix):].strip() for line in r.out.splitlines() if line.startswith(prefix)), "")
        try:
            value = ast.literal_eval(line)
        except (ValueError, SyntaxError):
            value = None
        c.add("Ukázka se skutečnými kartami", value == expected,
              "Ponechte hlavní blok: odmítnutý požadavek nic nerezervuje a kopie přehledu nemění skutečné počty.")
c.done()
