def nejdelsi(slova):
    """Vrátí nejdelší slovo; při shodě první, pro prázdný seznam prázdný text."""
    nej = ""
    for slovo in slova:
        if len(slovo) > len(nej):
            nej = slovo
    return nej

assert nejdelsi(['pes', 'kočka', 'kůň']) == 'kočka'


print(nejdelsi(['pes', 'kočka', 'kůň']))
