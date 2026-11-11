## Regrese náhody, skupin a hlídače

Napište regresní testy a **sestav_sadu()** pro čtyři pravidla: Vlny(17) a Vlny(23) mají odlišný rng.getstate; zahaj zachová stejnou Group a kill odstraní i další členství drona; HlidacBodu měří dosah od kotvy; Kolo po konec=True zmrazí čas/polohu/energii/náhodu.

Pro hlídače použijte kotvu (100,200), dosah 160, současnou polohu drona (260,200) a hráče (270,200). Hráč je blízko drona, ale mimo dosah kotvy, cílem je tedy kotva. Tato situace odliší dvě snadno zaměnitelné interpretace.

Kontrola postupně zavede ignorovaný seed, záměnu Group za novou, měření od drona a posun po konci. Správný model přijměte a všechny tyto regrese odhalte. Regresní test hlídá, aby se dříve opravená chyba nevrátila.
