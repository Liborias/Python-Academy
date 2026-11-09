### Kreslení do kopie pozadí

`vykresli_skupinu(skupina, pozadi)` vrátí **nový Surface**, kopii pozadí s vykreslenými členy. Zdrojové pozadí, obrázky, polohy i členství zachovejte. `Group.draw(surface)` používá dvojici image/rect. Vstupní sprity mají neprůhledné obrázky, leží uvnitř pozadí a nepřekrývají se, takže zde pořadí vrstev neřešíme. Prázdná skupina dá samostatnou nezměněnou kopii pozadí.
