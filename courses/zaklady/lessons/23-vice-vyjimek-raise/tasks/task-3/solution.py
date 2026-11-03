def obsah_ctverce(strana):
    if strana <= 0:
        raise ValueError("Nepovolená hodnota")
    return strana * strana

print(obsah_ctverce(2))
