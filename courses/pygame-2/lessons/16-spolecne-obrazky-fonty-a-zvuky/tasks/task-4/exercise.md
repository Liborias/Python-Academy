### Zvuk s bezpečným vypnutím

Vytvořte `Zvuky(vytvor, povoleno=True)` s veřejným přepínačem `povoleno`. `prehraj(jmeno, hlasitost=0.3)` vrací bool. Při vypnutí vraťte False bez volání továrny. Jinak zvuk pro jméno vytvořte nejvýše jednou po úspěšném načtení, omezte konečnou hlasitost na 0..1, zavolejte `set_volume` a pak `play`. True vracejte pouze tehdy, když play vrátil kanál, ne None. To znamená přijaté přehrání, nikoli záruku slyšitelnosti.

Zachyťte pouze `pygame.error` a vraťte False. Chybné načtení se příště zkusí znovu; už načtený zvuk ponechte i po chybě přehrávání. Ostatní výjimky, například ValueError programové chyby, předávejte dál. Mixer se v tomto modelu sám neinicializuje. Připravený pokus zvuk výslovně vypíná; volitelnou zkoušku zařízení spouští samostatný pomocný skript.
