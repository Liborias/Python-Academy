### Průhledná pauza

Vytvořte `Pauza(font)` se společným rozhraním režimu. Zpracuj vrátí 'zpet' pouze pro KEYDOWN klávesy P, jinak None. Update nic nemění a neposouvá podklad hry. Kresli vytvoří Surface velikosti předané plochy se SRCALPHA, vyplní ji (10,18,30,170), do středu vykreslí text PAUZA barvy (240,245,255) předaným fontem a celou vrstvu blitne na podklad.

Font je předem připravený. Průhlednost 170 míchá původní obraz s vrstvou, nesmí jej nahradit neprůhlednou barvou. Pauza podklad sama znovu nekreslí: o pořadí vrstev se stará zásobník.
