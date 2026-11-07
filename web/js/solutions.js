// Odkrývání vzorového řešení bez zásahu do rozepsaného kódu nebo postupu.
import { api } from './api.js';
import { highlight } from './editor/highlight.js';

export function setupSolutions(host, cid, lid) {
  if (!host) return { select() {} };
  const panel = document.createElement('details');
  panel.className = 'solution-help';
  panel.innerHTML = `<summary>Zobrazit možné řešení</summary>
    <div class="solution-body">
      <p class="solution-context"></p>
      <p class="hint">Jde o jeden možný postup. I jiný kód může správně splnit zadání. Porovnejte ho se svým řešením.</p>
      <p class="solution-status hint" role="status"></p>
      <pre class="code" tabindex="0" hidden><code></code></pre>
    </div>`;
  host.appendChild(panel);
  const summary = panel.querySelector('summary');
  const context = panel.querySelector('.solution-context');
  const status = panel.querySelector('.solution-status');
  const pre = panel.querySelector('pre');
  const code = pre.querySelector('code');
  const loaded = new Map();
  let selected = null, revision = 0;

  function load(task) {
    if (!loaded.has(task.id)) {
      const params = new URLSearchParams({ course: cid, lesson: lid, task: task.id });
      const request = api(`/api/solution?${params}`).then((value) => {
        if (typeof value.code !== 'string' || !value.code.trim()) throw new Error('Prázdné řešení');
        return value.code;
      }).catch((error) => { loaded.delete(task.id); throw error; });
      loaded.set(task.id, request);
    }
    return loaded.get(task.id);
  }

  panel.addEventListener('toggle', async () => {
    summary.textContent = panel.open ? 'Skrýt možné řešení' : 'Zobrazit možné řešení';
    if (!panel.open || !selected?.has_solution) return;
    const current = revision, task = selected;
    status.textContent = 'Načítám řešení…';
    pre.hidden = true;
    try {
      const source = await load(task);
      if (revision !== current || !panel.isConnected || !panel.open) return;
      code.innerHTML = highlight(source);
      pre.setAttribute('aria-label', `Možné řešení: ${context.textContent}`);
      status.textContent = '';
      pre.hidden = false;
    } catch {
      if (revision !== current || !panel.isConnected || !panel.open) return;
      status.textContent = 'Řešení se nepodařilo načíst. Zavřete panel a zkuste jej znovu.';
    }
  });

  return {
    select(task, label) {
      revision += 1;
      selected = task;
      panel.open = false;
      panel.hidden = !task.has_solution;
      summary.textContent = 'Zobrazit možné řešení';
      context.textContent = label;
      status.textContent = '';
      code.textContent = '';
      pre.hidden = true;
    }
  };
}
