import copy
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, os.getcwd())
from dilna_check import check
from kviz_model import Otazka

c = check()
c.utf8()
ns = c.load()
try:
    if ns is not None:
        data = {"response_code": 0, "results": [
            {"type": "boolean", "question": "  Řeka &amp; &quot;les&quot; &#039;A&#039;  ", "correct_answer": "False", "category": "Navíc"},
            {"type": "boolean", "question": "2 &lt; 3", "correct_answer": "True"},
        ]}
        original = copy.deepcopy(data)
        expected = [('Řeka & "les" \'A\'', False), ("2 < 3", True)]
        def verify(value):
            return isinstance(value, list) and len(value) == 2 and all(isinstance(q, Otazka) for q in value) and [(q.text, q.spravne) for q in value] == expected
        for _ in range(2):
            ok, value = c.call(ns, "preved_otazky", (data,))
            c.add("Převod zachová pořadí a význam odpovědí", ok and verify(value),
                  "Převeďte texty, entity i obě hodnoty odpovědi na objekty Otazka.")
            c.add("Zdrojová data se nemění", data == original, "Nevybírejte položky pomocí pop a nepřepisujte slovníky.")
        bad = [None, [], "JSON", {}, {"response_code": 1, "results": data["results"]},
               {"response_code": False, "results": data["results"]}, {"response_code": 0, "results": []},
               {"response_code": 0, "results": {}}, {"response_code": 0, "results": [None]}]
        for field, value in [("type", "multiple"), ("question", None), ("question", " \t "),
                             ("question", "&nbsp;"), ("correct_answer", True), ("correct_answer", "true"), ("correct_answer", "?")]:
            item = dict(data["results"][0])
            item[field] = value
            bad.append({"response_code": 0, "results": [dict(data["results"][1]), item]})
        missing = dict(data["results"][0])
        missing.pop("correct_answer")
        bad.append({"response_code": 0, "results": [missing]})
        for value in bad:
            c.raises(ns, "preved_otazky", (value,), ValueError)
        for filename in ["kontrola-řeka.json", "jine-otazky.json"]:
            path = Path(filename)
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            ok, value = c.call(ns, "nacti_soubor", (filename,))
            c.add("Čtení zadané cesty jako UTF-8", ok and verify(value), "Použijte předanou cestu a stejný převod, ne pevný soubor.")
        Path("vadny.json").write_text("{neplatný JSON", encoding="utf-8")
        c.raises(ns, "nacti_soubor", ("vadny.json",), ValueError)
        c.raises(ns, "nacti_soubor", ("neexistujici.json",), OSError)
except BaseException as exc:
    c.add("Načítání dat lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
