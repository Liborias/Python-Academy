from dilna_check import check
c = check()
c.defines_class("Teplomer")
ns = c.load()
cls = (ns or {}).get("Teplomer")
c.add("Teplomer je třída", isinstance(cls, type), "Definujte class Teplomer.")
if ns is not None and isinstance(cls, type):
    try:
        temperature = getattr(cls, "teplota", None)
        fahrenheit = getattr(cls, "fahrenheit", None)
        c.add("Property teplota", isinstance(temperature, property) and temperature.fget is not None and temperature.fset is not None,
              "Vytvořte property teplota s getterem i setterem.")
        c.add("Property pouze pro čtení", isinstance(fahrenheit, property) and fahrenheit.fget is not None,
              "Fahrenheit má být property pro čtení.")
        ok_a, a = c.call(ns, "Teplomer")
        ok_b, b = c.call(ns, "Teplomer", (0,))
        valid = ok_a and ok_b and isinstance(a, cls) and isinstance(b, cls)
        c.add("Vytvoření teploměrů", valid, "Použijte výchozí teplotu 20 a možnost zadat vlastní hodnotu.")
        if valid:
            def read(obj, expected):
                actual = getattr(obj, "teplota", None)
                converted = getattr(obj, "fahrenheit", None)
                c.add("Teplota se čte jako atribut", actual == expected, f"Očekávám teplotu {expected}.")
                c.add("Aktuální Fahrenheit", isinstance(converted, (int, float)) and abs(converted - (expected * 1.8 + 32)) < 1e-6,
                      "Fahrenheit přepočítejte z aktuální teploty bez zaokrouhlení.")

            def assign(obj, name, value):
                setattr(obj, name, value)

            read(a, 20)
            read(b, 0)
            for value in [-50, 100, -12.5, 0, 37.5]:
                ok, _ = c.call({"nastav": assign}, "nastav", (a, "teplota", value))
                c.add("Přijetí platné hodnoty", ok, "Setter přijímá i hranice -50 a 100 a běžná desetinná čísla.")
                read(a, value)
                read(b, 0)
            for value in [-50.1, 100.1, -100, 200]:
                ok, error = c.call({"nastav": assign}, "nastav", (a, "teplota", value))
                c.add("Neplatná změna", not ok and isinstance(error, ValueError), "Mimo rozsah vyvolejte ValueError.")
                read(a, 37.5)
                c.raises(ns, "Teplomer", (value,), ValueError)
                read(b, 0)
            ok, error = c.call({"nastav": assign}, "nastav", (a, "fahrenheit", 999))
            c.add("Zákaz přiřazení do fahrenheit", not ok and isinstance(error, AttributeError), "K fahrenheit nepřidávejte setter.")
            read(a, 37.5)
            for value in [-50, 100]:
                ok, obj = c.call(ns, "Teplomer", (value,))
                c.add("Hraniční počáteční hodnota", ok, "Hranice jsou platné i při vytvoření.")
                if ok:
                    read(obj, value)
            read(a, 37.5)
    except BaseException as exc:
        c.add("Ověření property bez chyby", False, f"{type(exc).__name__}: {exc}")
c.done()
