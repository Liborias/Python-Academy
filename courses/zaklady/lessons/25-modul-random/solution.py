import random


def hod_kostkou():
    return random.randint(1, 6)


def vyber(seznam):
    return random.choice(seznam)


def zamichej(seznam):
    kopie = list(seznam)
    random.shuffle(kopie)
    return kopie


def tajne_cislo(seed):
    random.seed(seed)
    return random.randint(1, 100)
