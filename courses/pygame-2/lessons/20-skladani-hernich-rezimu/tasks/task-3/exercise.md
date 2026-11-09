### Tlačítko vrací akci

Vytvořte `Tlacitko(rect, text, akce, font)` s vlastní kopií rect a předanými dalšími údaji. Vstupní rect může být Rect nebo čtveřice (x,y,šířka,výška). Zpracuj vrací akci pouze při levém MOUSEBUTTONDOWN uvnitř rect podle udalost.pos; jinak None. Rect zahrnuje levý a horní okraj, pravý a dolní už ne. Čtěte button/pos až po ověření typu události.

Kresli vykreslí zaoblený obdélník barvy (38,68,96), okraj (90,175,225) tloušťky 2 a uprostřed text barvy (240,245,255) předaným fontem. Okolí nemění. Akce je neprázdný textový požadavek, například 'hra'; tlačítko samo nic nespouští.
