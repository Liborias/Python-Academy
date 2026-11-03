import turtle

t = turtle.Turtle()
t.color("navy", "lightblue")     # čára, výplň
t.begin_fill()
for i in range(6):               # šestiúhelník
    t.forward(50)
    t.left(60)
t.end_fill()
t.penup()
t.goto(120, 0)                   # přesun bez kreslení
t.pendown()
t.color("darkgreen", "lightgreen")
t.begin_fill()
for i in range(3):               # trojúhelník
    t.forward(80)
    t.left(120)
t.end_fill()
turtle.done()
