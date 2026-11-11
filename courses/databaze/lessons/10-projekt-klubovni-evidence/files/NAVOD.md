# Databáze 6–10: dotazy, vazby a klubovní evidence

Python 3.12+, ověřeno Python 3.14.8/SQLite 3.53.1. Vše ze standardní knihovny,
bez instalace dalších balíčků nebo databázového serveru. Ve VS Code/VSCodium/
PyCharm a terminálu vyberte stejnou .venv. python reseni.py provede ukázku.

Ukázky pracují v paměti, nevytvářejí vaši trvalou evidenci. Běžný webový běh
je také dočasný. Pomocné .py soubory ponechte spolu s reseni.py. Pro vlastní
soubor nejprve uložte pracovní složku a otevřete ji v editoru.

Lekce 6–9 dostávají otevřené spojení od volajícího; kromě spojeni_s_vazbami
a zkus_typy ho nevytvářejí, nezavírají ani neukončují cizí transakci.
Cizí klíče se zapínají při autocommit=True, teprve pak přejdeme na False.
Nové relační schéma má kategorie, pomucky s kategorie_id a normalizované
vypujcky s pomucka_id. Staré soubory z 1–5 nejsou automaticky migrované.

Projekt 10 má spust_klub.py a konzolové příkazy. Po dokončení Evidence:
    python spust_klub.py --help
    python spust_klub.py kategorie "Sport"
    python spust_klub.py pomucka "Míč" 2 --kategorie 1
    python spust_klub.py prehled
    python spust_klub.py pujcit 1 "Žofie"
    python spust_klub.py vypujcky
    python spust_klub.py vratit 1

Příkazy používají klub.sqlite3 vedle skriptu. Čísla ID převezměte ze svého
skutečného výstupu. Volba --db CESTA před názvem příkazu určí jiný soubor,
rodičovský adresář už musí existovat. Bez příkazu se vypíše přehled.
Spust_klub.py importuje vaši Evidence z reseni.py, ne hotové cizí řešení.
Ukázka v aplikaci je naopak krátký paměťový pokus, aby neničila trvalá data.

Evidence vlastní spojení i transakce. Neměňte její con přímo mimo řízený pokus.
Půjčení ubere jeden dostupný kus a vytvoří výpůjčku v jediném celku, vrácení
přičte jeden kus nejvýše jednou. Kusy znamenají aktuálně dostupné množství.
Historie brání smazání pomůcky i po vrácení, smazaná kategorie pouze uvolní
zařazení pomůcky. Nejde o síťový server ani rozhraní pro souběžnou obsluhu
mnoha procesy; automatické opakování SQLITE_BUSY zde neřešíme.
