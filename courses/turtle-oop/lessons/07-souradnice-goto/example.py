import turtle

t = turtle.Turtle()
body = [(0, 0), (80, 60), (160, 0)]   # seznam dvojic (x, y)
t.penup()
t.goto(body[0])                       # přesun na první bod
t.pendown()
for x, y in body[1:]:                 # rozbalení dvojice do x a y
    t.goto(x, y)
    t.dot(10, "green")                # puntík v každém dalším bodu
x, y = t.pos()                        # poloha želvy jako dvojice
t.write(f"konec: {x:.0f}, {y:.0f}")
turtle.done()
