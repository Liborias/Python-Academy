// Společná příprava kurzu: stejná na jeho začátku i v průvodci nastavením.
import { api } from './api.js';
import { esc } from './util.js';
import { getChecks, setCheck } from './store.js';

const SYSTEMS = { windows: 'Windows (PowerShell)', macos: 'macOS', linux: 'Linux (Debian / Ubuntu)' };
const EDITORS = { vscode: 'VS Code', vscodium: 'VSCodium', pycharm: 'PyCharm' };

export async function renderPreparation(el, course) {
  el.textContent = 'Načítám přípravu…';
  let profile;
  try {
    profile = await api(`/api/preparation?course=${encodeURIComponent(course)}`);
  } catch (error) {
    el.innerHTML = `<p class="hint" role="status">Přípravu se nepodařilo načíst. ${esc(error.message)}</p>
      <button type="button" class="btn" data-prep-retry>Zkusit znovu</button>`;
    el.querySelector('[data-prep-retry]').addEventListener('click', () => renderPreparation(el, course));
    return;
  }
  let options = { os: 'windows', editor: 'vscodium' };
  try { options = { ...options, ...JSON.parse(localStorage.getItem('dilna-preparation-options') || '{}') }; } catch { /* výchozí volby */ }
  if (!SYSTEMS[options.os]) options.os = 'windows';
  if (!EDITORS[options.editor]) options.editor = 'vscodium';
  const select = (key, label, values) => `<label>${label} <select data-prep="${key}">${Object.entries(values).map(([v, t]) =>
    `<option value="${v}" ${options[key] === v ? 'selected' : ''}>${t}</option>`).join('')}</select></label>`;
  el.innerHTML = `<h2>Než začnete: příprava prostředí</h2>
    <p>${esc(profile.focus)}</p>
    <div class="prep-options">${select('os', 'Operační systém', SYSTEMS)}${select('editor', 'Editor', EDITORS)}</div>
    <div class="prep-instructions"></div>`;

  function draw() {
    const windows = options.os === 'windows';
    const python = windows ? 'py -3.14' : 'python3';
    const venv = windows ? '.\\.venv\\Scripts\\python.exe' : './.venv/bin/python';
    const interpreter = windows ? '.venv\\Scripts\\python.exe' : '.venv/bin/python';
    const install = options.os === 'windows'
      ? 'Stáhněte Python 3.14 z python.org. U klasického instalátoru zvolte instalaci launcheru a přidání Pythonu do PATH. Otevřete nový terminál a ověřte py -3.14 --version.'
      : options.os === 'macos'
        ? 'Použijte instalátor z python.org nebo Homebrew: brew install python@3.14. V novém terminálu ověřte python3 --version a cestu k používanému Pythonu.'
        : 'Pro systémový Python na Debianu/Ubuntu: sudo apt update a sudo apt install python3 python3-venv python3-pip. Verzi ověřte: python3 --version. Balíčky distribuce nemusí nabízet 3.14; potřebujete alespoň 3.12, doporučujeme 3.14. Systémový Python nepřepisujte.';
    const editor = options.editor === 'pycharm'
      ? `Otevřete složku dilna-pythonu jako projekt. V Settings → Project → Python Interpreter (název se může lišit) zvolte existující interpreter ${interpreter}. Nevytvářejte další venv, pokud už .venv máte. V Run Configuration nastavte skript start.py a pracovní složku projektu. Rozšíření VS Code sem neinstalujte.`
      : `${EDITORS[options.editor]}: otevřete celou složku dilna-pythonu. Doinstalujte Python, Python Debugger, BasedPyright a Ruff ${options.editor === 'vscodium' ? 'z Open VSX' : 'z Marketplace'}. Python: Select Interpreter → ${interpreter}. Nastavení .vscode v tomto projektu používá BasedPyright; nezapínejte současně druhý jazykový server. Pro Pandas přidejte Jupyter a vyberte stejné jádro .venv.`;
    const commands = [
      `${python} --version`,
      `${python} tools/setup_env.py --courses ${course}`,
      `${venv} -c "import sys; print(sys.executable); print(sys.version)"`,
      `${venv} -m pip check`,
      `${venv} -c ${'"' + profile.verify.replace(/"/g, "'") + '"'}`,
    ].join('\n');
    const checkKey = `preparation:${course}:${options.os}:${options.editor}`;
    el.querySelector('.prep-instructions').innerHTML = `
      <h3>1. Python</h3><p>${esc(install)} <a href="https://www.python.org/downloads/" target="_blank" rel="noopener noreferrer">Stažení Pythonu</a>.</p>
      <h3>2. Balíčky a virtuální prostředí</h3>
      <p>${profile.packages.length ? `Tento podkurz instaluje: <strong>${esc(profile.packages.join(', '))}</strong>.` : 'Tento podkurz nepotřebuje další pip balíčky.'}
      Spusťte příkazy v terminálu ve složce <code>dilna-pythonu</code>. Pomocník vytvoří společnou <code>.venv</code> pro tento výukový projekt; další kurzy do ní mohou přidávat své balíčky. Pro vlastní projekty vytvářejte vlastní prostředí.</p>
      <pre class="code"><code>${esc(commands)}</code></pre>
      <p class="hint">Ověřeno v této verzi na Pythonu 3.14.8. První příkaz ověřuje instalaci, cesta z dalšího musí vést do .venv. pip check má skončit bez konfliktů. Aktivace není nutná: používáme přímo Python z .venv.</p>
      ${profile.optional_packages.length ? `<details><summary>Volitelné součásti pro pozdější projekty</summary><p>${esc(profile.optional_packages.join(', '))}. Instalujte až pro příslušný projekt:</p><pre class="code"><code>${esc(`${python} tools/setup_env.py --courses ${course} --extras`)}</code></pre><p>Kompatibilitu a systémové součásti ověřte při použití; nejsou potřeba pro základní spuštění.</p></details>` : ''}
      <h3>3. ${esc(EDITORS[options.editor])}</h3><p>${esc(editor)}</p>
      <p><a href="#/priprava/${options.editor}">Podrobný návod pro ${esc(EDITORS[options.editor])}</a></p>
      <h3>4. Ověření a spuštění</h3><p>${esc(profile.system)}</p>
      ${['pygame-1', 'pygame-2'].includes(course) ? `<p>Pro ověření okna spusťte např. <code>${esc(venv)} -m pygame.examples.aliens</code> (ukončení zavřením okna). Potom se vraťte ke vlastní lekci.</p>` : ''}
      <pre class="code"><code>${esc(`${venv} start.py`)}</code></pre>
      <p>Otevřete místní adresu vypsanou v terminálu. Server běží, dokud ho v terminálu nezastavíte pomocí Ctrl+C. Pokud je port 8765 obsazen, použijte <code>start.py --port 8766</code>.</p>
      <label class="prep-check"><input type="checkbox" data-prep-check ${getChecks()[checkKey] ? 'checked' : ''}> Ověřil/a jsem interpreter, balíčky a spuštění tohoto kurzu.</label>
      <p class="hint">Vlastní potvrzení uložené v tomto prohlížeči. Nejde o automatickou kontrolu vašeho počítače a nic nezamyká.</p>
      <p><a href="#/kurz/priprava">Úvodní podkurz: prostředí, projekt a Git</a> · <a href="#/priprava/reseni-problemu">Řešení problémů</a></p>`;
    el.querySelector('[data-prep-check]').addEventListener('change', (event) => setCheck(checkKey, event.target.checked));
  }
  el.querySelectorAll('[data-prep]').forEach((control) => control.addEventListener('change', () => {
    options[control.dataset.prep] = control.value;
    try { localStorage.setItem('dilna-preparation-options', JSON.stringify(options)); } catch { /* volba funguje i bez uložení */ }
    draw();
  }));
  draw();
}
