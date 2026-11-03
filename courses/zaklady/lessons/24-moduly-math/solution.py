import math


def obsah_kruhu(r):
    return math.pi * r ** 2


def vzdalenost(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def pocet_krabic(kusu, kapacita):
    return math.ceil(kusu / kapacita)
