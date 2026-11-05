## Spojíme díly do hotové hry

Máme model, růst, kolize, stav partie, kreslení i šipky. Nyní přidáme společnou obsluhu a restart klávesou **Enter**. Výsledkem bude hratelná varianta Snake s průchozími okraji, červenou potravou, žlutou hlavou, zeleným tělem, skóre a zprávou o prohře nebo výhře.

Každá lekce projektu má vlastní funkční podklady. Pomocné soubory obsahují předchozí vzorová řešení; vaše rozpracované úkoly se nepřepisují. Při práci v externím editoru ponechte všechny připravené soubory vedle reseni.py. V aplikaci je připraví uložení do pracovní složky. Nic dalšího se neinstaluje přes pip, potřebujeme však grafické prostředí a Tkinter stejně jako v lekci 30.

## Kdo co dělá

`Had` a jeho odvozené třídy řeší tělo a pohyb. `Partie` uchovává potravu, skóre a výsledek. `RizenaHra` poskytne osvědčené ovládání s jednou čekající zatáčkou. Nová `SnakeHra` tyto části propojí a řídí časovač celé partie.

Připravený had_panel.py se stará o obrázek: pro tělo využívá dřívější kreslení, pro potravu druhé pero a pro rámeček i text třetí. Každá část maže pouze svou starou kresbu. Rámeček označuje hranici **průchozí** plochy. Skóre se píše nad ní, nápověda nebo výsledek pod ní. `write(...)` vypisuje text do okna; align a font určují zarovnání a vzhled.

Okno má také minimální šířku a výšku, aby zůstaly čitelné výsledky i při zkoušení velmi malé herní plochy. To nezvětšuje počet buněk, jen volné místo kolem rámečku.

Metoda `obnov()` připraví celý obrázek z aktuální Partie a zavolá update. Je hotová stejně jako konstruktor a připojení kláves. Vy doplníte restart, plánování a tik.

## Restart je nový stav, nikoli další souběžná hra

`self.zacatek` je vlastní kopie počátečního těla. Při restartu z něj vytvoříme novou Partii se stejnými rozměry a funkcí výběru. Tím se obnoví délka, směr doprava, skóre nula a nová potrava. `self.had` přesměrujeme na hada této partie a `self.cekajici` vyprázdníme.

Restart má také zvýšit `self.generace` o jedna, nastavit spusteno na True, obnovit první snímek a zavolat naplanuj. Neprovádí okamžitý krok. Opakované spust nic nepřidává; Enter naopak výslovně žádá novou partii i během hraní.

## Co se stane se starým časovačem

Turtle nenabízí v tomto rozhraní rušení konkrétního časovače. Jeho již naplánované volání proto může po restartu ještě přijít. Pokud by se chovalo jako běžný tik, rozehrálo by druhý řetězec a hra by zrychlovala.

Každý naplánovaný callback si proto zapamatuje **číslo své generace**. Staré volání po restartu zjistí, že už nepatří do aktuální hry, a skončí bez pohybu, kreslení i dalšího plánování.

```python
generace = self.generace
self.okno.ontimer(lambda: self.tik_generace(generace), self.interval)
```

`lambda` je krátká funkce bez jména. Zde nemá žádné parametry (mezi lambda a dvojtečkou nic není) a její tělo zavolá tik_generace s uloženým číslem. Samotný zápis funkci nespustí — předá ji časovači. Proto má stejnou roli jako dřívější předání self.tik, ale nyní navíc nese údaj o generaci.

Lokální proměnná generace vznikne při každém volání naplanuj znovu a callback si ji uchová. Důležitý je tento konkrétní tehdejší údaj. Zápis `lambda: self.tik_generace(self.generace)` by číslo četl až později a starý časovač by se vydával za nový. Hotová metoda tik_generace zavolá tik pouze při shodě uloženého a aktuálního čísla.

Naplanuj zakládá právě jeden časovač, a to pouze při stavu hra. Při prohře nebo plné ploše už nové volání nevzniká.

Také během update může okno zpracovat Enter. Před obnovením snímku si proto v restart i v tik uložíme tehdejší generaci. Po návratu z obnov zavoláme naplanuj jen tehdy, pokud se generace nezměnila. Jinak už novější restart zařídil vlastní pokračování. Tím se nevytvoří druhý řetězec ani při restartu přímo během překreslování.

## Jeden tik hotové hry

Ukončená partie se už nehýbe. Jinak nejprve použijeme případný čekající směr a vyprázdníme ho. Pak právě jednou zavoláme `self.partie.krok()`, obnovíme obrázek a požádáme naplanuj o pokračování. Tato metoda už sama pozná, zda hra skončila.

Tentokrát nepřipojujeme starý `super().tik()`: ten pohyboval samotným hadem bez potravy a stavu Partie. Obsluhu kroku jsme záměrně nahradili pro celé nové pravidlo. Ze základní třídy dál využíváme konstruktor a ovládání šipek. Volání starého tiku navíc by znamenalo druhý pohyb a další časovač.

## Váš úkol a vyzkoušení

Doplňte `restart`, `naplanuj` a `tik` podle výkladu. Ostatní metody a hlavní blok jsou připravené. Po spuštění okno aktivujte kliknutím; šipky mění směr, krátký stisk a uvolnění Enter obnoví hru. Zavřením okna nebo tlačítkem Stop v aplikaci program ukončíte.

1. Snězte červenou potravu: délka má vzrůst o jeden článek a skóre o 10.
2. Projeďte okrajem: had se objeví na druhé straně.
3. Po růstu se zatočte do těla: objeví se Konec hry a pohyb se zastaví.
4. Zmáčkněte Enter opakovaně během pohybu i po prohře. Nový had má startovní délku, skóre nula a nezrychluje.
5. Pro malé zkušební hřiště změňte rozměry při přípravě okna **i** při konstrukci SnakeHra a zvolte počáteční buňky uvnitř. Při zaplnění celé plochy hra ohlásí výhru a dál neplánuje pohyb.

Pokud šipky posouvají webovou stránku, fokus zůstal v prohlížeči. Kreslení se odehrává v samostatném okně na počítači s Pythonem, nikoli uvnitř stránky.
