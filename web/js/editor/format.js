// Zarovnání kódu: tabulátory na 4 mezery, odstranění mezer na koncích řádků, nejvýše 2 prázdné řádky za sebou, konec souboru s novým řádkem.
// Odsazení bloků kód nemění (v Pythonu má význam, nesmí se hádat).
export function formatCode(src) {
  const lines = src.replace(/\r\n?/g, '\n').split('\n').map((l) => l.replace(/^\t+/, (t) => '    '.repeat(t.length)).replace(/[ \t]+$/, ''));
  const out = [];
  let blank = 0;
  for (const l of lines) {
    blank = l === '' ? blank + 1 : 0;
    if (blank <= 2) out.push(l);
  }
  return out.join('\n').replace(/\n+$/, '') + '\n';
}
