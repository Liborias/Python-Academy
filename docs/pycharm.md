## PyCharm: projekt a interpreter

Stáhněte [PyCharm od JetBrains](https://www.jetbrains.com/pycharm/). Základní práce s Pythonem stačí bez placených funkcí; notebooky a vzdálený vývoj se mohou lišit podle verze a licence.

1. Nejprve nainstalujte Python samostatně podle záložky Instalace.
2. Otevřete existující složku `dilna-pythonu` přes Open. Pro vlastní pokusy vytvořte nový projekt v jiné složce.
3. Vytvořte `.venv` příkazy z přípravy vybraného podkurzu. Máte-li ji už připravenou, nevytvářejte další prostředí stejného projektu.
4. Settings → Project → Python Interpreter → Add Interpreter → Existing environment (názvy se liší mezi verzemi). Vyberte `.venv/Scripts/python.exe` na Windows nebo `.venv/bin/python` na macOS/Linux.
5. Ověřte v Python Console: `import sys; print(sys.executable)`. Cesta musí odpovídat vybrané `.venv`.
6. Pro spuštění Dílny vytvořte Run Configuration typu Python: Script path `start.py`, Working directory složka `dilna-pythonu`, interpreter z `.venv`. Spusťte Run.

## Balíčky a ladění

Příkazy z průvodce lze spustit v záložce Terminal. Používejte přímo Python z `.venv` s `-m pip`; neinstalujte balíčky do jiného interpreteru z globálního terminálu.

PyCharm poskytuje vlastní doplňování, inspekce a debugger. Rozšíření Python, Pylance nebo BasedPyright z VS Code sem neinstalujte. Pro ladění klikněte vedle čísla řádku na breakpoint a spusťte Debug pro správnou konfiguraci. Záložní postup je běžné spuštění skriptu z terminálu.

Pro Pandas ověřte podporu notebooků ve své edici; vždy lze použít obyčejný `.py` soubor. GUI kurzy vyžadují místní grafické prostředí.

Tlačítko „Otevřít ve VSCodium“ v lekci otevírá pouze VSCodium. V PyCharm otevřete vypsaný soubor `workspace/<kurz>/<lekce>/reseni.py` ručně. Po uložení v editoru použijte v Dílně „Načíst ze souboru“.

## Vlastní ověření

- [ ] Projekt má právě to prostředí, které chci používat.
- [ ] Python Console ukazuje interpreter v `.venv`.
- [ ] Terminálový příkaz s Pythonem z `.venv` funguje.
- [ ] Konfigurace pro `start.py` má správnou pracovní složku a spustí aplikaci.
- [ ] Debug zastaví na bodu přerušení (pokud jej potřebuji).

Kroky v grafickém rozhraní ověřte ve své verzi PyCharm; nejsou automaticky testované touto aplikací.
