// Zjistí, kde v kódu se nachází kurzor: 'code', 'comment', 'string', 'fstring' (text f-řetězce),
// 'fexpr' (uvnitř {…} f-řetězce) nebo 'fspec' (formátovací část za dvojtečkou, např. {x:.2f}).
// Prochází celý text před kurzorem, takže zvládne i víceřádkové řetězce.

function scanExpr(s, i, q) {           // i je za otevírací {
  let depth = 0;
  const n = s.length;
  while (i < n) {
    const c = s[i];
    if (c === '"' || c === "'") {
      if (c === q[0] && q.length === 1) return { end: i };   // f-řetězec končí, závorka zůstala otevřená
      const r = scanString(s, i + 1, c, false);
      if (r.ctx) return { ctx: 'string' };
      i = r.end; continue;
    }
    if ('([{'.includes(c)) depth++;
    else if (')]}'.includes(c)) { if (depth === 0) return { end: i + 1 }; depth--; }
    else if (depth === 0 && c === ':') {
      let d = 0, e = -1;
      for (let k = i + 1; k < n; k++) { if (s[k] === '{') d++; else if (s[k] === '}') { if (d === 0) { e = k; break; } d--; } }
      return e < 0 ? { ctx: 'fspec' } : { end: e + 1 };
    }
    i++;
  }
  return { ctx: 'fexpr' };
}

function scanString(s, i, q, isF) {    // i je za otevírací uvozovkou
  const n = s.length;
  while (i < n) {
    const c = s[i];
    if (c === '\\') { i += 2; continue; }
    if (s.startsWith(q, i)) return { end: i + q.length };
    if (q.length === 1 && c === '\n') return { end: i };    // nedokončený řetězec končí řádkem
    if (isF && c === '{') {
      if (s[i + 1] === '{') { i += 2; continue; }
      const r = scanExpr(s, i + 1, q);
      if (r.ctx) return { end: n, ctx: r.ctx };
      i = r.end; continue;
    }
    i++;
  }
  return { end: n, ctx: isF ? 'fstring' : 'string' };
}

export function contextAt(s) {
  let i = 0;
  const n = s.length;
  while (i < n) {
    const c = s[i];
    if (c === '#') { const e = s.indexOf('\n', i); if (e < 0) return 'comment'; i = e + 1; continue; }
    if (c === '"' || c === "'") {
      let k = i;
      while (k > 0 && i - k < 2 && /[rRbBuUfF]/.test(s[k - 1])) k--;
      const pre = k < i && !/\w/.test(s[k - 1] || '') ? s.slice(k, i) : '';
      const q = s.startsWith(c.repeat(3), i) ? c.repeat(3) : c;
      const r = scanString(s, i + q.length, q, /[fF]/.test(pre) && !/[bB]/.test(pre));
      if (r.ctx) return r.ctx;
      i = r.end; continue;
    }
    i++;
  }
  return 'code';
}
