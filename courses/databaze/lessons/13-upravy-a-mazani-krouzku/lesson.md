## Vybraná položka má dvě čísla

Index 0 v Listboxu znamená první viditelný řádek. Databázové id může být 37. Po smazání prvního kroužku se ostatní id nepřečíslují. Vybrané id proto vezmeme z self.data podle indexu výběru; nepočítáme index + 1 a nevylušťujeme ho ze zobrazovaného názvu.

```python
# Na místě 0 může být databázový klíč 37.
radky = [(37, 'Robotika', 2), (85, 'Šachy', 3)]
vybrany_index = 0
print('Databázové id:', radky[vybrany_index][0])
```

Dědičnost nám ponechá model a formulář z předchozích kroků. `formular.py` je přesná dřívější Aplikace, Model dědí od EvidenceKrouzku. `super()` volá hotové chování rodiče; nový kód doplní pouze rozdíly.

## Co znamená uložit a smazat

UPDATE mění řádek podle id. Rowcount 1 znamená nalezený řádek, i když jsme zadali stejné hodnoty. Chybějící id vrátí False. Název a kladnou kapacitu ověřujeme stejně jako při přidání; kapacita navíc nesmí být menší než už existující počet přihlášek.

DELETE odstraní zvolený kroužek ihned po kliknutí. Neprovádíme hromadné mazání. Pokud kroužek používají přihlášky, RESTRICT vyvolá IntegrityError a záznam zůstane. V dalších lekcích tak nejprve odhlásíme členy. Každá datová změna je celá transakce; chyba zachová také původní název.

Po úspěšné změně obnovíme seznam a zrušíme výběr; uživatel znovu vědomě vybere další řádek. Nový formulář pouze zruší výběr a vyčistí pole, nevytváří záznam v DB.

## Váš úkol

Doplňte Model.uprav a Model.smaz, Aplikace.vybrane_id, vyber, uprav a smaz. `uprav(ident, nazev, kapacita)` v modelu normalizuje název/ověří kapacitu, v transakci porovná počet přihlášek s kapacitou, provede parametrizovaný UPDATE a vrátí True/False. `smaz(ident)` provede parametrizovaný DELETE a vrátí True pouze při novém smazání. Chyby omezení nepohlcuje.

Vybrane_id vrátí id ze self.data, případně None. Vyber naplní název a kapacitu z vybrané n-tice. GUI uprav/smaz bez výběru oznámí „Nejprve vyberte kroužek.“ Při ValueError ukáže vysvětlení, při duplicitním názvu hlášku z lekce 12; při chráněném mazání „Kroužek nelze smazat: odhlaste členy.“ Vstupy při chybě zachová.

Při úspěchu zavolá obnov a novy, stav bude „Změny uloženy.“ nebo „Kroužek smazán.“ Chybějící řádek pro update oznámí „Kroužek už neexistuje. Obnovte seznam.“, při delete „Kroužek už neexistuje.“ Zbytek včetně spouštěče a Nového formuláře zůstává připravený. Zkuste smazat první řádek a upravit ten, který byl původně druhý.
