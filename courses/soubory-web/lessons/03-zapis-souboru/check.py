from dilna_check import check
c = check()
c.utf8()
ns = c.load()


def cti(nazev):
    with open(nazev, "rb") as f:
        return f.read().decode("utf-8").replace("\r\n", "\n")   # Windows zapisuje konce řádků jinak


if ns is not None:
    c.call(ns, "uloz_radky", ("t1.txt", ["první", "žluťoučký kůň", "třetí"]))
    try:
        c.add("uloz_radky: každý text na vlastním řádku", cti("t1.txt") == "první\nžluťoučký kůň\ntřetí\n",
              f"V souboru je {cti('t1.txt')!r}. Za každým textem má následovat nový řádek.")
    except (OSError, UnicodeDecodeError) as e:
        c.add("uloz_radky: soubor vznikl a je v UTF-8", False, f"{type(e).__name__}: {e}")
    c.call(ns, "uloz_radky", ("t1.txt", ["jen jeden"]))
    try:
        c.add("uloz_radky: starý obsah se přepíše", cti("t1.txt") == "jen jeden\n", f"V souboru je {cti('t1.txt')!r}.")
    except (OSError, UnicodeDecodeError) as e:
        c.add("uloz_radky: druhé volání", False, str(e))
    c.call(ns, "uloz_radky", ("t2.txt", []))
    try:
        c.add("uloz_radky: prázdný seznam dá prázdný soubor", cti("t2.txt") == "", "Pro prázdný seznam má vzniknout prázdný soubor.")
    except OSError as e:
        c.add("uloz_radky: prázdný seznam", False, str(e))
    c.call(ns, "uloz_radky", ("t3.txt", ["a"]))
    c.call(ns, "pridej_radek", ("t3.txt", "b"))
    c.call(ns, "pridej_radek", ("t3.txt", "č"))
    try:
        c.add("pridej_radek: řádky se přidávají na konec", cti("t3.txt") == "a\nb\nč\n", f"V souboru je {cti('t3.txt')!r}.")
    except (OSError, UnicodeDecodeError) as e:
        c.add("pridej_radek", False, str(e))
    c.call(ns, "pridej_radek", ("novy.txt", "x"))
    try:
        c.add("pridej_radek: nevzniklý soubor se vytvoří", cti("novy.txt") == "x\n", "Režim a soubor vytvoří, když neexistuje.")
    except OSError as e:
        c.add("pridej_radek: nový soubor", False, str(e))
    with open("zdroj.txt", "w", encoding="utf-8") as f:
        f.write("Příliš žluťoučký\nkůň\n")
    c.call(ns, "zkopiruj", ("zdroj.txt", "cil.txt"))
    try:
        c.add("zkopiruj: obsah je stejný", cti("cil.txt") == "Příliš žluťoučký\nkůň\n", f"V cílovém souboru je {cti('cil.txt')!r}.")
        c.add("zkopiruj: zdroj zůstal beze změny", cti("zdroj.txt") == "Příliš žluťoučký\nkůň\n", "Zdrojový soubor se nesmí měnit.")
    except (OSError, UnicodeDecodeError) as e:
        c.add("zkopiruj", False, str(e))
    ok, v = c.call(ns, "zkopiruj", ("zdroj.txt", "cil2.txt"))
    c.add("zkopiruj nic nevrací", ok and v is None, "Funkce zkopiruj má obsah jen zapsat, nic nevracet.")
c.done()
