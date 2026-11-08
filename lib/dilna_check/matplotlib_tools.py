"""Volitelné kontroly skutečných Figure/Axes, bez porovnávání obrázků pixel po pixelu."""
from copy import deepcopy
import os
from pathlib import Path

os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', str(Path('.matplotlib').resolve()))
import numpy as np
from matplotlib.figure import Figure
from .pandas_tools import equivalent


def near(actual, expected):
    a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    return a.shape == b.shape and np.allclose(a, b, rtol=1e-10, atol=1e-10, equal_nan=True)


def figure_matches(fig, spec):
    """Kontroluje význam grafu, barvu a písmo nechává studentovi."""
    if not isinstance(fig, Figure) or len(fig.axes) != len(spec['axes']):
        return False
    if 'size' in spec and not near(fig.get_size_inches(), spec['size']):
        return False
    if 'title' in spec and (fig._suptitle is None or fig._suptitle.get_text() != spec['title']):
        return False
    for ax, expected in zip(fig.axes, spec['axes']):
        for key, getter in [('title', ax.get_title), ('xlabel', ax.get_xlabel), ('ylabel', ax.get_ylabel)]:
            if key in expected and getter() != expected[key]:
                return False
        lines, bars, points = expected.get('lines', []), expected.get('bars'), expected.get('points', [])
        if len(ax.lines) != len(lines) or len(ax.collections) != len(points):
            return False
        for line, values in zip(ax.lines, lines):
            if not near(line.get_xdata(), values['x']) or not near(line.get_ydata(), values['y']):
                return False
            if 'marker' in values and line.get_marker() != values['marker']:
                return False
        if bars is None:
            if len(ax.patches):
                return False
        else:
            if len(ax.patches) != len(bars):
                return False
            for patch, value in zip(ax.patches, bars):
                if 'edges' in expected:
                    i = list(ax.patches).index(patch)
                    lo, hi = expected['edges'][i:i+2]
                    if not near([patch.get_x(), patch.get_width(), patch.get_y(), patch.get_height()], [lo, hi-lo, 0, value]):
                        return False
                elif expected.get('horizontal'):
                    i = list(ax.patches).index(patch)
                    if not near([patch.get_x(), patch.get_width(), patch.get_y()+patch.get_height()/2], [0, value, i]):
                        return False
                else:
                    i = list(ax.patches).index(patch)
                    if not near([patch.get_x()+patch.get_width()/2, patch.get_y(), patch.get_height()], [i, 0, value]):
                        return False
        for collection, values in zip(ax.collections, points):
            offsets = collection.get_offsets()
            wanted = np.column_stack((values['x'], values['y']))
            if np.ma.getmaskarray(offsets).any() or not near(offsets, wanted):
                return False
            if 'sizes' in values and not near(collection.get_sizes(), values['sizes']):
                return False
        if expected.get('ticks'):
            ticks = ax.get_yticklabels() if expected.get('horizontal') else ax.get_xticklabels()
            if [t.get_text() for t in ticks] != expected['ticks']:
                return False
        if 'legend' in expected:
            legend = ax.get_legend()
            if legend is None or [t.get_text() for t in legend.get_texts()] != expected['legend']:
                return False
        for key, getter in [('xlim', ax.get_xlim), ('ylim', ax.get_ylim)]:
            if key in expected and not near(getter(), expected[key]):
                return False
        if expected.get('zero') == 'y' and not near(ax.get_ylim()[0], 0):
            return False
        if expected.get('zero') == 'x' and not near(ax.get_xlim()[0], 0):
            return False
        if expected.get('inverted_y') and not ax.yaxis_inverted():
            return False
        if expected.get('equal') and ax.get_aspect() != 1:
            return False
    if spec.get('row'):
        a, b = [ax.get_position() for ax in fig.axes]
        if not near([a.y0, a.height], [b.y0, b.height]) or a.x1 >= b.x0:
            return False
    if spec.get('shared_y') and not all(near(fig.axes[0].get_ylim(), ax.get_ylim()) for ax in fig.axes):
        return False
    return True


def check_figures(checker, namespace, function, cases):
    for number, (args, spec) in enumerate(cases, 1):
        values, before = deepcopy(args), deepcopy(args)
        ok, result = checker.call(namespace, function, values)
        try:
            matches = ok and figure_matches(result, spec)
        except (AttributeError, TypeError, ValueError, IndexError):
            matches = False
        checker.add(f'Graf odpovídá zadání ({number})', matches,
                    'Vraťte Figure se správnými osami, daty, popisky a typem grafu. Barvu ani písmo nevyžadujeme.'
                    if ok else f'Volání skončilo chybou {type(result).__name__}: {result}')
        checker.add(f'Zdrojová data zachována ({number})', equivalent(values, before, exact=True),
                    'Vstupní seznamy a tabulky neměňte; pracujte s kopií.')


