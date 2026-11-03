// Spuštění kódu přes server: start, průběžné čtení výstupu, vstup pro input(), zastavení.
import { api } from './api.js';
import { esc } from './util.js';

// Vytvoří ovládání běhu uvnitř prvku `box` (výstupní panel + řádek vstupu). Vrací {run(code,timeout), stop(), running}.
export function makeConsole(box, { onDone } = {}) {
  box.classList.add('console');
  box.innerHTML = `<pre class="out" tabindex="0" aria-live="polite"></pre>
    <form class="stdin" hidden><label>Vstup: <input type="text" autocomplete="off" aria-label="Vstup pro input()"></label><button class="btn" type="submit">Odeslat</button></form>
    <div class="status" aria-live="polite"></div>`;
  const out = box.querySelector('.out'), form = box.querySelector('.stdin'),
        inp = form.querySelector('input'), status = box.querySelector('.status');
  let id = null, since = 0, timer = null;
  const api_ = { running: false };

  const add = (ch, text) => {
    const s = document.createElement('span');
    s.className = ch; s.textContent = text; out.appendChild(s);
    out.scrollTop = out.scrollHeight;
  };
  const finish = (p) => {
    clearTimeout(timer); api_.running = false; form.hidden = true; id = null;
    const msg = p.timed_out ? 'Program běžel příliš dlouho a byl zastaven.'
      : p.stopped ? 'Zastaveno.' : p.exit === 0 ? 'Hotovo.' : `Program skončil s chybou (kód ${p.exit}).`;
    if (p.truncated) add('err', '\n[Výstup byl zkrácen.]');
    status.textContent = msg; status.className = 'status ' + (p.exit === 0 && !p.timed_out ? 'ok' : 'bad');
    onDone && onDone(p);
  };
  const poll = async () => {
    if (!id) return;
    try {
      const p = await api(`/api/run/poll?id=${id}&since=${since}`);
      since = p.next;
      p.chunks.forEach((c) => add(c.ch, c.text));
      if (p.done) return finish(p);
    } catch (e) { api_.running = false; status.textContent = e.message; status.className = 'status bad'; return; }
    timer = setTimeout(poll, 80);
  };
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const t = inp.value + '\n'; inp.value = '';
    add('in', t);
    try { await api('/api/run/input', { id, text: t }); } catch { /* proces už mohl skončit */ }
  });

  api_.run = async (code, timeout = 20, ctx = {}) => {
    api_.stop();
    out.textContent = ''; status.textContent = 'Běží…'; status.className = 'status';
    since = 0; form.hidden = false; api_.running = true;
    try {
      id = (await api('/api/run', { code, timeout, course: ctx.course, lesson: ctx.lesson })).id;
      poll();
    } catch (e) { api_.running = false; form.hidden = true; status.textContent = e.message; status.className = 'status bad'; }
  };
  api_.stop = () => { if (id) { api('/api/run/stop', { id }).catch(() => {}); } };
  return api_;
}

export function renderResults(el, res) {
  if (res.error) { el.innerHTML = `<div class="res bad">${esc(res.error)}</div>`; return; }
  el.innerHTML = `<div class="res ${res.ok ? 'ok' : 'bad'}"><strong>${res.ok ? '✓ Správně!' : '✗ Ještě to není ono'}</strong><ul>${
    res.results.map((r) => `<li class="${r.ok ? 'ok' : 'bad'}"><span>${r.ok ? '✓' : '✗'}</span> ${esc(r.name)}${r.ok ? '' : `<div class="why">${esc(r.msg)}</div>`}</li>`).join('')}</ul></div>`;
}
