from datetime import date, timedelta


def dnu_do(od, do):
    return (do - od).days


def za_dni(datum, n):
    return datum + timedelta(days=n)


def formatuj(datum):
    return datum.strftime("%d. %m. %Y")


def je_vikend(datum):
    return datum.weekday() >= 5
