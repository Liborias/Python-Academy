## Hra nemusí zaměstnat Python nekonečným cyklem

Model už umí krok a zobrazení umí snímek. Nyní je propojíme třídou **Hra**. Její instance si pamatuje okno, hada, pero a interval mezi kroky.

Soubor `had_model.py` navazuje na lekci 29 a `had_pohled.py` obsahuje vzorové kreslení z lekce 30. Jejich import pouze zpřístupní třídu a funkce. Díky hlavnímu bloku se při importu neotevírají další okna.

## Co je funkce předaná jako hodnota

```python
self.okno.ontimer(self.tik, self.interval)
```

`ontimer` naplánuje jednorázové zavolání funkce. Interval se zadává v milisekundách: 160 znamená přibližně 0,16 sekundy. Není to záruka přesné frekvence; záleží i na kreslení a vytížení počítače.

Zápis `self.tik` **bez závorek** předá metodu svázanou s tímto objektem Hra. Časovač ji později zavolá bez dalších argumentů; Python jí doplní self. Zápis `self.tik()` by metodu spustil okamžitě a předal časovači její návratovou hodnotu. Opakované okamžité volání by navíc mohlo skončit rekurzí místo animace.

## Jeden tik znamená přesně jeden krok

Tělo metody `tik` má toto pořadí:

1. `self.had.krok()` změní model o jednu buňku.
2. `vykresli(self.had, self.pero)` připraví nový obrázek z aktuálního stavu.
3. `self.okno.update()` zobrazí připravený snímek.
4. `self.okno.ontimer(self.tik, self.interval)` naplánuje právě jeden další tik.

Metoda se pak vrátí. Po dobu čekání může okno reagovat na přesun, zavření a později na klávesnici. Kdyby kreslení předcházelo změně modelu, viděli bychom starý stav.

Jednorázový časovač sám neopakuje volání: další tik musí naplánovat právě končící metoda. Když ho naplánujeme dvakrát, začne se vytvářet více souběžných řetězců a hra zrychlí.

## První snímek a bezpečné spuštění

Metoda `spust` nejdříve ukáže **počáteční** stav bez pohybu, provede update a naplánuje první tik. Nevolá tik přímo. Před prvním intervalem tak had zůstává na své startovní buňce.

Příznak `self.spusteno` začíná jako False. Po prvním spuštění ho přepneme na True. Jestliže někdo zavolá spust znovu, metoda se hned vrátí a nic dalšího nenaplánuje. Zatím jde o jednorázový start, nikoli tlačítko restart nebo pauza; tyto části přijdou později.

Nepoužívejte zde `while True` ani `time.sleep`. Tento program už má smyčku událostí v `okno.mainloop()`. Vlastní nekončící práce v hlavním vlákně by bránila obsluze okna.

## Co uvidíte po spuštění

Žlutá hlava se posouvá doprava a dva zelené články ji následují. Na pravém okraji projde na levý, jak už umí model. Otisky se před každým snímkem mažou, takže po ploše nezůstává čára.

Změňte v hlavním bloku `hra = Hra(okno, had, pero, interval=400)` a znovu spusťte program. Nový interval znamená čekání přibližně 0,4 sekundy mezi kroky. Zatím se neovládá klávesnicí a nesbírá potravu. Okno zavřete křížkem nebo použijte Stop.

## Váš úkol

Doplňte `Hra.spust` a `Hra.tik` podle uvedeného pořadí. Konstruktor a hlavní blok jsou hotové. Použijte připravenou funkci vykresli a čtěte atributy této instance, včetně jejího intervalu.

Opakované spust nesmí znovu kreslit, posunout hada nebo přidat časovač. Každé pozdější volání tiku má udělat jeden krok a založit právě jeden další časovač. Předávejte volatelnou metodu, která pracuje s tímto objektem. Kontrola používá také jiné intervaly a dva nezávislé objekty, nejen výchozí ukázku.
