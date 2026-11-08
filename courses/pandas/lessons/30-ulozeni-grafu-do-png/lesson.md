## Obrázek musí jít znovu vytvořit

Graf je výstup programu, ne náhrada zdrojových dat. Ponechte si skript, vstupy i pravidla, kterými vznikl. Teď uložíme konkrétní Figure a ověříme, co skutečně vzniklo. Předané fig je důležité: při práci s více obrázky by globální plt.savefig mohlo uložit jiný „aktuální“ obrázek.

```python
from pathlib import Path
from matplotlib.figure import Figure
fig = Figure(figsize=(6, 4), layout="constrained")
ax = fig.subplots()
ax.plot([1, 2, 3], [8, 11, 9], marker="o")
ax.set(title="Cvičné teploty", xlabel="Den", ylabel="Teplota (°C)")
cesta = Path("teploty.png")
fig.savefig(cesta, format="png", dpi=120)
print("Uloženo:", cesta)
```

Path představuje cestu k souboru. Relativní cesta se vyhodnotí vůči pracovní složce procesu; pod stejným názvem se soubor při dalším uložení přepíše. Format="png" výslovně určuje formát i tehdy, když cesta nemá obvyklou příponu. Pro náhled aplikace používejte příponu .png. Savefig uloží obrázek, samo neotevírá okno ani jej neposílá na síť.

## Palce, DPI a pixely

Šířka/výška Figure jsou v palcích. DPI je počet obrazových bodů na palec. Bez těsného ořezu tedy 6 × 4 palce při DPI 100 dává 600 × 400 pixelů; při DPI 200 dvojnásobnou šířku i výšku, 1200 × 800. Pixelů je čtyřikrát více, velikost komprimovaného souboru však nemusí být přesně čtyřnásobná.

`fig.set_size_inches(sirka, vyska)` změní rozměr Figure. Parametr dpi při savefig mění rozlišení daného exportu a po uložení nemá přepsat původní fig.dpi. Více DPI nepřidá nová měření ani neudělá z nečitelných popisků správný výklad. Zkontrolujte také rozměr při běžném čtení, kontrast a jednotky.

## Pozadí a rámeček

`fig.savefig(cesta, format="png", dpi=100, transparent=True)` uloží průhledné pozadí Figure i Axes. Čáry a text zůstávají. Výsledné PNG má alfa kanál: průhlednost dovolí vložení na jiné pozadí, ale černé popisky pak mohou na tmavém podkladu zaniknout. V aplikaci náhled podkládáme bílou; skutečnou průhlednost má stažený soubor. Původní barvy pozadí Figure se po exportu zachovají.

`bbox_inches="tight"` při ukládání vybere rámeček podle vykresleného obsahu, včetně viditelných popisků či textu mimo obvyklou plochu. `pad_inches=0.1` kolem něj nechá desetinu palce. Tento rámeček může být menší i větší než původní plátno, takže už neplatí přesné figsize × DPI pro rozměr celého PNG. Constrained layout a tight export řeší související, ale různé věci: rozmístění prvků uvnitř obrázku a rozsah ukládaného rámečku. Výsledek vždy otevřete a prohlédněte.

## Složka pro dvě velikosti

`Path(slozka).mkdir(parents=True, exist_ok=True)` vytvoří složku včetně případných rodičů; nevadí, pokud už existuje. Operátor `/` u Path připojuje část cesty, například `slozka / "nahled.png"`. Do stejné složky uložíme náhled s DPI 100 a větší verzi s DPI 200. Jiné soubory nemažeme. Nový běh může přepsat právě tyto dva pojmenované výstupy, proto jim zvolíme srozumitelné názvy.

## Aplikace, editor a provoz bez okna

V prohlížeči po běhu uvidíte PNG a odkaz Stáhnout PNG. Náhledy platí pro aktuální běh; po obnovení stránky je znovu vytvoříte spuštěním skriptu. Pro trvalý obrázek použijte stažení nebo běh uloženého souboru v editoru. Automatická kontrola vytváří vlastní dočasné obrázky a není zobrazením vašeho právě spuštěného grafu.

Aplikace pro tyto lekce používá neokenní vykreslování Agg a načítá PNG. Samotné skripty vytvářejí Figure přímo a ukládají soubory, proto nepotřebují plt.show ani grafickou plochu. Pro jiné skripty používající pyplot lze v PowerShellu před spuštěním nastavit `$env:MPLBACKEND = "Agg"`, na macOS/Linuxu použít `MPLBACKEND=Agg python graf.py`. Agg umí obrázek vykreslit do souboru; nemá vlastní interaktivní okno. Zdejší skripty fungují bez tohoto ručního nastavení také.

Náhled aplikace podporuje nejvýše šest PNG, každý do 2 MB a 8 milionů pixelů, celkem do 4 MB. Při překročení dostanete vysvětlení; pro náhled snižte rozměr nebo DPI. Vlastní export z editoru tímto limitem náhledu omezený není.

## Váš úkol

Uložte předaný Figure jako PNG přesně do cesta (str nebo Path, rodič existuje) se zadaným kladným celočíselným DPI. Vraťte Path téže cesty. Neměňte velikost ani DPI původního Figure, nemažte jeho osy/data. Ukládejte předaný fig, nikoli náhodný aktuální obrázek z pyplot.

Dokončete `uloz_png(fig, cesta, dpi)`.

Další procvičování změní rozměr, uloží průhledné pozadí, těsný rámeček a dvě varianty do složky. Kontrola otevírá skutečné PNG a ověřuje formát, rozměry, DPI i příslušné nastavení. Přijímá jiný správný postup a hlídá, že se neztrácí předaný obrázek ani jeho data.
