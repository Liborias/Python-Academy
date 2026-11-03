## Cíl
Pochopit, jak se spojí virtuální prostředí, běžící server a oprávnění ke spuštění souboru. `.venv` určuje Python a balíčky. Token je dočasný náhodný údaj, kterým klient prokáže serveru, že smí požádat o spuštění. Token sám není příkaz pro Python.

Tok událostí: **klient odešle požadavek → server ověří token → Python ze stejné .venv spustí main.py → server vrátí výstup klientovi**. Klientem může být tlačítko v prohlížeči. V této první ukázce použijeme malého Python klienta, aby se současně nemusela učit tvorba webového rozhraní.

## Praktický krok
### 1. Připravte soubory
V rozbaleném archivu najdete `courses/priprava/lessons/09-server-a-token/files/`. Zkopírujte z něj `main.py`, `token_server.py` a `token_client.py` do **nové vlastní složky token-demo**. Tyto soubory neupravují hlavní server Dílny.

Otevřete tuto složku v editoru a v ní terminál. Nepoužívejte pro tuto ukázku `start.py`: tím byste spustili jinou aplikaci na jiném portu.

### 2. Vytvořte prostředí
Windows, PowerShell ve složce token-demo:
```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe main.py
```
macOS/Linux, terminál ve stejné složce:
```bash
python3 -m venv .venv
./.venv/bin/python main.py
```
První příkaz spustí modul `venv` instalovaným Pythonem a vytvoří prostředí do adresáře `.venv`. Druhý spustí `main.py` přímo jeho interpreterem. Uvidíte pozdrav, cestu k Pythonu a `Virtuální prostředí: True`. Ukázka používá jen standardní knihovnu, žádné pip balíčky navíc nepotřebuje. Pokud `.venv` již máte, znovu ji nevytvářejte; ověřte pouze její interpreter.

### 3. Spusťte server
Ve stejném terminálu spusťte Windows `.\.venv\Scripts\python.exe token_server.py`, macOS/Linux `./.venv/bin/python token_server.py`.

Proces zůstane běžet a obsadí místní port 8767. Vypíše nový náhodný token. Terminál nechte otevřený; token si odtud zkopírujete do klienta. Po restartu je starý token neplatný. Token nezapisujte do zdrojových souborů ani Gitu.

### 4. Pošlete požadavek
Otevřete **druhý terminál** ve stejné složce a spusťte Windows `.\.venv\Scripts\python.exe token_client.py`, macOS/Linux `./.venv/bin/python token_client.py`. Vložte do výzvy token z prvního terminálu a potvrďte Enter. Při vkládání nejsou znaky vidět, což je záměr.

Klient vytvoří HTTP požadavek `POST /run`. `POST` zde znamená žádost o akci; samotné otevření adresy v prohlížeči je požadavek `GET` a program nespustí. Hlavička `X-Project-Token` přenáší token, tělo požadavku zůstává prázdné. `127.0.0.1` je tento počítač, 8767 je port našeho serveru, `/run` je název jeho operace.

Při úspěchu uvidíte návratový kód 0, pozdrav z `main.py`, cestu do `.venv` a hodnotu True. Nula znamená, že program skončil bez chyby. Výstup pochází z nového Python procesu spuštěného serverem, ne z výpočtu v klientovi.

### Co se děje uvnitř serveru
Zdrojové soubory berte v této úvodní lekci jako připravenou pomůcku. Pro první pokus stačí umět je spustit a popsat tok požadavku; třídy a podrobnosti HTTP naprogramujete až v navazujícím kurzu.
- `secrets.token_urlsafe(32)` při startu vytvoří náhodný token. Je uložen pouze v paměti běžícího serveru a zobrazen v jeho místním terminálu pro tento pokus.
- `hmac.compare_digest` porovná přijatý token s platným. Při chybě odpoví HTTP 401 a subprocess vůbec nevytváří.
- `sys.executable` je přesná cesta k Pythonu, kterým běží server. Protože jsme server spustili přes `.venv`, stejný Python dostane i `main.py`.
- `subprocess.run([sys.executable, cesta_k_main])` spustí předem určený soubor jako nový proces a počká na konec. Klient nemůže vybrat soubor, poslat kód nebo shellový příkaz.
- `cwd` nastaví pracovní složku programu, `stdin=DEVNULL` zajistí, že program nebude čekat na vstup z klávesnice. Tato ukázka proto neobsluhuje interaktivní `input()` v main.py.
- `capture_output` zachytí výpisy místo zobrazení v terminálu serveru. Server je vrátí v JSON odpovědi, klient je zobrazí. `timeout=5` ukončí čekání na přímý podproces, pokud běží příliš dlouho; klient čeká na síťovou odpověď nejvýše 10 sekund.

### 5. Ověřte chybové stavy
Spusťte klienta znovu s chybným tokenem: očekávejte HTTP 401 a žádný pozdrav. Potom server zastavte Ctrl+C: klient má oznámit, že není dostupný. Po novém spuštění zkuste původní token (401) a pak nový (úspěch). Obsazený port znamená, že na něm už něco běží; nejprve ukončete svůj předchozí pokus.

Tento malý server poslouchá pouze místně a důvěřuje vlastnímu pevnému `main.py`. Token není izolace nebezpečného kódu. Ukázka neřeší veřejný provoz, souběžné úlohy nebo úplné omezení paměti a výstupu; žádný z těchto souborů nevystavujte veřejně. K ovládání tlačítkem ve vlastní stránce se vrátíme při tvorbě konkrétní webové aplikace. Dílna už obdobný princip používá ve svém API, kde má své vlastní názvy hlaviček a tokenů.

## Vlastní ověření
- [ ] Přímé spuštění main.py ukáže Python z mé .venv a True.
- [ ] Platný token vrátí pozdrav a stejný interpreter přes server.
- [ ] Chybný nebo starý token vrátí 401 a program nespustí.
- [ ] Umím server zastavit a vysvětlit rozdíl mezi prostředím, serverem a tokenem.
