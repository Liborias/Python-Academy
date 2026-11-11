## Skládáme nabídku, let, pauzu a výsledek

Kolo vlastní pravidla mise, Hra řídí jejich životní cyklus. Použijeme skutečný ZasobnikRezimu z lekce 20: jen vršek dostane vstup a čas, ale při pauze se vykreslí i podklad. Návrat tak obnoví stejný rozehraný objekt.

Sceny.py dodává Menu, Let, PauzaLetu a Vysledek se jmeno a rozhraním zpracuj/update/kresli. Let vlastní kolo a smer; update(dt) předá uložený směr do kola. Ostatní režimy jeho čas neposouvají. Renderer používá banku fontů a skutečné kreslení vrstev. Nová souběžná smyčka nevzniká.

```python
vrstvy = ['let', 'pauza']
print('Vstup a čas dostává:', vrstvy[-1])
vrstvy.pop()
print('Po pokračování:', vrstvy[-1])
```

Ve hře místo názvů držíme objekty. Pauza zachová let, restart naopak vytvoří nové Kolo(seed) a nový zásobník. Staré skupiny ani výsledky neměníme; jiné proměnné na ně mohou stále odkazovat.

## Váš úkol: Hra(seed=23)

Uložte seed, bezi=True, kolo=None a zasobnik=ZasobnikRezimu(Menu()). Čtená vlastnost **stav** vrací jmeno aktuálního režimu. Nabídka ještě nemá kolo. **novy_let()** nejprve vytvoří Kolo(self.seed), pak je uloží a vytvoří nový zásobník s Let(novy). Chyba konstrukce ponechá starou hru beze změny.

**zpracuj(udalost)** vždy přijme QUIT, jinak po bezi=False nic nepředá. Za běhu KEYDOWN Escape také ukončí program. Ostatní události předá zásobníku a zpracuje akci:

- 'start': novy_let; nabídka ji vrací na Mezerník, ostatní na R.
- 'nabidka': kolo=None a nový zásobník s Menu; výsledek ji vrací na Mezerník.
- 'pauza': vloží PauzaLetu na původní zásobník.
- 'zpet': odebere jen vršek, podklad zůstane stejný.
- None či neznámá akce nic nemění, KEYUP není další stisk.

**update(smer,dt)** po ukončení nic nedělá. Ve stavu hra uloží vlastní Vector2 kopii směru do aktuálního Let.smer. Za běhu pak zavolá zasobnik.update(dt). Pokud právě hrané kolo skončilo, nahradí zásobník jediným Vysledek(self.kolo), model zachová. **kresli(plocha)** předává kreslení zásobníku i pro poslední snímek po zavření.

## Vyzkoušejte celou misi

V aktivním herním okně Mezerník spustí let, šipky/WASD pohyb, P pauzu/pokračování, R nový let a Esc/křížek konec. Výsledek nabízí R nebo Mezerník do nabídky. R v nabídce nic nedělá. Vyzkoušejte vyčerpání štítu při čekání, obnovu mimo zónu, restart v pauze, výhru se šesti daty a konec bez jejich dostatku. Pauza zastaví i čas vlny, frontu a dobíjení; po návratu se čekání nedohání.

Seed=23 opakuje začátek nového pokusu, None zvolí novou posloupnost. Běžné zavření uloží droni.png, Stop uložení nezaručuje. Odkrytí řešení nepřepisuje práci. Další modul přidá vlastní testy, JSON výsledky a předání hry.
