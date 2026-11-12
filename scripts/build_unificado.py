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

RESUMEN_AVANCE = """  <div class="rs-cad" role="group" aria-label="Cadena" id="rs-cad"></div>
  <section class="rs-kpis" aria-label="Cifras clave">
    <div class="rs-k"><span class="lbl">Personas que deben ajustar su jornada</span><b data-rs="n">—</b><span class="sub" data-rs="n-sub">—</span></div>
    <div class="rs-k"><span class="lbl">Horas por semana que se reacomodan</span><b data-rs="h">—</b><span class="sub">con la propuesta: diurna a 46, mixta a 45</span></div>
    <div class="rs-k is-a"><span class="lbl">Equivale a (personas de tiempo completo)</span><b data-rs="eq">—</b><span class="sub" data-rs="eq-sub">—</span></div>
    <div class="rs-k"><span class="lbl">Contratos nuevos firmados</span><b data-rs="firm">—</b><span class="rs-bar" aria-hidden="true"><i data-rs-bar></i></span><span class="sub" data-rs="firm-sub">—</span></div>
  </section>
  <article class="gx-card" id="rs-regla">
    <div class="rs-head"><h2>La regla: cuánto baja cada tipo de jornada</h2><button type="button" class="gx-link" data-tab-go="t-seg">Ver avance de contratos →</button></div>
    <div class="rs-tipos">
      <div><span class="lbl">Diurna</span><b data-rs="d-n">—</b><span class="rule">personas · bajan a <strong>46 hrs</strong></span></div>
      <div><span class="lbl">Mixta</span><b data-rs="m-n">—</b><span class="rule">personas · bajan a <strong>45 hrs</strong>, su máximo legal (no cambia)</span></div>
      <div><span class="lbl">Nocturna</span><b data-rs="n-n">—</b><span class="rule pend">personas · ajuste por confirmar con el abogado</span></div>
    </div>
    <p class="rs-nota">Lo que pide la ley (todas a 46) equivale a <b data-rs="ley">—</b> personas (<span data-rs="ley-h">—</span> hrs). Bajar las mixtas a 45 suma <b data-rs="mix">—</b> (<span data-rs="mix-h">—</span> hrs). Con los horarios capturados hoy en el Seguimiento: <b data-rs="cap">—</b> personas.</p>
  </article>
  <article class="gx-card" id="rs-donde">
    <h2>¿Dónde está el impacto y cómo va cada club?</h2>
    <p class="note">Horas por semana que se dejan de trabajar con la propuesta y su equivalente en personas de 46 hrs (referencia de capacidad, no propuesta de contratación). Clic en un club para ver su captura.</p>
    <div class="cap-scroll">
      <table class="gx-table cap-tabla rs-tabla">
        <thead><tr><th>Cadena / club</th><th class="num">Personas</th><th class="num">Horas menos</th><th class="num">Equivale a</th><th>Horario validado</th><th>Contrato firmado</th></tr></thead>
        <tbody data-rs-tabla></tbody>
      </table>
    </div>
  </article>
"""


