### Průnik dvou masek

Napište `zasah_maskou(a, b)`, která vrací bool, zda se masky skutečně překrývají ve světě. Oba objekty už mají rect a mask. Posun druhé masky vůči první je `b.rect.topleft - a.rect.topleft`, může být i záporný. `a.mask.overlap(b.mask, posun)` vrací bod průniku nebo None. Průnik může být také v bodě (0,0), který je platný.

Nezaměňujte souřadnice obrázku, světa a druhé masky. Pouhé překrytí obdélníků nestačí. Nehýbejte objekty, neměňte obrázky a nic nemažte.
