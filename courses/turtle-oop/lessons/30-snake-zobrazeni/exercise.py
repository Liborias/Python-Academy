import turtle
from had_model import Had


def na_pixely(bod, sirka, vyska):
    # Buňka má 20 pixelů; střed celé mřížky leží v (0, 0).
    pass


def vykresli(had, pero):
    # Smažte předchozí otisky a vykreslete hlavu žlutě, tělo zeleně.
    pass


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
