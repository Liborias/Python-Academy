def telo_kodu(telo):
    if not isinstance(telo,str) or not 1<=len(telo)<=32 or not all('0'<=c<='9' for c in telo):
        raise ValueError('Tělo má mít 1 až 32 ASCII číslic, bez mezer a znamének.')
    return telo
