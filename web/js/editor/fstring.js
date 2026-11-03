// Zvýraznění f-řetězců: text jako řetězec, {závorky}, uvnitř proměnné, volání, atributy, čísla, řetězce a závorky,
// za ":" formátování (např. >3 nebo .2f) a za "!" převod (!r, !s, !a).
import { KEYWORDS, BUILTINS, esc, span } from './lexicon.js';

const KW = new Set(KEYWORDS), BI = new Set(BUILTINS);
const EXPR = /([rRbBuUfF]{0,2}(?:"(?:\\.|[^"\\])*"?|'(?:\\.|[^'\\])*'?))|(\b\d[\d_]*\.?\d*(?:[eE][+-]?\d+)?\b)|([A-Za-z_]\w*)(\s*\()?|([()[\]])/g;

export const isFString = (tok) => /^[rRuU]?[fF][rR]?["']/.test(tok) || /^[rR][fF]["']/.test(tok);

function exprHL(e) {
  let out = '', last = 0, m;
  EXPR.lastIndex = 0;
  while ((m = EXPR.exec(e))) {
    out += esc(e.slice(last, m.index));
    if (m[1]) out += span('c-str', esc(m[0]));
    else if (m[2]) out += span('c-num', esc(m[0]));
    else if (m[3]) {
      const name = m[3], afterDot = e[m.index - 1] === '.';
      const cls = KW.has(name) ? 'c-kw' : afterDot ? (m[4] ? 'c-call' : 'c-attr') : BI.has(name) ? 'c-bi' : m[4] ? 'c-call' : 'c-var';
      out += span(cls, esc(name)) + (m[4] ? esc(m[4].slice(0, -1)) + span('c-par', '(') : '');
    } else out += span('c-par', esc(m[0]));
    last = EXPR.lastIndex;
  }
  return out + esc(e.slice(last));
}

// Konec formátovací části: první } mimo vnořené {…}
function specEnd(t, i) {
  let d = 0;
  for (; i < t.length; i++) {
    if (t[i] === '{') d++;
    else if (t[i] === '}') { if (d === 0) return i; d--; }
  }
  return -1;
}

export function fstringHL(t) {
  const m = /^([rRbBuUfF]{0,2})("""|'''|"|')/.exec(t);
  const q = m[2];
  let out = '', lit = m[0], i = m[0].length;
  const flush = () => { if (lit) { out += span('c-str', esc(lit)); lit = ''; } };
  while (i < t.length) {
    const c = t[i];
    if (c === '\\') { lit += t.slice(i, i + 2); i += 2; continue; }
    if ((c === '{' && t[i + 1] === '{') || (c === '}' && t[i + 1] === '}')) { lit += c + c; i += 2; continue; }
    if (t.startsWith(q, i)) { lit += q; i += q.length; break; }
    if (c !== '{') { lit += c; i++; continue; }
    flush();
    let depth = 0, j = i + 1, inq = '', end = -1;
    for (; j < t.length; j++) {
      const ch = t[j];
      if (inq) { if (ch === '\\') j++; else if (ch === inq) inq = ''; continue; }
      if (ch === '"' || ch === "'") { if (q.length === 1 && ch === q) break; inq = ch; continue; }
      if ('([{'.includes(ch)) depth++;
      else if (')]}'.includes(ch)) { if (depth === 0) { end = j; break; } depth--; }
      else if (depth === 0 && (ch === ':' || (ch === '!' && t[j + 1] !== '='))) { end = j; break; }
    }
    if (end < 0) { out += span('c-brace', '{') + exprHL(t.slice(i + 1, j)); i = j; continue; }   // nedokončená závorka
    out += span('c-brace', '{') + exprHL(t.slice(i + 1, end));
    let k = end;
    if (t[k] === '!') { out += span('c-spec', esc(t.slice(k, k + 2))); k += 2; }
    if (t[k] === ':') {
      const close = specEnd(t, k + 1);
      const spec = t.slice(k, close < 0 ? t.length : close);
      let s = '', p = 0, r;
      const NEST = /\{([^{}]*)\}/g;
      while ((r = NEST.exec(spec))) {          // vnořené {šířka} ve formátu
        s += span('c-spec', esc(spec.slice(p, r.index))) + span('c-brace', '{') + exprHL(r[1]) + span('c-brace', '}');
        p = NEST.lastIndex;
      }
      out += s + span('c-spec', esc(spec.slice(p)));
      k = close < 0 ? t.length : close;
    }
    if (t[k] === '}') { out += span('c-brace', '}'); k++; }
    i = k;
  }
  flush();
  return out + esc(t.slice(i));
}
