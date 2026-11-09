### Výběr viditelných objektů

Napište `viditelne(objekty, kamera)`. Vrátí nový seznam původních objektů s kladným průnikem jejich rect a světového výhledu. Levý horní roh výhledu ve světě je kamera.posun, velikost kamera.vyhled.size. Posun může být desetinný; nezaokrouhlujte jej před rozhodnutím. Dotyk hran nestačí. Objekty mají kladné rozměry rect.

Zachovejte pořadí vstupu; případný stejný objekt opakovaný v seznamu ponechte opakovaně. Neměňte souřadnice ani členství a neodstraňujte neviditelné objekty ze hry. Kamera z kamera.py je připravená.