# Planeación de jornadas por club (misma plantilla seguimiento/plan.html). Metas de 2027 (46 diurna, 45 mixta):
# Las dos planeaciones son de 2027 (Patty corrigió Valle Real de 2028 a 2027 el 11 nov 2026).
PLANES = [
    {'prefijo': 'pl', 'tab': 't-plan', 'club': 'Gourmeteria', 'pestana': 'Planeación Gourmetería 2027',
     'titulo': 'Planeación Gourmetería 2027', 'coleccion': 'plan_gourmeteria', 'archivo': 'Planeacion Gourmeteria 2027',
     'apertura': {'sab': ['07:00', '17:00'], 'dom': ['08:30', '15:00']}, 'sab': '7:00–17:00', 'dom': '8:30–15:00',
     'sab_antes': '7:00–16:00', 'dom_antes': '9:00–15:00'},
    {'prefijo': 'plv', 'tab': 't-planvr', 'club': 'Valle Real', 'pestana': 'Planeación Valle Real 2027',
     'titulo': 'Planeación Valle Real 2027', 'coleccion': 'plan_valle_real', 'archivo': 'Planeacion Valle Real 2027',
     'apertura': {'sab': ['07:00', '17:00'], 'dom': ['08:30', '15:00']}, 'sab': '7:00–17:00', 'dom': '8:30–15:00',
     'sab_antes': '', 'dom_antes': '9:00–15:00'},
]


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
    # Pestañas (9 nov 2026, con Patty): se quitan «Personas» y «Jornadas por rol», que repetían
    # lo que ya muestran Seguimiento y Mapa por sucursal; «2027–2030» pasa a «Próximas etapas».
    ini = tab.index('    <button type="button" role="tab" data-tab="t-resumen"')
    fin = tab.index('  </nav>')
    tab = tab[:ini] + (
        '    <button type="button" role="tab" data-tab="t-resumen" aria-selected="true">Resumen</button>\n'
        '    <button type="button" role="tab" data-tab="t-seg" aria-selected="false">Seguimiento</button>\n'
        '    <button type="button" role="tab" data-tab="t-mapa" aria-selected="false">Mapa por sucursal</button>\n'
        + ''.join(f'    <button type="button" role="tab" data-tab="{c["tab"]}" aria-selected="false">{c["pestana"]}</button>\n' for c in PLANES) +
        '    <button type="button" role="tab" data-tab="t-etapas" aria-selected="false">Próximas etapas</button>\n') + tab[fin:]
    ini = tab.index('  <section class="gx-tab" id="t-personas" hidden>')
    fin = tab.index('  <section class="gx-tab" id="t-etapas" hidden>')
    tab = tab[:ini] + tab[fin:]
    # (12 nov 2026) La gráfica por sucursal ya no va al Resumen: la tabla «¿Dónde está el impacto?» la sustituye
    # Clic en un puesto: abre su plantilla en el Mapa por sucursal
    tab = reemplazar(tab, "  if (GX.puesto) abrirTab('t-personas');",
                     "  if (GX.puesto) { const pu = GX.puesto; GX.puesto = null; dash.draw('puestos'); window.dispatchEvent(new CustomEvent('mapa:puesto', { detail: pu })); abrirTab('t-mapa'); window.scrollTo({ top: 0 }); }")
    tab = reemplazar(tab, 'Clic en una barra para ver los nombres.</p>', 'Clic en una barra para ver su plantilla por turno en el Mapa por sucursal.</p>')
    tab = reemplazar(tab, '<a class="gx-link" href="https://claude.ai/artifact/HcTgQg9nxbEGeX3q2qks6k" target="_blank" rel="noopener">Ver avance de contratos →</a>',
                     '<button type="button" class="gx-link" data-tab-go="t-seg">Ver avance de contratos →</button>')
    # Encabezado sin cifras: las cifras viven en el Resumen (antes decía 99 y el Seguimiento 101)
    i = tab.index('    <p><b data-draw="kpi" data-source="kpis" data-field="sobre46"')
    tab = tab[:i] + '    <p>La reforma a la LFT baja la jornada máxima de 48 a <b>46 hrs en 2027</b> (44 en 2028, 42 en 2029 y 40 en 2030) sin reducir salario ni prestaciones. Aquí está a quién le toca, cuánto cuesta en horas y cómo va el cambio de contrato.</p>' + tab[tab.index('</p>', i) + len('</p>'):]
    # Resumen (12 nov 2026, para presentar): sin los 4 indicadores ni la tarjeta por tipo del tablero,
    # sin la gráfica por sucursal y sin la lista de puestos por año (se ven en Próximas etapas).
    i = tab.index('  <section class="gx-kpis" aria-label="Indicadores clave">')
    tab = tab[:i] + tab[tab.index('</section>', i) + len('</section>\n'):]
    i = tab.index('  <article class="gx-card" id="por-tipo">')
    tab = tab[:i] + tab[tab.index('</article>', i) + len('</article>\n'):]
    tab = re.sub(r'\s*<div class="gx-tl-roles"[^>]*></div>', '', tab)
    tab = reemplazar(tab, 'Debajo de cada año están los puestos que entran en esa etapa; abre un puesto para ver los nombres.',
                     'El detalle de puestos y nombres está en Próximas etapas.')
    tab = reemplazar(tab, """dash.draw('puestos', (el) => {
  const p = dash.data('por_puesto');""", """// Con una cadena elegida (Resumen o Próximas etapas), la gráfica de puestos cuenta solo esa cadena
function porPuestoCad() {
  const p = dash.data('por_puesto'); const cad = window.GXE && GXE.cad; if (!cad || p.status !== 'ok') return p;
  const pl = dash.data('plantilla'); if (pl.status !== 'ok') return p;
  const m = {};
  pl.data.filter((r) => r.captura === 'Capturado' && r.division === cad).forEach((r) => {
    m[r.puesto] = m[r.puesto] || { puesto: r.puesto, afectados: 0, entre: 0, total: 0 };
    m[r.puesto].total += 1;
    if (Number(r.horas_reales) >= 48) m[r.puesto].afectados += 1; else if (Number(r.horas_reales) > 46) m[r.puesto].entre += 1;
  });
  return { status: 'ok', data: Object.values(m).filter((d) => d.afectados + d.entre > 0).sort((a, b) => (b.afectados + b.entre) - (a.afectados + a.entre) || b.afectados - a.afectados) };
}
dash.draw('puestos', (el) => {
  const p = porPuestoCad();""")
    tab = reemplazar(tab, "  sel.onchange = () => { GXE.cad = sel.value; GXE.suc = ''; redrawEtapa(); };",
                     "  sel.onchange = () => { GXE.cad = sel.value; GXE.suc = ''; redrawEtapa(); dash.draw('puestos'); window.dispatchEvent(new Event('cadena:cambio')); };")
    tab = reemplazar(tab, '  <section class="gx-tab" id="t-resumen">\n',
                     '  <section class="gx-tab" id="t-resumen">\n' + RESUMEN_AVANCE)
    captura = (RAIZ / 'seguimiento' / 'captura.html').read_text(encoding='utf-8')
    seccion, script_seg = captura.split('\n\n<script>', 1)
    mapa = (RAIZ / 'seguimiento' / 'mapa.html').read_text(encoding='utf-8')
    seccion_mapa, script_mapa = mapa.split('\n\n<script>', 1)
    plan = (RAIZ / 'seguimiento' / 'plan.html').read_text(encoding='utf-8')
    secciones_plan, scripts_plan = [], []
    for c in PLANES:
        antes = lambda t: f'<span class="h">antes {t}</span>' if t else ''
        cfg = {'club': c['club'], 'titulo': c['titulo'], 'coleccion': c['coleccion'], 'archivo': c['archivo'],
               'apertura': c['apertura'], 'texto': {'sab': c['sab'], 'dom': c['dom']}}
        t = (plan.replace('{{P}}', c['prefijo']).replace('{{TAB}}', c['tab']).replace('{{TITULO}}', c['titulo'])
             .replace('{{SAB}}', c['sab']).replace('{{DOM}}', c['dom'])
             .replace('{{SAB_ANTES}}', antes(c.get('sab_antes'))).replace('{{DOM_ANTES}}', antes(c.get('dom_antes')))
             .replace('{{CONFIG}}', json.dumps(cfg, ensure_ascii=False)))
        assert '{{' not in t, 'Quedó una marca sin llenar en la planeación'
        sec, scr = t.split('\n\n<script>', 1)
        secciones_plan.append(sec.strip()); scripts_plan.append('<script>' + scr)
    tab = reemplazar(tab, '  <details class="gx-card gx-details" id="criterios">',
                     '  ' + seccion.strip() + '\n\n  ' + seccion_mapa.strip() + '\n\n  ' + '\n\n  '.join(secciones_plan) + '\n\n  <details class="gx-card gx-details" id="criterios">')
    tab = tab.rstrip() + "\n<script>\ndocument.querySelectorAll('[data-tab-go]').forEach((b) => b.addEventListener('click', () => { abrirTab(b.dataset.tabGo); window.scrollTo({ top: 0 }); }));\n</script>\n"

    estilos_seg = (RAIZ / 'seguimiento' / 'captura_estilos.css').read_text(encoding='utf-8') + '\n' + (RAIZ / 'seguimiento' / 'mapa_estilos.css').read_text(encoding='utf-8') + '\n' + (RAIZ / 'seguimiento' / 'plan_estilos.css').read_text(encoding='utf-8')
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
        *scripts_plan,
        '</div>',
        '',
    ])
    SALIDA.write_text(pagina, encoding='utf-8')
    print(f'Listo: {SALIDA.relative_to(RAIZ)} ({len(pagina.encode()) // 1024} KB)')


if __name__ == '__main__':
    main()
