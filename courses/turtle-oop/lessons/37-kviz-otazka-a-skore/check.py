from dataclasses import is_dataclass
from dilna_check import check

c = check()
for name in ["Otazka", "Kviz"]:
    c.defines_class(name)
ns = c.load()
question, quiz = [(ns or {}).get(name) for name in ["Otazka", "Kviz"]]
valid = isinstance(question, type) and is_dataclass(question) and isinstance(quiz, type)
c.add("Otazka je dataclass, Kviz je třída", valid, "Ponechte datový záznam Otazka a třídu Kviz.")
try:
    if ns is not None and valid:
        records = []
        for answers in [[], [True], [False], [True, False, False, True]]:
            questions = [question(f"Tvrzení {i}: Žluťoučký kůň?", answer) for i, answer in enumerate(answers)]
            supplied = list(questions)
            game = quiz(supplied)
            supplied.append(question("Pozdější změna vstupu", True))
            c.add("Počáteční a vlastní stav", game.index == 0 and game.skore == 0 and game.otazky == questions,
                  "Konstruktor uchová vlastní seznam a začne na nule.")
            state = (game.index, game.skore, list(game.otazky))
            for invalid in ["True", "False", 1, 0, None, []]:
                ok, value = c.call({"odpovez": game.odpovez}, "odpovez", (invalid,))
                c.add("Neplatná odpověď nemění stav", not ok and isinstance(value, ValueError)
                      and (game.index, game.skore, game.otazky) == state,
                      "Odmítněte vše kromě bool výjimkou ValueError před změnou skóre nebo indexu.")
            score = 0
            for i, original in enumerate(questions):
                for _ in range(2):
                    ok, value = c.call({"aktualni": game.aktualni}, "aktualni")
                    c.add("Čtení aktuální otázky je beze změny", ok and value is original and game.index == i and game.skore == score,
                          "Vraťte aktuální objekt, nic neposouvejte.")
                answer = original.spravne if i % 2 == 0 else not original.spravne
                expected = answer == original.spravne
                score += int(expected)
                ok, value = c.call({"odpovez": game.odpovez}, "odpovez", (answer,))
                c.add("Vyhodnocení a jediný posun", ok and type(value) is bool and value == expected
                      and game.index == i + 1 and game.skore == score and c.last_output == "",
                      "Přidejte bod pouze za shodu a posuňte se i po chybné odpovědi; nic nevypisujte.")
            ok, value = c.call({"aktualni": game.aktualni}, "aktualni")
            c.add("Konec vrací None", ok and value is None and game.index == len(questions) and game.skore == score,
                  "Dokončený i prázdný kvíz už nemá další otázku.")
            state = (game.index, game.skore, list(game.otazky))
            for answer in [True, False]:
                ok, value = c.call({"odpovez": game.odpovez}, "odpovez", (answer,))
                c.add("Po konci se nezapočítává znovu", not ok and isinstance(value, ValueError)
                      and (game.index, game.skore, game.otazky) == state, "Po konci vyvolejte ValueError beze změn.")
            c.add("Obsah otázek zůstal zachovaný", [(q.text, q.spravne) for q in questions]
                  == [(f"Tvrzení {i}: Žluťoučký kůň?", a) for i, a in enumerate(answers)], "Otázky pouze čtěte.")
            records.append((game, state))
        for game, state in records:
            c.add("Nezávislé kvízy", (game.index, game.skore, game.otazky) == state, "Neukládejte průběh do společných atributů.")
except BaseException as exc:
    c.add("Model kvízu lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
