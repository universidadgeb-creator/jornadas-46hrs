"""Arma la página única «Jornada 46 hrs 2027»: tablero + seguimiento.

Uso:
    python scripts/build_unificado.py

Junta, en seguimiento/nuevas_jornadas.html (lo que se publica en el artifact
https://claude.ai/artifact/HcTgQg9nxbEGeX3q2qks6k):
  - las pestañas del tablero (dashboard/index.html), con un `dash` local y los CSV
    de datos/ incrustados, igual que la versión para proyectar;
  - la pestaña «Seguimiento» (seguimiento/captura.html + captura_estilos.css), que
    guarda lo que captura el equipo en la base de datos del artifact;
  - una tarjeta de avance en el Resumen;
  - el texto de la plantilla del adendum (seguimiento/adendum_plantilla.docx), jsPDF para armar el PDF
    de una página y JSZip para juntar varios en un .zip;
  - la pestaña «Mapa por sucursal» (seguimiento/mapa.html + mapa_estilos.css): cobertura por hora
    hoy / 2027 / cambio y el archivo maestro en Excel (SheetJS 0.18.5).
"""
import base64
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'seguimiento' / 'nuevas_jornadas.html'
D3 = 'https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js'
JSZIP = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'
JSPDF = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
XLSX_JS = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js'

# Colores y tipografía de la página. Los nombres --color-* / --cds-* son los que usa
# el tablero; los cortos (--bg, --fg, ...) los usa la pestaña de seguimiento.
BASE_CSS = """
/* Una sola columna con pestañas: Resumen, Personas, Jornadas por rol, 2027–2030 y Seguimiento */
:root {
  --color-fg: #17252b; --color-fg-muted: #5b6a70; --color-bg: #f4f7f7; --color-panel: #ffffff; --color-border-line: #dce4e5;
  --color-ok: #2f7d4f; --color-ok-soft: #dcefe3; --color-warn: #a15c00; --color-warn-soft: #fbecd6; --color-bad: #a15c00;
  --color-accent: #0f8b8d; --color-accent-soft: #d6ecec; --color-accent-mid: #7cc3c3;
  --cds-chart-muted: #c9d3d5; --cds-chart-axis: #b7c2c4; --cds-chart-grid: #e7ecec; --cds-chart-status-critical: #a15c00;
  --cds-surface-popover: #ffffff; --cds-border: #dce4e5; --cds-shadow-popover: 0 6px 20px rgba(20, 40, 45, .14); --cds-text-secondary: #5b6a70;
  --font-anthropic-sans: "Figtree", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-anthropic-serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --cds-font-size-caption: .8rem; --cds-font-size-body: .95rem; --cds-font-size-heading: 1.12rem; --cds-font-size-title: 1.9rem; --cds-font-weight-medium: 600;
  --cds-gap-xs: .25rem; --cds-gap-sm: .5rem; --cds-gap-md: 1rem; --cds-gap-lg: 1.5rem; --cds-gap-xl: 2rem;
  --cds-pad-xs: .25rem; --cds-pad-sm: .5rem; --cds-pad-md: .85rem; --cds-pad-lg: 1.25rem; --cds-radius: 8px;
  --cds-dur-slow: .25s; --cds-ease-out: cubic-bezier(.2, .7, .2, 1);
  --bg: var(--color-bg); --panel: var(--color-panel); --fg: var(--color-fg); --muted: var(--color-fg-muted); --line: var(--color-border-line);
  --accent: var(--color-accent); --accent-soft: var(--color-accent-soft); --accent-mid: var(--color-accent-mid);
  --ok: var(--color-ok); --ok-soft: var(--color-ok-soft); --warn: var(--color-warn); --warn-soft: var(--color-warn-soft);
  --sans: var(--font-anthropic-sans); --serif: var(--font-anthropic-serif); --r: var(--cds-radius);
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --color-fg: #e5eeef; --color-fg-muted: #9aabb0; --color-bg: #11191c; --color-panel: #172226; --color-border-line: #2a3a3f;
  --color-ok: #6fcf97; --color-ok-soft: #1c3427; --color-warn: #f0b264; --color-warn-soft: #3a2c17; --color-bad: #f0b264;
  --color-accent: #3cc7c4; --color-accent-soft: #1d3b3c; --color-accent-mid: #2b7d7c;
  --cds-chart-muted: #33464c; --cds-chart-axis: #4a5c62; --cds-chart-grid: #22323a; --cds-chart-status-critical: #f0b264;
  --cds-surface-popover: #1d2a2f; --cds-border: #2a3a3f; --cds-shadow-popover: 0 6px 20px rgba(0, 0, 0, .45); --cds-text-secondary: #9aabb0;
  color-scheme: dark; } }
:root[data-theme="dark"] {
  --color-fg: #e5eeef; --color-fg-muted: #9aabb0; --color-bg: #11191c; --color-panel: #172226; --color-border-line: #2a3a3f;
  --color-ok: #6fcf97; --color-ok-soft: #1c3427; --color-warn: #f0b264; --color-warn-soft: #3a2c17; --color-bad: #f0b264;
  --color-accent: #3cc7c4; --color-accent-soft: #1d3b3c; --color-accent-mid: #2b7d7c;
  --cds-chart-muted: #33464c; --cds-chart-axis: #4a5c62; --cds-chart-grid: #22323a; --cds-chart-status-critical: #f0b264;
  --cds-surface-popover: #1d2a2f; --cds-border: #2a3a3f; --cds-shadow-popover: 0 6px 20px rgba(0, 0, 0, .45); --cds-text-secondary: #9aabb0;
  color-scheme: dark; }
body { background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); }
#dash-root { max-width: 1320px; margin-inline: auto; padding-block: 28px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.gx b, .gx strong { font-weight: 600; }
"""

