text = "  Python je   skvělý jazyk  "
slova = text.split()                  # ["Python", "je", "skvělý", "jazyk"]
print(slova, len(slova))
print(" ".join(slova))                # slova oddělená jednou mezerou
print(text.strip().upper())           # PYTHON JE SKVĚLÝ JAZYK
print(text.count("y"), text.find("je"))


def inicialy(jmeno):
    """Z 'Jan Novák' udělá 'J. N.'."""
    return " ".join(slovo[0].upper() + "." for slovo in jmeno.split())


print(inicialy("jan novák"))
