## Formulář ovládaný klávesnicí

Kliknutí na tlačítko už umíme. Teď dovolíme uživateli po napsání jména stisknout Enter. Fokus označuje widget, který právě přijímá klávesové události. `jmeno.focus_set()` požádá Tk, aby po aktivaci okna směroval psaní do vstupu. Uživatel může fokus později přesunout myší nebo Tabem. Operační systém může vyžadovat nejprve aktivaci celého okna.

Program nemá při zobrazení sám pozdravit. Počáteční zpráva je Zadejte jméno. Čtení aktuálního vstupu a odstranění krajních mezer nastane až po tlačítku nebo Enteru.

## Bind předá objekt události

```python
def pozdrav(udalost=None):
    text = jmeno.get().strip()
    # Zde se nastaví výsledek.

jmeno.bind("<Return>", pozdrav)
```

`bind` připojí funkci k události widgetu. Řetězec `<Return>` je Tk název klávesy Enter. Funkci opět předáváme bez závorek. Na rozdíl od command v tlačítku jí bind předá jeden argument: objekt události. Obsahuje například `udalost.widget`, odkaz na widget, kde událost vznikla.

Výchozí hodnota `udalost=None` umožní použít stejnou funkci oběma způsoby: tlačítko ji zavolá bez argumentů a použije se None, bind dodá objekt. Funkce zde obsah události nepotřebuje. Kdyby neměla parametr ani jiný obal pro bind, Enter by vyvolal TypeError. Samotné tlačítko by přitom mohlo fungovat.

Vazba je na vstupu, proto se týká Enteru při psaní jména. `okno.bind` je širší vazba na hlavní okno a může reagovat také na události jeho potomků. Pro tento úkol stačí cílená vazba na Entry. Návratový text `"break"` z handleru zastaví další zpracování téže události; v jednoduchém formuláři není nutný.

## Jedna akce, dvě cesty

Tlačítko má `command=pozdrav`. Vstup má `bind("<Return>", pozdrav)` a po vytvoření dostane `focus_set()`. Obě cesty mění tentýž výsledný popisek: prázdný či jen mezerový text dá Zadejte jméno., ostatní Ahoj, jméno! Zachovejte diakritiku a mezery uvnitř jména.

Nepište dvě různá pravidla pro tlačítko a Enter. Dvě drobné obalové funkce, které obě zavolají společnou akci, jsou také správná varianta. Hlavní smyčka zůstává jediná.

## Váš úkol

V připraveném formuláři dokončete funkci pozdrav tak, aby přijímala nepovinný argument události. Připojte ji k tlačítku Pozdravit i Enteru ve vstupu. Po vytvoření pole mu předejte fokus. Rozložení můžete ponechat.

Zkuste po aktivaci okna rovnou psát bez kliknutí do pole. Střídejte tlačítko a Enter, po prvním pozdravu změňte jméno a zkuste několik mezer. Samotné psaní zprávu nemění. Při chybě si všimněte rozdílu mezi funkcí volanou bez argumentů a funkcí, které Tk předává událost.
