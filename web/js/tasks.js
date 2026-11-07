import { api } from './api.js';
import { markdown } from './markdown.js';
import { createEditor } from './editor/editor.js';
import { makeConsole, renderResults } from './runner-client.js';
import { esc } from './util.js';
import { isTaskDone, markTaskDone } from './store.js';

export function setupTasks(el, lesson, cid, lid, gui, done) {
  const tasks = [{ id: 'task-1', title: 'Původní úkol', exercise: lesson.exercise,
    md: lesson.md.includes('## Váš úkol') ? lesson.md.split('## Váš úkol').slice(1).join('## Váš úkol') : 'Původní zadání najdete ve výkladu výše.' }, ...(lesson.tasks || [])];
  const multiple = tasks.length > 1;
  let selected = 0;
  const key = (i) => i === 0 ? `dilna-code-${cid}-${lid}` : `dilna-code-${cid}-${lid}-${tasks[i].id}`;
  const drafts = tasks.map((t, i) => { try { return localStorage.getItem(key(i)) ?? t.exercise; } catch { return t.exercise; } });
  const results = tasks.map(() => null), requests = tasks.map(() => 0);
  const switcher = el.querySelector('.task-switch');
  const description = el.querySelector('.task-description');
  const hint = el.querySelector('[data-role="hint"]');
  const res = el.querySelector('.results');
  const con = makeConsole(el.querySelector('.run-console'));
  const context = (i) => ({ course: cid, lesson: lid, ...(i ? { task: tasks[i].id } : {}) });
  const ed = createEditor(el.querySelector('.editor'), drafts[0], { onChange: (value) => {
    drafts[selected] = value;
    results[selected] = null;
    requests[selected] += 1; // Pozdější odpověď nesmí hodnotit již upravený kód.
    res.textContent = '';
    try { localStorage.setItem(key(selected), value); } catch { /* ignoruj */ }
  } });
  function drawButtons() {
    if (!multiple) return;
    switcher.innerHTML = tasks.map((task, i) => `<button type="button" class="btn${i === selected ? ' primary' : ''}" data-task="${i}" aria-pressed="${i === selected}">Úkol ${i + 1}${isTaskDone(cid, lid, task.id) ? ' ✓' : ''}</button>`).join('');
    description.innerHTML = markdown(`### Úkol ${selected + 1}: ${tasks[selected].title}\n\n${tasks[selected].md.replace(/^### [^\n]+\n+/, '')}`);
  }
  drawButtons();
  switcher.addEventListener('click', (event) => {
    const button = event.target.closest('[data-task]');
    if (!button || Number(button.dataset.task) === selected) return;
    con.clear();
    drafts[selected] = ed.get();
    selected = Number(button.dataset.task);
    // set volá onChange: uchovat již získaný výsledek vybraného úkolu.
    const previousResult = results[selected];
    ed.set(drafts[selected]);
    results[selected] = previousResult;
    if (previousResult) renderResults(res, previousResult); else res.textContent = '';
    hint.textContent = '';
    drawButtons();
    switcher.querySelector(`[data-task="${selected}"]`).focus({ preventScroll: true });
  });
  const act = {
    run: () => con.run(ed.get(), lesson.run_timeout ?? (gui ? 600 : 20), context(selected)),
    stop: () => con.stop(),
    reset: () => { if (confirm('Vrátit vybraný úkol do původní podoby? Jeho rozepsaný kód se přepíše.')) ed.set(tasks[selected].exercise); },
    check: async () => {
      const index = selected, code = ed.get(), request = ++requests[index];
      res.textContent = 'Kontroluji…';
      let result;
      try { result = await api('/api/check', { ...context(index), code }); }
      catch (error) { result = { error: error.message }; }
      if (requests[index] !== request) return;
      results[index] = result;
      if (result.ok) {
        markTaskDone(cid, lid, tasks[index].id);
        if (index === 0) done(true); // Dosavadní postup lekce zachovává původní úkol.
      }
      if (selected === index) { renderResults(res, result); drawButtons(); }
    },
    vsc: async () => {
      const index = selected;
      try {
        const r = await api('/api/workspace/open', { ...context(index), code: ed.get() });
        if (selected !== index) return;
        hint.innerHTML = r.opened ? `Soubor je otevřený ve VSCodium: <code>${esc(r.path)}</code>. Po uložení klikněte na „Načíst ze souboru“.`
          : `Otevřete soubor ručně ve svém editoru: <code>${esc(r.path)}</code>`;
      } catch (error) { if (selected === index) hint.textContent = error.message; }
    },
    reload: async () => {
      const index = selected, revision = requests[index];
      try {
        const r = await api(`/api/workspace?course=${cid}&lesson=${lid}${index ? `&task=${tasks[index].id}` : ''}`);
        if (selected !== index || requests[index] !== revision) return;
        if (!r.exists) { hint.textContent = 'Soubor tohoto úkolu ještě neexistuje. Nejdřív použijte „Otevřít ve VSCodium“.'; return; }
        ed.set(r.code); hint.textContent = 'Načteno ze souboru vybraného úkolu.';
      } catch (error) { if (selected === index) hint.textContent = error.message; }
    },
  };
  el.querySelector('.editor').parentElement.addEventListener('click', (event) => {
    const button = event.target.closest('[data-act]');
    if (button && act[button.dataset.act]) act[button.dataset.act]();
  });
  ed.onRun(act.run);
  return con;
}
