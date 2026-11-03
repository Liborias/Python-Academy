"""Pygame bez okna: dilna_check.pygame_run."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    import pygame  # noqa: F401
    HAVE = True
except ImportError:
    HAVE = False

PROG = '''import pygame
pygame.init()
screen = pygame.display.set_mode((320, 200))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
x = 100
running = True
font = pygame.font.Font(None, 30)
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            x += 50
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        x -= 10
    screen.fill((10, 20, 30))
    pygame.draw.circle(screen, (255, 0, 0), (x, 100), 20)
    screen.blit(font.render("Skore 5", True, (255, 255, 255)), (5, 5))
    pygame.display.flip()
    clock.tick(60)
print("konec")
'''


@unittest.skipUnless(HAVE, "pygame-ce není nainstalován")
class PgRunTest(unittest.TestCase):
    def run_prog(self, code, **kw):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "reseni.py").write_text(code, encoding="utf-8")
        env = dict(os.environ, DILNA_STUDENT=str(tmp / "reseni.py"), DILNA_RESULT=str(tmp / "r.json"), DILNA_DATA=str(tmp))
        sys.path.insert(0, str(ROOT / "lib"))
        old = dict(os.environ)
        os.environ.update(env)
        try:
            from dilna_check import check
            return check().pygame_run(**kw)
        finally:
            sys.path.pop(0)
            os.environ.clear(); os.environ.update(old)

    def test_udalosti_pixely_a_konec(self):
        r = self.run_prog(PROG, frames=6, pixels=[(100, 100)], colors=[(255, 0, 0)],
                          events={1: [{"type": "KEYDOWN", "key": "K_RIGHT"}], 4: [{"type": "QUIT"}]}, held={2: ["K_LEFT"]})
        self.assertIsNone(r.error)
        self.assertEqual(r.size, [320, 200]); self.assertEqual(r.caption, "Test")
        self.assertTrue(r.ended); self.assertEqual(r.frames, 5)
        self.assertEqual(r.pixel((100, 100), 0), (255, 0, 0))
        self.assertEqual(r.pixel((100, 100), 1), (10, 20, 30))      # po stisku doprava je kruh na x=150
        self.assertEqual(r.drew("circle")[1]["args"][1], [150, 100])
        self.assertEqual(r.drew("circle")[2]["args"][1], [140, 100])  # držená šipka vlevo
        self.assertTrue(r.rendered("Skore")); self.assertGreater(r.color_count((255, 0, 0), 0), 1000)
        self.assertEqual(r.out, "konec\n")

    def test_barvy_v_casti_okna(self):
        r = self.run_prog(PROG, frames=1, colors=[(255, 0, 0, 0, 0, 160, 200), (255, 0, 0, 160, 0, 160, 200)])
        self.assertGreater(r.color_count((255, 0, 0), 0, (0, 0, 160, 200)), 1000)     # kruh je vlevo od středu okna
        self.assertEqual(r.color_count((255, 0, 0), 0, (160, 0, 160, 200)), 0)

    def test_zastaveno_po_poctu_snimku(self):
        r = self.run_prog(PROG, frames=3)
        self.assertFalse(r.ended); self.assertEqual(r.frames, 3)

    def test_chyba_a_nekonecna_smycka(self):
        r = self.run_prog("import pygame\nprint(1/0)\n", frames=2)
        self.assertEqual(r.error["type"], "ZeroDivisionError"); self.assertEqual(r.error["line"], 2)
        r = self.run_prog("while True:\n    pass\n", frames=2, timeout=2)
        self.assertTrue(r.timed_out)

    def test_pg_no_error_hlasky(self):
        sys.path.insert(0, str(ROOT / "lib"))
        try:
            from dilna_check import check, PgResult
        finally:
            sys.path.pop(0)
        tmp = Path(tempfile.mkdtemp())
        os.environ.update(DILNA_STUDENT=str(tmp / "a.py"), DILNA_RESULT=str(tmp / "r.json"))
        c = check()
        self.assertFalse(c.pg_no_error(PgResult(timed_out=True)))
        self.assertIn("flip", c.results[-1]["msg"])
        self.assertTrue(c.pg_no_error(PgResult(frames=2)))


if __name__ == "__main__":
    unittest.main()
