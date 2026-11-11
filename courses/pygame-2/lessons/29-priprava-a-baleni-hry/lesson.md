## Předáváme projekt, který jde znovu spustit

Nestačí přenést samotný soubor .py. Příjemce potřebuje i importované pomocné soubory, requirements.txt, testy a návod. V této lekci je připravená hra.py původní Hon na dronech, model_hry.py jeho herní třídy a testy/test_modelu.py několik vlastních testů. Vaše reseni.py procvičuje cesty a příkazy.

```python
from pathlib import Path
soubor = Path('moje hra.py')
prikaz = ['python', '-X', 'utf8', str(soubor)]
print('Počet argumentů:', len(prikaz))
print('Poslední argument:', prikaz[-1])
```

Jsou čtyři argumenty; mezera v cestě z ní nevytvoří dva. Seznam argumentů je vhodný pro subprocess.run. Neslepujeme ho do řetězce se shell=True. Běžné ukázky příkazy pouze vypisují: neinstalují balíčky ani nespouštějí stavbu.

## Čisté prostředí před balením

Nejprve uložte pracovní složku přes aplikaci a otevřete ji ve zvoleném editoru. Projektovou .venv z jiného počítače nekopírujte. V terminálu složky vytvořte vlastní:

```powershell
python -m venv .venv
```

Příkaz -m spouští modul venv právě tímto Pythonem, .venv je cílový adresář. Aktivujte prostředí podle systému a stejné vyberte ve VS Code/VSCodium/PyCharm. Windows PowerShell používá:

```powershell
.\.venv\Scripts\Activate.ps1
```

Na macOS/Linux použijte source .venv/bin/activate. Pokud aktivaci PowerShell nepovolí, nemusíte měnit jeho zásady: příkazy spouštějte plnou cestou .\.venv\Scripts\python.exe. Následující python má označovat vybraný interpreter:

```powershell
python -m pip install -r requirements.txt
python over_projekt.py
python hra.py
```

Pip s -r čte seznam závislostí ze souboru; zde pygame-ce==2.5.8. Over_projekt.py spustí vlastní testy a předá jejich návratový kód. Hra.py otevře místní okno, Mezerník startuje. Import pygame ověřte ve stejném prostředí; samotné nainstalované rozšíření editoru knihovnu nepřidá.

## Volitelná distribuční složka

PyInstaller 6.22.3 je volitelný nástroj; standardní průchod kurzem ho nevyžaduje. Ve zvolené .venv lze samostatně zadat:

```powershell
python -m pip install "pyinstaller==6.22.3"
python -m PyInstaller --version
```

První příkaz instaluje konkrétní verzi nástroje, druhý ověří, že ji vidí právě tento Python. Tato verze podporuje Python 3.14 a je dostupná ve zdejším ověřovacím prostředí. Skutečný výsledek stavby tohoto projektu je uveden v dokumentaci předání.

Až v Úkolu 4 dokončíte prikaz_baleni, můžete vědomě spustit python sestavit.py. Pomocník načte vaši funkci z reseni.py a sestaví hra.py do sestaveni/dist/KuryrskaSmena. Check=True hlásí neúspěšný proces jako chybu, nic nepředstírá úspěch. Celou složku včetně _internal ponechte pohromadě. Grafika vzniká kódem, není třeba přibalovat cizí média.

Stavějte a zkoušejte na cílovém systému; linuxový výsledek není Windows aplikací. Ověřte start, ovládání, zavření a čitelný návod. Základní testy modelu neověřují fyzickou klávesnici, grafickou plochu ani všechny varianty instalace.

## Váš úkol

Vytvořte **koren_aplikace(soubor, spustitelny, zmrazeno=False)**. V běžném projektu vyberte soubor, v zabalené hře spustitelny, a vraťte Path(...).resolve().parent. Funkce nic nevytváří, nepřepíná cwd a nic nespouští.

Soubor bývá __file__, spustitelny je sys.executable a zmrazeno je getattr(sys, 'frozen', False). Pracovní adresář je místo, odkud jsme program spustili; nemusí to být složka hry. U --onedir jsou uživatelské výsledky vedle spustitelného programu v data, nikoli uvnitř interních knihoven. Zvolte složku, kam smíte zapisovat.

Před další stavbou zkopírujte vlastní výsledky z distribuční složky mimo dist: sestavení s --noconfirm nahrazuje předchozí výstup.
