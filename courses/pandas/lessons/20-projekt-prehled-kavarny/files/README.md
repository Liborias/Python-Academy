# Malá kavárna: cvičná data

Syntetické položky prodejů, žádný skutečný podnik ani zákaznické údaje.
den je den ve formátu YYYY-MM-DD, produkt textový kód, kusy počet jednotek
na řádku a cena cena jedné jednotky v Kč pro daný řádek. Cena se může měnit.
Řádek neznamená jednoho zákazníka ani celou objednávku. Nulový počet je platný.

CSV je UTF-8 se středníkem, desetinnou čárkou a hlavičkou. V terminálu přejděte
do pracovní složky, kde vedle reseni.py leží prodeje.csv. Pandas nevyžaduje síť.

Kontrolní výsledek: 7 řádků, 15 kusů, 687 Kč tržby.
Denní tržby: 2026-11-01 = 270, 2026-11-02 = 148, 2026-11-03 = 269.
Produktové tržby: caj = 282, kava = 305, voda = 100.
Tržba je součet kusy * cena po řádcích. Není to zisk ani daňový výpočet.
Původní soubor ponechte; vlastní variantu si vytvořte do kopie.

Zkuste změnit pořadí řádků, přidat nulový prodej nebo několik položek se stejným
produktem a jinou cenou. Ověřte oba přehledy i celkový souhrn. Samotný soulad
součtů nezaručuje správné skupiny: zkontrolujte i jejich klíče a jednotlivé hodnoty.