RESUMEN_AVANCE = """  <article class="gx-card" id="avance-contratos">
    <div class="seg-avance">
      <div>
        <h2>Avance del cambio de contrato</h2>
        <div class="big"><span data-seg="done">—</span> <small>de <span data-seg="total">—</span> personas que pasan de 46 hrs</small></div>
        <div class="seg-bar" aria-hidden="true"><i data-seg-bar></i></div>
        <div class="sub"><b data-seg="pct">—</b> con contrato nuevo · <b data-seg="hor">—</b> con nuevo horario · <b data-seg="lid">—</b> con líder asignado</div>
      </div>
      <button type="button" class="gx-btn-acc" data-tab-go="t-seg">Ir al seguimiento</button>
    </div>
  </article>
"""


def parrafos_adendum():
    """Texto de la plantilla del adendum, párrafo por párrafo, con negritas y alineación."""
    import html, zipfile
    xml = zipfile.ZipFile(RAIZ / 'seguimiento' / 'adendum_plantilla.docx').read('word/document.xml').decode('utf-8')
    out = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, re.S):
        jc = re.search(r'<w:jc w:val="(\w+)"', p)
        runs = []
        for r in re.findall(r'<w:r[ >].*?</w:r>', p, re.S):
            t = ''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', r, re.S))
            if '<w:tab/>' in r:
                t += ' '
            t = re.sub(r'\s+', ' ', html.unescape(t))
            if t:
                b = bool(re.search(r'<w:b/>|<w:b w:val="(true|1)"', r))
                if runs and runs[-1]['b'] == b:
                    runs[-1]['t'] += t
                else:
                    runs.append({'t': t, 'b': b})
        if runs and not ''.join(x['t'] for x in runs).strip():
            runs = []
        out.append({'align': jc.group(1) if jc else '', 'runs': runs})
    return out


def reemplazar(texto, viejo, nuevo):
    assert texto.count(viejo) == 1, f'No encontré exactamente una vez: {viejo[:70]}'
    return texto.replace(viejo, nuevo)


