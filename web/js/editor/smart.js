// Chytré úpravy: závorky a uvozovky, odsazování po ":", Backspace po 4 mezerách, Tab, komentování, zarovnání.
import { formatCode } from './format.js';
import { contextAt } from './context.js';

const IND = '    ';
const PAIRS = { '(': ')', '[': ']', '{': '}' };
const CLOSERS = new Set([')', ']', '}']);
const lineStart = (v, i) => i > 0 ? v.lastIndexOf('\n', i - 1) + 1 : 0;
const lineEnd = (v, i) => { const e = v.indexOf('\n', i); return e < 0 ? v.length : e; };

export function attachSmart(ta, { onRun, onChange }) {
  let busy = false, escTab = false;

  // Nahradí [a,b) textem t pomocí execCommand (zachová Ctrl+Z); kurzor dá na a + caret.
  function replace(a, b, t, caret = t.length) {
    busy = true; ta.dataset.busy = '1';
    ta.focus(); ta.setSelectionRange(a, b);
    let ok = true;
    try { ok = t === '' ? document.execCommand('delete') : document.execCommand('insertText', false, t); } catch { ok = false; }
    if (!ok) { ta.setRangeText(t, a, b, 'end'); ta.dispatchEvent(new Event('input', { bubbles: true })); }
    ta.setSelectionRange(a + caret, a + caret);
    busy = false; delete ta.dataset.busy;
    ta.dispatchEvent(new Event('dilna-caret'));
  }
  // Úryvek s | jako kurzorem; další řádky dostanou odsazení aktuálního řádku.
  function replaceSnippet(a, b, t) {
    const v = ta.value, ind = v.slice(lineStart(v, a)).match(/^ */)[0];
    t = t.split('\n').join('\n' + ind);
    const c = t.indexOf('|');
    replace(a, b, c < 0 ? t : t.replace('|', ''), c < 0 ? t.length : c);
  }
  const dedentElse = (v, s) => {
    const ls = lineStart(v, s), before = v.slice(ls, s);
    if (!/^ {4,}(else|elif .*|except.*|finally)$/.test(before)) return false;
    const ind = before.match(/^ */)[0];
    const prevLines = v.slice(0, ls).split('\n'); prevLines.pop();
    while (prevLines.length && !prevLines[prevLines.length - 1].trim()) prevLines.pop();
    const p = prevLines[prevLines.length - 1];
    if (p === undefined || p.match(/^ */)[0] !== ind || /:\s*$/.test(p)) return false;
    replace(ls, ls + 4, '', 0);
    return true;
  };

  ta.addEventListener('beforeinput', (e) => {
    if (busy || ta.readOnly) return;
    const v = ta.value, s = ta.selectionStart, en = ta.selectionEnd, t = e.inputType;
    if (t === 'insertText' && e.data && e.data.length === 1) {
      const ch = e.data, next = v[en] || '', prev = v[s - 1] || '', sel = v.slice(s, en);
      if (CLOSERS.has(ch) && s === en && next === ch) { e.preventDefault(); ta.setSelectionRange(s + 1, s + 1); return; }
      if (ch === '{' && !sel && contextAt(v.slice(0, s)) === 'fstring') { e.preventDefault(); replace(s, en, '{}', 1); return; }   // f-řetězec: {} vždy do páru
      if (ch in PAIRS) {
        if (sel) { e.preventDefault(); replace(s, en, ch + sel + PAIRS[ch], sel.length + 2); return; }
        if (!next || /[\s)\]},:]/.test(next)) { e.preventDefault(); replace(s, en, ch + PAIRS[ch], 1); return; }
      }
      if (ch === '"' || ch === "'") {
        if (sel) { e.preventDefault(); replace(s, en, ch + sel + ch, sel.length + 2); return; }
        if (next === ch) { e.preventDefault(); ta.setSelectionRange(s + 1, s + 1); return; }
        if (v.slice(s - 2, s) === ch + ch && v[s - 3] !== ch) { e.preventDefault(); replace(s, en, ch + ch + ch, 1); return; }
        const wordBefore = /[\w]$/.test(prev) && !/(^|[^\w])[rRbBuUfF]{1,2}$/.test(v.slice(lineStart(v, s), s));
        if (!wordBefore && (!next || /[\s)\]},:]/.test(next))) { e.preventDefault(); replace(s, en, ch + ch, 1); return; }
      }
      if (ch === ':' && s === en) { if (dedentElse(v, s)) { /* dvojtečka se vloží normálně */ } return; }
    } else if (t === 'insertLineBreak' || t === 'insertParagraph') {
      e.preventDefault();
      const ls = lineStart(v, s), before = v.slice(ls, s);
      let ind = before.match(/^[ \t]*/)[0];
      const code = before.replace(/\s+#.*$/, '').trimEnd();
      const prev = v[s - 1] || '', next = v[en] || '';
      if (/:$/.test(code)) ind += IND;
      else if (/^\s*(return|pass|break|continue|raise)\b/.test(before) && ind.length >= 4 && !/[([{,]\s*$/.test(code)) ind = ind.slice(0, -4);
      if (prev in PAIRS && PAIRS[prev] === next) { replace(s, en, '\n' + ind + IND + '\n' + ind, 1 + ind.length + 4); return; }
      if (prev in PAIRS) ind += IND;
      replace(s, en, '\n' + ind);
    } else if (t === 'deleteContentBackward' && s === en && s > 0) {
      const prev = v[s - 1], next = v[s] || '';
      if ((prev in PAIRS && PAIRS[prev] === next) || ((prev === '"' || prev === "'") && next === prev)) { e.preventDefault(); replace(s - 1, s + 1, '', 0); return; }
      const before = v.slice(lineStart(v, s), s);
      if (/^ +$/.test(before)) { e.preventDefault(); const n = before.length % 4 || 4; replace(s - n, s, '', 0); }
    }
  });

  function eachLine(fn) {
    const v = ta.value; let s = ta.selectionStart, en = ta.selectionEnd;
    const a = lineStart(v, s), b = lineEnd(v, en > s && v[en - 1] === '\n' ? en - 1 : en);
    const lines = v.slice(a, b).split('\n').map(fn);
    const text = lines.join('\n');
    replace(a, b, text, text.length);
    ta.setSelectionRange(a, a + text.length);
  }
  const indent = () => eachLine((l) => (l.trim() ? IND + l : l));
  const dedent = () => eachLine((l) => l.replace(/^( {1,4}|\t)/, ''));
  const toggleComment = () => {
    const v = ta.value, s = ta.selectionStart, en = ta.selectionEnd;
    const direction = ta.selectionDirection;
    const a = lineStart(v, s), b = lineEnd(v, en > s && v[en - 1] === '\n' ? en - 1 : en);
    const ls = v.slice(a, b).split('\n'), act = ls.filter((l) => l.trim());
    const allCom = act.length && act.every((l) => /^\s*#/.test(l));
    const min = act.length ? Math.min(...act.map((l) => l.match(/^[ \t]*/)[0].length)) : ls[0].length;
    const edits = []; let offset = a;
    const out = ls.map((l) => {
      const start = offset; offset += l.length + 1;
      if (!l.trim() && ls.length > 1) return l;
      const prefix = allCom ? l.match(/^([ \t]*)# ?/) : null;
      const at = prefix ? prefix[1].length : min, removed = prefix ? prefix[0].length - at : 0;
      const added = allCom ? '' : '# ';
      edits.push({ at: start + at, removed, added: added.length });
      return l.slice(0, at) + added + l.slice(at + removed);
    }).join('\n');
    if (out === v.slice(a, b)) return;
    // Zachovat původní výběr i kurzor; koncový začátek dalšího řádku se nekomentuje.
    const moved = (pos) => {
      let delta = 0;
      for (const edit of edits) {
        if (pos < edit.at) break;
        if (pos <= edit.at + edit.removed) return edit.at + delta + edit.added;
        delta += edit.added - edit.removed;
      }
      return pos + delta;
    };
    replace(a, b, out, moved(s) - a);
    ta.setSelectionRange(moved(s), moved(en), direction);
    ta.dispatchEvent(new Event('dilna-caret'));
  };
  const format = () => {
    const before = ta.value, after = formatCode(before);
    if (after === before) return;
    const pos = ta.selectionStart;
    replace(0, before.length, after, Math.min(pos, after.length));
  };

  ta.addEventListener('keydown', (e) => {
    if (ta.readOnly) return;
    const mod = e.ctrlKey || e.metaKey;
    if (e.key === 'Escape') { escTab = true; setTimeout(() => (escTab = false), 1500); return; }
    if (e.key === 'Tab' && !mod && !e.altKey) {
      if (escTab) return;                         // Esc, pak Tab = opustit editor
      e.preventDefault();
      const v = ta.value, s = ta.selectionStart, en = ta.selectionEnd;
      if (e.shiftKey) return dedent();
      if (s !== en && v.slice(s, en).includes('\n')) return indent();
      const col = s - lineStart(v, s);
      replace(s, en, ' '.repeat(4 - (col % 4)));
    } else if (mod && !e.altKey && (e.key === '/' || (e.shiftKey && e.code === 'Digit7'))) { e.preventDefault(); toggleComment(); }
    else if (mod && e.key === ']') { e.preventDefault(); indent(); }
    else if (mod && e.key === '[') { e.preventDefault(); dedent(); }
    else if (mod && e.key === 'Enter') { e.preventDefault(); onRun && onRun(); }
    else if ((mod && e.shiftKey && e.key.toLowerCase() === 'f') || (e.altKey && e.shiftKey && e.key.toLowerCase() === 'f')) { e.preventDefault(); format(); }
  });
  return { replace, replaceSnippet, format };
}
