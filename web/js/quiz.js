import { esc } from './util.js';

// Možnosti se při každém zobrazení zamíchají (value zůstává původní index), aby správná odpověď nebyla pořád na stejném místě.
function shuffled(opts) {
  const a = opts.map((o, j) => [o, j]);
  for (let i = a.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [a[i], a[k]] = [a[k], a[i]]; }
  return a;
}

// Kvíz: [{q, options[], answer, why}]. Odpověď se vyhodnotí hned po kliknutí.
export function renderQuiz(el, quiz, onAllCorrect) {
  if (!quiz.length) { el.hidden = true; return; }
  const state = quiz.map(() => null);
  el.innerHTML = `<h2>Kvíz</h2>` + quiz.map((q, i) => `<fieldset class="q" data-i="${i}"><legend>${esc(q.q)}</legend>${
    shuffled(q.options).map(([o, j]) => `<label><input type="radio" name="q${i}" value="${j}"> ${esc(o)}</label>`).join('')}
    <div class="why" hidden></div></fieldset>`).join('');
  el.addEventListener('change', (e) => {
    const f = e.target.closest('.q'); if (!f) return;
    const i = +f.dataset.i, v = +e.target.value, ok = v === quiz[i].answer;
    state[i] = ok;
    const w = f.querySelector('.why');
    w.hidden = false; w.className = 'why ' + (ok ? 'ok' : 'bad');
    w.textContent = (ok ? '✓ Správně. ' : '✗ Zkuste to znovu. ') + (ok ? (quiz[i].why || '') : '');
    if (state.every(Boolean)) onAllCorrect && onAllCorrect();
  });
}
