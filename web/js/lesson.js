import { setupTasks } from './tasks.js';
import { api } from './api.js';
import { getCatalog } from './catalog.js';
import { isDone, markDone, getChecks, setCheck } from './store.js';
import { markdown } from './markdown.js';
import { makeConsole, renderResults } from './runner-client.js';
import { renderQuiz } from './quiz.js';
import { esc } from './util.js';
import { createEditor } from './editor/editor.js';

export async function renderLesson(el, cid, lid) {
  const [cat, course, lesson] = await Promise.all([
    getCatalog(), api(`/api/course?id=${cid}`), api(`/api/lesson?course=${cid}&lesson=${lid}`).catch(() => null)]);
  const c = cat.find((x) => x.id === cid);
  const flat = course.modules.flatMap((m) => m.lessons);
  const idx = flat.findIndex((l) => l.id === lid);
  const prev = flat[idx - 1], next = flat[idx + 1];
  const crumbs = `<div class="crumbs"><a href="#/">Přehled</a> › <a href="#/kurz/${esc(cid)}">${esc(c?.title || cid)}</a></div>`;
  if (!lesson) { el.innerHTML = `${crumbs}<h1>Lekce nenalezena</h1>`; return; }

  const gui = lesson.kind === 'gui';
  const guide = lesson.kind === 'guide';
  const examples = [{ id: 'original', title: lesson.example_title || lesson.title, code: lesson.example,
    description: 'Ukázka z výkladu lekce.' }, ...(lesson.examples || [])];
  const multipleExamples = examples.length > 1;

  el.innerHTML = `${crumbs}
    <article class="lesson">
      <h1>${esc(lesson.title)}</h1>
      <div class="meta" style="margin-top:8px">${lesson.minutes ? `<span>asi ${lesson.minutes} min</span>` : ''}${gui ? '<span class="badge">otevře okno</span>' : ''}${lesson.preview_images ? '<span class="badge">náhled grafu</span>' : ''}</div>
      ${guide ? '<div class="note"><strong>Návrh lekce úvodního podkurzu.</strong> Postup proveďte na svém počítači. Zaškrtnutí je vlastní ověření, aplikace instalaci ani stav GitHubu nekontroluje.</div>' : ''}
      <div class="prose">${markdown(lesson.md)}</div>
      ${lesson.example ? `<section class="block"><h2>Ukázka</h2>
        ${multipleExamples ? `<div class="bar-btns example-switch" role="group" aria-label="Výběr příkladu">
          ${examples.map((ex, i) => `<button type="button" class="btn${i === 0 ? ' primary' : ''}" data-example="${i}" aria-pressed="${i === 0}">${esc(ex.title)}</button>`).join('')}
        </div><p class="hint example-description" aria-live="polite"></p>
        <p class="hint">Příklady můžete upravit a spustit. Každý má vlastní rozepsaný kód; váš úkol níže se nemění.</p>` : ''}
        <div class="ex-editor"></div>
        <div class="bar-btns"><button class="btn primary" data-act="run-ex">▶ Spustit ukázku</button><button class="btn" data-act="stop-ex">■ Stop</button>${multipleExamples ? '<button class="btn" data-act="reset-ex">Obnovit příklad</button>' : ''}</div>
        <div class="ex-console"></div></section>` : ''}
      ${lesson.exercise ? `<section class="block"><h2>Váš úkol</h2><div class="bar-btns task-switch" role="group" aria-label="Výběr úkolu"></div><div class="prose task-description"></div><div class="editor"></div>
        <div class="bar-btns">
          <button class="btn primary" data-act="run">▶ Spustit</button>
          <button class="btn" data-act="stop">■ Stop</button>
          ${lesson.has_check ? '<button class="btn primary" data-act="check">✓ Zkontrolovat</button>' : ''}
          <button class="btn" data-act="vsc" title="Uloží soubor do složky workspace a otevře ho ve VSCodium">Otevřít ve VSCodium</button>
          <button class="btn" data-act="reload" title="Načte změny uložené ve VSCodium">↻ Načíst ze souboru</button>
          <button class="btn" data-act="reset">Začít znovu</button>
        </div>
        <p class="hint" data-role="hint"></p>
        <div class="run-console"></div><div class="results" aria-live="polite"></div>
        ${lesson.has_solution || lesson.tasks?.some((task) => task.has_solution) ? '<div class="solution-slot"></div>' : ''}</section>` : ''}
      <section class="block quiz"></section>
      <footer class="lesson-foot">
        <label class="done-toggle"><input type="checkbox" ${isDone(cid, lid) ? 'checked' : ''}> ${guide ? 'Ověřil/a jsem u sebe' : 'Mám splněno'}</label>
        <span class="spacer"></span>
        ${prev ? `<a class="btn" href="#/kurz/${esc(cid)}/${esc(prev.id)}">← ${esc(prev.title)}</a>` : ''}
        ${next ? `<a class="btn primary" href="#/kurz/${esc(cid)}/${esc(next.id)}">${esc(next.title)} →</a>` : ''}
      </footer>
    </article>`;

  if (guide) {
    el.querySelectorAll('.prose input[data-chk]').forEach((input) => {
      const key = `guide:${cid}:${lid}:${input.dataset.chk}`;
      input.checked = !!getChecks()[key];
      input.addEventListener('change', () => setCheck(key, input.checked));
    });
  }
  const hint = el.querySelector('[data-role="hint"]');
  const done = (on = true) => { markDone(cid, lid, on); el.querySelector('.done-toggle input').checked = on; };
  el.querySelector('.done-toggle input').addEventListener('change', (e) => done(e.target.checked));

  // Ukázky: vlastní rozepsaný kód pro každou variantu, oddělený od úkolu.
  let exCon = null;
  if (lesson.example) {
    let selected = 0;
    const draftKey = (i) => `dilna-example-${cid}-${lid}-${examples[i].id}`;
    const drafts = examples.map((example, i) => {
      try { return localStorage.getItem(draftKey(i)) ?? example.code; }
      catch { return example.code; }
    });
    const ex = createEditor(el.querySelector('.ex-editor'), drafts[0], {
      readOnly: !multipleExamples,
      onChange: (code) => {
        if (!multipleExamples) return;
        drafts[selected] = code;
        try { localStorage.setItem(draftKey(selected), code); } catch { /* ignoruj */ }
      }
    });
    if (multipleExamples) {
      const description = el.querySelector('.example-description');
      description.textContent = examples[0].description;
      el.querySelectorAll('[data-example]').forEach((button) => {
        button.onclick = () => {
          const index = Number(button.dataset.example);
          if (index === selected) return;
          exCon.clear();
          drafts[selected] = ex.get();
          selected = index;
          ex.set(drafts[selected]);
          description.textContent = examples[selected].description;
          el.querySelectorAll('[data-example]').forEach((b) => {
            const active = Number(b.dataset.example) === selected;
            b.setAttribute('aria-pressed', String(active));
            b.classList.toggle('primary', active);
          });
        };
      });
    }
    if (multipleExamples) {
      el.querySelector('[data-act="reset-ex"]').onclick = () => {
        if (confirm('Obnovit původní kód vybraného příkladu? Vaše úpravy tohoto příkladu se přepíšou.')) {
          exCon.clear();
          ex.set(examples[selected].code);
        }
      };
    }
    exCon = makeConsole(el.querySelector('.ex-console'));
    const runExample = () => exCon.run(ex.get(), lesson.run_timeout ?? (gui ? 600 : 20), { course: cid, lesson: lid });
    el.querySelector('[data-act="run-ex"]').onclick = runExample;
    ex.onRun(runExample);
    el.querySelector('[data-act="stop-ex"]').onclick = () => exCon.stop();
  }

  // úkol
  let ed = null, con = null;
  if (lesson.exercise) {
    con = setupTasks(el, lesson, cid, lid, gui, done);
  }

  renderQuiz(el.querySelector('.quiz'), lesson.quiz || [], () => { if (!lesson.has_check) done(true); });
  // opuštění stránky ukončí běžící programy
  const stopAll = () => { con?.stop(); exCon?.stop(); removeEventListener('hashchange', stopAll); };
  addEventListener('hashchange', stopAll);
}
