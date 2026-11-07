## Data a jejich zobrazení

Listbox zobrazuje řádky, ze kterých může uživatel vybírat. Nejde o běžný seznam Pythonu. V proměnné ukoly máme data, v seznam máme widget. Po změně dat funkce obnov vymaže řádky widgetu a znovu jej naplní aktuálním obsahem modelu. Díky tomu máme jedno místo, kde vzniká zobrazení.

V ukázce jsou úkoly Přečíst zadání, Vyzkoušet ukázku a znovu Přečíst zadání. Opakování je záměrné: dvě položky mohou mít stejný text, ale jiné místo v seznamu.

## Listbox se bere přímo z tkinter

```python
seznam = tk.Listbox(okno, selectmode="browse", exportselection=False)
seznam.insert(tk.END, "Přečíst zadání")
```

Listbox není součást ttk. Režim browse vybírá jednu položku. Exportselection=False ponechá výběr v seznamu i při přesunu fokusu do jiného widgetu; zejména na Linuxu by jinak mohl zaniknout při změně systémového výběru textu. Metoda insert s tk.END připojí řádek na konec. Delete(0, tk.END) odstraní všechny řádky. U Listbox jsou oba krajní indexy mazání zahrnuté a end označuje poslední řádek.

Příkazy `okno.rowconfigure(1, weight=1)` a sticky="nsew" přidělují seznamu i volnou výšku. Jde o obdobu již známého roztažení sloupce: n/s jsou horní a dolní okraj buňky.

## Nejprve ověříme výběr

```python
vyber = seznam.curselection()
if not vyber:
    zprava.configure(text="Nejprve vyberte úkol.")
    return
text = ukoly.pop(vyber[0])
```

Curselection vrací n-tici indexů, například (2,), nebo prázdnou n-tici (). Číslování začíná nulou. Teprve po ověření můžeme číst vyber[0]. Pop odstraní a zároveň vrátí prvek modelu na daném indexu. Remove(text) by hledalo první shodný text a u opakovaných názvů mohlo smazat jiný úkol.

Obnov nejdřív smaže všechny řádky, takže původní výběr zanikne. Po odebrání proto uživatel pro další akci znovu vybere položku. Nepoužíváme starý index uložený při vytváření okna.

## Váš úkol

Dokončete pridej a odeber. Přidání přečte aktuální Entry, odstraní pouze krajní mezery, prázdný text odmítne zprávou Napište název úkolu. Jinak přidá položku do modelu, obnoví Listbox, vyprázdní Entry a zobrazí Přidáno: název. Vnitřní mezery a diakritiku zachovejte, stejné názvy jsou povolené.

Odebrání bez výběru zobrazí Nejprve vyberte úkol. a data nezmění. S výběrem odstraní právě vybraný index, obnoví seznam a zobrazí Odebráno: název. Ponechte počáteční tři úkoly, rozložení i zprávu Přidejte nebo odeberte úkol.

Nejprve odeberte třetí položku: zůstat musí první dva řádky ve stejném pořadí. Potom přidejte vlastní úkol, odeberte další a zkontrolujte, že se dříve smazaný neobjevil znovu. Prázdný seznam i kliknutí bez výběru jsou běžné situace, ne důvod k pádu.
