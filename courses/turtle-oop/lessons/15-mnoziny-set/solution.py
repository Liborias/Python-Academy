def unikatni_pocet(seznam):
    return len(set(seznam))


def spolecne(a, b):
    return sorted(set(a) & set(b))


def jen_v_prvnim(a, b):
    return sorted(set(a) - set(b))


def vsechna_pismena(text):
    return sorted({znak for znak in text.lower() if znak.isalpha()})


def ma_duplicity(seznam):
    return len(set(seznam)) < len(seznam)
