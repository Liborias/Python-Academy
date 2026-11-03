import turtle


def mnohouhelnik(t, strany, delka):
    """Nakreslí pravidelný mnohoúhelník."""
    uhel = 360 / strany
    for i in range(strany):
        t.forward(delka)
        t.left(uhel)


t = turtle.Turtle()
t.color("purple")
mnohouhelnik(t, 5, 60)       # pětiúhelník
t.penup()
t.goto(100, 0)               # přesun bez kreslení
t.pendown()
mnohouhelnik(t, 8, 30)       # osmiúhelník
turtle.done()
