import os
import sys
sys.path.insert(0, os.getcwd())
from dilna_check import check
from kviz_model import Otazka

c = check()
ns = c.load()
try:
    if ns is not None:
        def play(answers, lines, expected, feedback, reads):
            questions = [Otazka(f"Otázka Ž{i}", answer) for i, answer in enumerate(answers)]
            before = [(q.text, q.spravne) for q in questions]
            output, prompts = [], []
            remaining = iter(lines)
            def input_line(prompt):
                prompts.append(prompt)
                if len(prompts) > len(lines) + 1:
                    raise RuntimeError("Vstup se zbytečně opakuje po konci")
                try:
                    return next(remaining)
                except StopIteration:
                    raise EOFError
            def write(message):
                output.append(str(message))
            ok, value = c.call(ns, "hraj", (questions, input_line, write))
            c.add("Výsledek a počet skutečných odpovědí", ok and value == expected and isinstance(value, tuple),
                  "Vraťte (skóre, počet odpovědí); neplatný vstup ani q/EOF se nepočítají.")
            text = "\n".join(output)
            c.add("Výpis a práce s předaným vstupem", len(prompts) == reads and all(word in text for word in feedback),
                  "Použijte vstup/vypis, zobrazte otázky, zpětnou vazbu a výsledek.")
            c.add("Otázky se nemění", [(q.text, q.spravne) for q in questions] == before,
                  "Průběh patří modelu kvízu, zadané otázky nepřepisujte.")
            c.add("Vypisuje se přes předanou funkci", c.last_output == "", "Nevypisujte přímo print mimo předaný vypis.")
            return output
        play([True, False, True], ["?", " A ", "N", "n"], (2, 3),
             ["1/3: Otázka Ž0", "2/3: Otázka Ž1", "3/3: Otázka Ž2", "Zadejte a, n nebo q.", "Správně.", "Nesprávně.", "Správná odpověď: a", "Výsledek: 2/3"], 4)
        play([False], ["a"], (0, 1), ["Správná odpověď: n", "Výsledek: 0/1"], 1)
        play([False, True], ["n", " Q "], (1, 1), ["Kvíz ukončen.", "Průběžné skóre: 1/1"], 2)
        play([True], [], (0, 0), ["Vstup skončil.", "Průběžné skóre: 0/0"], 1)
        play([True, False], ["a"], (1, 1), ["Vstup skončil.", "Průběžné skóre: 1/1"], 2)
        play([], [], (0, 0), ["Výsledek: 0/0"], 0)

        original_source = ns.get("ziskej_otazky")
        calls, output = [], []
        def source(online=False):
            calls.append(online)
            return [Otazka("Vlastní otázka", True)], "záloha" if online else "offline", "Testovací výpadek" if online else ""
        ns["ziskej_otazky"] = source
        for selection, online in [("", False), (" API ", True)]:
            remaining = iter([selection, "a"])
            output.clear()
            def input_line(prompt):
                try:
                    return next(remaining)
                except StopIteration:
                    raise EOFError
            ok, value = c.call(ns, "hlavni", (input_line, output.append))
            c.add("Hlavní program propojí zdroj a kvíz", ok and value == (1, 1) and calls[-1] is online
                  and f"Zdroj: {'záloha' if online else 'offline'}" in output and (not online or "Testovací výpadek" in output),
                  "Ponechte volbu zdroje a zobrazení případného důvodu zálohy.")
        def broken_source(online=False):
            raise OSError("Chybí záloha")
        ns["ziskej_otazky"] = broken_source
        output.clear()
        ok, value = c.call(ns, "hlavni", (lambda prompt: "", output.append))
        c.add("Chyba načtení je srozumitelná", ok and value is None and any("Otázky se nepodařilo načíst" in line for line in output),
              "Vadná záloha nemá spustit neplatný kvíz.")
        ns["ziskej_otazky"] = original_source
except BaseException as exc:
    c.add("Závěrečnou aplikaci lze ověřit", False, f"{type(exc).__name__}: {exc}")
r = c.run(stdin="\na\nn\na\nn\na\n")
if c.no_error(r):
    c.output_contains(r, "Zdroj: offline", "Výchozí volba používá český místní soubor.")
    c.output_contains(r, "Výsledek: 5/5", "Ponechte hlavní blok a propojte všech pět otázek.")
c.done()
