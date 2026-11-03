// Našeptávač: úryvky (| = pozice kurzoru), proměnné a funkce z kódu, klíčová slova, vestavěné funkce, metody po tečce.
// Funguje i uvnitř {…} f-řetězce (nabízí hlavně proměnné), v textu řetězce a v komentáři mlčí.
import { KEYWORDS, BUILTINS } from './lexicon.js';
import { contextAt } from './context.js';

const SNIPS = {
  print: ['print(|)', 'výpis'], input: ['input("|")', 'vstup od uživatele'],
  def: ['def |():\n    ', 'funkce'], for: ['for i in range(|):\n    ', 'cyklus for'],
  while: ['while |:\n    ', 'cyklus while'], if: ['if |:\n    ', 'podmínka'], elif: ['elif |:\n    ', 'další podmínka'],
  else: ['else:\n    |', 'jinak'], try: ['try:\n    |\nexcept Exception as e:\n    print(e)', 'ošetření chyby'],
  class: ['class |:\n    def __init__(self):\n        ', 'třída'],
  with: ['with open("|", encoding="utf-8") as f:\n    ', 'práce se souborem'],
  main: ['if __name__ == "__main__":\n    |', 'hlavní blok'], range: ['range(|)', 'řada čísel'], len: ['len(|)', 'délka'],
  import: ['import |', 'import modulu'], return: ['return |', 'vrátí hodnotu'],
};
const NO_EXACT = new Set(['return', 'import', 'else']);          // tyto po úplném napsání nenabízet
const METHODS = ['append', 'clear', 'copy', 'count', 'endswith', 'extend', 'find', 'format', 'get', 'index', 'insert', 'items', 'join',
  'keys', 'lower', 'lstrip', 'pop', 'remove', 'replace', 'reverse', 'rstrip', 'sort', 'split', 'startswith', 'strip', 'title', 'update', 'upper', 'values'];
const FEXPR_KW = ['and', 'or', 'not', 'in', 'is', 'if', 'else', 'None', 'True', 'False', 'lambda'];

// Proměnné a funkce definované v kódu (přiřazení, cykly for, parametry funkcí, with/as, def, class, import)
export function collectNames(code) {
  const vars = new Set(), funcs = new Set();
  const addList = (txt) => txt.split(',').forEach((x) => { const n = x.replace(/[*\s]/g, '').split(/[=:]/)[0]; if (/^[A-Za-z_]\w*$/.test(n)) vars.add(n); });
  for (const m of code.matchAll(/^[ \t]*([A-Za-z_]\w*(?:[ \t]*,[ \t]*[A-Za-z_]\w*)*)[ \t]*(?:[-+*/%]|\/\/|\*\*)?=(?!=)/gm)) addList(m[1]);
  for (const m of code.matchAll(/\bfor[ \t]+([A-Za-z_][\w, \t]*?)[ \t]+in\b/g)) addList(m[1]);
  for (const m of code.matchAll(/\bdef[ \t]+([A-Za-z_]\w*)[ \t]*\(([^)]*)\)/g)) { funcs.add(m[1]); addList(m[2]); }
  for (const m of code.matchAll(/\b(?:class)[ \t]+([A-Za-z_]\w*)/g)) funcs.add(m[1]);
  for (const m of code.matchAll(/\bas[ \t]+([A-Za-z_]\w*)/g)) vars.add(m[1]);
  for (const m of code.matchAll(/^[ \t]*import[ \t]+([A-Za-z_]\w*)/gm)) vars.add(m[1]);
  return { vars: [...vars], funcs: [...funcs] };
}

