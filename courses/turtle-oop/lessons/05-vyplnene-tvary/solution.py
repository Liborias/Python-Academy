import turtle

t = turtle.Turtle()
t.color("brown", "yellow")
t.begin_fill()
for i in range(4):
    t.forward(100)
    t.left(90)
t.end_fill()
t.penup()
t.goto(0, 100)
t.pendown()
t.color("brown", "red")
t.begin_fill()
for i in range(3):
    t.forward(100)
    t.left(120)
t.end_fill()
turtle.done()
