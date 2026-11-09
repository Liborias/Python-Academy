### Animace přehraná jednou

Vytvořte `AnimaceJednou(snimky, trvani)` se stejnou validací a kopiemi snímků jako v Úkolu 1. Uloží `trvani`, `cas=0.0`, `index=0`, `hotovo=False`; `obraz()` vrací uložený aktivní Surface. `update(dt)` z celkového času vypočítá fázi, ale index zastaví na posledním snímku. Hotovo nastane až po `počet_snímků × trvani`: poslední obrázek má také trvat celý interval. Po dokončení další update nemění čas ani index.

Například tři snímky po 0,1 s mají v čase 0,2 s index 2 a ještě nejsou hotové. V čase 0,3 s zůstanou na indexu 2 a hotovo=True. I jediný snímek musí trvat svůj interval. Dt a přesnost float mají stejné podmínky jako v Úkolu 1.
