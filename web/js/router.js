// Jednoduchý hash router: #/ , #/kurz/<id> , #/kurz/<id>/<lekce> , #/priprava
const routes = [];
export const route = (re, fn) => routes.push([re, fn]);
export function start(notFound) {
  const go = () => {
    const path = location.hash.replace(/^#/, '') || '/';
    for (const [re, fn] of routes) {
      const m = path.match(re);
      if (m) { fn(...m.slice(1).map(decodeURIComponent)); window.scrollTo(0, 0); return; }
    }
    notFound(path);
  };
  addEventListener('hashchange', go);
  go();
}
