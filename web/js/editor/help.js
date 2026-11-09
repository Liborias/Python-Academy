// Okno s nápovědou k editoru (tlačítko ? v rohu).
const ROWS = [
  ['Čísla řádků', 'Vlevo ukazují pořadí řádků v kódu, včetně prázdných. Aktualizují se při psaní a posouvají se spolu s kódem. Při kopírování kódu se nepřidávají.'],
  ['Našeptávač', 'Píšete-li aspoň 2 znaky (nebo tečku), objeví se nabídka. ↑ ↓ vybírají, Enter nebo Tab vloží, Esc zavře.'],
  ['f-řetězce', 'Složené závorky { } se barevně odliší, uvnitř se zvýrazní proměnné, čísla, řetězce a volání. Po napsání { se nabídnou proměnné z kódu. Za dvojtečkou (formát) a v textu řetězce se nenašeptává.'],
  ['Úryvky', 'def, for, while, if, try, class, with, main, print… se po výběru rozbalí do celé struktury.'],
  ['Závorky a uvozovky', 'Zavírací znak se doplní sám, při psaní se přeskočí. Označený text se jimi obalí. Backspace smaže prázdný pár.'],
  ['Enter', 'Zachová odsazení, po dvojtečce přidá 4 mezery. Po return, pass, break, continue a raise odsazení vrátí o úroveň zpět.'],
  ['else, elif, except, finally', 'Po napsání dvojtečky se řádek sám zarovná k příslušnému bloku.'],
  ['Tab / Shift+Tab', 'Vloží mezery do násobku 4, na označených řádcích odsadí nebo předsadí.'],
  ['Backspace', 'V odsazení maže po 4 mezerách.'],
  ['Ctrl+/ nebo Ctrl+Shift+7', 'Bez výběru přidá nebo odebere komentář # na aktuálním řádku. Označíte-li více řádků, přepne celý blok: jsou-li všechny neprázdné řádky zakomentované, odkomentuje je; jinak přidá #. Prázdné řádky uvnitř bloku zachová. Ctrl+Shift+7 je alternativa pro klávesnice s hůře dostupným lomítkem.'],
  ['Ctrl+] a Ctrl+[', 'Odsadí nebo předsadí označené řádky.'],
  ['Ctrl+Shift+F  (Alt+Shift+F)', 'Zarovná kód: tabulátory na mezery, smaže mezery na koncích řádků a přebytečné prázdné řádky.'],
  ['Ctrl+Enter', 'Spustí program.'],
  ['Esc, potom Tab', 'Opustí editor (pro ovládání klávesnicí).'],
  ['Ctrl+Z / Ctrl+Y', 'Zpět a znovu (funguje i po automatických úpravách).'],
];
let dlg = null;
export function openHelp() {
  if (!dlg) {
    dlg = document.createElement('dialog'); dlg.className = 'dlg';
    dlg.innerHTML = `<h2>Nápověda k editoru</h2><table><tbody>${ROWS.map(([k, d]) => `<tr><th scope="row">${k}</th><td>${d}</td></tr>`).join('')}</tbody></table>
      <p class="hint">Mac: místo Ctrl používejte Cmd.</p><form method="dialog"><button class="btn primary">Zavřít</button></form>`;
    document.body.appendChild(dlg);
  }
  dlg.showModal();
}
