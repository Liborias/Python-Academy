def je_cislo(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

print(je_cislo('12'))
