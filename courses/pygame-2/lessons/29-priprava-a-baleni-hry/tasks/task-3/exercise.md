## Spuštění se stejným Pythonem

Vytvořte **prikaz_spusteni(python, skript)**. Interpreter musí být neprázdný text a skript existující soubor s příponou .py bez ohledu na velikost písmen; jinak ValueError. Vrátíte [python, '-X', 'utf8', absolutni_cesta_skriptu].

-X utf8 zapíná režim UTF-8. Každá položka je jeden argument; cesta s mezerami zůstává jedním textem bez přidaných uvozovek. Funkce příkaz pouze připraví, nic nespustí. Při skutečném použití subprocess.run(seznam, check=True) nepoužíváme shell=True; sys.executable vybere stejný Python jako nyní.
