// Ukládání postupu a nastavení do localStorage (vše v try/catch, aplikace funguje i bez něj).
const KEY = 'dilna-python-v1';
let mem = { done: {}, theme: '' };

function load() {
  try { const s = localStorage.getItem(KEY); if (s) mem = { ...mem, ...JSON.parse(s) }; } catch { /* ignoruj */ }
}
function save() { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch { /* ignoruj */ } }
load();

export const isDone = (course, lesson) => !!(mem.done[course] && mem.done[course][lesson]);
export const doneCount = (course) => Object.keys(mem.done[course] || {}).length;
export function markDone(course, lesson, on = true) {
  const c = (mem.done[course] ||= {});
  if (on) c[lesson] = 1; else delete c[lesson];
  save();
}
export const getTheme = () => mem.theme;
export function setTheme(t) { mem.theme = t; save(); applyTheme(); }
export function applyTheme() {
  const r = document.documentElement;
  if (mem.theme) r.setAttribute('data-theme', mem.theme); else r.removeAttribute('data-theme');
}

// Zaškrtnuté položky kontrolního seznamu (příprava prostředí)
export const getChecks = () => mem.checks || {};
export function setCheck(id, on) { mem.checks = { ...(mem.checks || {}), [id]: on ? 1 : 0 }; save(); }
