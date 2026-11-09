### Sprite s měnícím se obrázkem

Vytvořte `AnimovanySprite(snimky, stred, trvani=0.125)` jako skutečný Sprite. Použije připravenou Animace z animator.py, uloží ji do `animace`, aktuální `image` a vlastní `rect` vystředěný na celočíselný stred. `update(dt)` posune animaci, přepne image a přestaví rect pro nový rozměr, ale zachová jeho **aktuální střed**. Ten mohl být jinde než při konstrukci.

Snímky smějí mít různé rozměry. Samotné přiřazení nového image starý rect neopraví. Objekt má fungovat i přes Group.update(dt). Kreslení nemění zdrojové snímky.
