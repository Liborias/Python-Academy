## VS Code: instalace a výběr Pythonu

Stáhněte [Visual Studio Code](https://code.visualstudio.com/). Python instalujte samostatně podle záložky Instalace; editor sám interpreter nenahrazuje.

1. Otevřete složku `dilna-pythonu` přes File → Open Folder, nikoli jen jeden soubor.
2. V terminálu vytvořte prostředí podle přípravy zvoleného podkurzu. Vlastní projekty mají vlastní `.venv`.
3. V panelu Extensions nainstalujte Python (`ms-python.python`), Python Debugger (`ms-python.debugpy`), BasedPyright (`detachhead.basedpyright`) a Ruff (`charliermarsh.ruff`) z Marketplace.
4. Ctrl+Shift+P (macOS Cmd+Shift+P) → Python: Select Interpreter → Enter interpreter path. Vyberte `.venv/Scripts/python.exe` na Windows nebo `.venv/bin/python` na macOS/Linux.
5. Otevřete nový integrovaný terminál a ověřte `python -c "import sys; print(sys.executable)"`. Pokud neukazuje do `.venv`, použijte přímo cestu k jejímu Pythonu z průvodce.
6. Soubor `.py` spusťte přes Run Python File in Terminal nebo příkazem s Pythonem z `.venv`. Pro ladění nainstalujte Python Debugger, nastavte breakpoint a zvolte F5 → Python File.

> Projektová `.vscode` nastavení používají BasedPyright, stejný jako ve VSCodium. Pylance je alternativa pro VS Code, ale nenechávejte aktivní dva jazykové servery zároveň. Pokud chcete Pylance, vědomě upravte vlastní nastavení a vypněte BasedPyright. Pro tento kurz stačí doporučené nastavení.

## Notebooky a aplikace

Pro Pandas přidejte rozšíření Jupyter (`ms-toolsai.jupyter`). V notebooku nebo u buněk `# %%` zvolte jádro odpovídající `.venv`, ve které je ipykernel. Záložní postup je spustit soubor jako běžný `.py` skript.

Dílnu Pythonu spustíte ve složce projektu příkazem s Pythonem z `.venv` a souborem `start.py`. Tlačítko „Otevřít ve VSCodium“ v lekci nadále míří na VSCodium; pro VS Code otevřete vypsanou cestu ručně přes File → Open File. Není nutné instalovat druhý editor.

## Vlastní ověření

- [ ] Otevřel/a jsem celou složku projektu.
- [ ] Rozšíření Python a Python Debugger jsou dostupná.
- [ ] Interpreter a terminál ukazují do stejné `.venv`.
- [ ] Soubor `.py` se spustí a vypíše očekávaný výsledek.
- [ ] Bod přerušení skutečně zastaví program (pokud chci ladit).

Konkrétní názvy menu a funkce rozšíření ověřte ve své verzi VS Code. Tento návod nenahrazuje ověření na vašem počítači.
