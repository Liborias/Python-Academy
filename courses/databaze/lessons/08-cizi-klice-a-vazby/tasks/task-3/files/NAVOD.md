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


Navazující projekt propojí toto schéma s konzolovou obsluhou.
