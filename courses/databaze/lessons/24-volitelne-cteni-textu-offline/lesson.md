## Text lze přečíst i bez síťové služby

Tato lekce je volitelná. Hlavní ukázka vždy běží jako náhled: ukáže krátký fiktivní text, nic neinstaluje a nepřehrává. Skutečnou řeč zapneme až výslovně z místního terminálu.

```python
# Prohlédnout text není totéž jako spustit hlasový program.
text = 'Ukázková poznámka.'
print('Náhled:', text)
```

`hlas.py` vybírá systémový program. Windows: powershell.exe se System.Speech a instalovaným hlasem; macOS: say; Linux: espeak-ng nebo espeak s hlasem cs. Když program/hlas chybí, náhled zůstává použitelný. Ve Windows/macOS výslovnost závisí na výchozím instalovaném hlasu. Nepoužíváme pyttsx3 ani online API.

## Text je vstup, ne příkaz

Spouštíme pevný seznam argv bez shell=True. Text předáme přes stdin, včetně češtiny a uvozovek. Znak ; nebo text připomínající příkaz tak nezmění spouštěný program. U PowerShellu zůstává script pevný, čtený text do něj nevkládáme. Nepředáváme hesla ani ověřovací záznamy.

Timeout 15 s ukončí příliš dlouhé čtení; proto volíme krátké poznámky. Návratový kód programu ověří check=True. Úspěšné převzetí textu hlasovým programem samo neověří zapnutý reproduktor či kvalitu výslovnosti, to vyzkoušíte místně.

## Váš úkol

Doplňte **precti(text, mluv=False)** s pojmenovaným mluv. Text ověřte over_text (neprázdný UTF-8 do 2000 znaků, původní obsah zachován). Bez mluv vrátí `nahled` a nevolá subprocess ani hlas. S mluv získá vyber_prikaz; None znamená `nedostupne`.

Jinak spustí subprocess.run s argv, input=text, text=True, encoding='utf-8', check=True, capture_output=True, errors='replace', timeout=15, bez shellu. Chybový výstup různých systémů čteme s errors='replace', aby neznámé kódování diagnostiky nezpůsobilo pád; vstupní text už over_text ověřil jako platné UTF-8. Úspěch vrátí `precteno`; OSError, CalledProcessError nebo TimeoutExpired vrátí `nedostupne`. Chybný text je ValueError. Nečeká na input při importu ani nic sám nečte nahlas.

V uložené složce:

```powershell
python precti.py "Ukázková poznámka."
python precti.py "Ukázková poznámka." --mluv
```

První příkaz je náhled, druhý skutečná volba zvuku. Pokud chybí systémový hlas, doinstalujte jej podle svého OS; Linux např. balíček espeak-ng a hlas cs. Stav nedostupne vrátí kód 2. Ostatní lekce ani kontrola řešení hlasový program nepotřebují. Podrobnosti jsou v NAVOD.md.
