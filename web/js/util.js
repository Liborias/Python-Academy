export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
export const stars = (n) => `<span class="stars" role="img" aria-label="Obtížnost ${n} z 4">${'★'.repeat(n)}<i>${'★'.repeat(4 - n)}</i></span>`;
export const STATUS = { concept: 'Koncept', ready: 'Hotovo', draft: 'Rozpracováno', planned: 'Připravujeme' };
