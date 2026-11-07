## Hodnoty propojené s ovládáním

Obyčejná proměnná Pythonu sama o sobě nezmění stav zaškrtávátka. Tk má vlastní propojené proměnné: StringVar uchovává text, IntVar celé číslo. Vytvoříme je po hlavním okně a okno předáme jako rodiče:

```python
krehke = tk.IntVar(okno, value=0)
doprava = tk.StringVar(okno, value="odber")
```

`value` určí počáteční hodnotu. Metoda `get()` přečte aktuální obsah, `set(nova_hodnota)` jej změní a propojené widgety změnu převezmou. Zápis `doprava = "kuryr"` by místo toho přepsal proměnnou Pythonu a ztratil náš odkaz na StringVar. Příklady nastavování z kódu zkoušejte přes `doprava.set("kuryr")`.

## Nezávislá volba a skupina možností

Checkbutton je zaškrtávátko pro nezávislé ano/ne. `variable=krehke, onvalue=1, offvalue=0` jej propojí s IntVar. Kliknutí přepne aktuální hodnotu: 0 znamená ne, 1 ano. Parametr je variable, nikoli textvariable používaný u textu popisku.

Radiobutton je přepínač ve skupině. Dvě tlačítka budou sdílet tutéž proměnnou doprava, ale každé má jiné value:

```python
ttk.Radiobutton(okno, text="Osobní odběr", variable=doprava, value="odber")
ttk.Radiobutton(okno, text="Kurýr", variable=doprava, value="kuryr")
```

Widgety ještě umístíme přes pack. Když uživatel vybere Kurýr, hodnota se změní na kuryr a Osobní odběr přestane být vybraný. Pokud by měly dva různé StringVar, nebyla by to jedna skupina. Text je popisek pro člověka, value je hodnota pro program.

## Potvrzení přečte aktuální nastavení

Tlačítko Zobrazit volby teprve sestaví výsledek. Neodesílá zásilku a nic nerezervuje. Podle `doprava.get()` připravíme název odběr nebo kurýr, podle `krehke.get()` ano/ne. Výsledek bude například Doprava: kurýr; křehké: ano.

Změna přepínače okamžitě mění propojenou hodnotu. Náš výsledný popisek se však aktualizuje až po tlačítku, protože k volbám nepřidáváme žádný vlastní command pro přepočet. Jde o dvě různé věci: uložené nastavení a jeho poslední potvrzené zobrazení.

## Váš úkol

Vytvořte jedno zaškrtávátko Křehký obsah (výchozí ne), dva přepínače Osobní odběr a Kurýr ve společné skupině (výchozí odběr) a tlačítko Zobrazit volby. Použijte IntVar pro křehkost a StringVar pro dopravu. Ponechte výchozí zprávu Zvolte možnosti a potvrďte.

Po potvrzení zobrazte přesně Doprava: odběr; křehké: ne. nebo odpovídající kombinaci s kurýr a ano. Měňte tentýž popisek a čtěte hodnoty při každém potvrzení. Zkuste všechny čtyři kombinace a přepněte Kurýr zpět na Osobní odběr. Opakovaný klik na již vybraný Radiobutton jej nesmí odškrtnout; Checkbutton se naopak přepíná tam i zpět.
