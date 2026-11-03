## Cíl
Spustit program správným interpreterem a rozpoznat chybu programu od chyby nastavení.

## Praktický krok
Vraťte se do vlastního projektu `moje-akademie`. Spusťte Windows `.\.venv\Scripts\python.exe main.py` nebo macOS/Linux `./.venv/bin/python main.py`. Ověřte pozdrav a číslo 5.

V editoru zvolte stejnou `.venv`. VS Code/VSCodium: Python: Select Interpreter. PyCharm: nastavení interpreteru a Run Configuration pro `main.py`. Pracovní adresář konfigurace je složka tohoto projektu. Pro jednoduchý pokus dejte breakpoint na druhý řádek a spusťte Debug. Sledujte, kde se běh zastaví, a poté pokračujte.

Pro Dílnu použijte místo `main.py` soubor `start.py` ve složce `dilna-pythonu`. Otevře místní webovou aplikaci. `Ctrl+C` ji ukončí. Volba `--no-browser` potlačí automatické otevření prohlížeče.

- „No module named …“: ověřte cestu interpreteru a instalaci balíčku právě do něj.
- „Can't open file …“: ověřte pracovní adresář a jméno souboru.
- SyntaxError nebo traceback s řádkem vašeho kódu: přečtěte poslední řádek chyby a opravte uložený soubor.

## Co příkazy dělají a co se děje
Příkaz s cestou do `.venv` a názvem `main.py` se provede jednou a skončí. `start.py` oproti tomu zahájí dlouho běžící server: proto se shellová výzva ihned nevrátí. `Ctrl+C` pošle běžícímu programu požadavek k přerušení. `--no-browser` pouze potlačí otevření prohlížeče, server dál běží a místní adresu vypíše.

Breakpoint je místo, kde debugger pozastaví vykonávání, aby bylo možné číst hodnoty proměnných. Nastavení pracovní složky určuje, odkud program čte relativní soubory. Nastavení interpreteru určuje Python a balíčky. Tyto dvě volby jsou různé a musí obě odpovídat projektu.

## Vlastní ověření
- [ ] Z terminálu i editoru běží stejný soubor stejným Pythonem.
- [ ] Rozumím rozdílu mezi spuštěním skriptu a spuštěním serveru.
- [ ] Zkusil/a jsem breakpoint, nebo mám funkční záložní terminálový postup.
