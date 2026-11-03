def na_int(text):
    try:
        return int(text)
    except ValueError:
        return 0

print(na_int('12'))
