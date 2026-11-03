from dataclasses import fields, is_dataclass, MISSING
from dilna_check import check
c = check()
c.defines_class("ZaznamHrace")
ns = c.load()
cls = (ns or {}).get("ZaznamHrace")
valid_class = isinstance(cls, type) and is_dataclass(cls)
c.add("ZaznamHrace je dataclass", valid_class, "Použijte dekorátor dataclass ze standardní knihovny.")
if ns is not None and valid_class:
    try:
        metadata = {field.name: field for field in fields(cls)}
        c.add("Tři požadovaná pole", list(metadata) == ["jmeno", "body", "udalosti"], "Deklarujte pole v pořadí jmeno, body, udalosti.")
        log_field = metadata.get("udalosti")
        c.add("Továrna na výchozí seznam", log_field is not None and log_field.default_factory is not MISSING
              and callable(log_field.default_factory), "Pro události použijte field(default_factory=list) nebo jinou továrnu na nový seznam.")
        ok_a, a = c.call(ns, "ZaznamHrace", ("Ema",))
        ok_b, b = c.call(ns, "ZaznamHrace", ("Ema",))
        ok_d, d = c.call(ns, "ZaznamHrace", ("Žaneta", -3))
        valid = ok_a and ok_b and ok_d and all(isinstance(obj, cls) for obj in (a, b, d))
        c.add("Automatická inicializace", valid, "Povinné je jméno, body mají výchozí hodnotu 0 a události vlastní prázdný seznam.")
        if valid:
            c.add("Správné počáteční hodnoty", a.jmeno == "Ema" and b.jmeno == "Ema" and d.jmeno == "Žaneta"
                  and a.body == b.body == 0 and d.body == -3 and a.udalosti == b.udalosti == d.udalosti == [], "Uložte argumenty beze změny.")
            c.add("Vlastní seznamy", isinstance(a.udalosti, list) and isinstance(b.udalosti, list)
                  and isinstance(d.udalosti, list) and len({id(a.udalosti), id(b.udalosti), id(d.udalosti)}) == 3,
                  "Factory vytváří nový prázdný seznam pro každou instanci.")
            c.add("Hodnotová rovnost a odlišná identita", a == b and a is not b and a != d, "Využijte rovnost dataclass, objekty neslučujte.")
            representation = repr(a)
            c.add("Užitečný repr", representation.startswith("ZaznamHrace(") and "jmeno='Ema'" in representation
                  and "body=0" in representation and "udalosti=[]" in representation, "Ponechte přehledný repr s hodnotami všech polí.")
            expected = []
            for text in ["start", "bod", "start", ""]:
                expected.append(text)
                ok, result = c.call({"zapis": getattr(a, "zapis", None)}, "zapis", (text,))
                c.add("Zápis vrací počet a uchovává pořadí", ok and type(result) is int and result == len(expected)
                      and a.udalosti == expected, "Přidejte každý text na konec a vraťte nový počet.")
                c.add("Ostatní seznamy zůstaly prázdné", b.udalosti == [] and d.udalosti == [], "Neměňte události ostatních hráčů.")
            c.add("Události ovlivní rovnost", a != b, "Automatické porovnání má zahrnovat i události.")
            a.udalosti.clear()
            c.add("Po obnovení hodnot jsou záznamy rovné", a == b, "Rovnost má sledovat aktuální pole.")
            a.body = 7
            c.add("Body ovlivní rovnost", a != b and b.body == 0, "Pole jsou měnitelná a každá instance má vlastní stav.")
            ok, explicit = c.call(ns, "ZaznamHrace", ("Jan", 12, ["připojení"]))
            c.add("Lze předat i vlastní seznam", ok and explicit.jmeno == "Jan" and explicit.body == 12
                  and explicit.udalosti == ["připojení"], "Vygenerovaný konstruktor umožňuje zadat hodnoty všech polí.")
    except BaseException as exc:
        c.add("Práce s dataclass bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
