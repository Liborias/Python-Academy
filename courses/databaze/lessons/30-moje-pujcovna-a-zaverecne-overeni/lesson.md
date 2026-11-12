## Vaše varianta půjčovny

Propojíme SQL, transakce, kódy, export a vlastní ověření. Hotový model z 28 zůstává základem. Vytvoříte MojePujcovna s inventárními kartami. Každá ukáže skutečné id, název, Luhn kód, dostupné kusy, počet aktivních výpůjček a celkový počet.

```python
# Celkem je v tomto modelu součet volných a aktuálně půjčených kusů.
dostupne = 1
aktivni_vypujcky = 2
print('Celkem:', dostupne + aktivni_vypujcky)
```

Vrácená historie se do vypůjčených kusů nepočítá. LEFT JOIN musí ponechat i pomůcku bez aktivního půjčení a COUNT(v.id) dát nulu. COUNT(*) by prázdnou pravou stranu počítal chybně. Kódy se tvoří ze skutečných id, ne z indexu seznamu.

## Váš úkol

Doplňte **MojePujcovna.karty**, **souhrn** a **stitky_csv**. Karty vrátí seznam slovníků v pořadí id s přesnými klíči id, nazev, kod, dostupne, vypujceno a celkem. Vypujceno je počet právě aktivních výpůjček, celkem dostupne + vypujceno. Starou vrácenou historii nepočítejte.

Souhrn vrátí {'pomucky': počet řádků, 'dostupne': součet volných, 'vypujceno': součet aktivních}. Prázdná DB má prázdné karty a tři nuly. Stitky_csv(cesta) zapíše UTF-8 CSV se středníkem a hlavičkou `id`, `nazev`, `kod`, `dostupne`, `vypujceno`, `celkem`, přesné názvy/kódy a vrátí počet datových řádků. Použijte csv.DictWriter nebo jiný správný zápis s citováním a `bezpecny_cil(cesta, self.cesta)`. Chyba nesmí přepsat zdrojovou DB či starý export.

## Spuštění hotového projektu

Uložte pracovní složku a dokončete reseni.py. Spust_pujcovnu.py importuje právě vaši MojePujcovna; převezme cesty/zálohu z 29 a volitelný QR z 27.

```powershell
python spust_pujcovnu.py --help
python overeni.py
python spust_pujcovnu.py pridat "Míč" 2
python spust_pujcovnu.py pujcit 18 "Žofie"
python spust_pujcovnu.py vypujcky
python spust_pujcovnu.py vratit 1
python spust_pujcovnu.py export stitky.csv
python spust_pujcovnu.py zaloha kopie.sqlite3
python spust_pujcovnu.py qr 1 stitek.png
```

Kód 18 je příklad pro první id1; použijte skutečný výstup. Vrací se podle id výpůjčky, ne id předmětu nebo kódu. Bez příkazu se vypíše přehled. Výchozí DB je vedle spouštěče, --db CESTA před příkazem naváže na jinou složku, rodič musí existovat. QR vyžaduje volitelnou knihovnu, ostatní funkce bez ní běží dál. Do QR patří jen inventární text, ne jména členů.

Overeni.py provede osm izolovaných testů: šest z 28 nad vaší třídou a dva navíc pro karty/CSV. Hlavní ukázka v Akademii používá paměť a vytvoří pouze CSV v dočasné kopii; v editoru python reseni.py vytvoří stitky.csv v cwd. Pro vlastní data používejte uložený spouštěč. Vyzkoušejte návrat stejné výpůjčky dvakrát, zavření/nové spuštění i otevření zálohy. Všechny příkazy mají význam vysvětlený v NAVOD.md.

Další vlastní varianta může změnit názvy pomůcek či přidat přehled kategorií. Zachovejte testy, správné id a hranice transakcí. Poslední dvě plánované lekce se věnují volitelné serverové databázi; tento místní projekt ji nepotřebuje.
