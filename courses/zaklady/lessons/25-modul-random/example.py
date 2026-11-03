import random

random.seed(7)                                # pevný výchozí bod: výsledky se budou opakovat
hod = random.randint(1, 6)                    # celé číslo od 1 do 6 včetně
print("Padlo", hod)

zvirata = ["pes", "kocka", "ptak", "kun"]
print(random.choice(zvirata))                 # jeden náhodný prvek

kopie = list(zvirata)                         # kopie, abychom nezměnili původní seznam
random.shuffle(kopie)                         # shuffle zamíchá přímo kopii a nic nevrací
print(kopie)
print(zvirata)                                # původní seznam zůstal beze změny
