def cislo_nebo(text, nahrada):
    try:
        return int(text)
    except ValueError:
        return nahrada

print(cislo_nebo('x', 7))
