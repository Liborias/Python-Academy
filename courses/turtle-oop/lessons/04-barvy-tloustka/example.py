import turtle

turtle.bgcolor("navy")           # pozadí okna
t = turtle.Turtle()
t.speed(0)                       # nejrychlejší kreslení
t.pensize(5)                     # tlustá čára
t.pencolor("yellow")             # barva jménem
t.forward(100)
t.pencolor("#ff69b4")            # barva kódem
t.left(90)
t.forward(100)
turtle.colormode(255)            # čísla 0 až 255
t.pencolor(0, 255, 255)          # barva trojicí
t.left(90)
t.forward(100)
t.hideturtle()
turtle.done()
