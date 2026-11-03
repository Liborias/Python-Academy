def slevy(ceny):
    """Vraťte nový seznam cen snížených na polovinu."""
    vysledek = []
    for cena in ceny:
        po_sleve = cena * 0.5
        vysledek.append(po_sleve)
    return vysledek

print(slevy([10, 20]))
