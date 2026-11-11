## Pomůcky bez aktivní výpůjčky

Vytvořte **bez_aktivni_vypujcky(con)**. Vrátí (id, nazev, kusy) jen u pomůcek bez jediné aktivní výpůjčky, v pořadí id. Vraceno=0 znamená aktivní, 1 vrácenou. Pomůcka může mít zároveň vrácené i aktivní půjčení; v takovém případě do výběru nepatří.

Hodí se NOT EXISTS se vnořeným dotazem navázaným na p.id. SELECT 1 ve vnitřním dotazu jen zjišťuje existenci řádku. Každou pomůcku vracejte jednou. Jde o stav výpůjček, ne jen o kontrolu, že kusy>0.
