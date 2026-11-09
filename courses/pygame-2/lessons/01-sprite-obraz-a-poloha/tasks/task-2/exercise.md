### Kruh s průhlednými rohy

Doplňte `Meteorit(stred, polomer)` jako Sprite s vlastním průhledným Surface **2r × 2r**. `polomer` je celé číslo nejméně 2. Uprostřed nakreslete vyplněný kruh barvy **(235, 145, 75)** s poloměrem r; rohy zůstanou průhledné. Rect vystřeďte na celočíselné `stred`. `pygame.SRCALPHA` zapne alfa kanál, `draw.circle(image, barva, (r, r), r)` kreslí v místních souřadnicích obrázku. Průhledný roh pořád leží uvnitř obdélníku rect.
