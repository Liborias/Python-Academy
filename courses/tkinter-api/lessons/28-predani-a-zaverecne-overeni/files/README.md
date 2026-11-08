# Korespondenční dílna

Místní výuková aplikace: připraví zprávu, přílohu a náhled, uloží koncept JSON a zprávu předá pouze do vlastního záchytu na 127.0.0.1. Nevyžaduje osobní schránku, přihlášení ani veřejný SMTP server.

## Spuštění

Ověřený interpreter projektu: Python 3.14.8, runtime aiosmtpd 1.4.6. Tk ověřte ve stejné .venv na grafické ploše. V terminálu v této složce:

```powershell
python -m pip install -r requirements.txt
python -m tkinter
python test_projekt.py
python aplikace.py
```

Pokud používáte jiný název příkazu, například python3, nahraďte jej všude konzistentně. Tk není pip balíček; systémovou instalaci popisuje příprava kurzu. Vlastní testy nevytvářejí okno a nahrazují přenos řízenými výsledky. Skutečné SMTP a GUI ověřte také podle SCENARE.md.

## Soubory zdrojového projektu a data

- aplikace.py: hlavní okno, zdroje a klávesové zkratky z lekce 27.
- dilna.py: ověření a uložení/načtení konceptu z lekce 24; další moduly obsahují dřívější hotové kroky.
- data/vychozi-koncept.json: ukázka pouze ke čtení, Načíst ukázku ji najde podle souboru aplikace, nezávisle na pracovní složce.
- test_projekt.py: pět unittest scénářů z lekce 25.
- sestavit.py a baleni.py: volitelná stavba z lekce 26.
- koncept-predani.json: vstup závěrečné konzolové zkoušky v reseni.py.

Vlastní koncept uložte přes dialog na vybranou zapisovatelnou cestu, například do Dokumentů. JSON má verzi 1 a čtyři textová pole. Zachová i neúplnou adresu a vlastní mezery. Příloha je jen nativní absolutní cesta, nikoli kopie obsahu souboru. Při přesunu nebo smazání přílohy koncept načtete a vyberete nový soubor; při přenosu mezi systémy s jiným zápisem cest vyprázdněte v JSON pole priloha a vyberte ji znovu.

## Ovládání a výsledek

Ctrl+S ukládá, Ctrl+O načítá, Ctrl+Enter ověřuje náhled. Vazby používají Control také na macOS. Předání má samostatné tlačítko. V Text použijte pro změnu fokusu Ctrl+Tab.

Během předání lze dál psát. Pracovník dostává samostatný snímek včetně již načtené přílohy. Zrušený dialog nebo chyba načtení zachová práci. Při nejistém výsledku nejprve zkontrolujte záchyt: zpráva už může být uvnitř a nový pokus může vytvořit kopii. Nic se automaticky neopakuje. Záchyt existuje jen v paměti do zavření aplikace a žádnou zprávu nepřeposílá.

## Volitelné sestavení

```powershell
python -m pip install -r requirements-build.txt
python -m PyInstaller --version
python sestavit.py
```

Tato cesta používá PyInstaller 6.22.3. Výsledek je celá složka sestaveni/dist/KorespondencniDilna včetně _internal a přibalených dat. Ve Windows se spouští .exe, na Linuxu stejnojmenný spustitelný soubor. Pro každý cílový systém sestavujte a ověřujte zvlášť. Ověřte spuštění z jiné složky a čtení ukázky; vlastní data ukládejte mimo distribuční adresář. Při chybě čtěte zachovaný výstup konzole.

## Moje předání

Doplňte před sdílením své kopie:

- Operační systém a verze Pythonu/Tk/balíčků:
- Výsledek vlastních testů a praktických scénářů:
- Balení: nepoužito / systém a ověřený výsledek:
- Vlastní vysvětlení: widgety → koncept → EmailMessage → pracovník → místní záchyt:
- Známé omezení nebo neověřená část:
