# Spustí se samostatné okno Turtle na počítači s Pythonem.
# Potřebné soubory projektu jsou připravené vedle tohoto programu.
import turtle
from had_model import Had


def na_pixely(bod, sirka, vyska):
    x, y = bod
    return ((x - (sirka - 1) / 2) * 20, (y - (vyska - 1) / 2) * 20)


def vykresli(had, pero):
    pero.clear()
    for i, bod in enumerate(had.body):
        pero.goto(na_pixely(bod, had.sirka, had.vyska))
        if i == 0:
            pero.color("yellow")
        else:
            pero.color("green")
        pero.stamp()


def priprav_okno(had):
    okno = turtle.Screen()
    okno.setup(had.sirka * 20 + 40, had.vyska * 20 + 40)
    okno.title("Snake — mřížka a zobrazení")
    okno.bgcolor("black")
    okno.tracer(0)
    pero = turtle.Turtle()
    pero.shape("square")
    pero.shapesize(0.8, 0.8)
    pero.penup()
    pero.hideturtle()
    return okno, pero


if __name__ == "__main__":
    had = Had([(8, 8), (7, 8), (6, 8)])
    okno, pero = priprav_okno(had)
    vykresli(had, pero)
    okno.update()
    okno.mainloop()
