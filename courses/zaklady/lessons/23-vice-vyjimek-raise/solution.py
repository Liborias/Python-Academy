def nacti_vek(text):
    vek = int(text)
    if vek < 0 or vek > 150:
        raise ValueError("Věk musí být 0 až 150")
    return vek


def je_vek_platny(text):
    try:
        nacti_vek(text)
    except ValueError:
        return False
    return True


def prvek(seznam, index):
    try:
        return seznam[index]
    except IndexError:
        return None


def hodnota(slovnik, klic):
    try:
        return slovnik[klic]
    except KeyError:
        return "?"
