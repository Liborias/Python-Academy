"""Meteority 6–10: samostatné modely, návaznost i skutečný SDL běh."""
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
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/pygame-2/lessons'
IDS=['06-meteority-hrac-a-smycka','07-meteority-proud-kamenu','08-meteority-zivoty-a-ochrana','09-meteority-skore-a-stit','10-meteority-pauza-a-restart']


class MeteorityTest(unittest.TestCase):
    def variants(self,index,wrong,correct):
        d=BASE/IDS[index];source=(d/'solution.py').read_text('utf-8')
        for expected,variants in [(False,wrong),(True,correct)]:
            for changes in variants:
                code=source
                for before,after in changes:
                    self.assertIn(before,code);code=code.replace(before,after)
                self.assertNotEqual(code,source)
                with self.subTest(lesson=index+6,expected=expected,changes=changes),tempfile.TemporaryDirectory() as temp:
                    result=run_check(d,code,ROOT/'lib',Path(temp))
                    self.assertNotIn('error',result,result);self.assertEqual(result['ok'],expected,result)

    def test_player_input_time_diagonal_precision_and_whole_ship_bounds(self):
        self.variants(0,[
            [('self.pozice += vektor * self.rychlost * dt','self.pozice += vektor * self.rychlost')],
            [('vektor = vektor.normalize()','vektor = vektor')],
            [('self.pozice += vektor * self.rychlost * dt','self.pozice += vektor * self.rychlost * dt\n        self.pozice.update(round(self.pozice.x),round(self.pozice.y))')],
            [('self.hranice.right - pul_sirky','self.hranice.right')],
            [('self.hranice = hranice.copy()','self.hranice = HRANICE.copy()')],
            [('int(klavesy[pygame.K_RIGHT]) - int(klavesy[pygame.K_LEFT])','int(klavesy[pygame.K_LEFT]) - int(klavesy[pygame.K_RIGHT])')],
            [('self.pozice = pygame.Vector2(stred)','self.pozice = stred')],
        ],[
            [('vektor = vektor.normalize()','vektor.normalize_ip()')],
            [('super().__init__()','pygame.sprite.Sprite.__init__(self)')],
            [('int(klavesy[pygame.K_RIGHT]) - int(klavesy[pygame.K_LEFT])','klavesy[pygame.K_RIGHT] - klavesy[pygame.K_LEFT]')],
        ])

    def test_stream_injected_rng_catchup_remainder_existing_motion_and_misses(self):
        self.variants(1,[
            [('self.pozice.y += self.rychlost * dt','self.pozice.y += dt')],
            [('self.pozice.y += self.rychlost * dt','self.pozice.y += self.rychlost')],
            [('self.rng = rng','self.rng = random.Random(7)')],
            [('while self.cas >= self.interval:','if self.cas >= self.interval:')],
            [('self.cas -= self.interval','self.cas = 0')],
            [('self.minulo += 1','self.minulo = 1')],
            [('meteorit.rect.top >= hranice.bottom','meteorit.rect.top > hranice.bottom')],
            [('meteorit.kill()','self.objekty.remove(meteorit)')],
            [('self.objekty.update(dt)','pass')],
        ],[
            [('self.objekty.update(dt)','for meteorit in self.objekty:\n            meteorit.update(dt)')],
            [('self.objekty.add(meteorit)','self.objekty.add([meteorit])')],
            [('self.pozice.y += self.rychlost * dt','self.pozice.y = self.pozice.y + self.rychlost * dt')],
        ])

    def test_health_immunity_batch_circle_hits_and_no_bogus_points(self):
        self.variants(2,[
            [('self.nezranitelnost = 0.0','self.nezranitelnost = ochrana')],
            [('max(0, self.nezranitelnost - dt)','self.nezranitelnost - dt')],
            [('self.zivoty == 0 or self.nezranitelnost > 0','self.zivoty == 0')],
            [('self.zivoty -= 1','self.zivoty -= 2')],
            [('proud.objekty, True, pygame.sprite.collide_circle','proud.objekty, False, pygame.sprite.collide_circle')],
            [(', pygame.sprite.collide_circle)',')')],
            [('return zdravi.zasah() if zasahy else False','return False')],
        ],[
            [('self.nezranitelnost = max(0, self.nezranitelnost - dt)','self.nezranitelnost -= min(self.nezranitelnost,dt)')],
            [('return zdravi.zasah() if zasahy else False','if zasahy:\n        return zdravi.zasah()\n    return False')],
            [('zasahy = pygame.sprite.spritecollide(hrac, proud.objekty, True, pygame.sprite.collide_circle)','zasahy = pygame.sprite.spritecollide(hrac, proud.objekty, False, pygame.sprite.collide_circle)\n    for kamen in zasahy:\n        kamen.kill()')],
        ])

    def test_round_score_bonus_timing_pickup_before_hit_shield_and_game_over(self):
        self.variants(3,[
            [('random.Random(seed)','random.Random(7)')],
            [('self.skore = self.proud.minulo','self.skore += self.proud.minulo')],
            [('while self.bonus_cas >= 6:','if self.bonus_cas >= 6:')],
            [('self.bonusy.update(dt)','pass')],
            [('bonus.kill()','self.bonusy.remove(bonus)')],
            [('self.stit = True','self.stit = False')],
            [('if zasahy and self.zdravi.nezranitelnost == 0:','if zasahy:')],
            [('if self.zdravi.zivoty == 0:','if False:')],
            [('self.zdravi.nezranitelnost = self.zdravi.ochrana','self.zdravi.nezranitelnost = 0')],
        ],[
            [('self.bonusy.update(dt)','for bonus in self.bonusy:\n            bonus.update(dt)')],
            [('self.skore = self.proud.minulo','self.skore = int(self.proud.minulo)')],
            [('self.zdravi.nezranitelnost == 0','not self.zdravi.nezranitelnost')],
        ])

    def test_game_pause_quit_restart_seed_and_old_world_preservation(self):
        self.variants(4,[
            [('self.bezi and not self.pauza and self.kolo.zdravi.zivoty > 0','self.bezi and self.kolo.zdravi.zivoty > 0')],
            [('self.kolo.update(smer, dt)','self.kolo.update(smer, 1)')],
            [('self.kolo = Kolo(self.seed)','self.kolo.proud.objekty.empty()\n                self.kolo = Kolo(self.seed)')],
            [('self.kolo = Kolo(self.seed)\n                self.pauza = False','self.kolo = Kolo(self.seed)')],
            [('udalost.key == pygame.K_r:','udalost.key == pygame.K_r and self.kolo.zdravi.zivoty == 0:')],
            [('udalost.type == pygame.KEYDOWN:','udalost.type in (pygame.KEYDOWN, pygame.KEYUP):')],
            [('self.bezi = False','self.bezi = not self.bezi')],
        ],[
            [('self.kolo = Kolo(self.seed)\n                self.pauza = False','self.kolo, self.pauza = Kolo(self.seed), False')],
            [('not self.pauza','self.pauza is False')],
            [('self.pauza = not self.pauza','self.pauza = not bool(self.pauza)')],
        ])

    def test_standalone_gui_entrypoint_and_import_guard_are_required(self):
        source=(BASE/IDS[4]/'solution.py').read_text()
        code=source.split('# Okno se otevírá')[0]
        with tempfile.TemporaryDirectory() as temp:
            result=run_check(BASE/IDS[4],code,ROOT/'lib',Path(temp))
            self.assertNotIn('error',result,result);self.assertFalse(result['ok'],result)

    def test_scope_helper_snapshots_and_exact_possible_solutions(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(course['modules'][-1]['lessons'],IDS)
        previous={}
        for i,lid in enumerate(IDS):
            d=BASE/lid;view=lesson_view(ROOT/'courses','pygame-2',lid)
            self.assertEqual((view['kind'],view['run_timeout'],len(view['examples']),len(view['tasks']),len(view['quiz'])),('gui',600,0,0,3))
            self.assertTrue(view['preview_images'])
            self.assertEqual(solution_view(ROOT/'courses','pygame-2',lid)['code'],(d/'solution.py').read_text())
            self.assertEqual((d/'example.py').read_bytes(),(d/'solution.py').read_bytes())
            if i:
                helpers={n.name:ast.dump(n) for n in ast.parse((d/'files/predchozi.py').read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
                self.assertEqual(helpers,previous)
            previous.update({n.name:ast.dump(n) for n in ast.parse((d/'solution.py').read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))})
            for name in ['podklady.py','sestava.py','herni_okno.py']:
                self.assertEqual((d/'files'/name).read_bytes(),(BASE/IDS[0]/'files'/name).read_bytes())

    def test_real_sdl_quit_saves_png_and_all_teaching_snippets_run(self):
        from PIL import Image
        count=0
        for lid in IDS:
            d=BASE/lid
            with self.subTest(lesson=lid),tempfile.TemporaryDirectory() as temp:
                work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
                before={p.name:p.read_bytes() for p in work.glob('*.py')}
                (work/'main.py').write_bytes((d/'solution.py').read_bytes())
                (work/'spec.json').write_text(json.dumps({'frames':80,'events':{'59':[{'type':'QUIT'}]},'colors':[[235,145,75,0,0,640,70],[235,145,75,20,70,600,390]]}))
                p=subprocess.run([sys.executable,str(ROOT/'lib/dilna_check/pgrun.py'),'main.py','spec.json','out.json'],cwd=work,capture_output=True,text=True,timeout=15)
                self.assertEqual(p.returncode,0,p.stderr)
                result=json.loads((work/'out.json').read_text())
                self.assertIsNone(result['error']);self.assertTrue(result['ended']);self.assertEqual(result['frames'],60)
                self.assertTrue(all(s['colors']['235,145,75@0,0,640,70']==0 for s in result['shots']), 'Kameny nesmějí překrývat informační pruh.')
                if lid != IDS[0]:self.assertGreater(result['shots'][-1]['colors']['235,145,75@20,70,600,390'],0,'Po vzniku musí být skutečný kámen vidět na ploše.')
                with Image.open(work/'meteority.png') as img:img.load();self.assertEqual((img.format,img.size),('PNG',(640,480)))
                for name,content in before.items():self.assertEqual((work/name).read_bytes(),content)
                for code in re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S):
                    (work/'snippet.py').write_text(code,encoding='utf-8')
                    p=subprocess.run([sys.executable,'-X','utf8','snippet.py'],cwd=work,capture_output=True,text=True,timeout=10,env=dict(os.environ,PYGAME_HIDE_SUPPORT_PROMPT='1',SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'))
                    self.assertEqual(p.returncode,0,p.stdout+p.stderr);count+=1
        self.assertEqual(count,5)


if __name__=='__main__':unittest.main()
