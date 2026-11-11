## Malá evidence, kterou opravdu spustíme

Sestavíme konzolovou aplikaci: kategorie, pomůcky, půjčení a vrácení. Evidence vlastní databázové spojení i celé transakce. Konzolová obsluha jen načte argumenty a zavolá veřejnou metodu, SQL zůstává v datové vrstvě.

Hotové součásti z 8–9 jsou v relacni_schema.py, operace.py a dotazy.py. Soubor `pomoc.py` poskytuje kontrolu názvů, přesného nezáporného int a kompatibility sloupců. Starý sklad z 1–5 se nepřevádí: při nekompatibilním schématu příprava skončí srozumitelnou chybou a starý obsah zůstane zachovaný.

```python
dostupne = 2
dostupne -= 1
vraceno = False
if not vraceno:
    dostupne += 1
    vraceno = True
print('Po jednom půjčení a vrácení:', dostupne)
```

Vráceno se nesmí provést podruhé. V databázi stejný princip vážeme na id konkrétní výpůjčky a oba zápisy uděláme v jedné transakci. Selhání INSERT výpůjčky musí vrátit odečet ze skladu; selhání označení vrácení nesmí přidat kus navíc.

## Odpovědnosti modelu

Prázdné názvy jsou chyba, krajní mezery ořízneme; to je vědomá úprava na hranici tohoto projektu. Kusy jsou přesný nezáporný int, bool není počet. Půjčení vyžaduje dostupný kus, historie zůstává i po vrácení. Nevytváříme síťový server a nepřidáváme automatické opakování po SQLITE_BUSY.

Čtecí metody také mohou použít krátký with self.con: model vlastní celé spojení a po přečtení tak uvolní transakci. To se liší od samostatných funkcí z 6–9 s cizím con, které ho potvrzovat nesmějí. Do modelu nevkládáme napůl hotové změny přes jeho interní con.

## Ukázka proti vlastní evidenci

Tlačítko Spustit provede malou ukazka(Evidence) v paměti, rychle skončí a nic trvalého nemění. Pro vlastní konzoli uložte pracovní složku a otevřete ji ve VS Code, VSCodium nebo PyCharm se stejnou .venv. Pak v terminálu této složky:

```powershell
python spust_klub.py --help
python spust_klub.py kategorie "Sport"
python spust_klub.py pomucka "Míč" 2 --kategorie 1
python spust_klub.py prehled
python spust_klub.py pujcit 1 "Žofie"
python spust_klub.py vypujcky
python spust_klub.py vratit 1
```

Help vypíše přehled argumentů. Kategorie vytvoří záznam a vypíše id; pomucka vloží dostupné množství a volitelné přiřazení. Prehled čte sklad, pujcit vypíše nové id výpůjčky, vypujcky aktivní půjčení a vratit zkusí vrátit právě toto id. Jedničky jsou příklad pro prázdný soubor: použijte skutečná id z vašeho výstupu.

Výchozí soubor klub.sqlite3 leží vedle spouštěče. Volba --db CESTA před názvem příkazu zvolí jiný soubor; jeho rodičovská složka už musí existovat. Bez příkazu se jen vypíše přehled. Soubor `spust_klub.py` importuje vaši dokončenou Evidence z reseni.py, nepoužívá náhradní hotový model.

Znovu spusťte přehled po zavření původního procesu: potvrzená data zůstanou. Běžné webové spuštění oproti tomu používá dočasnou kopii. Žádné další balíčky, grafickou plochu ani internet nepotřebujete.

## Váš úkol

Doplňte **Evidence(cesta)** se všemi popsanými metodami. Konstruktor uloží vlastní con ze spojeni_s_vazbami; uvnitř transakce vytvoří schéma a zkontroluj_schema ověří kompatibilitu. Při chybě spojení zavře a výjimku předá, při úspěchu přípravu potvrdí. close spojení zavře, lze ho zavolat znovu; po close se spojení automaticky neobnovuje.

`pridej_kategorii(nazev)` ořízne krajní mezery přes cisty_nazev, v transakci vloží kategorii a vrátí id. `pridej_pomucku(nazev, kusy, kategorie_id=None)` ořízne název, vyžaduje nezáporný přesný int bez bool a v transakci zavolá hotovou zapis_pomucku. Neplatný text/počet je ValueError, chybný odkaz/duplicita IntegrityError. Nezakrývejte chyby.

prehled vrátí všechny pomůcky přes hotovou vsechny_pomucky. `pujc(pomucka_id, clen)` ořízne jméno, podmíněně odečte jeden dostupný kus a vloží výpůjčku v jedné transakci. Není-li pomůcka nebo dost kusů, ValueError bez změn. Při chybě INSERT se vrátí i odečet. Výsledkem úspěchu je id výpůjčky.

`vrat(vypujcka_id)` v jedné transakci vyhledá dosud aktivní výpůjčku, přičte kus pomůcce a označí vraceno=1. Vrátí True pouze při novém vrácení, pro neexistující či už vrácenou False. aktivni_vypujcky vrací (id_výpůjčky, název_pomůcky, člen) pro aktivní záznamy v pořadí id.

Veřejné operace vlastní celé transakce, i čtení může krátký kontext ukončit, protože Evidence vlastní celé spojení. Nepřidávejte cizí napůl hotové změny přímo do con. Čtěte popis ukazka.py/konzole.py, ale do podpůrných souborů není třeba zasahovat. Hlavní blok zůstává paměťovou ukázkou; skutečnou uloženou konzoli spouští spust_klub.py.
