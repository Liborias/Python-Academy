PLANETY = {
    "Merkur": {"vzdalenost": 58, "prumer": 4879},
    "Venuše": {"vzdalenost": 108, "prumer": 12104},
    "Země": {"vzdalenost": 150, "prumer": 12742},
    "Mars": {"vzdalenost": 228, "prumer": 6779},
    "Jupiter": {"vzdalenost": 778, "prumer": 139820},
    "Saturn": {"vzdalenost": 1434, "prumer": 116460},
    "Uran": {"vzdalenost": 2871, "prumer": 50724},
    "Neptun": {"vzdalenost": 4495, "prumer": 49244},
}

# Úkol:
#   napoveda(planety, jmeno)   -> "Je 228 mil. km od Slunce a má průměr 6779 km."
#   je_spravne(tip, jmeno)     -> True/False (bez ohledu na mezery a velikost písmen)
#   vyber_planetu(planety)     -> náhodné jméno planety
#   pocet_pokusu(tipy, jmeno)  -> pořadí prvního správného tipu (od 1), nebo None
#   hra(planety, jmeno)        -> hádací cyklus, vrací počet pokusů
#
# Na konec souboru dejte: if __name__ == "__main__": hra(PLANETY, vyber_planetu(PLANETY))
