## Testy omezeného štítu

Napište testy **model.StitZakladny** a **sestav_sadu()**. Ověřte přesnou i nedostatečnou energii pro celý krok, prázdný štít při dt=0, spotřebu uvnitř, obnovu pouze mimo přístav a její strop.

Například kapacita 1 přesně pokryje krok 1 s, energie 0,01 nepokryje 0,02 s. Z kapacity 2,5 po 0,5 s uvnitř zbudou 2 s, po 0,5 s mimo přibude 0,25 s. I dlouhá obnova skončí nejvýše na kapacitě. Samotná hodnota True neověří správnou zbývající energii.

Vaše sada má přijmout správný model a odmítnout ochranu při nedostatečné energii, dobíjení uvnitř a překročení kapacity. Sestav_sadu vrací pokaždé novou sadu; již proběhlá unittest sada může své testy spotřebovat.
