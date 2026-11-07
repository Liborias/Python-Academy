## Kliknutí spustí funkci

Tlačítko je widget Button. Parametr command mu předá funkci, kterou má Tk zavolat při kliknutí. Takové předané funkci říkáme zpětné volání neboli callback. Základy funkcí už znáte; nové je, že okamžik volání určuje událost v okně.

Vytvoříme stavový popisek a dvě tlačítka. Potvrdit změní zprávu, Obnovit vrátí původní text. Počet součástí okna se při klikání nezvětšuje.

## Předat funkci, nebo ji hned zavolat?

```python
ttk.Button(okno, text="Potvrdit", command=potvrd)
```

potvrd bez závorek označuje funkci samotnou. Tk si ji uloží a zavolá později, až tlačítko použijeme. Při běžném command ji zavolá bez argumentů.

Zápis command=potvrd() by funkci provedl hned při vytváření tlačítka a do command vložil její návratovou hodnotu. Naše funkce vrací None, takže by navíc nezůstala připravená reakce na pozdější kliknutí. Sledujte proto stav už při otevření okna: má stále čekat na potvrzení.

## Měníme existující widget

```python
def potvrd():
    stav.configure(text="Akce potvrzena.")
```

configure změní vlastnost již vytvořeného popisku. Zkrácený zápis config dělá totéž. Nepotřebujeme další Label při každém kliknutí. Tk si změnu při zpracování událostí překreslí.

Funkce čte odkaz na existující stav a volá jeho metodu. Proměnnou stav nepřiřazuje znovu, proto nepotřebuje global. Popisek musí existovat před prvním voláním funkce. V ukázce je vytvořený před funkcemi a tlačítky.

## Smyčka má zůstat volná pro události

Funkce tlačítka má dokončit svou krátkou práci a vrátit řízení Tk. Dlouhé while nebo sleep uvnitř funkce by okno zablokovaly. O načítání pomalých API bez zamrznutí bude samostatná pozdější část kurzu.

## Váš úkol

Ponechte připravené okno a popisek s počátečním textem Čekám na potvrzení. Doplňte funkce a připojte je k tlačítkům:

- Potvrdit nastaví přesně Akce potvrzena.
- Obnovit vrátí přesně Čekám na potvrzení.

Použijte tentýž popisek. Obě tlačítka mají fungovat i při opakovaném klikání, v libovolném pořadí. Ke změně zprávy má dojít až po kliknutí. mainloop zůstává jeden, na konci programu.

Spusťte ukázku a zkuste Potvrdit dvakrát, potom Obnovit a znovu Potvrdit. Před vlastním řešením vysvětlete rozdíl mezi jménem funkce a voláním se závorkami.