def main():
    # 1. El `dash` local, tomado de la versión para proyectar, con los CSV de hoy
    proy = (RAIZ / 'dashboard' / 'Jornada_46hrs_2027_proyectar.html').read_text(encoding='utf-8')
    shim = re.search(r'<script>\n\(function\(\)\{\n  const raw = .*?\n</script>', proy, re.S).group(0)
    raw = {
        'plantilla': (RAIZ / 'datos' / 'plantilla_jornadas.csv').read_text(encoding='utf-8'),
        'horarios': (RAIZ / 'datos' / 'horarios_por_rol.csv').read_text(encoding='utf-8'),
    }
    linea = '  const raw = { ' + ', '.join(f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in raw.items()) + ' };'
    shim = re.sub(r'^  const raw = \{.*\};$', lambda _: linea, shim, count=1, flags=re.M)

    # 2. El tablero, con la pestaña nueva y la tarjeta de avance
    tab = (RAIZ / 'dashboard' / 'index.html').read_text(encoding='utf-8')
    tab = tab.replace('<meta name="dash-one-writer">\n', '', 1)
    tab = reemplazar(tab, '<button type="button" role="tab" data-tab="t-etapas" aria-selected="false">2027–2030</button>\n',
                     '<button type="button" role="tab" data-tab="t-etapas" aria-selected="false">2027–2030</button>\n'
                     '    <button type="button" role="tab" data-tab="t-seg" aria-selected="false">Seguimiento</button>\n'
                     '    <button type="button" role="tab" data-tab="t-mapa" aria-selected="false">Mapa por sucursal</button>\n')
    tab = reemplazar(tab, '<a class="gx-link" href="https://claude.ai/artifact/HcTgQg9nxbEGeX3q2qks6k" target="_blank" rel="noopener">Ver avance de contratos →</a>',
                     '<button type="button" class="gx-link" data-tab-go="t-seg">Ver avance de contratos →</button>')
    tab = reemplazar(tab, '  <section class="gx-tab" id="t-resumen">\n',
                     '  <section class="gx-tab" id="t-resumen">\n' + RESUMEN_AVANCE)
    captura = (RAIZ / 'seguimiento' / 'captura.html').read_text(encoding='utf-8')
    seccion, script_seg = captura.split('\n\n<script>', 1)
    mapa = (RAIZ / 'seguimiento' / 'mapa.html').read_text(encoding='utf-8')
    seccion_mapa, script_mapa = mapa.split('\n\n<script>', 1)
    tab = reemplazar(tab, '  <details class="gx-card gx-details" id="criterios">',
                     '  ' + seccion.strip() + '\n\n  ' + seccion_mapa.strip() + '\n\n  <details class="gx-card gx-details" id="criterios">')
    tab = tab.rstrip() + "\n<script>\ndocument.querySelectorAll('[data-tab-go]').forEach((b) => b.addEventListener('click', () => { abrirTab(b.dataset.tabGo); window.scrollTo({ top: 0 }); }));\n</script>\n"

    estilos_seg = (RAIZ / 'seguimiento' / 'captura_estilos.css').read_text(encoding='utf-8') + '\n' + (RAIZ / 'seguimiento' / 'mapa_estilos.css').read_text(encoding='utf-8')
    pagina = '\n'.join([
        '<title>Jornada 46 hrs 2027</title>',
        '<meta name="claude:viewport-fit-sides" content="cover">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">',
        '<style>' + BASE_CSS + '\n' + estilos_seg + '</style>',
        f'<script src="{D3}"></script>',
        f'<script src="{JSZIP}"></script>',
        f'<script src="{JSPDF}"></script>',
        f'<script src="{XLSX_JS}"></script>',
        '<script>window.ADENDUM_PARRAFOS = ' + json.dumps(parrafos_adendum(), ensure_ascii=False) + ';</script>',
        shim,
        '<div id="dash-root">',
        tab,
        '<script>' + script_seg,
        '<script>' + script_mapa,
        '</div>',
        '',
    ])
    SALIDA.write_text(pagina, encoding='utf-8')
    print(f'Listo: {SALIDA.relative_to(RAIZ)} ({len(pagina.encode()) // 1024} KB)')


if __name__ == '__main__':
    main()
