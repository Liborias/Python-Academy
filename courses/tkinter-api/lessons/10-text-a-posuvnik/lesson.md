## Text na více řádcích

Entry je jednořádkové pole. Pro delší poznámku použijeme tk.Text. V ukázce dostane třicet řádků, které můžeme upravovat i posouvat. Wrap="word" zalamuje dlouhý řádek na hranicích slov podle šířky okna. Zalomení na obrazovce však do dat nepřidává znak nového řádku.

Výchozí obsah vznikne v cyklu a spojí se přes "\n".join(radky). Znak \n označuje nový řádek v uloženém textu. Samotné automatické zalomení dlouhé věty se při počítání řádků neuplatní.

## Text používá jiné indexy než Listbox

```python
obsah = text.get("1.0", "end-1c")
```

Index "1.0" znamená první řádek a nultý znak v něm. Řádky Text začínají jedničkou, sloupce nulou. "end" leží za povinným koncovým novým řádkem, který Text udržuje i v prázdném widgetu. "end-1c" znamená o jeden znak před koncem a tento automatický znak vynechá. Get čte do druhého indexu bez jeho zahrnutí, na rozdíl od intervalů Listbox.

Nový obsah lze vložit přes insert("1.0", obsah). Delete("1.0", "end") vyprázdní poznámku; automatický koncový nový řádek si widget zachová. Pro prázdnou poznámku proto get("1.0", "end-1c") vrátí prázdný text.

## Posuvník potřebuje dvě propojení

```python
posuvnik = ttk.Scrollbar(okno, orient="vertical", command=text.yview)
text.configure(yscrollcommand=posuvnik.set)
```

První vazba posílá pohyb jezdce do textu. Yview je metoda pro svislý výřez. Předáváme ji bez závorek, aby ji Tk zavolal až podle uživatele. Druhá vazba hlásí aktuální polohu z textu zpět do posuvníku. Set dostává začátek a konec viditelné části jako podíly od 0 do 1. Jen jedna vazba nestačí: text a jezdec by se mohly rozcházet při psaní, klávesnici nebo změně velikosti.

Scrollbar umístíme vedle Text a necháme jej vyplnit svislou výšku přes sticky="ns". Tk má také vodorovné posouvání, které dnes nepoužíváme.

## Váš úkol

Propojte připravený svislý Scrollbar s Text oběma směry a dokončete spocitej. Tlačítko Spočítat přečte aktuální obsah bez automatického koncového znaku a zobrazí Znaků: N; řádků: R. Znak nového řádku uvnitř obsahu se počítá jako jeden znak. Prázdný obsah má 0 řádků; jinak je počet řádků počet znaků \n plus jedna. Ručně napsaný nový řádek na konci tedy založí další prázdný řádek.

Příklady: A má 1 znak a 1 řádek; A následované Enterem a B má 3 znaky a 2 řádky; A, Enter, B, Enter má 4 znaky a 3 řádky. Samotné psaní ani posun souhrn nepřepočítává, až tlačítko. Obsah při počítání neměňte.

Ponechte počátečních třicet řádků a zprávu Text můžete upravit. Vyzkoušejte jezdec dolů i nahoru, upravte text a potom vše smažte. Zúžte okno: vizuálních zalomení přibude, ale počet znaků \n v obsahu zůstane stejný.
