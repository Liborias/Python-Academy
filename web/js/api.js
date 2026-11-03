// Komunikace se serverem. Token dostaneme v adrese (?t=...), uložíme ho a z adresy odstraníme.
let token = '';
try {
  const u = new URL(location.href);
  const t = u.searchParams.get('t');
  if (t) {
    sessionStorage.setItem('dilna-token', t);
    u.searchParams.delete('t');
    history.replaceState(null, '', u.pathname + u.search + u.hash);
  }
  token = sessionStorage.getItem('dilna-token') || '';
} catch { /* soukromé okno apod.; bez tokenu půjde jen prohlížení */ }

export const hasToken = () => !!token;

export async function api(path, body) {
  const opt = { headers: { 'X-Dilna-Token': token } };
  if (body !== undefined) {
    opt.method = 'POST';
    opt.headers['Content-Type'] = 'application/json';
    opt.body = JSON.stringify(body);
  }
  const r = await fetch(path, opt);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || `Chyba serveru (${r.status})`);
  return data;
}
