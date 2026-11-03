import json

# Úkol (soubor kontakty.json je ve složce programu; kontakt je slovník jmeno, telefon, email):
#   nacti_kontakty(nazev)                          -> seznam kontaktů, chybějící soubor dává [] (ošetřete pomocí try a except)
#   pridej_kontakt(nazev, jmeno, telefon, email="")-> True, nebo False, když jméno už existuje
#   najdi(nazev, text)                             -> kontakty, jejichž jméno obsahuje text
#   smaz_kontakt(nazev, jmeno)                     -> True, nebo False, když takový kontakt není
#   vypis(nazev)                                   -> řádky "Eva Nováková: 777111222" podle jména, nebo "Žádné kontakty."
