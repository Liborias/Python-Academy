import { applyTheme, getTheme, setTheme, hasStorageProblem } from './store.js';
import { route, start } from './router.js';
import { renderCatalog, renderCourse } from './catalog.js';
import { renderLesson } from './lesson.js';
import { renderSetup } from './setup.js';
import { hasToken } from './api.js';
import { esc } from './util.js';

applyTheme();
const main = document.getElementById('main');
const storageNotice = document.createElement('p');
storageNotice.id = 'storage-warning';
storageNotice.className = 'note';
storageNotice.setAttribute('role', 'status');
storageNotice.textContent = 'Prohlížeč teď neukládá postup. Změny držíme v této otevřené stránce a další změna postupu zkusí uložení znovu. Před zavřením si rozepsaný kód uložte do souboru.';
main.before(storageNotice);

const dark = () => (getTheme() ? getTheme() === 'dark' : matchMedia('(prefers-color-scheme:dark)').matches);
const themeBtn = document.getElementById('theme');
const paintTheme = () => { themeBtn.textContent = dark() ? '☀ Světlý' : '☾ Tmavý'; };
const paintStore = () => { paintTheme(); storageNotice.hidden = !hasStorageProblem(); };
addEventListener('dilna-store-change', paintStore);
themeBtn.addEventListener('click', () => { setTheme(dark() ? 'light' : 'dark'); paintTheme(); });
paintStore();

const guard = (fn) => (...a) => fn(main, ...a).catch((e) => {
  main.innerHTML = `<h1>Něco se nepovedlo</h1><p class="lead">${esc(e.message)}</p>
    <p>Spusťte aplikaci znovu příkazem <code>python start.py</code> a otevřete adresu, kterou vypíše.</p>`;
});

route(/^\/$/, guard(renderCatalog));
route(/^\/kurz\/([a-z0-9-]+)$/, guard(renderCourse));
route(/^\/kurz\/([a-z0-9-]+)\/([a-z0-9-]+)$/, guard(renderLesson));
route(/^\/priprava$/, guard(renderSetup));
route(/^\/priprava\/([a-z-]+)$/, guard(renderSetup));
start((p) => { main.innerHTML = `<h1>Stránka nenalezena</h1><p><a href="#/">Zpět na přehled</a></p>`; });

if (!hasToken()) {
  document.getElementById('warn').hidden = false;
}
