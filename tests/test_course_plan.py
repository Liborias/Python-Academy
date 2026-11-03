"""Samostatný OOP kurz je zatím jen oddělený plán, ne hotové lekce."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.content import course_view


class CoursePlanTest(unittest.TestCase):
    def test_standalone_outline_only(self):
        catalog = json.loads((ROOT/'courses/catalog.json').read_text('utf-8'))['courses']
        entry = next(c for c in catalog if c['id']=='oop')
        self.assertEqual(entry['status'], 'concept')
        self.assertEqual(entry['lessons'], 0)
        self.assertEqual(entry['planned_lessons'], 20)
        self.assertEqual(entry['level'], 3)
        self.assertEqual(entry['doporuceno'], ['zaklady'])
        self.assertEqual(catalog[1]['id'], 'zaklady')
        self.assertEqual(catalog[2]['id'], 'oop')
        course = course_view(ROOT/'courses', 'oop')
        self.assertEqual(course['modules'], [])
        self.assertEqual(course['learning_plan']['level'], 3)
        self.assertIn('expediční', course['learning_plan']['title'])
        self.assertIn('cosmicpython/code', course['learning_plan']['md'])
        self.assertEqual(course['learning_plan']['md'], (ROOT/'courses/oop/plan.md').read_text('utf-8'))
        self.assertEqual(list((ROOT/'courses/oop/lessons').glob('*/lesson.json')), [])
        self.assertEqual(list((ROOT/'courses/oop').rglob('*.py')), [])

    def test_combined_course_keeps_its_lessons(self):
        course = course_view(ROOT/'courses', 'turtle-oop')
        ids = [lesson['id'] for module in course['modules'] for lesson in module['lessons']]
        self.assertEqual(len(ids), 24)
        self.assertIn('17-trida-a-instance', ids)
        self.assertIn('24-super-a-rozsireni', ids)
        self.assertNotIn('learning_plan', course)
        self.assertNotIn('learning_plan', course_view(ROOT/'courses', 'zaklady'))


if __name__=='__main__':
    unittest.main()
