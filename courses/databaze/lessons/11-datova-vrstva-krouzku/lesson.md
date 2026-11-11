## Jeden projekt, dvě odpovědnosti

Postavíme **Evidenci kroužků**: nejprve skutečnou databázi, potom okno a přihlášky. Jde o pět návazných kroků, každý s jedním možným řešením. Používáme fiktivní data. Připravené součásti z předchozí lekce jsou v dalším kroku přiložené, můžete je porovnat se svým postupem.

Model nezná Entry ani tlačítka. Dostane běžné Python hodnoty, ověří je, provede SQL a vrátí data. Okno později načte text z polí a zavolá model. Stejný model tak otestujeme i bez grafické plochy.

```python
# Funkce nezávisí na okně: vstup ověříme před zápisem do databáze.
def zkontroluj_kapacitu(kapacita):
    return type(kapacita) is int and kapacita > 0
print(zkontroluj_kapacitu(2), zkontroluj_kapacitu(True))
```

Výsledek je True, False. Bool je v Pythonu potomkem int, proto zde používáme přesný typ. Text z formuláře převedeme až v lekci 12. Model přijímá pouze kladný int, ne text či 2.0.

## Co připraví spojení

`priprava.py` zapne a ověří vazby před transakcí, vytvoří tabulky a vrátí živé spojení s autocommit=False. Krouzky mají id, jedinečný název a kladnou celočíselnou kapacitu. Prihlasky už připravují vazbu na kroužek, členy začneme přidávat v lekci 14. RESTRICT brání smazání kroužku s přihláškami. CREATE IF NOT EXISTS není migrace: pro tento projekt používejte nový `krouzky.sqlite3`.

`with self.con` uzavře jednu transakci: při úspěchu commit, při výjimce rollback. Nezavře spojení. `close` zavře spojení při konci aplikace. Model vlastní celé spojení, nepřidávejte do něj cizí napůl hotové změny. Také jeho čtecí metoda může krátkou vlastní transakci ukončit.

## Prostředí pro tento blok

Python 3.12+, ověřeno 3.14.8; SQLite a unittest nepotřebují pip. Pro další tři lekce ověřte Tkinter příkazem `python -m tkinter`: otevře zkušební okno, které zavřete. Windows: instalace Pythonu s Tcl/Tk; Linux: odpovídající systémový balíček python3-tk; macOS: oficiální Python s Tk. VS Code, VSCodium i PyCharm musí používat stejnou .venv jako terminál. Podrobnosti jsou také v Přípravě kurzu a NAVOD.md.

## Váš úkol

Doplňte **EvidenceKrouzku(cesta)**: připravený konstruktor uloží spojení jako self.con, close ho zavře a lze ho opakovat. Doplňte `pridej(nazev, kapacita)` a `seznam()`.

Pridej použije cisty_nazev (ořízne krajní mezery, prázdný/ne-textový název je ValueError) a kladna_kapacita (přesný kladný int bez bool, jinak ValueError). V jedné vlastní transakci vloží hodnoty přes ? parametry a vrátí skutečné lastrowid. Duplicitní název předá jako sqlite3.IntegrityError. Rozlišujeme velikost písmen i v názvech.

Seznam vrátí [(id, název, kapacita)] v pořadí id; prázdná databáze dává []. Žádné widgety ani SQL spojení se nevytvářejí při importu. Hlavní ukázka použije TemporaryDirectory, databázi zavře a znovu přečte: uložený záznam zůstane. Po ukázce se dočasná složka uklidí.
