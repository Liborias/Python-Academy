### Dva klíče bez složitého indexu

Seskupte podle dvojice různých existujících str sloupců a vraťte DataFrame [prvni_klic, druhy_klic, radky, prumer]. Klíče nekolidují s radky/prumer. Počet řádků je int64, průměr float64 hodnot vynechává NaN. Zachovejte i kombinace s chybějícím klíčem; kombinace řaďte vzestupně podle obou klíčů s chybějícím na konci příslušného klíče. Výstup má RangeIndex, prázdný vstup je platný.

Doplňte `prehled_dvou_klicu(tabulka, prvni_klic, druhy_klic, hodnota)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
