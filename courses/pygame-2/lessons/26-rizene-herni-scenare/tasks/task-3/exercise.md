## Stisky rozložené do snímků

Vytvořte **naplanuj_vstup(pocet, zmeny)**. Pocet je nezáporný int, bool ani desetinné číslo nejsou počet; neplatnou hodnotu odmítněte ValueError. Zmeny je mapa čísla snímku na dvousložkový směr; klíče a směry dostáváte platné. Vrátíte pocet n-tic směru.

Před první změnou platí (0, 0). Změna se projeví už ve svém snímku a trvá do další změny. Pro pocet=4 a {1: [1, 0]} dostanete [(0, 0), (1, 0), (1, 0), (1, 0)]. Vstupní seznamy neměňte ani je nevracejte jako sdílené odkazy. V reálné hře je směr stav držených kláves; plán jej nahrazuje opakovatelnými hodnotami.
