### Maska po změně obrázku

Napište `obnov_masku(sprite, novy_obraz, prah=127)`. Zachová dosavadní střed rect, vytvoří vlastní kopii nového image, přestaví rect na nový rozměr se zachovaným středem a vytvoří mask z nového image a prahu. Návratovou hodnotu nepoužíváme. Zdrojový nový obrázek nesmí pozdější změna spritu poškodit.

To je potřeba po změně snímku či otočení obrázku. Pouhý přesun stejného obrázku mění rect, ne jeho lokální masku. Při jiné podobě však stará maska vede ke kolizím s neviditelnými pixely.
