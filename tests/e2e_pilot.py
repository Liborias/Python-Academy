"""Projde v prohlížeči všechny lekce podkurzu Základy: vzorové řešení → kontrola projde, ukázka doběhne."""
import json
import shutil
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server

srv = create_server(ROOT, "127.0.0.1", 0)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}/"
course = json.loads((ROOT / "courses/zaklady/course.json").read_text("utf-8"))
ids = [lid for m in course["modules"] for lid in m["lessons"]]
errors = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 900})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(f"{base}?t={srv.token}")
        pg.wait_for_selector(".card")
        assert "Rozpracováno" in pg.inner_text('a[href="#/kurz/zaklady"]')
        for lid in ids:
            lesson = ROOT / "courses/zaklady/lessons" / lid
            title = json.loads((lesson / "lesson.json").read_text("utf-8"))["title"]
            pg.goto(f"{base}#/kurz/zaklady/{lid}")
            pg.wait_for_function("t => document.querySelector('.lesson h1')?.textContent === t", arg=title)   # počkat na překreslení
            pg.wait_for_selector(".editor .ed-ta")
            pg.fill(".editor .ed-ta", (lesson / "solution.py").read_text("utf-8"))
            pg.click('[data-act="check"]')
            pg.wait_for_selector(".results .res")
            assert pg.locator(".results .res.ok").count() == 1, f"{lid} neprošla: " + pg.inner_text(".results")

            # ukázka: vstupy bere z example.stdin (po jednom řádku, když program čeká na vstup)
            sf = lesson / "example.stdin"
            feed = sf.read_text("utf-8").splitlines() if sf.is_file() else []
            pg.click('[data-act="run-ex"]')
            for _ in range(80):
                if "Hotovo" in pg.inner_text(".ex-console .status"):
                    break
                if feed and pg.locator(".ex-console .stdin:not([hidden]) input").count():
                    shown = pg.inner_text(".ex-console .out")
                    if shown and not shown.endswith("\n"):          # program vypsal výzvu bez konce řádku
                        pg.fill(".ex-console .stdin input", feed.pop(0))
                        pg.press(".ex-console .stdin input", "Enter")
                        pg.wait_for_timeout(150)
                        continue
                pg.wait_for_timeout(150)
            assert "Hotovo" in pg.inner_text(".ex-console .status"), f"ukázka {lid}: " + pg.inner_text(".ex-console")
        pg.goto(f"{base}#/kurz/zaklady")
        pg.wait_for_selector(".mod li")
        assert pg.locator(".mod li.done").count() == len(ids)
        b.close()
finally:
    srv.runs.stop_all()
    srv.shutdown()
    shutil.rmtree(ROOT / "workspace" / "zaklady", ignore_errors=True)
print("CHYBY:", errors) if errors else print("OK")
sys.exit(1 if errors else 0)
