"""Samostatný OOP kurz má vlastní osnovu a první výukový modul."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.content import course_view


class CoursePlanTest(unittest.TestCase):
    def test_standalone_outline_and_first_module(self):
        catalog = json.loads((ROOT/'courses/catalog.json').read_text('utf-8'))['courses']
        entry = next(c for c in catalog if c['id']=='oop')
        self.assertEqual(entry['status'], 'draft')
        self.assertEqual(entry['lessons'], 20)
        self.assertEqual(entry['planned_lessons'], 20)
        self.assertEqual(entry['level'], 3)
        self.assertEqual(entry['doporuceno'], ['zaklady'])
        self.assertEqual(catalog[1]['id'], 'zaklady')
        self.assertEqual(catalog[2]['id'], 'oop')
        course = course_view(ROOT/'courses', 'oop')
        self.assertGreaterEqual(len(course['modules']), 1)
        self.assertEqual(course['modules'][0]['id'], 'm01')
        ids = [lesson['id'] for lesson in course['modules'][0]['lessons']]
        self.assertEqual(len(ids), 4)
        self.assertEqual(course['learning_plan']['status'], 'draft')
        self.assertEqual(course['learning_plan']['level'], 3)
        self.assertIn('expediční', course['learning_plan']['title'])
        self.assertIn('cosmicpython/code', course['learning_plan']['md'])
        self.assertEqual(course['learning_plan']['md'], (ROOT/'courses/oop/plan.md').read_text('utf-8'))
        self.assertGreaterEqual(len(list((ROOT/'courses/oop/lessons').glob('*/lesson.json'))), 4)
        self.assertIn('Modul 1', course['learning_plan']['md'])
        combined_ids = [lesson['id'] for module in course_view(ROOT/'courses', 'turtle-oop')['modules'] for lesson in module['lessons']]
        self.assertFalse(set(ids) & set(combined_ids))

    def test_combined_course_keeps_its_lessons(self):
        course = course_view(ROOT/'courses', 'turtle-oop')
        ids = [lesson['id'] for module in course['modules'] for lesson in module['lessons']]
        self.assertEqual(len(ids), 40)
        self.assertIn('17-trida-a-instance', ids)
        self.assertIn('24-super-a-rozsireni', ids)
        self.assertNotIn('learning_plan', course)
        self.assertNotIn('learning_plan', course_view(ROOT/'courses', 'zaklady'))


if __name__=='__main__':
    unittest.main()
