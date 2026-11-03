## Cíl
Rozlišit nástroje, aby se instalace nepletla s programováním. Python vykonává kód, editor ho pomáhá psát, terminál přijímá příkazy a prohlížeč zobrazuje web. Projekt je složka se soubory. Server je běžící program, nikoli zvláštní druh složky.

Pro první lekce nepotřebujete GitHub, účet v cloudu ani virtuální server. Zvolte jeden editor: VS Code, VSCodium nebo PyCharm. Výuková aplikace má vlastní webový editor, takže vnější editor můžete přidat postupně.

## Praktický krok
1. Najděte složku rozbalené Dílny, kde leží `start.py` a adresáře `courses`, `server`, `web`.
2. Otevřete terminál právě v této složce. Windows: PowerShell; macOS/Linux: Terminal.
3. Ověřte obsah složky: Windows `Get-ChildItem`, macOS/Linux `ls`. Nezadávejte Python kód do shellu ani shellové příkazy za Python prompt `>>>`. Z Python konzole se vrátíte příkazem `exit()`.
4. Na stránce svého podkurzu vyberte systém a editor v části Příprava. Návod se přizpůsobí vašemu výběru.

## Co příkazy dělají a co se děje
`Get-ChildItem` a `ls` vypisují soubory aktuální složky; nic nemažou ani neinstalují. Terminál si pracovní složku pamatuje. Příkaz proto hledá relativní cesty právě v ní. `>>>` je naopak značka interaktivní Python konzole, kde se píše Python kód; `exit()` ji ukončí a vrátí ovládání terminálu.

## Vlastní ověření
- [ ] Dokážu najít `start.py` a otevřít v jeho složce terminál.
- [ ] Rozlišuji editor od interpreteru Pythonu.
- [ ] Vím, že zavřením terminálu se může zastavit spuštěný server.
