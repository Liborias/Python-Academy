### Přidání do skupiny při vzniku

`Hrac(stred, skupina)` má stejný vlastní vzhled a rozměry jako Lod z Úkolu 1. Nová instance navíc patří do předané `pygame.sprite.Group`; dřívější členové zůstanou. Můžete předat skupinu do `super().__init__(skupina)` nebo po inicializaci použít `skupina.add(self)`. Zatím jde jen o členství, nikoli vykreslení.
