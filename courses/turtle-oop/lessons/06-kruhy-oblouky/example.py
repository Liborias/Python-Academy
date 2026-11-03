import turtle

t = turtle.Turtle()
t.circle(40)                     # kruh po levé straně
t.penup()
t.goto(120, 0)
t.pendown()
t.circle(40, 180)                # jen půlkruh
t.penup()
t.goto(-120, 0)
t.pendown()
t.circle(40, steps=5)            # pětiúhelník ve tvaru "kruhu"
t.penup()
t.goto(0, -80)
t.pendown()
t.dot(30, "orange")              # vyplněná tečka
turtle.done()