def check_exports(checker, namespace, function, mode):
    """Ověří skutečný PNG, rozměry, průhlednost a zachování předaného obrázku."""
    import tempfile
    from PIL import Image
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib import pyplot as plt
    for number in range(2):
        with tempfile.TemporaryDirectory(prefix='export-') as temp:
            root = Path(temp)
            fig = Figure(figsize=(2, 1.5), dpi=80, facecolor='#112233')
            ax = fig.subplots(); ax.set_facecolor('#ddeeff')
            line, = ax.plot([0, 1], [0, 1], color='red', linewidth=4)
            ax.set(title='Pokus', xlabel='Čas', ylabel='Délka')
            original_size = fig.get_size_inches().copy()
            colors = (fig.get_facecolor(), ax.get_facecolor())
            # Cizí aktuální pyplot Figure odhalí záměnu fig.savefig a plt.savefig.
            other = plt.figure(figsize=(1, 1), facecolor='yellow')
            path = root / ('měření 1.png' if number == 0 else 'bez_pripony')
            folder = root / 'výstupy' / 'den'
            sentinel = folder / 'poznamka.txt'
            if mode == 'variants' and number:
                folder.mkdir(parents=True)
                sentinel.write_text('zachovat', encoding='utf-8')
                (folder/'nahled.png').write_text('stará verze')
            if mode == 'tight' and number:
                fig.text(1.3, 0.5, 'Vnější text', color='red')
            args = ((fig, 6, 3) if mode == 'size' else (fig, folder) if mode == 'variants'
                    else (fig, str(path) if number == 0 else path, 100+20*number) if mode == 'png'
                    else (fig, path))
            ok, result = checker.call(namespace, function, args)
            preserved = (fig.axes == [ax] and list(ax.lines) == [line]
                         and near(line.get_xdata(), [0, 1]) and near(line.get_ydata(), [0, 1])
                         and (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == ('Pokus', 'Čas', 'Délka')
                         and near(fig.dpi, 80) and (fig.get_facecolor(), ax.get_facecolor()) == colors)
            preserved = preserved and near(fig.get_size_inches(), [6, 3] if mode == 'size' else original_size)
            checker.add(f'Předaný Figure zachován ({number+1})', ok and preserved,
                        'Zachovejte původní osy, čáru, popisky, barvy a DPI; rozměr mění jen připrav_tisk.')
            try:
                if mode == 'size':
                    valid = ok and result is fig
                    files = []
                elif mode == 'variants':
                    files = [(folder/'nahled.png', 100), (folder/'tisk.png', 200)]
                    valid = ok and isinstance(result, tuple) and result == tuple(p for p, _ in files) and all(isinstance(p, Path) for p in result)
                    valid = valid and (not number or sentinel.read_text('utf-8') == 'zachovat')
                else:
                    files = [(path, 100+20*number if mode == 'png' else 100)]
                    valid = ok and isinstance(result, Path) and result == path
                for output, dpi in files:
                    with Image.open(output) as image:
                        image.load()
                        valid = valid and image.format == 'PNG'
                        rgba = np.asarray(image.convert('RGBA'))
                        red = (rgba[:,:,0] > 180) & (rgba[:,:,1] < 100) & (rgba[:,:,2] < 100) & (rgba[:,:,3] > 150)
                        valid = valid and bool(red.any())
                        valid = valid and all(abs(d-dpi) < 0.1 for d in image.info.get('dpi', [0,0]))
                        if mode == 'tight':
                            fig.set_dpi(100)
                            canvas = FigureCanvasAgg(fig);canvas.draw()
                            bounds = fig.get_tightbbox(canvas.get_renderer())
                            expected = (int((bounds.width+0.2)*100), int((bounds.height+0.2)*100))
                            fig.set_dpi(80)
                            valid = valid and image.size == expected
                        else:
                            valid = valid and image.size == (int(original_size[0]*dpi), int(original_size[1]*dpi))
                        if mode == 'transparent':
                            valid = valid and rgba[0,0,3] == 0 and rgba[:,:,3].max() > 0
                        else:
                            if mode != 'tight':
                                valid = valid and tuple(rgba[0,0,:3]) == (17,34,51)
                checker.add(f'Skutečný výstup a návratová hodnota ({number+1})', valid,
                            'Ověřte cestu/Path, skutečný formát PNG, DPI, rozměr a požadované nastavení pozadí či rámečku.')
            except (OSError, TypeError, ValueError, AttributeError):
                checker.add(f'Skutečný výstup a návratová hodnota ({number+1})', False,
                            'Uložte platné PNG do zadané cesty a vraťte požadovaný objekt.')
            finally:
                plt.close(other)
