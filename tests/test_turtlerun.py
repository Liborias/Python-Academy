"""Želva bez okna: dilna_check.turtle_run."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PROG = '''import turtle
t = turtle.Turtle()
t.pensize(3)
t.color("red", "yellow")
t.begin_fill()
for i in range(4):
    t.forward(100)
    t.left(90)
t.end_fill()
t.penup()
t.goto(-50, 20)
t.pendown()
t.dot(10, "blue")
t.write("Ahoj", font=("Arial", 12, "bold"))
turtle.bgcolor("black")
turtle.done()
print("nedoběhne")
'''


class TurtleRunTest(unittest.TestCase):
    def run_prog(self, code, **kw):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "reseni.py").write_text(code, encoding="utf-8")
        env = dict(os.environ, DILNA_STUDENT=str(tmp / "reseni.py"), DILNA_RESULT=str(tmp / "r.json"), DILNA_DATA=str(tmp))
        sys.path.insert(0, str(ROOT / "lib"))
        old = dict(os.environ)
        os.environ.update(env)
        try:
            from dilna_check import check
            return check().turtle_run(**kw)
        finally:
            sys.path.pop(0)
            os.environ.clear(); os.environ.update(old)

    def test_ctverec_vyplne_texty(self):
        r = self.run_prog(PROG)
        self.assertIsNone(r.error); self.assertTrue(r.ended and r.mainloop)
        self.assertAlmostEqual(r.length("red"), 400, places=2)
        self.assertEqual(r.widths(), {3}); self.assertEqual(r.colors(), {"red"})
        self.assertEqual(len(r.corners()), 3)
        self.assertEqual(r.bbox(), (0.0, 0.0, 100.0, 100.0))
        self.assertTrue(r.covers((50, 0))); self.assertFalse(r.covers((50, 50)))
        self.assertEqual(len(r.fills), 1); self.assertEqual(r.fills[0]["color"], "yellow")
        self.assertAlmostEqual(r.fill_area("yellow"), 10000, places=1)
        self.assertEqual(r.dots[0][:2], [-50.0, 20.0]); self.assertEqual(r.dots[0][3], "blue")
        self.assertEqual(r.texts[0]["text"], "Ahoj")
        self.assertEqual(r.bgcolor, "black")
        self.assertEqual(r.called("forward"), 4); self.assertEqual(r.out, "")

    def test_kruh_je_mnohouhelnik_a_barvy_rgb(self):
        r = self.run_prog("import turtle\nturtle.colormode(255)\nturtle.color(255, 0, 0)\nturtle.circle(50)\nturtle.pencolor((0.0, 0.5, 1.0)) if False else None\n")
        self.assertEqual(r.colors(), {"red"})            # základní barvy se vrací jménem
        self.assertTrue(all(s[7] == "circle" for s in r.segments))
        self.assertAlmostEqual(r.length(), 2 * 3.14159 * 50, delta=8)
        self.assertEqual(r.corners(), [])

    def test_barvy_chyby_vec2d_clear_screen(self):
        r = self.run_prog("import turtle\nt = turtle.Turtle()\nt.pencolor('#FFF')\nt.forward(10)\nt.pencolor('#123456')\nt.forward(10)\n")
        self.assertEqual(sorted(r.colors()), ["#123456", "white"])
        r = self.run_prog("import turtle\nturtle.pencolor(255, 165, 0)\n")           # bez colormode(255) je to chyba jako v pravém turtle
        self.assertEqual(r.error["type"], "TurtleGraphicsError")
        r = self.run_prog("import turtle\nt = turtle.Turtle()\nt.goto(0, 0)\nt.forward(5)\nt.goto(5, 0)\nt.screen.bgcolor('black')\n"
                          "p = t.pos() + (1, 1)\nprint(p, abs(turtle.Vec2D(3, 4)))\nt.speed('fastest')\nt.speed(11)\n")
        self.assertEqual(len(r.segments), 1)                                           # úsečky nulové délky se nezapisují
        self.assertEqual(r.bgcolor, "black"); self.assertEqual(r.out, "(6.00,1.00) 5.0\n"); self.assertEqual(r.turtles[0]["speed"], 0)
        r = self.run_prog("import turtle\nt = turtle.Turtle()\nu = turtle.Turtle()\nt.forward(5)\nu.forward(7)\nt.clear()\n")
        self.assertEqual(len(r.segments), 1); self.assertEqual(r.segments[0][6], 1)

    def test_udalosti_a_casovac(self):
        code = ('import turtle\nt = turtle.Turtle()\ns = turtle.Screen()\n'
                'def nahoru(): t.sety(t.ycor() + 10)\n'
                'def tik():\n    t.forward(5)\n    s.ontimer(tik, 100)\n'
                's.onkey(nahoru, "Up")\ns.listen()\ns.ontimer(tik, 100)\ns.mainloop()\n')
        r = self.run_prog(code, keys=["Up", "Up"], ticks=3)
        self.assertEqual(r.handlers["onkey"], ["Up"])
        self.assertEqual(r.turtles[0]["y"], 20.0); self.assertEqual(r.turtles[0]["x"], 15.0)

    def test_chyba_a_nekonecna_smycka(self):
        r = self.run_prog("import turtle\nprint(1/0)\n")
        self.assertEqual(r.error["type"], "ZeroDivisionError")
        r = self.run_prog("import turtle\nwhile True:\n    turtle.forward(1)\n", max_ops=1000)
        self.assertTrue(r.ended); self.assertGreaterEqual(r.called("forward"), 1000)
        r = self.run_prog("while True:\n    pass\n", timeout=2)
        self.assertTrue(r.timed_out)

    def test_import_from(self):
        r = self.run_prog("from turtle import *\nforward(10)\nleft(90)\nforward(10)\nexitonclick()\n")
        self.assertEqual(r.length(), 20); self.assertEqual(r.turtles[0]["heading"], 90.0)


if __name__ == "__main__":
    unittest.main()
