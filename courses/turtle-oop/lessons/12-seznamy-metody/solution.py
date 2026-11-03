def bez_duplicit(seznam):
    videno = []
    for x in seznam:
        if x not in videno:
            videno.append(x)
    return videno


def serad_podle_delky(slova):
    return sorted(slova, key=lambda s: (len(s), s))


def posun(seznam, k):
    if not seznam:
        return []
    k = k % len(seznam)
    return seznam[k:] + seznam[:k]


def odeber_vsechny(seznam, hodnota):
    return [x for x in seznam if x != hodnota]
