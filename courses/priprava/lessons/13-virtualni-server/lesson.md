## Cíl
Vyzkoušet malý projekt na Linuxovém serveru a přistupovat k němu přes SSH tunel. Virtuální server je jiný počítač s vlastním OS a Pythonem; `.venv` uvnitř něj izoluje jen balíčky.

Tato část je volitelná. Použijte vlastní školní virtuální počítač nebo VPS s Linuxem, uživatelským účtem a SSH přístupem. Poskytovatel může účtovat peníze. Krok není podmínkou pro žádný běžný podkurz. Nenasazujeme zde Dílnu, která záměrně spouští studentský kód; přesouváme pouze vlastní malý projekt.

## Praktický krok
1. Na svém počítači použijte `ssh uzivatel@adresa-serveru`. Účet a adresu nahraďte skutečnými údaji. Otisk serverového klíče porovnejte s údajem od správce/poskytovatele; nepotvrzujte neznámý server naslepo.
2. Na serveru ověřte `python3 --version` (alespoň 3.12) a `git --version`. Na vhodném Debianu/Ubuntu může správce doinstalovat `python3 python3-venv python3-pip git`. Příkaz distribuce neslibuje přesnou verzi 3.14.
3. V domovské složce serverového uživatele naklonujte svůj repozitář. V jeho složce vytvořte `python3 -m venv .venv`, případně obnovte balíčky z `requirements.txt`, potom spusťte `./.venv/bin/python main.py`.
4. Pro statický web z lekce 08 nejprve doma přidejte jen `public/index.html` do Gitu, commitněte a odešlete; na serveru jej stáhněte přes `git pull --ff-only` nebo nový clone. Na serveru spusťte:
```bash
./.venv/bin/python -m http.server 8000 --bind 127.0.0.1 --directory public
```
Na svém počítači otevřete druhý terminál a spusťte:
```bash
ssh -N -L 8080:127.0.0.1:8000 uzivatel@adresa-serveru
```
Ve svém prohlížeči otevřete `http://127.0.0.1:8080`. Lokální port 8080 vede tunelem na serverový port 8000. Žádný veřejný port pro tento pokus neotevírejte. Tunel i testovací server ukončíte Ctrl+C v příslušném terminálu. Při ukončení SSH nemusí testovací proces zůstat běžet.

## Co příkazy dělají a co se děje
`ssh uzivatel@adresa-serveru` otevře vzdálenou shellovou relaci. Příkazy zadané v této relaci už mění server, nikoli váš počítač. `git clone`, vytvoření `.venv` i instalaci balíčků proto provedete znovu na serveru. `./.venv/bin/python main.py` zde ověří serverový interpreter a u terminálového programu vypíše výsledek zpět do SSH relace.

V příkazu tunelu `ssh -N -L 8080:127.0.0.1:8000 ...` znamená `-N`, že neotevřete vzdálený shell. `-L` nastaví předávání: místní port 8080 vede přes SSH na 127.0.0.1:8000 z pohledu serveru. Tunel sám žádný webový server nespustí. Proto musí zároveň běžet první serverový proces. Při zobrazení místní adresy :8080 dostává prohlížeč soubor ze serveru, ačkoli vzdálený port není veřejně otevřený. Každý terminál drží jiný proces; Ctrl+C v jednom automaticky nenahradí zastavení druhého.

## Vlastní ověření
- [ ] Rozlišuji příkazy na svém počítači od příkazů na serveru.
- [ ] Vlastní `main.py` běží na serverovém Pythonu z `.venv`.
- [ ] Přes tunel vidím statickou stránku a umím obě spojení ukončit.
