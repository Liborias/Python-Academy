### Rect, kruh a maska vedle sebe

Napište `porovnej_kolize(a, b)`. Vrací nový slovník se třemi bool: rect podle Rect.colliderect, kruh podle vzdálenosti rect.center nejvýše součet radius a maska podle skutečného překrytí masek. Oba objekty už mají kladné rozměry rect, nezáporné konečné radius a mask. Pomocná zasah_maskou je v masky.py.

Pouhý dotyk obdélníků je False, dotyk kruhů je True a maska vyžaduje společný pevný pixel. Průhledný otvor může vést k True u obdélníku i kruhu, ale False u masky. Nejde o tři názvy téhož pravidla. Vstupy neměňte.
