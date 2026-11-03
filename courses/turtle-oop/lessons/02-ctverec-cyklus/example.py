import turtle

t = turtle.Turtle()
t.color("green")         # barva čáry
t.pensize(2)             # tloušťka čáry
for i in range(4):       # čtyřikrát: strana a zatáčka
    t.forward(60)
    t.left(90)
turtle.done()
