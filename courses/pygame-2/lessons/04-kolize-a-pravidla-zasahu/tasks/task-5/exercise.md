### Zvolit kruhovou kolizi

`zasahy_kruhem(hrac, nepratele)` vrátí seznam skutečných zasažených členů, nic nemění ani neodstraňuje. Všichni mají kladný číselný radius a celočíselný rect.center. Zásahem je vzdálenost středů **nejvýše** součet poloměrů; přesný dotyk kruhů se tedy počítá. Předaný callback pygame.sprite.collide_circle použije radius. Zde se řídíme tímto výslovným pravidlem, nikoli velikostí obrázku nebo maskou jeho pixelů.
