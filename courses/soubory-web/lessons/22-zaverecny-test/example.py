def nejdrazsi(ceny):
    if not ceny:
        return None                    # prázdný seznam: není co vybírat
    return max(ceny)


def prumer(ceny):
    if not ceny:
        return 0
    return round(sum(ceny) / len(ceny), 1)    # zaokrouhlení na 1 desetinné místo


ceny = [249, 199, 289]
print(nejdrazsi(ceny), prumer(ceny))          # 289 245.7
print(nejdrazsi([]), prumer([]))              # None 0
