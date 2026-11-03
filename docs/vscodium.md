## Proč VSCodium a co je jinak než v PyCharm

PyCharm má vše v sobě. VSCodium je editor, který se skládá z **rozšíření**. VSCodium je stahuje z registru **Open VSX**, ne z obchodu Microsoftu. Některá rozšíření Microsoftu (například **Pylance**, vzdálený vývoj, Live Share) mají licenci jen pro produkty Microsoftu a ve VSCodium nejsou nebo nefungují.

- Spuštění programu: **Ctrl+Shift+B** (úloha „Spustit aktuální soubor“), nebo `python soubor.py` v terminálu.
- Ladění: **F5** (rozšíření Python Debugger), body přerušení klikem vedle čísla řádku.
- Virtuální prostředí: složka `.venv` ve složce projektu, vytvoří ji `tools/setup_env.py`.
- Otevřít složku: Soubor → Otevřít složku → složka `dilna-pythonu`. Pak se použije nastavení z `.vscode/`.

## Doporučená rozšíření (Open VSX)

- `ms-python.python` – základ pro Python.
- `ms-python.debugpy` – ladění.
- `detachhead.basedpyright` – našeptávání, kontrola typů, přechod k definici. **Náhrada za Pylance.**
- `charliermarsh.ruff` – kontrola stylu a formátování (náhrada za inspekce PyCharm).
- `ms-toolsai.jupyter` – notebooky (podkurz Pandas).

Nainstalujete je jedním příkazem: `python tools/install_extensions.py`, nebo ručně v panelu Rozšíření (Ctrl+Shift+X).

## Kontrolní seznam: ověřte u sebe

Rozšíření se mění a mohou se chovat různě podle verze VSCodium. Projděte a zaškrtněte:

- [ ] VSCodium se spustí a otevře složku projektu.
- [ ] V panelu Rozšíření jsou nainstalovaná všechna rozšíření ze seznamu výše.
- [ ] Příkaz `python tools/doctor.py` v terminálu nehlásí chybějící povinné věci.
- [ ] Ctrl+Shift+B spustí otevřený soubor `.py` a výstup se objeví v terminálu.
- [ ] Při psaní `pri` se nabídne `print` (našeptávání BasedPyright).
- [ ] F5 zastaví program na bodu přerušení (ladění).
- [ ] Ve spodní liště je vidět Python z `.venv` (rozšíření Python).
- [ ] Tlačítko „Otevřít ve VSCodium“ v lekci otevře soubor (jinak se zobrazí cesta k ručnímu otevření).
- [ ] Pro podkurz Pandas: soubor s buňkami `# %%` jde spustit po buňkách (Jupyter).

Co nefunguje, najdete v části Řešení problémů. Aplikace se dá používat i bez všech rozšíření: lekce spouští a kontroluje kód sama.

## Soubory v `.vscode/`

- `extensions.json` – doporučená rozšíření.
- `settings.json` – 4 mezery, UTF-8, Ruff jako formátovač, BasedPyright jako jediný jazykový server.
- `tasks.json` – úlohy: spustit soubor, spustit aplikaci, doctor.
- `launch.json` – ladění aktuálního souboru Pythonem z `.venv`.
- `pyrightconfig.json` (v kořeni) – řekne BasedPyright, kde je `.venv`.
