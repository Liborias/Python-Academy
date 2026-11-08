"""Přepínatelné příklady: API, vyhrazený rozsah a odhalení rozbitého obsahu."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.content import lesson_view
from tools import validate_courses as validator


class ExamplesTest(unittest.TestCase):
    def test_scope_and_api(self):
        count = 0
        for path in (ROOT / 'courses').glob('*/lessons/*/lesson.json'):
            lesson = path.parent
            course = lesson.parent.parent.name
            view = lesson_view(ROOT / 'courses', course, lesson.name)
            extra = view['examples']
            expected = ((course == 'zaklady' and (int(lesson.name[:2]) <= 31 or 37 <= int(lesson.name[:2]) <= 39))
                        or (course == 'pandas' and (int(lesson.name[:2]) <= 19 or 21 <= int(lesson.name[:2]) <= 30)))
            self.assertEqual(len(extra), 2 if expected else 0, str(lesson))
            self.assertEqual(view['example'], (lesson / 'example.py').read_text('utf-8') if (lesson / 'example.py').is_file() else '')
            count += len(extra)
        self.assertEqual(count, 126)

    def validate(self, value):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'examples.json').write_text(json.dumps(value), encoding='utf-8')
            before = len(validator.errors)
            validator.validate_extra_examples(path)
            result = validator.errors[before:]
            del validator.errors[before:]
            return result

    def example(self, **overrides):
        return dict(id='test-1', title='Test', description='Zkouška',
                    code='# První komentář\n# Druhý komentář\nprint(3)\n', **overrides)

    def test_valid_example_with_input(self):
        ex = self.example()
        ex.update(code='# Čte text\n# Vypisuje délku\nprint(len(input()))\n', stdin='ahoj\n')
        self.assertEqual(self.validate([ex]), [])

    def test_failed_execution_is_detected(self):
        ex = self.example()
        ex['code'] = '# Dělení\n# Nulou\nprint(1 / 0)\n'
        self.assertTrue(any('skončila chybou' in e for e in self.validate([ex])))

    def test_bad_metadata_is_detected(self):
        for bad in ({}, [], [None], [{'id': 'x'}]):
            with self.subTest(value=bad):
                self.assertTrue(self.validate(bad))
        ex = self.example()
        self.assertTrue(any('duplicitní' in e for e in self.validate([ex, ex])))
        ex['stdin'] = 4
        self.assertTrue(any('stdin' in e for e in self.validate([ex])))


if __name__ == '__main__':
    unittest.main()
