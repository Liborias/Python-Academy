## Vlastní testy před předáním

Půjčovna v model.py navazuje na datovou vrstvu Evidence z 10 a Luhn z 26. Má pomůcky, dostupné kusy, výpůjčky a vrácení. Navíc kod(id) vytvoří inventární kód a id_z_kodu jej ověří i vyhledá. Obecně platný Luhn tak nestačí: předmět musí existovat a id musí mít kanonický zápis bez úvodních nul.

```python
# Test trvalosti potřebuje nové spojení po zavření původního modelu.
from tempfile import TemporaryDirectory
from pathlib import Path
with TemporaryDirectory() as adresar:
    print((Path(adresar) / 'zkouska.sqlite3').name)
```

Testy pracují s fiktivními daty a novou TemporaryDirectory pro každý případ. AddCleanup zaregistrujte hned: nejprve úklid složky, potom model.close. Pořadí úklidu je opačné, takže soubor nebude otevřený při mazání. QR knihovna není pro testy potřeba.

## Ověření vlastností, ne jen běhu

Test nemá pouze zavolat funkci. Musí porovnat skutečný výsledek s očekáváním a u chyby ověřit zachování stavu. Vrat podle stejného id vrátí kus nejvýše jednou. Chyba při vložení výpůjčky nesmí zanechat odečet ve skladu. To lze ověřit skutečným SQL triggerem, který vyvolá chybu druhé části operace.

Sada dostane Pujcovna jako parametr. Spustíme ji nad správným modelem i cílenými poruchami. Názvy testů nejsou podstatné; pokud test projde i při chybné vlastnosti, zatím nás před ní nechrání.

## Váš úkol

Doplňte **vytvor_sadu(Pujcovna)** vracející unittest.TestSuite s alespoň šesti nepřeskakovanými případy. Sama sadu nespouští, používá předanou třídu. Hlavní blok spustí testy a vrátí kód 0/1 podle výsledku.

Pokryjte trvalé přidání po close/reopen včetně přesného názvu s apostrofem; správný kód i změnu jeho poslední číslice; odmítnutí půjčení nedostupného kusu bez vytvoření výpůjčky; vrácení právě jednou; neexistující předmět a kód s úvodními nulami; chybu druhého SQL zápisu, při níž se vrátí odečet.

Model metody: pridej_pomucku, prehled, pujc_kod, vrat, aktivni_vypujcky, kod a id_z_kodu. Všechny vlastní transakce i spojení, do con nevkládejte cizí rozpracované změny mimo řízený test. Možné řešení ukazuje jednu sadu, vlastní struktura je vítaná. Nepoužívejte svou jedinou DB.
