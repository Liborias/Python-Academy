import turtle

turtle.bgcolor("midnightblue")
t = turtle.Turtle()
t.speed(0)
t.pensize(2)
t.hideturtle()
barvy = ["gold", "orange"]
for i in range(18):                  # 18 kruhů po 20°
    t.pencolor(barvy[i % 2])         # střídání dvou barev
    t.circle(60)
    t.left(20)
turtle.done()
