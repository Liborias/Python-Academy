// Spuštění kódu přes server: start, průběžné čtení výstupu, vstup pro input(), zastavení.
import { api } from './api.js';
import { esc } from './util.js';

// Vytvoří ovládání běhu uvnitř prvku `box` (výstupní panel + řádek vstupu). Vrací {run(code,timeout), stop(), running}.
export function makeConsole(box, { onDone } = {}) {
  box.classList.add('console');
  box.innerHTML = `<pre class="out" tabindex="0" aria-live="polite"></pre>
    <div class="plot-gallery" aria-label="Vytvořené grafy" hidden></div>
    <div class="file-downloads" aria-label="Soubory ke stažení" hidden></div>
    <form class="stdin" hidden><label>Vstup: <input type="text" autocomplete="off" aria-label="Vstup pro input()"></label><button class="btn" type="submit">Odeslat</button></form>
    <div class="status" aria-live="polite"></div>`;
  const out = box.querySelector('.out'), gallery = box.querySelector('.plot-gallery'), form = box.querySelector('.stdin'),
        downloads = box.querySelector('.file-downloads'), inp = form.querySelector('input'), status = box.querySelector('.status');
  let id = null, since = 0, timer = null, generation = 0;
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
    gallery.replaceChildren();
    for (const plot of p.images || []) {
      const figure = document.createElement('figure'), img = document.createElement('img');
      const caption = document.createElement('figcaption'), link = document.createElement('a');
      img.src = `data:image/png;base64,${plot.data}`;
      img.alt = `Graf ze souboru ${plot.name}`;
      link.href = img.src; link.download = plot.name.split('/').pop();
      link.textContent = `Stáhnout PNG: ${plot.name}`;
      caption.appendChild(link); figure.append(img, caption); gallery.appendChild(figure);
    }
    if (p.image_notice) {
      const note = document.createElement('p'); note.className = 'hint';
      note.textContent = p.image_notice; gallery.appendChild(note);
    }
    gallery.hidden = !gallery.childElementCount;
    downloads.replaceChildren();
    for (const file of p.files || []) {
      const link = document.createElement('a');
      link.href = `data:${file.mime};base64,${file.data}`;
      link.download = file.name.split('/').pop(); link.textContent = `Stáhnout soubor: ${file.name}`;
      downloads.appendChild(link);
    }
    if (p.file_notice) {
      const note = document.createElement('p'); note.className = 'hint'; note.textContent = p.file_notice;
      downloads.appendChild(note);
    }
    downloads.hidden = !downloads.childElementCount;
    status.textContent = msg; status.className = 'status ' + (p.exit === 0 && !p.timed_out ? 'ok' : 'bad');
    onDone && onDone(p);
  };
  const poll = async (version) => {
    if (!id || version !== generation) return;
    try {
      const p = await api(`/api/run/poll?id=${id}&since=${since}`);
      if (version !== generation) return;
      since = p.next;
      p.chunks.forEach((c) => add(c.ch, c.text));
      if (p.done) return finish(p);
    } catch (e) { if (version !== generation) return; api_.running = false; status.textContent = e.message; status.className = 'status bad'; return; }
    timer = setTimeout(() => poll(version), 80);
  };
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const t = inp.value + '\n'; inp.value = '';
    add('in', t);
    try { await api('/api/run/input', { id, text: t }); } catch { /* proces už mohl skončit */ }
  });

  api_.run = async (code, timeout = 20, ctx = {}) => {
    api_.stop();
    const version = ++generation;
    out.textContent = ''; gallery.replaceChildren(); gallery.hidden = true;
    downloads.replaceChildren(); downloads.hidden = true;
    status.textContent = 'Běží…'; status.className = 'status';
    since = 0; form.hidden = false; api_.running = true;
    try {
      const run = await api('/api/run', { code, timeout, course: ctx.course, lesson: ctx.lesson, task: ctx.task });
      if (version !== generation) { api('/api/run/stop', { id: run.id }).catch(() => {}); return; }
      id = run.id;
      poll(version);
    } catch (e) { if (version !== generation) return; api_.running = false; form.hidden = true; status.textContent = e.message; status.className = 'status bad'; }
  };
  api_.stop = () => {
    generation += 1;
    clearTimeout(timer);
    const previousId = id;
    id = null;
    if (api_.running) { status.textContent = 'Zastaveno.'; status.className = 'status'; }
    api_.running = false; form.hidden = true;
    if (previousId) api('/api/run/stop', { id: previousId }).catch(() => {});
  };
  api_.clear = () => { api_.stop(); out.textContent = ''; status.textContent = ''; gallery.replaceChildren(); gallery.hidden = true; downloads.replaceChildren(); downloads.hidden = true; };

  return api_;
}

export function renderResults(el, res) {
  if (res.error) { el.innerHTML = `<div class="res bad">${esc(res.error)}</div>`; return; }
  el.innerHTML = `<div class="res ${res.ok ? 'ok' : 'bad'}"><strong>${res.ok ? '✓ Správně!' : '✗ Ještě to není ono'}</strong><ul>${
    res.results.map((r) => `<li class="${r.ok ? 'ok' : 'bad'}"><span>${r.ok ? '✓' : '✗'}</span> ${esc(r.name)}${r.ok ? '' : `<div class="why">${esc(r.msg)}</div>`}</li>`).join('')}</ul></div>`;
}
