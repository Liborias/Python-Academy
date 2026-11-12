# BMI tracker: projekt, prostředí a vlastní data

Python 3.12+, ověřeno 3.14.8/SQLite 3.53.1. Výpočet, databáze, CSV, záloha
ani unittest nepotřebují pip balíčky či internet. Pro okno 19 a závěrečné GUI
potřebujete systémový Tkinter a grafickou plochu. python -m tkinter otevře
zkušební okno; zavřete ho. Tkinter se neinstaluje přes pip. Windows: Python
s Tcl/Tk; Debian/Ubuntu: python3-tk pro správný Python; macOS: oficiální Python
s Tk. VS Code/VSCodium/PyCharm a terminál musí používat stejnou .venv.

Používáme fiktivní údaje. BMI = kg / (výška v metrech)^2 je orientační
ukazatel pro dospělé, nikoli posouzení individuálního zdraví či léčby.
Samotné BMI nerozliší svaly, tuk a další souvislosti. U dětí a těhotenství
se tato jednoduchá dospělá pásma nepoužívají stejným způsobem.

Tlačítko Spustit v 16–18/20 používá paměť nebo TemporaryDirectory.
V 19 otevře paměťovou ukázku se dvěma záznamy. Nic z toho není vaše trvalá
evidence; běžný webový běh používá dočasnou kopii. Okno běží u Pythonu,
nevykresluje se uvnitř webové stránky.

Uložte pracovní složku, dokončete reseni.py a ponechte vedle něj helpery.
V 19 a 20:
    python spust_bmi.py --help
    python spust_bmi.py

Help nevytváří okno ani DB. Druhý příkaz otevře vlastní prázdnou evidenci
bmi.sqlite3 vedle spouštěče, i když příkaz spustíte z jiného adresáře.
--db CESTA před příkazem vybere jiný soubor, rodičovská složka musí existovat.
Každá lekce má vlastní pracovní složku; pro pokračování s měřeními z předchozího
kroku použijte --db s absolutní cestou k jejímu bmi.sqlite3. Schéma 17–20
se nemění. Nepoužívejte soubory klub.sqlite3 ani krouzky.sqlite3.

V 19 formulář přijímá desetinnou čárku i tečku. Datum musí být přesné
RRRR-MM-DD a existovat v kalendáři. Prázdné Od/Do znamená bez meze, neprázdné
meze jsou včetně. Chyba zachová vstupy i předchozí přehled. Po uložení zmizí
hmotnost a poznámka, datum/výška zůstanou. Nový záznam může být mimo aktivní
období; pro úplný přehled klikněte Všechna měření.

Závěr 20 přidává příkazy:
    python spust_bmi.py export mereni.csv --od 2026-04-01 --do 2026-04-30
    python spust_bmi.py zaloha kopie.sqlite3
    python overeni.py

Export píše UTF-8 CSV se středníkem, hlavičkou a desetinnou tečkou pro čísla.
Uvozovky a nové řádky v poznámce ošetří csv.writer. Export vrací počet řádků
bez hlavičky. Není náhradou celé SQLite databáze. Záloha zachová celou DB
přes Connection.backup, funguje i z paměti a vrací absolutní Path cíle.
Existující cílový export/záloha se při úspěchu nahradí; běžící zdrojová DB
se cílem stát nesmí. Při chybě zůstane starý cíl, dočasný soubor se uklidí.

Overeni.py importuje studentův Tracker z reseni.py a provede tři vlastní
izolované unittest testy bez grafické plochy a bez změny vašich dat.
Export/záloha/--help v závěru nepotřebují Tkinter; grafické importy nastanou
teprve při spuštění okna. Návratový kód chyby CLI je 2, testy vracejí 0/1.
Model vlastní spojení a transakce, close jej zavře; nepřidávejte vlastní
napůl hotové změny přímo přes con. Před backup nemá být rozpracovaná transakce
mimo veřejné metody modelu. Projekt je pro jednoho místního uživatele.
