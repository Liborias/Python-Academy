## Rozdělení času na malé kroky

Vytvořte **rozdel_cas(celkem, krok=0.05)**. Vraťte seznam kladných délek, jejichž součet odpovídá celkem s tolerancí 1e-10. Plné kroky mají délku krok, jen poslední smí být kratší. Například 0,12 s při kroku 0,05 s vytvoří přibližně [0.05, 0.05, 0.02]. Pro nulu vraťte [].

Celkem musí být konečné nezáporné číslo a krok konečný v intervalu (0; 0,05]; jinak ValueError. Math.isfinite vyloučí nekonečno a NaN. Drobné zbytky do 1e-12 můžete zanedbat: desetinné zlomky nemají v binárním float vždy přesný zápis. Funkce nic nehraje, pouze připraví herní čas.
