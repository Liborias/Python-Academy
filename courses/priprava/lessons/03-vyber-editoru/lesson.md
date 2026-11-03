## Cíl
Vybrat jeden editor a otevřít v něm celý projekt. Všechny tři možnosti vedou ke stejnému Pythonu; změna editoru nemá vyžadovat přepsání programu.

## Praktický krok
1. Nainstalujte vybraný editor z jeho oficiálního webu: [VS Code](https://code.visualstudio.com/), [VSCodium](https://vscodium.com/) nebo [PyCharm](https://www.jetbrains.com/pycharm/).
2. Otevřete složku `dilna-pythonu`, nejen soubor `start.py`.
3. VS Code: rozšíření Python, Python Debugger, BasedPyright a Ruff z Marketplace. VSCodium: obdobná rozšíření z Open VSX. VSCodium nenabízí všechny licencované doplňky Microsoftu. Projekt používá BasedPyright, proto souběžně nezapínejte Pylance.
4. PyCharm: použijte vestavěné nástroje Pythonu; rozšíření VS Code sem nepatří.
5. Interpreter vyberete po vytvoření `.venv` v páté lekci: VS Code/VSCodium přes Python: Select Interpreter, PyCharm přes nastavení Python Interpreter → Existing environment.

Podrobný návod pro každý editor najdete ve společné Přípravě prostředí nebo přes odkaz v přípravě svého kurzu. Názvy menu se mohou mezi verzemi lišit. Terminálový příkaz s přesnou cestou k Pythonu je společný záložní postup.

## Co příkazy dělají a co se děje
Otevření celé složky určuje kontext projektu: editor pak najde soubory a nastavení. Instalace rozšíření mění schopnosti editoru, nikoli verzi Pythonu. Volba interpreteru říká editoru, který spustitelný soubor má použít pro běh a kontrolu importů. Integrovaný terminál je samostatná shellová relace; ověřte v něm cestu k Pythonu zvlášť.

## Vlastní ověření
- [ ] Otevřel/a jsem složku v jednom z editorů.
- [ ] Najdu integrovaný terminál a v něm složku projektu.
- [ ] Vím, kde po vytvoření `.venv` vybrat její interpreter.
