// Malý bezpečný Markdown: nadpisy ##/###, odstavce, seznamy, ``` bloky, `kód`, **tučné**, *kurzíva*, [odkaz](https://..), > poznámka.
import { esc } from './util.js';

function inline(t) {
  const codes = [];
  t = t.replace(/`([^`]+)`/g, (_, c) => { codes.push(c); return `\u0000${codes.length - 1}\u0000`; });
  t = esc(t)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  return t.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${esc(codes[+i])}</code>`);
}

let boxN = 0;
function listItem(t) {
  const m = t.match(/^\[( |x)\]\s+(.*)$/);
  if (!m) return `<li>${inline(t)}</li>`;
  const id = 'chk-' + (++boxN);
  return `<li class="task"><label><input type="checkbox" data-chk="${id}" ${m[1] === 'x' ? 'checked' : ''}> ${inline(m[2])}</label></li>`;
}

export function markdown(src) {
  boxN = 0;
  const lines = src.replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (/^```/.test(l)) {
      const buf = []; i++;
      while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
      i++;
      out.push(`<pre class="code"><code>${esc(buf.join('\n'))}</code></pre>`);
    } else if (/^#{1,3}\s/.test(l)) {
      const n = l.match(/^#+/)[0].length;
      out.push(`<h${n + 1}>${inline(l.replace(/^#+\s+/, ''))}</h${n + 1}>`); i++;
    } else if (/^[-*]\s/.test(l)) {
      const items = [];
      while (i < lines.length && /^[-*]\s/.test(lines[i])) items.push(listItem(lines[i++].replace(/^[-*]\s+/, '')));
      out.push(`<ul>${items.join('')}</ul>`);
    } else if (/^\d+\.\s/.test(l)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) items.push(`<li>${inline(lines[i++].replace(/^\d+\.\s+/, ''))}</li>`);
      out.push(`<ol>${items.join('')}</ol>`);
    } else if (/^>\s?/.test(l)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) buf.push(lines[i++].replace(/^>\s?/, ''));
      out.push(`<div class="note">${inline(buf.join(' '))}</div>`);
    } else if (!l.trim()) {
      i++;
    } else {
      const buf = [];
      while (i < lines.length && lines[i].trim() && !/^(```|#{1,3}\s|[-*]\s|\d+\.\s|>)/.test(lines[i])) buf.push(lines[i++]);
      out.push(`<p>${inline(buf.join(' '))}</p>`);
    }
  }
  return out.join('\n');
}
