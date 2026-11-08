"""Náhledy: přepnutí příkladu, opožděný poll a nový běh bez grafu."""
import os
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.app import create_server


def graph(name):
    return ('from matplotlib.figure import Figure\nfig=Figure(figsize=(2,1))\n'
            'fig.subplots().plot([1,2],[3,4])\n'+f'fig.savefig({name!r})\nprint("uloženo")\n')


with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for name in ['courses','web','lib']:shutil.copytree(ROOT/name,root/name)
    server=create_server(root,'127.0.0.1',0,python=os.environ.get('DILNA_TEST_PYTHON'))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            page=browser.new_page();page.set_default_timeout(30000)
            page.goto(f'http://127.0.0.1:{server.server_address[1]}/?t={server.token}#/kurz/pandas/26-figure-axes-a-popisky')
            page.wait_for_selector('.ex-editor textarea')
            editor=page.locator('.ex-editor textarea');gallery=page.locator('.ex-console .plot-gallery')
            page.locator('.editor textarea').fill('# moje rozepsaná práce\n')
            page.click('[data-act="run-ex"]')
            page.wait_for_function('document.querySelector(".ex-console .plot-gallery img")?.naturalWidth > 100')
            page.click('[data-example="1"]')
            assert gallery.is_hidden()
            assert page.locator('.ex-console pre.out').inner_text()==''
            held=[]
            def delayed(route):
                response=route.fetch();data=response.json()
                if data.get('done') and any(img['name']=='stary.png' for img in data.get('images',[])):
                    held.append((route,response))
                else:route.fulfill(response=response)
            page.route('**/api/run/poll?*',delayed)
            editor.fill(graph('stary.png'));page.click('[data-act="run-ex"]')
            end=time.monotonic()+30
            while not held and time.monotonic()<end:page.wait_for_timeout(50)
            assert held,'Starý poll nedorazil'
            page.click('[data-example="2"]')
            editor.fill(graph('<b>čas.png'));page.click('[data-act="run-ex"]')
            page.wait_for_function('document.querySelector(".ex-console .status").textContent === "Hotovo."')
            page.wait_for_function('document.querySelector(".ex-console .plot-gallery img")?.naturalWidth > 100')
            assert gallery.locator('a').inner_text()=='Stáhnout PNG: <b>čas.png'
            assert gallery.locator('b').count()==0
            for route,response in held:route.fulfill(response=response)
            page.wait_for_timeout(300)
            assert gallery.locator('a').inner_text()=='Stáhnout PNG: <b>čas.png'
            editor.fill('print("Nový běh bez obrázku")');page.click('[data-act="run-ex"]')
            assert gallery.is_hidden()
            page.wait_for_function('document.querySelector(".ex-console .status").textContent === "Hotovo."')
            assert gallery.is_hidden() and gallery.locator('img').count()==0
            assert page.locator('.editor textarea').input_value()=='# moje rozepsaná práce\n'
            assert not page.is_checked('.done-toggle input')
            browser.close()
        print('OK: obrázek se vymaže při změně příkladu i novém běhu, opožděný poll nepřepíše nový graf, jméno je prostý text, rozepsaná práce/postup zachovány')
    finally:server.runs.stop_all();server.shutdown();server.server_close()
