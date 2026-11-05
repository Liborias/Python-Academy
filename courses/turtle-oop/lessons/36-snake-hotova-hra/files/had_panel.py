"""Grafická část: tělo, potrava, hranice plochy a textový panel."""
import turtle
from had_model import Had
from had_pohled import priprav_okno, na_pixely, vykresli


def priprav_hriste(sirka, vyska):
    okno, pero = priprav_okno(Had([(0, 0)], sirka, vyska))
    okno.setup(max(440, sirka * 20 + 40), max(240, vyska * 20 + 110))
    okno.title("Snake — šipky: pohyb, Enter: nová hra")
    jidlo = turtle.Turtle()
    jidlo.penup()
    jidlo.hideturtle()
    jidlo.shape("circle")
    jidlo.shapesize(0.65, 0.65)
    jidlo.color("red")
    text = turtle.Turtle()
    text.penup()
    text.hideturtle()
    return okno, pero, jidlo, text


def vykresli_partii(partie, pero, jidlo, text):
    had = partie.had
    vykresli(had, pero)
    jidlo.clear()
    if partie.potrava is not None:
        jidlo.goto(na_pixely(partie.potrava, had.sirka, had.vyska))
        jidlo.stamp()
    text.clear()
    text.color("gray")
    x, y = had.sirka * 10, had.vyska * 10
    text.goto(-x, -y)
    text.pendown()
    for bod in [(x, -y), (x, y), (-x, y), (-x, -y)]:
        text.goto(bod)
    text.penup()
    text.color("white")
    text.goto(0, y + 15)
    text.write(f"Skóre: {partie.skore}", align="center", font=("Arial", 14, "bold"))
    zpravy = {
        "hra": "Šipky: pohyb | Enter: nová hra",
        "konec": "Konec hry — Enter pro restart",
        "vyhra": "Vyhráno! — Enter pro novou hru",
    }
    text.goto(0, -y - 30)
    text.write(zpravy[partie.stav], align="center", font=("Arial", 11, "normal"))
