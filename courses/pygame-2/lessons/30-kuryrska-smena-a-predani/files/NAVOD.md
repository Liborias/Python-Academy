# Kurýrská směna: předání projektu

Použijte Python 3.14 (ověřeno 3.14.8) a vlastní .venv. Interpreter zvolte stejně
ve VS Code, VSCodium či PyCharm i terminálu. Podklady ve složce ponechte spolu.
Příkazy spouštějte ve složce tohoto návodu. Vytvoření prostředí:
python -m venv .venv; aktivace ve Windows PowerShellu .\.venv\Scripts\Activate.ps1,
na macOS/Linux source .venv/bin/activate. Pokud aktivaci nechcete, použijte cestu
k python.exe ve .venv. Dále každý příkaz zadejte samostatně:

    python -m pip install -r requirements.txt
    python over_projekt.py
    python reseni.py

Pip -r čte závislosti ze souboru, over_projekt provede testy původního modelu.
Přidejte vlastní testy rozšíření do testy. Neúspěšný test znamená neúspěšný
návratový kód pomocníka. Okno potřebuje místní grafickou plochu hostitele Pythonu.
Nativní okno se ze vzdáleného serveru nepřenáší do webového prohlížeče.

Mezerník: start či výsledek do nabídky, šipky/WASD: pohyb, P: pauza/pokračování,
R: nový pokus, Esc/křížek: zavření. Nasbírejte šest dat a přežijte tři vlny.
Přístav má omezenou energii. Normální zavření uloží droni.png, Stop to nezaručí.

Závěrečná HraSPoradim ukládá nejlepších pět výsledků do data/vysledky.json
vedle zdrojového či sestaveného programu. Potřebuje zapisovatelnou složku.
Předchozí hra.py z25 tabulku ještě nemá. Při chybě přístupu se v závěrečné
hře zobrazí zpráva, poškozený JSON při samotném čtení zůstane nezměněný.
Jednoduchý souborový žebříček neřeší souběžné zápisy více procesů.

Pro předání přiložte všechny .py podklady, requirements.txt, testy a tento návod.
Vlastní .venv ani osobní výsledky nekopírujte jako součást zdrojového projektu.
Čistou kopii ověřte novým prostředím, testy a skutečným spuštěním okna.

Volitelný PyInstaller 6.22.3 musí být ve stejném prostředí:
python -m pip install "pyinstaller==6.22.3"
Pak v Úkolu4 lekce29 nebo závěrečné lekci30 python sestavit.py.
Tento pomocník opravdu spouští stavbu, běžné ukázky ji jen popisují.
Výstup je sestaveni/dist/KuryrskaSmena: předávejte celou složku i s _internal.
Stavějte a testujte na cílovém OS. Zdejší Linux zkouška neověřuje Windows/macOS
ani fyzickou klávesnici příjemce.

Před novou stavbou zálohujte výsledky mimo dist, protože se starší distribuční výstup nahrazuje.
