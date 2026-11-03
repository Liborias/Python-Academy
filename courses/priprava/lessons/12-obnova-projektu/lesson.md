## Cíl
Získat stejný projekt z Gitu a nově vytvořit místní prostředí. Repozitář přenáší zdrojové soubory, nikoli běžící procesy a nainstalovaný interpreter.

## Praktický krok
Proveďte ve druhé nové složce, ne uvnitř původního projektu. Nahraďte adresu svou:
```bash
git clone https://github.com/VAS-UCET/moje-akademie.git moje-akademie-kopie
cd moje-akademie-kopie
git status
```
Nainstalujte Python a editor stejně jako v úvodu. Na Windows vytvořte `py -3.14 -m venv .venv`, na macOS/Linux `python3 -m venv .venv`. Pokud projekt má `requirements.txt`, spusťte Pythonem z nové `.venv` příkaz `-m pip install -r requirements.txt`. Pokud žádné externí závislosti nemá, tento krok vynechte; soubor nevymýšlejte jen kvůli příkazu.

Vyberte nový interpreter v editoru, spusťte `main.py` a porovnejte výsledek. Pro přenesenou Dílnu použijte její `tools/setup_env.py --courses vybrany-kurz`, protože právě ten zná balíčky podkurzů. Hodnotu vybrany-kurz nahraďte skutečným id, například `zaklady`.

Přístupy k soukromému repozitáři se řeší přihlášením nového počítače. `.env` nebo klíče se nepřenášejí veřejným commitem. Databáze a vaše pracovní data potřebují samostatný domluvený způsob zálohy. Server je po obnově nutné znovu spustit.

## Co příkazy dělají a co se děje
`git clone ADRESA moje-akademie-kopie` stáhne repozitář včetně historie do nové složky a připraví pracovní kopii. `cd` do ní přepne terminál. `git status` potvrdí, na jaké větvi jste a zda má kopie neuložené změny. Git neinstaluje Python, balíčky ani editor.

Proto následuje `-m venv .venv`, které vytvoří prostředí na tomto konkrétním stroji. Instalace `-m pip install -r requirements.txt` přečte uložené požadavky a stáhne balíčky znovu. Potom spusťte program a ověřte jeho výsledek. Odpovídající commit ověříte `git log --oneline -1`; samotná shoda historie ještě nedokazuje funkčnost prostředí. Ani clone ani pip install znovu nespouštějí server.

## Vlastní ověření
- [ ] Nová kopie má stejný poslední commit jako původní projekt.
- [ ] `.venv` vznikla znovu a nekopíroval/a jsem ji mezi systémy.
- [ ] Po výběru interpreteru jde projekt spustit z nové složky.
