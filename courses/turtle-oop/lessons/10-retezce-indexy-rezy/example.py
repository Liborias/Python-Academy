s = "programovani"
print(s[0], s[-1], len(s))          # první, poslední, délka
print(s[:7])                        # programo
print(s[7:])                        # vani
print(s[::-1])                      # pozpátku
print(s[::3])                       # každý třetí znak
print("gram" in s)                  # True


def prostredni(text):
    """Vrátí prostřední znak (u sudé délky horní z obou)."""
    return text[len(text) // 2]


print(prostredni("python"), prostredni("abc"))
