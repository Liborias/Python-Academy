## Co nyní předáváme

Kurz má hotový projekt od formuláře až po místní SMTP záchyt. V této lekci k němu přidáme popis spuštění, vlastní testy, přibalený ukázkový koncept a závěrečnou konzolovou zkoušku. Otevřením v editoru získáte celou pracovní složku: aplikace.py je okno z lekce 27, test_projekt.py testy z 25 a sestavit.py s baleni.py volitelné sestavení z 26. README.md vysvětluje spuštění a SCENARE.md obsahuje praktické zkoušky.

Závěrečný reseni.py provede jednu místní konzolovou zkoušku. Okno otevřete samostatně pomocí `python aplikace.py`. Oba vstupy používají stejné hotové modely a přenosové funkce. Žádný z nich nepracuje s osobní schránkou a záchyt nic nepřeposílá.

## Nejprve popište a ověřte běžné spuštění

V terminálu s Pythonem ze správné .venv použijte ze složky projektu:

```powershell
python -m pip install -r requirements.txt
python -m tkinter
python test_projekt.py
python aplikace.py
```

Requirements.txt obsahuje ověřenou runtime závislost aiosmtpd==1.4.6. Pip s -r čte seznam ze souboru. Tk je součást systému/instalace Pythonu a neinstaluje se tímto pip příkazem; příprava kurzu uvádí postup pro váš systém. Test_projekt.py spustí pět vlastních unittest scénářů. Aplikace.py otevře skutečné okno na počítači, kde běží Python.

Pokud chcete balit, requirements-build.txt zahrnuje běžné requirements a PyInstaller 6.22.3. Potom lze spustit sestavit.py, který po úspěšné stavbě přidá do výsledku také README.md a SCENARE.md pomocí shutil.copy2. Ta zkopíruje obsah souboru i základní metadata. README rozlišuje tento volitelný postup od běžného spuštění. Výsledek zkoušejte jako celou složku i z jiného pracovního adresáře a pro každý cílový operační systém zvlášť.

## Ověření přečte to, co záchyt skutečně přijal

Dokončíme `prover_predani(cesta)`. Nejprve načte koncept a přes sestav_zpravu ověří adresu, předmět, tělo i přílohu. Potom pomocí with cvicna_posta spustí čerstvý místní záchyt. Nová Queue slouží pro výsledek predat_zpravu, které předáme hotovou zprávu, posta.host, posta.port, timeout 2 a tuto frontu.

V konzolové zkoušce zavoláme pracovní funkci přímo: neběží zde Tk smyčka, kterou bychom blokovali. Ve skutečném okně ji nadále spouští Thread. Get_nowait po dokončení funkce přečte výsledek. Jiný stav než prijato vyvolá RuntimeError a další pokus se automaticky nespustí. Ani potvrzení samo nestačí: ověříme, že posta.zpravy má přesně jeden záznam.

Zaznam.data obsahuje přijaté MIME bajty. BytesParser s policy=default je rozebere; str nad Subject poskytne dekódovaný český předmět. Get_body s preferencelist=("plain",) najde textovou část a get_content ji dekóduje. Konce řádků sjednotíme z CRLF/CR na LF. Přijemci v záznamu patří do SMTP obálky. Iter_attachments projde skutečně přijaté přílohy, get_filename vrátí jejich jméno a get_payload(decode=True) přesné bajty pro výpočet velikosti.

Výsledkem je slovník s těmito údaji:

- stav: prijato a zachyceno: skutečný počet záznamů, tedy 1.
- prijemce: první obálkový příjemce přijatého záznamu.
- predmet a text: dekódovaný obsah skutečně zachycené zprávy, tělo s LF.
- prilohy: seznam slovníků nazev a velikost v bajtech; bez přílohy prázdný seznam.

Souhrn má vycházet ze zachycených dat, ne z původního konceptu a pevných očekávaných hodnot. Koncem with se server zastaví i při výjimce. Zprávy byly v jeho paměti, nikoli ve skutečné doručené poště.

## Váš úkol

Dokončete prover_predani. Proveďte právě jeden pokus, odmítnutí, nejistotu i chybu přeložte na RuntimeError a vraťte popsaný souhrn ze skutečného záznamu. Neplatný vstup se má ohlásit už při načtení nebo sestavení. Hlavní blok používá přibalený koncept-predani.json a vypíše výsledek. Automatická kontrola ověřuje tento průchod a jeho chybové stavy; vzhled předané aplikace a kvalitu vašeho vysvětlení nenahrazuje.

Potom projděte SCENARE.md ve skutečném okně. Ověřte zrušený dialog a vadný soubor bez ztráty práce, původní přílohu při změně souboru během čekání, odmítnutí, ruční nový pokus a timeout po převzetí. U nejistého výsledku nejprve zkontrolujte záchyt; načtení jiného konceptu nemá tuto podmínku obejít.

Doplňte si do README použitý systém, verze Pythonu/Tk/balíčků, způsob spuštění a výsledky svých zkoušek. Vysvětlete vlastními slovy cestu dat od widgetů přes koncept a EmailMessage do záchytu. Připomeňte, že JSON ukládá cestu přílohy, její obsah se nekopíruje a po uzavření programu se místní záchyt vyprázdní. Tím je obsah všech 28 lekcí dokončený; další krok je vyzkoušení a připomínky k hotovému kurzu.
