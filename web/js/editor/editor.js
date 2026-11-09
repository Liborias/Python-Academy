// Editor kódu v Pythonu: textarea nad zvýrazněnou vrstvou. Rozhraní: createEditor(el, text, {readOnly, onChange}) -> {get,set,onRun,focus}.
import { highlight } from './highlight.js';
import { attachSmart } from './smart.js';
import { attachComplete } from './autocomplete.js';
import { openHelp } from './help.js';

export function createEditor(el, text, opts = {}) {
  const wrap = document.createElement('div'); wrap.className = 'ed';
  const gutter = document.createElement('div'); gutter.className = 'ed-gutter'; gutter.setAttribute('aria-hidden', 'true');
  const numbers = document.createElement('pre'); numbers.className = 'ed-lines'; gutter.appendChild(numbers);
  const code = document.createElement('div'); code.className = 'ed-code';
  const pre = document.createElement('pre'); pre.className = 'ed-hl'; pre.setAttribute('aria-hidden', 'true');
  const ta = document.createElement('textarea'); ta.className = 'ed-ta';
  ta.value = text.replace(/\s+$/, '') + '\n'; ta.spellcheck = false; ta.readOnly = !!opts.readOnly;
  ta.setAttribute('autocapitalize', 'off'); ta.setAttribute('autocomplete', 'off'); ta.setAttribute('wrap', 'off');
  ta.setAttribute('aria-label', opts.readOnly ? 'Ukázka kódu v Pythonu' : 'Editor kódu v Pythonu');
  code.append(pre, ta); wrap.append(gutter, code); el.appendChild(wrap);

  let run = () => {}, lineCount = 0;
  const paint = () => {
    pre.innerHTML = highlight(ta.value);
    const count = ta.value.split('\n').length;
    if (count !== lineCount) {
      numbers.textContent = Array.from({ length: count }, (_, i) => i + 1).join('\n');
      wrap.style.setProperty('--ed-gutter', `calc(${Math.max(2, String(count).length)}ch + 20px)`);
      lineCount = count;
    }
  };
  const fit = () => {
    const { scrollTop, scrollLeft } = ta;
    ta.style.height = 'auto'; ta.style.height = Math.min(Math.max(ta.scrollHeight + 2, 90), 560) + 'px';
    ta.scrollTop = scrollTop; ta.scrollLeft = scrollLeft;
  };
  const sync = () => { pre.scrollTop = numbers.scrollTop = ta.scrollTop; pre.scrollLeft = ta.scrollLeft; };
  const refresh = () => { paint(); fit(); sync(); };
  ta.addEventListener('input', () => { refresh(); opts.onChange && opts.onChange(ta.value); });
  ta.addEventListener('scroll', sync);

  if (!opts.readOnly) {
    const smart = attachSmart(ta, { onRun: () => run() });
    attachComplete(ta, (a, b, t) => smart.replaceSnippet(a, b, t));   // musí být před smart keydown? ne: používá stopImmediatePropagation
    const help = document.createElement('button');
    help.type = 'button'; help.className = 'ed-help'; help.textContent = '?'; help.title = 'Nápověda k editoru a klávesové zkratky';
    help.setAttribute('aria-label', 'Nápověda k editoru');
    help.addEventListener('click', openHelp);
    code.appendChild(help);
  }
  refresh();
  document.fonts && document.fonts.ready.then(refresh);
  return { get: () => ta.value, set: (v) => { ta.value = v; refresh(); opts.onChange && opts.onChange(v); },
           onRun: (f) => { run = f; }, focus: () => ta.focus() };
}
