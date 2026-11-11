## Volitelný příkaz pro PyInstaller

Vytvořte **prikaz_baleni(python, skript, vystup, jmeno='KuryrskaSmena')**. Zkontrolujte interpreter a existující .py jako v Úkolu 3. Jméno má 1–40 ASCII znaků, začíná písmenem, zbytek dovoluje písmena/číslice/_/-. Neplatné hodnoty znamenají ValueError.

Seznam začíná [python, '-m', 'PyInstaller', '--onedir', '--console', '--clean', '--noconfirm', '--name', jmeno]. Následují --distpath, --workpath a --specpath s absolutními cestami vystup/dist, vystup/build a vystup/spec. Poslední je absolutní skript. Nic nevytvářejte ani nespouštějte.

Onedir připraví celou distribuční složku, console nechá viditelnou diagnostiku, clean vyčistí stavební cache, noconfirm dovolí nahradit starší výstup v určené stavební složce. Uživatelské JSON výsledky nepřibalujeme; hra je vytvoří při používání. Sestavit.py v tomto úkolu načte právě vaši funkci a sestaví připravenou hra.py, pouze když jej sami spustíte.
