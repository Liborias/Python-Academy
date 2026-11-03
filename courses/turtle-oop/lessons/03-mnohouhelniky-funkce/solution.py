import turtle


def mnohouhelnik(t, strany, delka):
    uhel = 360 / strany
    for i in range(strany):
        t.forward(delka)
        t.left(uhel)


t = turtle.Turtle()
t.penup()
t.goto(-150, 0)
t.pendown()
mnohouhelnik(t, 3, 100)
t.penup()
t.goto(50, 0)
t.pendown()
mnohouhelnik(t, 6, 50)
turtle.done()
