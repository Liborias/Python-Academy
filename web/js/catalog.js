import { api } from './api.js';
import { renderPreparation } from './preparation.js';
import { doneCount, isDone } from './store.js';
import { esc, stars, STATUS } from './util.js';

let cache = null;
export async function getCatalog() {
  return (cache ||= (await api('/api/catalog')).courses);
}
const byId = (list, id) => list.find((c) => c.id === id);

function card(c, all) {
  const done = doneCount(c.id);
  const pct = c.lessons ? Math.round((100 * done) / c.lessons) : 0;
  const rec = c.doporuceno.map((id) => byId(all, id)?.title).filter(Boolean);
  return `<a class="card" href="#/kurz/${esc(c.id)}">
    <div class="meta">${stars(c.level)}<span class="badge ${esc(c.status)}">${STATUS[c.status] || ''}</span></div>
    <h2>${esc(c.title)}</h2>
    <p>${esc(c.summary)}</p>
    ${rec.length ? `<p style="font-size:.82rem">Hodí se znát: ${esc(rec.join(', '))}</p>` : ''}
    <div class="bar" aria-hidden="true"><i style="width:${pct}%"></i></div>
    <div class="meta"><span>${done} / ${c.lessons} lekcí</span></div>
  </a>`;
}

export async function renderCatalog(el) {
  const all = await getCatalog();
  let level = 0;
  const draw = () => {
    el.querySelector('.grid').innerHTML = all.filter((c) => !level || c.level === level).map((c) => card(c, all)).join('');
    el.querySelectorAll('.filters button').forEach((b) => b.setAttribute('aria-pressed', String(+b.dataset.l === level)));
  };
  el.innerHTML = `<h1>Vyberte si, co se chcete naučit</h1>
    <p class="lead">Každý podkurz je samostatný. Začněte kterýmkoli, nic se nezamyká. Hvězdičky ukazují obtížnost, „Hodí se znát“ je jen tip.</p>
    <div class="filters" role="group" aria-label="Obtížnost">
      <button data-l="0" aria-pressed="true">Vše</button>
      ${[1, 2, 3, 4].map((n) => `<button data-l="${n}" aria-pressed="false">${'★'.repeat(n)}</button>`).join('')}
    </div>
    <div class="grid"></div>`;
  el.querySelector('.filters').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return; level = +b.dataset.l; draw();
  });
  draw();
}

export async function renderCourse(el, id) {
  const all = await getCatalog();
  const c = byId(all, id);
  if (!c) { el.innerHTML = '<h1>Podkurz neexistuje</h1><p><a href="#/">Zpět na přehled</a></p>'; return; }
  let course = { modules: [] };
  try { course = await api(`/api/course?id=${encodeURIComponent(id)}`); } catch { /* bez obsahu */ }
  const rec = c.doporuceno.map((rid) => byId(all, rid)).filter(Boolean);
  const total = course.modules.reduce((n, m) => n + m.lessons.length, 0);
  const mods = course.modules.map((m) => `<section class="mod"><h3>${esc(m.title)}</h3><ol>${m.lessons.map((l) =>
    `<li class="${isDone(id, l.id) ? 'done' : ''}"><a href="#/kurz/${esc(id)}/${esc(l.id)}"><span class="n">${esc(l.n)}</span><span>${esc(l.title)}</span><span class="ck" aria-label="splněno">✓</span></a></li>`).join('')}</ol></section>`).join('');
  el.innerHTML = `<div class="crumbs"><a href="#/">Přehled</a> › ${esc(c.title)}</div>
    <h1>${esc(c.title)}</h1>
    <div class="meta" style="margin-top:12px">${stars(c.level)}<span class="badge ${esc(c.status)}">${STATUS[c.status]}</span><span>${total || c.lessons} lekcí</span></div>
    <p class="lead">${esc(c.summary)}</p>
    ${rec.length ? `<div class="note"><strong>Tip, ne podmínka.</strong> Půjde se vám snáz, když znáte: ${rec.map((r) => `<a class="chip" href="#/kurz/${esc(r.id)}">${esc(r.title)}</a>`).join(' ')}. Můžete ale začít rovnou tady.</div>` : ''}
    <details class="course-preparation" open><summary>Příprava pro tento podkurz</summary><section class="prep-content"></section></details>
    ${c.status === 'concept' ? '<div class="note"><strong>Koncept podkurzu.</strong> Lekce níže jsou návrh s cíli, praktickými kroky a vlastním ověřením. Nejde o hotový kurz s automatickými kontrolami instalace.</div>' : ''}
    ${mods || '<div class="empty">Lekce tohoto podkurzu se připravují.</div>'}`;
  await renderPreparation(el.querySelector('.prep-content'), id);
}
