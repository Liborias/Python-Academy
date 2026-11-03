## Cíl
Vytvořit vlastní malý projekt oddělený od výukové aplikace. Příkazy této lekce patří do vlastního pracovního adresáře, nikoli do `courses` Dílny.

## Praktický krok
V terminálu v místě pro vaše projekty vytvořte novou složku. Pokud již existuje, použijte jiný název a nezahazujte její obsah:
```bash
mkdir moje-akademie
cd moje-akademie
```
V editoru v této složce vytvořte soubor `main.py`:
```python
print("Můj první projekt")
print(2 + 3)
```
Spusťte z terminálu Windows `py -3.14 main.py`, macOS/Linux `python3 main.py`. Očekávejte dva řádky: pozdrav a číslo 5. Později budeme místo globálního Pythonu používat vlastní `.venv`.

Vytvořte `README.md` a vlastními slovy zapište, co projekt dělá a jak ho spustit. Soubor uložte jako UTF-8. Dbejte, aby se na Windows soubor nejmenoval skrytě `main.py.txt`. Nespojíte-li správnou pracovní složku a jméno souboru, dostanete chybu, že soubor neexistuje.

## Co příkazy dělají a co se děje
`mkdir moje-akademie` vytvoří adresář v aktuálním místě. `cd moje-akademie` do něj přesune pracovní složku tohoto terminálu. Ani jeden příkaz nevytváří `.py` soubor; ten uložíte v editoru. `py -3.14 main.py` nebo `python3 main.py` předá uložený soubor interpreteru, který vykoná jeho řádky shora dolů. `print` vypíše text nebo výsledek výrazu do terminálu. Po druhém výpisu program skončí a objeví se shellová výzva.

README je textový návod pro člověka, nespouští se Pythonem. Relativní jméno `main.py` se vyhodnocuje vůči aktuální pracovní složce; chyba „soubor neexistuje“ proto může znamenat správný soubor v jiné složce.

## Vlastní ověření
- [ ] Vlastní projekt má svou složku, `main.py` a `README.md`.
- [ ] Spuštění vypíše pozdrav a číslo 5.
- [ ] Změna uloženého textu se projeví při příštím spuštění.
