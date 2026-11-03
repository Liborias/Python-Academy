// Zvýrazňování syntaxe Pythonu: jeden průchod regulárním výrazem přes celý text (zvládne i víceřádkové řetězce).
import { KEYWORDS, BUILTINS, esc } from './lexicon.js';
import { fstringHL, isFString } from './fstring.js';
export { KEYWORDS, BUILTINS };
const KW = new Set(KEYWORDS), BI = new Set(BUILTINS);
const RE = /(#[^\n]*)|([rRbBuUfF]{0,2}(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*(?:"|$)|'(?:\\.|[^'\\\n])*(?:'|$)))|(\b\d[\d_]*\.?\d*(?:[eE][+-]?\d+)?\b|\.\d+)|(@[A-Za-z_][\w.]*)|([A-Za-z_]\w*)/g;

export function highlight(src) {
  let out = '', last = 0, prev = '', m;
  RE.lastIndex = 0;
  while ((m = RE.exec(src))) {
    out += esc(src.slice(last, m.index));
    const t = m[0];
    let cls = '';
    if (m[1]) cls = 'c-com';
    else if (m[2]) { out += isFString(t) ? fstringHL(t) : `<span class="c-str">${esc(t)}</span>`; prev = ''; last = RE.lastIndex; continue; }
    else if (m[3]) cls = 'c-num';
    else if (m[4]) cls = 'c-dec';
    else if (m[5]) cls = prev === 'def' || prev === 'class' ? 'c-fn' : KW.has(t) ? 'c-kw' : BI.has(t) ? 'c-bi' : '';
    out += cls ? `<span class="${cls}">${esc(t)}</span>` : esc(t);
    if (m[5]) prev = t; else if (!/^\s+$/.test(t)) prev = '';
    last = RE.lastIndex;
    if (m[0] === '') RE.lastIndex++;
  }
  return out + esc(src.slice(last)) + '\n';
}
