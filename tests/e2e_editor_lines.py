"""Čísla řádků a komentáře: skutečné klávesy, výběr, historie, posun a mobil."""
import shutil
import sys
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

shots = Path(sys.argv[sys.argv.index('--shots') + 1]) if '--shots' in sys.argv else None
if shots:
    shots.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ['courses', 'web', 'lib']:
        shutil.copytree(ROOT / name, root / name)
    server = create_server(root, '127.0.0.1', 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}/'
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'{base}?t={server.token}#/kurz/zaklady/01-prvni-program')
            page.wait_for_selector('.editor .ed-ta')
            page.evaluate('document.fonts.ready')
            ta = page.locator('.editor .ed-ta')

            def lines(selector='.editor'):
                editor = page.locator(selector)
                value = editor.locator('.ed-ta').input_value()
                assert editor.locator('.ed-lines').inner_text().splitlines() == [str(i + 1) for i in range(value.count('\n') + 1)]
                assert editor.locator('.ed-gutter').get_attribute('aria-hidden') == 'true'
                assert editor.locator('.ed-gutter').evaluate('el => getComputedStyle(el).userSelect') == 'none'

            def select(start, end=None, direction='none'):
                ta.focus()
                ta.evaluate('(el, s) => el.setSelectionRange(s[0], s[1], s[2])', [start, start if end is None else end, direction])

            def selection():
                return ta.evaluate('el => [el.selectionStart, el.selectionEnd, el.selectionDirection]')

            def shortcut(key='Control+/'):
                page.keyboard.press(key)
                lines()

            lines()
            lines('.ex-editor')
            ta.fill('prvni = 1\n    druhy = 2\ntreti = 3')
            original = ta.input_value()
            caret = original.index('druhy') + 3
            select(caret)
            shortcut()
            assert ta.input_value() == 'prvni = 1\n    # druhy = 2\ntreti = 3'
            assert selection()[:2] == [caret + 2, caret + 2]
            shortcut()
            assert ta.input_value() == original and selection()[:2] == [caret, caret]

            # Česká klávesnice nepotřebuje vyrobit znak /; Ctrl i Cmd fungují.
            for key in ['Control+Shift+Digit7', 'Meta+/', 'Meta+Shift+Digit7']:
                select(caret)
                shortcut(key)
                assert '# druhy' in ta.input_value(), key
                shortcut(key)
                assert ta.input_value() == original, key

            # Prázdný první řádek a odsazený prázdný řádek lze také komentovat.
            for value, cursor, expected in [('\nnext = 1', 0, '# \nnext = 1'), ('    ', 4, '    # ')]:
                ta.fill(value)
                select(cursor)
                shortcut()
                assert ta.input_value() == expected
                shortcut()
                assert ta.input_value() == value and selection()[:2] == [cursor, cursor]

            # Výběr končí na začátku dalšího řádku: ten zůstane beze změny.
            original = 'if a:\n    b = 2\n\nc = 3'
            ta.fill(original)
            end = original.index('c =')
            select(2, end, 'backward')
            shortcut()
            assert ta.input_value() == '# if a:\n#     b = 2\n\nc = 3'
            assert selection()[2] == 'backward'
            shortcut()
            assert ta.input_value() == original and selection() == [2, end, 'backward']
            for original, expected in [
                ('    #poznámka\n    # další', '    poznámka\n    další'),
                ('    x = 1\n        y = 2', '    # x = 1\n    #     y = 2'),
                ('# poznámka\nx = 1', '# # poznámka\n# x = 1'),
                ('\tx = 1\n\ty = 2', '\t# x = 1\n\t# y = 2'),
            ]:
                ta.fill(original)
                select(0, len(original))
                shortcut()
                assert ta.input_value() == expected
                if not original.startswith('    #'):
                    shortcut()
                    assert ta.input_value() == original

            ta.fill('x = 1\ny = 2')
            page.keyboard.press('Control+A')
            shortcut()
            commented = ta.input_value()
            page.keyboard.press('Control+Z')
            assert ta.input_value() == 'x = 1\ny = 2'
            page.keyboard.press('Control+Shift+Z')
            assert ta.input_value() == commented
            lines()
            ta.fill('x = 1')
            page.keyboard.press('Control+End')
            page.keyboard.press('Enter')
            assert ta.input_value() == 'x = 1\n'
            lines()
            page.keyboard.press('Control+Z')
            assert ta.input_value() == 'x = 1'
            lines()

            # Více než 999 řádků, dlouhý řádek, oba posuvníky a růst na konci.
            long_code = '\n'.join(f'radek_{i} = {i}' for i in range(1000)) + '\ntext = "' + 'a' * 250 + '"'
            # Skutečné vložení bloku ze schránky včetně události insertFromPaste.
            page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
            page.evaluate('text => navigator.clipboard.writeText(text)', long_code)
            ta.focus()
            page.keyboard.press('Control+A')
            page.keyboard.press('Control+V')
            assert ta.input_value() == long_code
            page.keyboard.press('Control+A')
            page.keyboard.press('Control+C')
            assert page.evaluate('navigator.clipboard.readText()') == long_code
            lines()
            gutter = page.locator('.editor .ed-gutter')
            left = gutter.bounding_box()['x']
            ta.evaluate('el => { el.scrollTop = el.scrollHeight; el.scrollLeft = el.scrollWidth; }')
            page.wait_for_function('''() => {
                const ta = document.querySelector('.editor .ed-ta'), n = document.querySelector('.editor .ed-lines'), hl = document.querySelector('.editor .ed-hl');
                return ta.scrollTop > 0 && ta.scrollLeft > 0 && Math.abs(n.scrollTop - ta.scrollTop) < 1 && hl.scrollTop === ta.scrollTop && hl.scrollLeft === ta.scrollLeft;
            }''')
            assert gutter.bounding_box()['x'] == left
            aligned = page.locator('.editor .ed-lines').evaluate('''el => {
                const hl = el.closest('.ed').querySelector('.ed-hl'), row = 999;
                const top = (element) => {
                    let index = element.textContent.split('\\n').slice(0, row - 1).join('\\n').length + 1;
                    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
                    let node;
                    while ((node = walker.nextNode())) {
                        if (index >= node.length) { index -= node.length; continue; }
                        const r = document.createRange(); r.setStart(node, index); r.setEnd(node, index + 1);
                        return r.getBoundingClientRect().top;
                    }
                    return NaN;
                };
                // Skutečné souřadnice glyphů: zaokrouhlený computed lineHeight po 999 řádcích driftuje.
                return Math.abs(top(el) - top(hl)) < 1;
            }''')
            assert aligned, 'Čísla se při posunu rozcházejí s kódem.'
            page.keyboard.press('Control+End')
            page.keyboard.press('Enter')
            lines()
            assert ta.evaluate('el => el.scrollTop') > 0

            # Přepínání příkladů/úkolů volá programatické set; drafty a postup trvají.
            draft = '# Moje korektura\nx = 1\n\nprint(x)\n'
            ta.fill(draft)
            page.locator('.done-toggle input').check()
            page.click('[data-task="1"]')
            lines()
            page.click('[data-task="0"]')
            assert ta.input_value() == draft
            example = page.locator('.ex-editor .ed-ta')
            example.fill('print("upravená ukázka")\n\n')
            page.click('[data-example="1"]')
            lines('.ex-editor')
            page.click('[data-example="0"]')
            assert example.input_value() == 'print("upravená ukázka")\n\n'
            lines('.ex-editor')
            example.focus()
            page.keyboard.press('Control+Home')
            page.keyboard.press('Control+/')
            assert example.input_value().startswith('# print')
            lines('.ex-editor')
            page.reload()
            page.wait_for_selector('.editor .ed-lines')
            assert ta.input_value() == draft and page.is_checked('.done-toggle input')
            lines()

            # Vzhled s čísly i nápověda zůstávají použitelné na úzké obrazovce.
            display_code = '# Součet cen\nceny = [25, 12, 8]\ncelkem = 0\nfor cena in ceny:\n    celkem += cena\nprint(f"Celkem: {celkem} Kč")\n'
            ta.fill(display_code)
            for width in [1100, 380, 320]:
                page.set_viewport_size({'width': width, 'height': 900 if width == 1100 else 800})
                lines()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.locator('.editor .ed').evaluate('el => el.scrollIntoView({block: "center"})')
                if shots and width != 320:
                    page.locator('.editor .ed').screenshot(path=str(shots / f'editor-lines-{width}.png'))
                page.click('.editor .ed-help')
                dialog = page.locator('dialog[open]')
                assert 'Ctrl+Shift+7' in dialog.inner_text() and 'aktuálním řádku' in dialog.inner_text()
                assert 'označíte-li více řádků' in dialog.inner_text().lower() and 'Cmd' in dialog.inner_text()
                assert dialog.evaluate('el => el.scrollWidth <= el.clientWidth'), f'Nápověda přetéká při {width}px.'
                if shots and width == 380:
                    dialog.locator('th', has_text='Ctrl+/').scroll_into_view_if_needed()
                    page.screenshot(path=str(shots / 'editor-help-mobile.png'))
                page.keyboard.press('Escape')

            page.goto(f'{base}#/kurz/zaklady/32-projekt-hadej-planetu')
            page.wait_for_selector('.ex-editor .ed-lines')
            readonly = page.locator('.ex-editor .ed-ta')
            assert readonly.evaluate('el => el.readOnly')
            before = readonly.input_value()
            readonly.focus()
            page.keyboard.press('Control+/')
            page.keyboard.press('Control+Shift+Digit7')
            assert readonly.input_value() == before
            lines('.ex-editor')
            assert not errors, errors
            browser.close()
        print('OK: čísla řádků, oba posuvníky, 1001+ řádků, výběr/kurzor, Ctrl/Cmd a česká alternativa, prázdné řádky, undo/redo, ukázky/úkoly, readonly, reload/postup, mobil a nápověda')
    finally:
        server.runs.stop_all()
        server.shutdown()
        server.server_close()
