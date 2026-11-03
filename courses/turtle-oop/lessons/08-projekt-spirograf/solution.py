import turtle

barvy = ["red", "orange", "yellow", "green", "blue", "purple"]
turtle.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
t.pensize(2)
t.hideturtle()
for i in range(36):
    t.pencolor(barvy[i % 6])
    t.circle(80)
    t.left(10)
turtle.done()
