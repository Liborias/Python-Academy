### Výřezy z pásu snímků

Napište `vyrez_snimky(pas, sirka)`. Vrátí seznam vlastních Surface z vodorovného pásu zleva doprava. Každý má šířku sirka a celou původní výšku včetně všech pixelů a průhlednosti. Sirka je celé číslo; nekladnou hodnotu nebo šířku, která celý pás nerozdělí beze zbytku, odmítněte ValueError.

`subsurface(rect)` je pohled na původní paměť. Přidejte copy, aby změna výřezu neměnila pás. Vstupní Surface se nesmí změnit. Podklady poskytují pas_snimku() jako vlastní jednoduchý spritesheet.
