## Začneme jednotkami, ne databází

Postavíme **BMI tracker**: výpočet, měření s datem, období a souhrny, vlastní okno, export a záloha. Jde o samostatný projekt. Používáme fiktivní údaje, které nepředstavují doporučení pro konkrétního člověka. Každý krok má možné řešení a v dalším kroku přiložené hotové součásti.

BMI se počítá jako hmotnost v kilogramech dělená druhou mocninou výšky v metrech. Formulář ale budeme zadávat v centimetrech, proto je nejprve dělíme stem.

```python
# Centimetry převedeme před umocněním; 180 cm je 1,8 m.
hmotnost_kg = 81
vyska_cm = 180
vyska_m = vyska_cm / 100
print(hmotnost_kg / vyska_m ** 2)
```

Výsledek je 25.0. Dělení přímo 180 na druhou by dalo desetitisíckrát menší výsledek. Před uložením ani porovnáním nezaokrouhlujeme. Výpis se dvěma desetinnými místy je pouze způsob zobrazení.

## Validace není odhad zdravotního stavu

`validace.py` poskytuje kladne_cislo: přijme pouze int/float bez bool, kladné a konečné. NaN znamená nečíselnou hodnotu, infinity nekonečno; ani jedna není použitelné měření. Neplatný vstup vyvolá ValueError. Extrémní hodnoty mohou překročit možnosti float; takový výsledek také odmítneme.

BMI je orientační ukazatel pro dospělé a samo neposuzuje individuální zdraví. Nerozlišuje svaly od tuku a nezohlední všechny souvislosti. Dětské hodnocení a těhotenství nelze převzít z těchto jednoduchých dospělých pásem. Tracker nebude navrhovat léčbu, cílovou hmotnost ani hodnotit člověka.

## Hranice a zaokrouhlený výpis

Pro procvičení porovnávání rozdělíme kladné hodnoty do pásem: pod 18,5; od 18,5 pod 25; od 25 pod 30; 30 a více. Každá spodní hranice už patří do následujícího pásma. Hodnota 24.999 se může zobrazit jako 25.00, ale stále patří pod 25. Přepínatelné ukázky to ukazují vedle sebe.

## Prostředí a váš úkol

Python 3.12+, ověřeno 3.14.8. Zatím jen standardní knihovna, bez pip. V Přípravě kurzu vyberte VS Code/VSCodium/PyCharm a stejnou .venv jako v terminálu. Pro pozdější okno lze ověřit `python -m tkinter`, podrobnosti jsou v NAVOD.md.

Doplňte **bmi(hmotnost_kg, vyska_cm)** a **pasmo(hodnota)**. BMI vrací nezaokrouhlený kladný konečný float. Použijte kladne_cislo pro oba vstupy, převeďte cm na m a vypočtěte podíl. Nelze-li kladný konečný výsledek reprezentovat, vyvolejte ValueError, včetně příliš malé výšky po převodu.

Pasmo nejprve ověří kladnou konečnou hodnotu a vrátí přesně jeden text: `pod 18,5`, `18,5 až pod 25`, `25 až pod 30`, `30 a více`. Nemá zaokrouhlovat. Procvičte 81/180, 64/160, hodnoty těsně pod hranicemi, nulu, bool a NaN. Porovnejte možné řešení se svým výpočtem; více matematicky správných zápisů je v pořádku.
