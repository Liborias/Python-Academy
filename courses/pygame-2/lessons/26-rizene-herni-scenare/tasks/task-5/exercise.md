## Dva nezávislé pokusy

Vytvořte **dvojice_behu(seed, kroky)**. Vraťte dvojici stop dvou nezávislých volání připravené prehraj. Kroky mohou být generátor, proto jeho hodnoty nejdřív zachovejte pro obě přehrání.

Stejný číselný seed a stejné vstupy dávají stejné hodnoty, ale pokusy nesdílejí seznamy ani slovníky snímků. Změna a[0]['skore'] nesmí změnit b. Pouhé return stopa, stopa nebo mělká kopie nestačí. Seed=None obecně opakovatelnost nezaručuje: znamená nový náhodný začátek.
