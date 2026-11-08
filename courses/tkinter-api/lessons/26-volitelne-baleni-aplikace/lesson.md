## Balení je volitelný další krok

Hotový Python projekt můžete dál spouštět z .venv. PyInstaller z něj umí připravit složku s programem a potřebnými moduly pro konkrétní systém. Pro běžné úkoly této lekce ho instalovat nemusíte: naše funkce pouze připraví seznam argumentů. Skutečnou stavbu spustíte zvlášť, až budete chtít výsledek vyzkoušet.

[PyInstaller 6.22.3 na PyPI](https://pypi.org/project/pyinstaller/6.22.3/) uvádí podporu Pythonu 3.14. Tuto verzi jsme použili se zdejším Pythonem 3.14.8 pro skutečné sestavení na Linuxu. Windows a macOS vyžadují vlastní sestavení i zkoušku na daném systému; jeden linuxový výsledek není aplikací pro všechny systémy.

## Jeden interpreter od testů ke stavbě

Nejdřív spusťte původní projekt a vlastní testy ze správné .venv. Pak lze v terminálu s aktivovaným prostředím zadat:

```powershell
python --version
python -m pip install "pyinstaller==6.22.3"
python -m PyInstaller --version
```

První příkaz ukáže používaný Python. Druhý do stejného prostředí nainstaluje přesně uvedenou ověřenou verzi nástroje a její závislosti. Třetí ověří, že ji vidí právě tento Python. Pokud je název python na macOS/Linux jiný, použijte python3 ze zvolené .venv. Tk ověřte na grafické ploše přes `python -m tkinter`. PyInstaller neopraví chybějící Tk v původním interpreteru.

## Připravíme seznam argumentů

`prikaz_sestaveni(python, skript, vystup, jmeno="KorespondencniDilna")` vrátí seznam textů. Python je neprázdný text s interpreterem, skript existující soubor .py a vystup adresář pro výsledek. Path.resolve určí absolutní cesty. Funkce nic nevytváří a nic nespouští.

Název aplikace má 1–40 znaků ASCII, začíná písmenem a dále dovoluje písmena, číslice, _ a -. Isascii ověří znaky ASCII, isalpha první písmeno, isalnum písmena/číslice a all projde zbytek pravidla. Jde o jméno sestaveného programu; zobrazovaný český titulek okna zůstává samostatná vlastnost Tk.

Začátek seznamu tvoří `[python, "-m", "PyInstaller"]`. Tím spustíme modul pomocí předaného interpreteru. Jednotlivé volby znamenají:

- --onedir: výsledek je celá distribuční složka, kterou předáváme pohromadě.
- --console: zůstane dostupný terminál s diagnostikou; jeho potlačení patří až k ověřenému balení.
- --clean: odstraní dočasnou mezipaměť předchozí stavby používanou PyInstallerem.
- --noconfirm: dovolí nahradit starší výsledek v určené výstupní složce bez další otázky. Pro pokusy používejte vlastní složku sestaveni.
- --name: pojmenuje výsledek.
- --distpath, --workpath a --specpath: určí podsložky dist pro výsledek, build pro pracovní soubory a spec pro popis sestavení.

Pokud vedle skriptu existuje složka data, přidáme dvojici `--add-data` a `cesta:data`. PyInstaller tak přibere i nepythonové zdroje. Zápis SOURCE:DEST používá tato verze nástroje; celé spojení je jeden argument. Posledním argumentem je absolutní cesta skriptu. Cesty s mezerami neslepujeme do shellového příkazu a ručně k nim nepřidáváme uvozovky.

## Skutečné sestavení spusťte vědomě

Otevřením lekce v editoru získáte vedle reseni.py hotový projekt dilna.py a pomocný sestavit.py. Až dokončíte funkci v reseni.py, spusťte ze stejné složky:

```powershell
python sestavit.py
```

Sestavit.py importuje vaši funkci, použije sys.executable pro současný interpreter a předá vrácený seznam do `subprocess.run(prikaz, check=True)`. Bez shell=True dostane proces přesně oddělené argumenty. Check=True vyvolá chybu při neúspěšném návratovém kódu, takže skript nebude vydávat selhání za úspěch. Běžná ukázka v lekci tento příkaz pouze vypíše a instalaci ani stavbu neprovádí.

Výsledek bude v sestaveni/dist/KorespondencniDilna. Ve Windows spouštějte KorespondencniDilna.exe, na Linuxu stejnojmenný spustitelný soubor. Zachovejte celou složku včetně _internal. Program potřebuje kompatibilní systém a u Tk také grafickou plochu. Nový uživatelský koncept ukládejte mimo distribuční složku; další lekce oddělí přibalená data od vašich souborů.

## Váš úkol

Dokončete prikaz_sestaveni podle uvedených pravidel. Přijměte předaný interpreter i název, zachovejte cesty s mezerami a složku data zahrňte jen tehdy, když existuje jako adresář. Neplatný interpreter, název či vstupní soubor odmítněte ValueError. Funkce má vracet seznam a nemá vytvářet složky ani spouštět další proces.

Automatická kontrola ověří argumenty a chyby bez závislosti na nainstalovaném PyInstalleru. Skutečná stavba a zkouška výsledku na vašem počítači jsou navazující praktický krok.
