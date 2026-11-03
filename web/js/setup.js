// Příprava prostředí: profily kurzů, tři editory a společné dokumenty.
import { renderPreparation } from './preparation.js';
import { getCatalog } from './catalog.js';
import { esc } from './util.js';
import { api } from './api.js';
import { markdown } from './markdown.js';
import { getChecks, setCheck } from './store.js';

const TABS = [['instalace', 'Instalace'], ['vscodium', 'VSCodium'], ['vscode', 'VS Code'], ['pycharm', 'PyCharm'], ['reseni-problemu', 'Řešení problémů']];

export async function renderSetup(el, tab = 'instalace') {
  if (!TABS.some(([id]) => id === tab)) tab = 'instalace';
  const doc = await api(`/api/doc?name=${tab}`);
  el.innerHTML = `<h1>Příprava prostředí</h1>
    <p class="lead">Vyberte si VS Code, VSCodium nebo PyCharm. Aplikace spouští a kontroluje kód. Nic z toho není podmínka pro čtení lekcí.</p>
    <section class="setup-course"><h2>Co potřebuje váš podkurz?</h2>
      <label>Podkurz <select id="prep-course"></select></label><div id="course-preparation"></div></section>
    <div class="filters" role="tablist" aria-label="Části návodu">${TABS.map(([id, t]) =>
      `<button role="tab" data-t="${id}" aria-pressed="${id === tab}" aria-selected="${id === tab}">${t}</button>`).join('')}</div>
    <article class="prose setup" id="setup-doc">${markdown(doc.md)}</article>`;
  el.querySelector('.filters').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (b) location.hash = `/priprava/${b.dataset.t}`;
  });
  const catalog = await getCatalog();
  const courseSelect = el.querySelector('#prep-course');
  courseSelect.innerHTML = catalog.map((c) => `<option value="${esc(c.id)}">${esc(c.title)}</option>`).join('');
  const drawPreparation = () => {
    const panel = document.createElement('div');
    el.querySelector('#course-preparation').replaceChildren(panel);
    return renderPreparation(panel, courseSelect.value);
  };
  await drawPreparation();
  courseSelect.addEventListener('change', () => drawPreparation().catch((error) => {
    el.querySelector('#course-preparation').textContent = error.message;
  }));
  const saved = getChecks();
  el.querySelectorAll('input[data-chk]').forEach((c) => {
    const key = `${tab}:${c.dataset.chk}`;
    if (saved[key]) c.checked = true;
    c.addEventListener('change', () => setCheck(key, c.checked));
  });
}
