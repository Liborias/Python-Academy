## Graf začíná otázkou

Chceme poznat vývoj teploty, porovnat objednávky, nebo ukázat rozložení čekání? Nejdřív pojmenujeme otázku a jednotky. Barva sama nevysvětlí, co číslo znamená. V tomto modulu používáme vlastní smyšlená data; závěry se týkají jen těchto příkladů.

## Knihovna a tři způsoby práce

Matplotlib kreslí grafy. Instalace kurzu už jej zahrnuje: v terminálu ve složce projektu spusťte `python tools/setup_env.py --courses pandas`, pokud jej ještě nemáte. Pomocník připraví projektovou .venv; tu vyberte i ve VS Code, VSCodium nebo PyCharm. Verzi ověří `python -c "import matplotlib; print(matplotlib.__version__)"`. Ověřená kombinace je Python 3.14.8 a Matplotlib 3.11.2.

V aplikaci spustíte ukázku a pod textovým výstupem se objeví PNG s odkazem ke stažení. Vytvoří se až při dokončení programu; po novém běhu se nahradí. V editoru nebo terminálu se stejný PNG uloží do aktuální pracovní složky procesu: otevřete jej jako obrázek. Notebook není nutný. Značky # %% dovolují rozdělit skript do buněk, ale celý .py funguje také přímo. U běžného lokálního skriptu ovlivňuje cestu pracovní složka terminálu, nemusí to být automaticky složka skriptu.

## Figure je celý obrázek, Axes jeho kreslicí oblast

`from matplotlib.figure import Figure` načte třídu celého obrázku. Vytvořením `Figure(figsize=(6, 4), layout="constrained")` vznikne objekt široký šest a vysoký čtyři palce. Nejsou to pixely. Constrained nechá Matplotlib rozmístit popisky tak, aby se vešly; výsledek přesto vždy prohlédneme.

`fig.subplots()` přidá jednu kreslicí oblast Axes a vrátí ji. Axes má osu x, osu y, data, titulek i legendu. Názvy Figure/Axes označují různé objekty. Proměnné fig/ax jsou jen běžné, libovolně pojmenované proměnné.

```python
from matplotlib.figure import Figure
fig = Figure(figsize=(6, 4), layout="constrained")
ax = fig.subplots()
ax.set_title("Cvičné teploty")
ax.set_xlabel("Den")
ax.set_ylabel("Teplota (°C)")
ax.plot([1, 2, 3], [8, 11, 9], marker="o", label="Ráno")
ax.legend()
fig.savefig("graf.png", dpi=120)
```

Set_title nastaví titulek oblasti, set_xlabel/set_ylabel popisky os. Plot přidá čáru přes dvojice x/y; marker="o" označí skutečné body měření. Podrobnosti výběru grafu přijdou v další lekci. Label pojmenuje datovou řadu; teprve `ax.legend()` vytvoří legendu podle těchto názvů. Legenda nenahrazuje jednotky na osách. `ax.set(title=..., xlabel=..., ylabel=...)` je kratší zápis stejných nastavení a objeví se v následujících řešeních.

Savefig uloží konkrétní Figure do souboru. DPI 120 znamená počet bodů obrazu na palec; bez ořezu má 6 × 4 palce obrázek 720 × 480 pixelů. Zde je ukládání způsob, jak graf zobrazíme a předáme; více možností bude v lekci 30. Import Figure a ukládání PNG fungují bez otevírání samostatného okna. Aplikace tak nepotřebuje grafickou plochu.

## Rozsah osy je součást sdělení

`ax.set_ylim(minimum, maximum)` nastaví dolní a horní mez y. Set_xlim nastaví totéž pro x. Příliš těsný rozsah může zvýraznit malé změny; příliš široký je zakryje. U čáry teploty může být vhodná i záporná dolní mez. U sloupců se délka čte od nuly, proto na nule začneme v další lekci. Při porovnávání grafů si změny měřítka vždy všimneme.

## Dva panely, jeden nadpis

`fig.subplots(1, 2)` vytvoří jednu řadu se dvěma Axes a vrátí dvojici oblastí, například `leva, prava`. Každá má vlastní popisky i data. `fig.suptitle(text)` přidá společný titulek celého Figure; není to titulek jen poslední oblasti.

V návodech také potkáte `fig, ax = plt.subplots()` po importu matplotlib.pyplot. To je další způsob vytvoření stejných objektů. Zde používáme Figure přímo, aby byl každý obrázek výslovný a šel uložit bez okna; není potřeba globální „aktuální graf“ ani plt.show. Vlastní funkce budou vracet fig, takže je lze dál upravit či uložit.

## Váš úkol

Vraťte nový Figure velikosti 6 × 4 palce s právě jednou Axes. Nastavte její titulek a oba popisky podle parametrů. Zatím nic nekreslete. Funkce soubor neukládá; ukázkové volání pod ní přidá měření a uloží PNG.

Dokončete `priprav_graf(titulek, x_popisek, y_popisek)`.

Další úkoly doplní popisky už existující oblasti, legendu, rozsah a dva panely. Zachování objektu je důležité: nové vytvoření Axes by mohlo původní měření zahodit. Funkce připravuje graf; ukázkové volání pod ní jej doplní a uloží. Automatická kontrola ověřuje obsah objektů, nikoli oblíbenou barvu nebo font.
