## Postup se mění mezi kartami nebo se neukládá

Aktualizujte projekt a obnovte všechny otevřené karty aplikace. Opravené ukládání
před zápisem převezme poslední stav ostatních karet. Používejte stejný profil
prohlížeče a adresu aplikace; Git uložený postup mezi počítači nepřenáší.

Při upozornění „Prohlížeč teď neukládá postup“ ponechte stránku otevřenou,
uložte si rozepsaný kód do souboru a ověřte povolení úložiště v prohlížeči.
Další změna postupu zkusí zápis znovu a po úspěchu upozornění zmizí.

## Nejde načíst přípravu kurzu

V přípravném panelu použijte „Zkusit znovu“. Seznam lekcí zůstává přístupný.
Při trvající chybě ověřte, že místní server aplikace běží, a spusťte jej znovu
pomocí Pythonu ze správné .venv.

## Rozšíření Python nenajde interpreter nebo nejde vytvořit prostředí

Zjištěný stav (podle hlášení k VSCodium, verze rozšíření 2026.4.0): rozšíření `ms-python.python` z Open VSX může postrádat složku `python-env-tools/bin` s programem `pet`, a pak nenajde interpretery. Oprava ze strany VSCodium se nechystá, protože jde o proprietární rozšíření Microsoftu. Stav se může změnit, ověřte u sebe.

Co s tím, od nejjednoduššího:

1. **Nic nepotřebujete řešit.** Úlohy a ladění z `.vscode/` ukazují přímo na `.venv`, takže Ctrl+Shift+B a F5 fungují i bez detekce interpreteru.
2. V rozšíření Python **vypněte „Python Environments“** a interpreter zvolte ručně: Ctrl+Shift+P → „Python: Select Interpreter“ → „Enter interpreter path“ → `.venv/bin/python` (Windows `.venv\Scripts\python.exe`). Hlášení uvádějí, že pak může být slabší automatické doplňování importů.
3. Do složky rozšíření `python-env-tools/bin/` zkopírujte program `pet` z oficiálních sestavení Microsoftu (postup potvrdilo několik uživatelů).
4. Zůstaňte u BasedPyright a rozšíření `ms-python.python` vypněte. Spouštění a ladění zůstane na úlohách a `launch.json`.

## BasedPyright nic nenašeptává

- Zkontrolujte, že v kořeni projektu je `pyrightconfig.json` a existuje složka `.venv`.
- Zkuste Ctrl+Shift+P → „Developer: Reload Window“.
- Záložně v `.vscode/settings.json` změňte `"python.languageServer": "None"` na `"Jedi"` (potřebuje rozšíření Python).

## Rozšíření se nenainstaluje

- Zkuste Ctrl+Shift+X a vyhledejte je podle identifikátoru.
- Soubor `.vsix` lze nainstalovat ručně: Ctrl+Shift+P → „Extensions: Install from VSIX“.
- Bez rozšíření stačí terminál: `python soubor.py`.

## `pip install` hlásí „externally-managed-environment“

Instalujete do systémového Pythonu. Aktivujte `.venv` (`source .venv/bin/activate`, Windows `.venv\Scripts\activate`) a zkuste znovu.

## Nejde `import tkinter`

- Linux: `sudo apt install python3-tk`.
- macOS (Homebrew): `brew install python-tk@3.14`.
- Windows: v instalátoru Pythonu musí být zaškrtnuto „tcl/tk and IDLE“.
- macOS 27 a Tkinter: podle poznámek k vydání Pythonu 3.15 se IDLE a aplikace Tkinter mohou při otevření dialogu zaseknout. Ověřte u sebe a pokud ano, zkuste novější drobnou verzi Pythonu.

## `pip install pygame` selže

Použijte `pip install pygame-ce`. Nemějte nainstalované obě varianty najednou (`pip uninstall pygame`).

## Tlačítko „Otevřít ve VSCodium“ nic neotevře

Příkaz `codium` není v PATH. Soubor ručně otevřete podle cesty, kterou aplikace zobrazí. Na macOS příkaz přidáte z VSCodium: „Shell Command: Install 'codium' command in PATH“.

## Aplikace hlásí „Chybí token“

Otevřete adresu, kterou vypsal `python start.py` (obsahuje `?t=…`). Po restartu se token mění.

## Na webu se nespustí okno Tkinter nebo Pygame

Program se spouští na vašem počítači a potřebuje grafické prostředí. Na vzdáleném serveru bez displeje okno neotevře.
