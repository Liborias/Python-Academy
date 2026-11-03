# Tady chyby zachytíme, abychom viděli jejich jména. Samotný program by jinak spadl.
try:
    print(10 / 0)
except ZeroDivisionError as chyba:            # as chyba: výjimka se uloží do proměnné
    print("ZeroDivisionError:", chyba)        # division by zero

try:
    print(int("abc"))
except ValueError as chyba:
    print("ValueError:", chyba)               # invalid literal for int()

try:
    print([1, 2, 3][3])
except IndexError as chyba:
    print("IndexError:", chyba)               # list index out of range

try:
    print(nezname_jmeno)
except NameError as chyba:
    print("NameError:", chyba)                # name 'nezname_jmeno' is not defined
