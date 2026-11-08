// Postup a nastavení se ukládají pod původním klíčem; rozepsaný kód má vlastní klíče.
const KEY = 'dilna-python-v1';
const dict = () => Object.create(null);
const record = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

function flags(value, depth, keepOff = false) {
  const result = dict();
  if (!record(value)) return result;
  for (const [key, item] of Object.entries(value)) {
    if (depth === 1) {
      if (item === 1 || item === true) result[key] = 1;
      else if (keepOff && (item === 0 || item === false)) result[key] = 0;
    } else {
      const nested = flags(item, depth - 1);
      if (Object.keys(nested).length) result[key] = nested;
    }
  }
  return result;
}

function normalize(value) {
  return {
    ...value,
    done: flags(value.done, 2),
    theme: ['dark', 'light'].includes(value.theme) ? value.theme : '',
    checks: flags(value.checks, 1, true),
    tasks: flags(value.tasks, 3),
  };
}

let mem = normalize({});
let storageProblem = false;
// Při odmítnutém zápisu uchováme vlastní operace i pro příští pokus o uložení.
let pending = [];
function refresh() {
  let raw;
  try { raw = localStorage.getItem(KEY); }
  catch { storageProblem = true; return; }
  try {
    const value = raw === null ? {} : JSON.parse(raw);
    if (!record(value)) return;
    mem = normalize(value);
    for (const change of pending) change(mem);
  } catch { /* Nedostupné či nerozpoznatelné úložiště nepřepíše stav této stránky. */ }
}
function update(change) {
  // Každý zápis začne aktuálním stavem ostatních karet, nikoli starým snímkem.
  refresh();
  change(mem);
  pending.push(change);
  try {
    localStorage.setItem(KEY, JSON.stringify(mem));
    pending = [];
    storageProblem = false;
  } catch { storageProblem = true; }
  dispatchEvent(new Event('dilna-store-change'));
}
refresh();

export const hasStorageProblem = () => storageProblem;
export const isDone = (course, lesson) => !!mem.done[course]?.[lesson];
export const doneCount = (course) => Object.keys(mem.done[course] || {}).length;
export function markDone(course, lesson, on = true) {
  update((state) => {
    const lessons = (state.done[course] ||= dict());
    if (on) lessons[lesson] = 1; else delete lessons[lesson];
  });
}
export const getTheme = () => mem.theme;
export function setTheme(theme) { update((state) => { state.theme = theme; }); applyTheme(); }
export function applyTheme() {
  const root = document.documentElement;
  if (mem.theme) root.setAttribute('data-theme', mem.theme); else root.removeAttribute('data-theme');
}

// Zaškrtnuté položky kontrolního seznamu (příprava prostředí).
export const getChecks = () => mem.checks;
export function setCheck(id, on) { update((state) => { state.checks[id] = on ? 1 : 0; }); }

// Procvičovací úkoly se evidují samostatně, staré označení lekcí se nemění.
export const isTaskDone = (course, lesson, task) => !!mem.tasks[course]?.[lesson]?.[task];
export function markTaskDone(course, lesson, task) {
  update((state) => {
    const lessons = (state.tasks[course] ||= dict());
    (lessons[lesson] ||= dict())[task] = 1;
  });
}

addEventListener('storage', (event) => {
  if (event.key !== KEY && event.key !== null) return;
  // Čteme nejnovější obsah; opožděná událost nesmí vrátit starší snímek.
  refresh();
  applyTheme();
  dispatchEvent(new Event('dilna-store-change'));
});