export function attachComplete(ta, replace) {
  const box = document.createElement('div');
  box.className = 'ac'; box.setAttribute('role', 'listbox'); box.hidden = true;
  document.body.appendChild(box);
  let items = [], sel = 0, word = '';
  const cvs = document.createElement('canvas').getContext('2d');

  const close = () => { box.hidden = true; items = []; };
  const open = () => !box.hidden;
  const paint = () => {
    box.innerHTML = items.map((it, i) => `<div class="ac-i${i === sel ? ' on' : ''}" role="option" data-i="${i}"><b>${it.label}</b><span>${it.detail}</span></div>`).join('');
  };
  function place() {
    const cs = getComputedStyle(ta), r = ta.getBoundingClientRect();
    cvs.font = `${cs.fontSize} ${cs.fontFamily}`;
    const cw = cvs.measureText('M').width, lh = parseFloat(cs.lineHeight) || 20;
    const before = ta.value.slice(0, ta.selectionStart), line = before.split('\n').length - 1, col = before.length - before.lastIndexOf('\n') - 1;
    const x = r.left + parseFloat(cs.paddingLeft) + col * cw - ta.scrollLeft, y = r.top + parseFloat(cs.paddingTop) + (line + 1) * lh - ta.scrollTop;
    box.style.left = Math.max(4, Math.min(x, innerWidth - 260)) + 'px';
    box.style.top = (y + 2 + 200 > innerHeight ? y - lh - box.offsetHeight - 2 : y + 2) + 'px';
  }
  function accept(i = sel) {
    const it = items[i]; if (!it) return;
    const s = ta.selectionStart;
    replace(s - word.length, s, it.text);
    close();
  }
  function update() {
    const v = ta.value, s = ta.selectionStart;
    if (s !== ta.selectionEnd) return close();
    const ctx = contextAt(v.slice(0, s));
    if (ctx === 'comment' || ctx === 'string' || ctx === 'fstring' || ctx === 'fspec') return close();
    const inF = ctx === 'fexpr';
    const lineBefore = v.slice(v.lastIndexOf('\n', s - 1) + 1, s);
    word = (/[A-Za-z_]\w*$/.exec(lineBefore) || [''])[0];
    const afterDot = lineBefore.slice(0, lineBefore.length - word.length).endsWith('.');
    const low = word.toLowerCase();
    const starts = (n) => n.toLowerCase().startsWith(low) && n !== word;
    const own = collectNames(v.slice(0, s - word.length) + '\n' + v.slice(s));     // bez slova, které právě píšeme
    const cand = [], seen = new Set();
    const add = (label, text, detail) => { if (!seen.has(label)) { seen.add(label); cand.push({ label, text, detail }); } };

    if (afterDot) {
      if (!word && !lineBefore.endsWith('.')) return close();
      METHODS.filter(starts).forEach((n) => add(n, n + (inF ? '' : '(|)'), 'metoda'));
    } else if (inF) {
      if (word.length < 1 && !lineBefore.endsWith('{')) return close();                       // v {…} stačí 1 znak, nebo hned po {
      own.vars.filter(starts).forEach((n) => add(n, n, 'proměnná'));
      own.funcs.filter(starts).forEach((n) => add(n, n + '(|)', 'funkce'));
      BUILTINS.filter((n) => starts(n) && n !== 'self').forEach((n) => add(n, n + (/^[a-z]/.test(n) ? '(|)' : ''), 'vestavěné'));
      FEXPR_KW.filter(starts).forEach((n) => add(n, n, 'klíčové slovo'));
      for (const n of new Set(v.match(/[A-Za-z_]\w{2,}/g) || [])) if (starts(n)) add(n, n, 'z kódu');
    } else {
      if (word.length < 2) return close();
      for (const [k, [t, d]] of Object.entries(SNIPS)) if (k.startsWith(low) && (k !== word || !NO_EXACT.has(k))) add(k, t, d);
      own.vars.filter(starts).forEach((n) => add(n, n, 'proměnná'));
      own.funcs.filter(starts).forEach((n) => add(n, n + '(|)', 'funkce'));
      for (const n of [...KEYWORDS, ...BUILTINS]) if (starts(n)) add(n, n, KEYWORDS.includes(n) ? 'klíčové slovo' : 'vestavěné');
      for (const n of new Set(v.match(/[A-Za-z_]\w{2,}/g) || [])) if (starts(n)) add(n, n, 'z kódu');
    }
    // v {…} po napsání { se nabídne seznam všech proměnných
    items = cand.slice(0, 8); sel = 0;
    if (!items.length) return close();
    box.hidden = false; paint(); place();
  }
  ta.addEventListener('input', () => { if (!ta.dataset.busy) update(); });     // úpravy z smart.js hlásí 'dilna-caret' až po nastavení kurzoru
  ta.addEventListener('dilna-caret', () => update());
  ta.addEventListener('blur', () => setTimeout(close, 120));
  ta.addEventListener('scroll', () => open() && place());
  ta.addEventListener('keydown', (e) => {
    if (!open()) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); e.stopImmediatePropagation(); sel = (sel + (e.key === 'ArrowDown' ? 1 : items.length - 1)) % items.length; paint(); }
    else if (e.key === 'Enter' || e.key === 'Tab') { if (e.ctrlKey || e.metaKey) return close(); e.preventDefault(); e.stopImmediatePropagation(); accept(); }
    else if (e.key === 'Escape') { e.preventDefault(); e.stopImmediatePropagation(); close(); }
  }, true);   // capture: musí se spustit dřív než klávesy chytrého editoru
  box.addEventListener('mousedown', (e) => { e.preventDefault(); const i = e.target.closest('.ac-i'); if (i) accept(+i.dataset.i); });
  return { close, open };
}
