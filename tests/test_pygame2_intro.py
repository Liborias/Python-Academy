"""Pygame 2: skutečné objekty, různé správné zápisy a typické herní chyby."""
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
BASE = ROOT / 'courses/pygame-2/lessons'
IDS = ['01-sprite-obraz-a-poloha', '02-pohyb-vektor-a-cas', '03-skupiny-update-a-draw', '04-kolize-a-pravidla-zasahu', '05-stav-hry-pauza-a-restart']


class Pygame2IntroTest(unittest.TestCase):
    def directory(self, stage, task):
        d = BASE / IDS[stage]
        return d if task == 0 else d / 'tasks' / f'task-{task + 1}'

    def changed(self, stage, task, replacements):
        d = self.directory(stage, task)
        source = (d / 'solution.py').read_text('utf-8')
        changed = source
        for before, after in replacements:
            self.assertIn(before, changed)
            changed = changed.replace(before, after)
        self.assertNotEqual(changed, source)
        return d, changed

    def variants(self, stage, variants):
        for task, (wrong, correct) in enumerate(variants):
            for expected, changes in [(False, wrong), (True, correct)]:
                for replacements in changes:
                    directory, code = self.changed(stage, task, replacements)
                    with self.subTest(stage=stage, task=task, expected=expected, changes=replacements), tempfile.TemporaryDirectory() as temp:
                        result = run_check(directory, code, ROOT / 'lib', Path(temp))
                        self.assertNotIn('error', result, result)
                        self.assertEqual(result['ok'], expected, result)

    def test_sprite_geometry_pixels_identity_and_source_preservation(self):
        self.variants(0, [
            ([[('get_rect(center=stred)', 'get_rect(topleft=stred)')], [('self.image.fill((80, 180, 255))', 'self.image.fill((255, 0, 0))')], [('class Lod(pygame.sprite.Sprite):', 'def Lod(stred):\n    return ZakladSprite(stred)\n\nclass NepouzitaLod(pygame.sprite.Sprite):')]],
             [[('super().__init__()', 'pygame.sprite.Sprite.__init__(self)')]]),
            ([[('pygame.SRCALPHA)', '0)')]], [[('self.image.get_rect(center=stred)', 'self.image.get_rect(center=tuple(stred))')]]),
            ([[('pygame.Surface(velikost, pygame.SRCALPHA)', 'pygame.Surface((32, 24), pygame.SRCALPHA)')], [('self.image.fill(barva)', 'barva[0] = 111\n        self.image.fill(barva)')]],
             [[('self.image.fill(barva)', 'self.image.fill(tuple(barva))')]]),
            ([[('self.image = obrazek.copy()', 'self.image = obrazek')], [('self.image = obrazek.copy()', 'obrazek.fill((1, 2, 3))\n        self.image = obrazek.copy()')]],
             [[('obrazek.copy()', 'obrazek.subsurface(obrazek.get_rect()).copy()')]]),
            ([[('super().__init__(skupina)', 'super().__init__()')]], [[('super().__init__(skupina)', 'super().__init__()\n        skupina.add(self)')]]),
        ])

    def test_motion_time_fractional_steps_normalization_bounds_and_target(self):
        self.variants(1, [
            ([[('self.rychlost * dt', 'self.rychlost')], [('self.pozice += self.rychlost * dt', 'self.pozice += self.rychlost * dt\n        self.pozice.update(round(self.pozice.x), round(self.pozice.y))')], [('self.pozice = pygame.Vector2(stred)', 'self.pozice = stred')]],
             [[('self.pozice += self.rychlost * dt', 'self.pozice.update(self.pozice + self.rychlost * dt)')]]),
            ([[('vektor = vektor.normalize()', 'vektor = vektor')], [('if vektor.length_squared() > 0:', 'if True:')]],
             [[('vektor = vektor.normalize()', 'vektor.normalize_ip()')]]),
            ([[('self.hranice.right - 16', 'self.hranice.right')], [('self.pozice.x = max(', 'self.pozice.update(round(self.pozice.x), round(self.pozice.y))\n        self.pozice.x = max(')]],
             [[('self.pozice += self.rychlost * dt', 'self.pozice = self.pozice + self.rychlost * dt')]]),
            ([[('self.rychlost += self.zrychleni * dt\n        self.pozice += self.rychlost * dt', 'self.pozice += self.rychlost * dt\n        self.rychlost += self.zrychleni * dt')]],
             [[('self.rychlost += self.zrychleni * dt', 'self.rychlost = self.rychlost + self.zrychleni * dt')]]),
            ([[('self.pozice = self.cil.copy()', 'self.pozice += rozdil * 2')]],
             [[('if vzdalenost <= krok:\n            self.pozice = self.cil.copy()\n        elif vzdalenost > 0:\n            self.pozice += rozdil / vzdalenost * krok', 'self.pozice.move_towards_ip(self.cil, krok)')]]),
        ])

    def test_groups_sorted_report_real_drawing_kill_and_shared_membership(self):
        self.variants(2, [
            ([[('return sorted(objekt.rect.center for objekt in skupina)', 'return [objekt.rect.center for objekt in skupina]')], [('skupina.update(dt)', 'skupina.update(1)')]],
             [[('skupina.update(dt)', 'for objekt in skupina:\n        objekt.update(dt)')]]),
            ([[('pozadi.copy()', 'pozadi')]], [[('skupina.draw(vysledek)', 'for objekt in skupina:\n        vysledek.blit(objekt.image, objekt.rect)')]]),
            ([[('objekt.kill()', 'skupina.remove(objekt)')]],
             [[('objekt.kill()', 'for clenstvi in objekt.groups():\n                clenstvi.remove(objekt)')]]),
            ([[('isinstance(objekt, typ)', 'type(objekt) is typ')]],
             [[('return pygame.sprite.Group(objekt for objekt in skupina if isinstance(objekt, typ))', 'vyber = [objekt for objekt in skupina if isinstance(objekt, typ)]\n    return pygame.sprite.Group(vyber)')]]),
            ([[('return pygame.sprite.Group(prvni, druha)', 'return pygame.sprite.Group({objekt.rect.center:objekt for objekt in [*prvni,*druha]}.values())')]],
             [[('return pygame.sprite.Group(prvni, druha)', 'vysledek = pygame.sprite.Group()\n    vysledek.add(prvni)\n    vysledek.add(druha)\n    return vysledek')]]),
        ])

    def test_collisions_edges_actual_objects_removal_and_circle_rule(self):
        self.variants(3, [
            ([[('return pygame.sprite.spritecollide(hrac, nepratele, False)', 'return list(nepratele)')]],
             [[('return pygame.sprite.spritecollide(hrac, nepratele, False)', 'return [o for o in nepratele if o.rect.colliderect(hrac.rect)]')]]),
            ([[('bonusy, True)', 'bonusy, False)')], [('sum(bonus.hodnota for bonus in chycené)', 'len(chycené)')]],
             [[('chycené = pygame.sprite.spritecollide(hrac, bonusy, True)', 'chycené = [o for o in bonusy if o.rect.colliderect(hrac.rect)]\n    for o in chycené:\n        o.kill()')]]),
            ([[('return pygame.sprite.spritecollideany(hrac, nepratele)', 'return bool(pygame.sprite.spritecollideany(hrac, nepratele))')]],
             [[('return pygame.sprite.spritecollideany(hrac, nepratele)', 'return next((o for o in nepratele if o.rect.colliderect(hrac.rect)), None)')]]),
            ([[('strely, nepratele, False, False', 'strely, nepratele, True, True')]],
             [[('return pygame.sprite.groupcollide(strely, nepratele, False, False)', 'return {s: shody for s in strely if (shody := [o for o in nepratele if s.rect.colliderect(o.rect)])}')]]),
            ([[(', pygame.sprite.collide_circle)', ')')]],
             [[('return pygame.sprite.spritecollide(hrac, nepratele, False, pygame.sprite.collide_circle)', 'return [o for o in nepratele if (o.rect.centerx-hrac.rect.centerx)**2 + (o.rect.centery-hrac.rect.centery)**2 <= (o.radius+hrac.radius)**2]')]]),
        ])

    def test_game_state_repeated_events_timer_and_independent_restart(self):
        self.variants(4, [
            ([[('if self.bezi and not self.pauza:', 'if self.bezi:')], [('if udalost.type == pygame.QUIT:', 'if udalost.type == pygame.QUIT and not self.pauza:')]],
             [[('self.pauza = not self.pauza', 'self.pauza = not bool(self.pauza)')]]),
            ([[('return pred > 0 and self.zbyva == 0', 'return self.zbyva == 0')]],
             [[('self.zbyva = max(0, self.zbyva - dt)', 'self.zbyva -= min(self.zbyva, dt)')]]),
            ([[('self.zbyva = max(0, self.zbyva - 1)', 'self.zbyva -= 1')]],
             [[('self.zbyva = max(0, self.zbyva - 1)', 'if self.zbyva > 0:\n            self.zbyva -= 1')]]),
            ([[("if self.stav == 'menu' and udalost.key == pygame.K_RETURN:", 'if udalost.key == pygame.K_RETURN:')]],
             [[("self.stav = 'pauza' if self.stav == 'hra' else 'hra'", "self.stav = {'hra':'pauza', 'pauza':'hra'}[self.stav]")]]),
            ([[('def restart(self):\n        self.objekty = self.tvorba()', 'def restart(self):\n        self.objekty.empty()\n        self.objekty = self.tvorba()')]],
             [[('def restart(self):\n        self.objekty = self.tvorba()\n        self.skore = 0', 'def restart(self):\n        self.objekty, self.skore = self.tvorba(), 0')]]),
        ])

    def test_course_scope_solution_api_and_exact_previous_motion(self):
        data = json.loads((BASE.parent / 'course.json').read_text())
        self.assertEqual(data['modules'][0]['lessons'], IDS)
        entry = next(c for c in json.loads((ROOT / 'courses/catalog.json').read_text())['courses'] if c['id'] == 'pygame-2')
        self.assertEqual((entry['status'], entry['planned_lessons'], entry['level']), ('draft', 30, 4))
        previous = next(n for n in ast.parse((BASE / IDS[1] / 'solution.py').read_text()).body if isinstance(n, ast.ClassDef))
        for i, lid in enumerate(IDS):
            d = BASE / lid
            view = lesson_view(ROOT / 'courses', 'pygame-2', lid)
            self.assertEqual((view['kind'], len(view['examples']), len(view['tasks']), len(view['quiz'])), ('console', 2, 4, 3))
            self.assertTrue(view['preview_images'])
            for task in range(5):
                target = self.directory(i, task)
                self.assertEqual(solution_view(ROOT / 'courses', 'pygame-2', lid, f'task-{task+1}')['code'], (target / 'solution.py').read_text('utf-8'))
                if i >= 2:
                    copied = next(n for n in ast.parse((target / 'files/pohyb.py').read_text()).body if isinstance(n, ast.ClassDef))
                    self.assertEqual(ast.dump(previous), ast.dump(copied))

    def test_all_standalone_solutions_examples_and_teaching_snippets(self):
        from PIL import Image
        count = 0
        for i, lid in enumerate(IDS):
            d = BASE / lid
            for task in range(5):
                target = self.directory(i, task)
                codes = [(target / 'solution.py').read_text('utf-8')]
                if task == 0:
                    codes += [e['code'] for e in json.loads((d / 'examples.json').read_text())]
                    codes += re.findall(r'```python\n(.*?)```', (d / 'lesson.md').read_text(), re.S)
                for index, code in enumerate(codes):
                    with self.subTest(lesson=lid, task=task, code=index), tempfile.TemporaryDirectory() as temp:
                        work = Path(temp); shutil.copytree(target / 'files', work, dirs_exist_ok=True)
                        originals = {p.relative_to(work): p.read_bytes() for p in work.rglob('*.py')}
                        (work / 'main.py').write_text(code, encoding='utf-8')
                        result = subprocess.run([sys.executable, '-X', 'utf8', 'main.py'], cwd=work, capture_output=True, text=True, timeout=15,
                                                env=dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', PYGAME_HIDE_SUPPORT_PROMPT='1'))
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                        if index == 0 or (task == 0 and index < 3):
                            with Image.open(work / 'nahled.png') as image:
                                image.load(); self.assertEqual((image.format, image.size), ('PNG', (640, 360)))
                        for name, content in originals.items():self.assertEqual((work / name).read_bytes(), content)
                        count += 1
        self.assertEqual(count, 40)  # 25 řešení, deset dalších ukázek a pět úryvků výkladu.


if __name__ == '__main__':
    unittest.main()
