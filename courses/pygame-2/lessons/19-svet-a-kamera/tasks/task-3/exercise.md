### Z obrazovky zpět do světa

Napište `do_sveta(kamera, bod)`: nový Vector2 roven obrazovkovému bodu plus kamera.posun minus kamera.vyhled.topleft. Je to opačný převod k na_obrazovku. Platí i pro bod mimo výhled, nic zde neořezáváme a vstupy neměníme.

Místo kliknutí je nejprve v souřadnicích okna. Jestli chcete vybrat objekt v posunutém světě, musíte jej tímto převést. Není správné porovnat obrazovkovou pozici rovnou se světovým rect.
