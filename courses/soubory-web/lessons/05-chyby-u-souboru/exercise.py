# Úkol (soubory ok.txt a teploty.txt jsou ve stejné složce jako program).
# Obě „bezpečné“ funkce ošetřete pomocí try a except; zachyťte OSError, ne jednotlivé podtypy:
#   nacti_bezpecne(nazev, vychozi="")  -> obsah souboru, nebo vychozi, když soubor nejde otevřít
#   nacti_cisla_bezpecne(nazev)        -> seznam celých čísel, špatné a prázdné řádky přeskočit,
#                                         chybějící soubor dává []
#   zaloha(nazev)                      -> zkopíruje soubor do nazev + ".bak", vrátí True; když
#                                         soubor neexistuje, vrátí False
