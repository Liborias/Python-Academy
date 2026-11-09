"""Chyť robota 11–15: jiné správné zápisy, chyby, návaznost a reálné SDL."""
import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check
from server.content import lesson_view, solution_view

BASE = ROOT/'courses/pygame-2/lessons'
IDS = ['11-roboti-cil-a-kliknuti','12-roboti-ruzne-pohyby','13-roboti-zasahy-a-body','14-roboti-cas-a-vlny','15-roboti-nabidka-a-restart']


class RobotiTest(unittest.TestCase):
    def variants(self, index, wrong, correct):
        directory = BASE/IDS[index]
        source = (directory/'solution.py').read_text('utf-8')
        for expected, cases in [(False, wrong), (True, correct)]:
            for replacements in cases:
                code = source
                for before, after in replacements:
                    self.assertIn(before, code)
                    code = code.replace(before, after)
                with self.subTest(lesson=index+11, expected=expected, replacements=replacements), tempfile.TemporaryDirectory() as temp:
                    result = run_check(directory, code, ROOT/'lib', Path(temp))
                    self.assertNotIn('error', result, result)
                    self.assertEqual(result['ok'], expected, result)

    def test_circles_rounded_centres_sources_identity_and_topmost_selection(self):
        self.variants(0, [
            [('self.radius = polomer', 'self.radius = 22')],
            [('self.pozice = pygame.Vector2(stred)', 'self.pozice = stred')],
            [('return rozdil.length_squared() <= self.radius ** 2', 'return self.rect.collidepoint(bod)')],
            [('pygame.Vector2(bod) - self.rect.center', 'pygame.Vector2(bod) - self.pozice')],
            [('reversed(roboty.sprites())', 'roboty.sprites()')],
            [('return robot\n', 'return Robot(robot.rect.center)\n')],
            [('return robot\n', 'robot.kill()\n            return robot\n')],
        ], [
            [('rozdil.length_squared() <= self.radius ** 2', 'rozdil.length() <= self.radius')],
            [('super().__init__()', 'pygame.sprite.Sprite.__init__(self)')],
            [('reversed(roboty.sprites())', 'roboty.sprites()[::-1]')],
        ])

    def test_movement_time_all_boundaries_bounce_and_sine_anchor(self):
        self.variants(1, [
            [('self.rychlost = pygame.Vector2(rychlost)', 'self.rychlost = rychlost')],
            [('self.pozice += self.rychlost * dt', 'self.pozice += self.rychlost')],
            [('self.pozice += self.rychlost * dt', 'self.pozice += self.rychlost * dt\n        self.pozice.update(round(self.pozice.x), round(self.pozice.y))')],
            [('self.rychlost.x = -abs(self.rychlost.x)', 'self.rychlost.x = abs(self.rychlost.x)')],
            [('self.rychlost.y = abs(self.rychlost.y)', 'self.rychlost.y = -abs(self.rychlost.y)')],
            [('self.kotva = pygame.Vector2(stred)', 'self.kotva = stred')],
            [('self.cas += dt', 'self.cas = dt')],
            [('self.kotva.x + self.amplituda', 'self.pozice.x + self.amplituda')],
            [('self.cas / self.perioda', 'self.cas / 2')],
        ], [
            [('self.pozice += self.rychlost * dt', 'self.pozice.update(self.pozice.x + self.rychlost.x * dt, self.pozice.y + self.rychlost.y * dt)')],
            [('self.cas += dt', 'self.cas = self.cas + dt')],
            [('self.kotva = pygame.Vector2(stred)', 'self.kotva = self.pozice.copy()')],
        ])

    def test_events_single_target_kill_memberships_points_accuracy_and_death(self):
        self.variants(2, [
            [('self.roboty = pygame.sprite.Group(roboty)', 'self.roboty = roboty')],
            [('udalost.type != pygame.MOUSEBUTTONDOWN', 'udalost.type != pygame.MOUSEBUTTONUP')],
            [('udalost.button != 1', 'udalost.button != 3')],
            [('self.zivoty == 0 or not self.roboty', 'not self.roboty')],
            [('self.zivoty == 0 or not self.roboty', 'self.zivoty == 0')],
            [('self.skore += robot.body', 'self.skore += 10')],
            [('robot.kill()', 'self.roboty.remove(robot)')],
            [('self.zivoty -= 1', 'self.zivoty -= 2')],
            [('100 * self.zasahy / self.pokusy', 'round(100 * self.zasahy / self.pokusy)')],
        ], [
            [('self.roboty = pygame.sprite.Group(roboty)', 'self.roboty = pygame.sprite.Group()\n        self.roboty.add(roboty)')],
            [('self.skore += robot.body', 'self.skore = self.skore + robot.body')],
            [('return 100 * self.zasahy / self.pokusy if self.pokusy else 0.0', 'if not self.pokusy:\n            return 0.0\n        return self.zasahy / self.pokusy * 100')],
        ])

    def test_waves_rng_progress_caps_preserved_counts_and_deadline(self):
        self.variants(3, [
            [('random.Random(seed)', 'random.Random(11)')],
            [('if self.konec or self.lov.roboty:', 'if self.konec:')],
            [('self.cislo += 1', 'self.cislo += 1\n        self.lov.skore = 0')],
            [('min(2 + self.cislo, 6)', '2 + self.cislo')],
            [('min(80 + 15 * (self.cislo - 1), 220)', '80 + 15 * (self.cislo - 1)')],
            [('max(0.7, 2 - 0.15 * (self.cislo - 1))', '2')],
            [('max(0, self.zbyva - dt)', 'self.zbyva - dt')],
            [('self.lov.roboty.update(dt, self.hranice)', 'pass')],
            [('if self.konec:\n            return None', 'if False:\n            return None')],
        ], [
            [('self.lov.roboty.update(dt, self.hranice)', 'for robot in self.lov.roboty:\n                robot.update(dt, self.hranice)')],
            [('self.cislo += 1', 'self.cislo = self.cislo + 1')],
            [('self.hranice = HRANICE.copy()', 'self.hranice = pygame.Rect(HRANICE)')],
            [('max(0.7, 2 - 0.15 * (self.cislo - 1))', 'max(0.7, (200 - 15 * (self.cislo - 1)) / 100)')],
        ])

    def test_menu_pause_result_restart_old_world_and_shutdown(self):
        self.variants(4, [
            [("self.stav = 'nabidka'", "self.stav = 'hra'")],
            [('Kolo(self.seed)', 'Kolo(11)')],
            [("self.bezi and self.stav == 'hra'", "self.bezi and self.stav in ('hra', 'pauza')")],
            [('self.kolo.update(dt)', 'self.kolo.update(1)')],
            [('if not self.bezi:', 'if False:')],
            [("elif self.stav == 'hra':", "elif self.stav in ('hra', 'pauza'):")],
            [('self.kolo = Kolo(self.seed)', 'if self.kolo is not None:\n            self.kolo.lov.roboty.empty()\n        self.kolo = Kolo(self.seed)')],
            [("self.stav == 'vysledek':", "self.stav == 'nikdy':")],
        ], [
            [('self.kolo = Kolo(self.seed)', 'self.kolo = Kolo(seed=self.seed)')],
            [("'pauza' if self.stav == 'hra' else 'hra'", "{'hra': 'pauza', 'pauza': 'hra'}[self.stav]")],
            [("self.bezi and self.stav == 'hra'", "self.stav == 'hra' and self.bezi")],
        ])

    def test_gui_entrypoint_and_import_guard(self):
        source = (BASE/IDS[-1]/'solution.py').read_text()
        for code in [source.split('# GUI se spouští')[0], source.replace('class Hra:', 'pygame.display.init()\npygame.display.set_mode((1, 1))\n\nclass Hra:')]:
            with self.subTest(code=code[:80]), tempfile.TemporaryDirectory() as temp:
                result = run_check(BASE/IDS[-1], code, ROOT/'lib', Path(temp))
                self.assertNotIn('error', result, result)
                self.assertFalse(result['ok'], result)

    def test_scope_previous_models_helpers_and_exact_solutions(self):
        course = json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id'] == 'm03')['lessons'], IDS)
        previous = {}
        for index, lid in enumerate(IDS):
            directory = BASE/lid
            view = lesson_view(ROOT/'courses', 'pygame-2', lid)
            self.assertEqual((view['kind'], view['run_timeout'], len(view['examples']), len(view['tasks']), len(view['quiz'])), ('gui', 600, 0, 0, 3))
            self.assertTrue(view['preview_images'])
            self.assertEqual(solution_view(ROOT/'courses', 'pygame-2', lid)['code'], (directory/'solution.py').read_text())
            self.assertEqual((directory/'example.py').read_bytes(), (directory/'solution.py').read_bytes())
            if index:
                snapshot = {n.name: ast.dump(n) for n in ast.parse((directory/'files/predchozi.py').read_text()).body if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
                self.assertEqual(snapshot, previous)
            previous.update({n.name: ast.dump(n) for n in ast.parse((directory/'solution.py').read_text()).body if isinstance(n, (ast.ClassDef, ast.FunctionDef))})
            for name in ['podklady.py', 'sestava.py', 'herni_okno.py']:
                self.assertEqual((directory/'files'/name).read_bytes(), (BASE/IDS[0]/'files'/name).read_bytes())

    def run_sdl(self, directory, source, spec):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            shutil.copytree(directory/'files', work, dirs_exist_ok=True)
            originals = {p.name: p.read_bytes() for p in work.glob('*.py')}
            (work/'main.py').write_text(source, encoding='utf-8')
            (work/'spec.json').write_text(json.dumps(spec), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'lib/dilna_check/pgrun.py'), 'main.py', 'spec.json', 'out.json'], cwd=work, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((work/'out.json').read_text())
            self.assertIsNone(data['error'], data)
            self.assertTrue(data['ended'], data)
            png = (work/'roboti.png').read_bytes()
            self.assertTrue(png.startswith(b'\x89PNG\r\n\x1a\n'))
            import struct
            self.assertEqual(struct.unpack('>II', png[16:24]), (720, 520))
            for name, content in originals.items():
                self.assertEqual((work/name).read_bytes(), content)
            return data

    def test_real_sdl_click_quit_png_and_standalone_teaching_snippets(self):
        count = 0
        for index, lid in enumerate(IDS):
            directory = BASE/lid
            with self.subTest(lesson=lid):
                events = {'9': [{'type': 'QUIT'}]}
                if index == 4:
                    events['0'] = [{'type': 'KEYDOWN', 'key': 'K_SPACE'}]
                data = self.run_sdl(directory, (directory/'solution.py').read_text(), {'frames': 20, 'events': events})
                self.assertEqual(data['frames'], 10)
                self.assertTrue(any(t['text'].startswith('Body: ') for t in data['texts']))
                with tempfile.TemporaryDirectory() as temp:
                    work = Path(temp)
                    shutil.copytree(directory/'files', work, dirs_exist_ok=True)
                    for snippet in re.findall(r'```python\n(.*?)```', (directory/'lesson.md').read_text(), re.S):
                        (work/'snippet.py').write_text(snippet, encoding='utf-8')
                        result = subprocess.run([sys.executable, '-X', 'utf8', 'snippet.py'], cwd=work, capture_output=True, text=True, timeout=10, env=dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy'))
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                        count += 1
        self.assertEqual(count, 5)

    def test_actual_loop_expires_before_click_in_the_same_frame(self):
        from random import Random
        rng = Random(11)
        for i in range(3):
            point = (rng.randint(114, 606), rng.randint(118, 434))
            if i % 2 == 0:
                rng.choice((-1, 1))
        for index in [3, 4]:
            directory = BASE/IDS[index]
            source = (directory/'solution.py').read_text()
            source = source.replace('Kolo=Kolo)', 'Kolo=lambda: Kolo(limit=.01))') if index == 3 else source.replace('Kolo(self.seed)', 'Kolo(self.seed, limit=.01)')
            events = {'1': [{'type': 'MOUSEBUTTONDOWN', 'button': 1, 'pos': point}], '3': [{'type': 'QUIT'}]}
            if index == 4:
                events['0'] = [{'type': 'KEYDOWN', 'key': 'K_SPACE'}]
            data = self.run_sdl(directory, source, {'frames': 10, 'events': events})
            texts = [t['text'] for t in data['texts']]
            self.assertIn('ČAS VYPRŠEL', texts)
            self.assertNotIn('Body: 10', texts)


if __name__ == '__main__':
    unittest.main()
