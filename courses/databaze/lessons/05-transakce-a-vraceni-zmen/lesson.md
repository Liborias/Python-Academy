## Několik změn tvoří jednu věc

Přesun kusů ze zdroje do cíle má dvě změny. Kdyby první zůstala uložená a druhá selhala, sklad by přišel o kusy. Transakce stanoví hranici: buď se potvrdí celý celek, nebo se jeho změny vrátí.

V této lekci vytváří volající spojení s autocommit=False. Python udržuje otevřenou transakci; commit ji potvrdí a začne další, rollback ji vrátí a také začne novou. Proto samotné in_transaction nemusí po commit přejít na False. Trvalý výsledek si ověříme druhým spojením k souboru.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=False)) as con:
    con.execute('CREATE TABLE pokus (hodnota INTEGER)')
    con.commit()
    con.execute('INSERT INTO pokus VALUES (7)')
    con.rollback()
    print('Po vrácení:', con.execute('SELECT COUNT(*) FROM pokus').fetchone()[0])
```

Výstup je 0. Schéma jsme nejdřív potvrdili, proto rollback další změny neodstranil samotnou tabulku. `closing` nakonec spojení zavře; sám nenahrazuje commit.

## Co přesně znamená with con

Uvnitř kontextu provedeme několik příkazů. Úspěšný odchod potvrdí celou transakci; výjimka ji vrátí a pokračuje dál k volajícímu. Spojení zůstane otevřené. Při autocommit=True nemá tento kontext stejnou ochranu pro celou dávku, proto tento režim v úkolech výslovně odmítáme.

Return není chyba. Pokud už odečteme kusy a pak jen vrátíme False kvůli chybějícímu cíli, kontext by se uzavřel jako úspěšný. Tady musí vzniknout výjimka, která vrátí první část přesunu.

## Kdo vlastní hranici transakce

V lekcích 2–4 funkce pouze pracovaly s předaným con a samy nepotvrzovaly. Nyní tvoříme vyšší operace, které vlastní celý celek včetně commit/rollback. Volající před jejich voláním nesmí mít další nepotvrzenou práci. Nejde o vnořené transakce; ty vyžadují další návrh, například savepoint.

Podklady poskytují vyzaduj_transakce a kladny_pocet. SQL hodnoty stále předáváme jako parametry. Podmíněný UPDATE kontroluje dostupný počet přímo ve WHERE; záznam mění jen při dostatku kusů.

## Zkouška souboru bez cizích dat

Hlavní ukázky vytvářejí soubor v TemporaryDirectory, na konci jej uklidí. Druhé spojení čte jen potvrzený stav. Pro vlastní trvalou evidenci použijte uloženou pracovní složku a svoji cestu místo dočasné složky. Běžný běh v prohlížeči pracuje s dočasnou kopií.

## Váš úkol

Vytvořte **uloz_davku(con, radky)**. Vyžaduje autocommit=False, jinak ValueError ještě před změnou. V jedné transakci parametrizovaně vloží dvojice (nazev, kusy), při úspěchu vše potvrdí a vrátí None. Při chybě se vrátí celá dávka a původní výjimka se předá.

Použijte například vyzaduj_transakce z podklady.py a with con kolem executemany. Prázdná dávka i generátor jsou platné. Spojení nezavírejte. Funkce zde vlastní hranici celé transakce: před voláním nesmí mít volající jiné nepotvrzené změny. Jinak by se potvrzovaly či vracely spolu s ní.
