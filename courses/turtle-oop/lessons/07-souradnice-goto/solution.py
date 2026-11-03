import turtle

body = [(-100, -50), (-50, 50), (0, -50), (50, 50), (100, -50)]
t = turtle.Turtle()
t.pencolor("red")
t.pensize(3)
t.penup()
t.goto(body[0])
t.dot(8, "blue")
t.pendown()
for x, y in body[1:]:
    t.goto(x, y)
    t.dot(8, "blue")
turtle.done()
