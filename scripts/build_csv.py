"""Genera los dos CSV del dashboard a partir de la revisión de jornadas.

Uso:
    python scripts/build_csv.py datos/Revision_Jornadas_48hrs_GEB.xlsx datos/

Lee la hoja «Base de Datos» (encabezados en la fila 3) y escribe:
  - plantilla_jornadas.csv  -> una fila por colaborador activo (TabBD = «Sí»)
  - horarios_por_rol.csv    -> lo mismo + entrada/salida y horas por día (lun..dom)
"""
import re
import sys
import datetime
import pandas as pd

DIAS = [('Lunes', 'lun'), ('Martes', 'mar'), ('Miércoles', 'mie'), ('Jueves', 'jue'),
        ('Viernes', 'vie'), ('Sábado', 'sab'), ('Domingo', 'dom')]


def hhmm(v):
    if pd.isna(v) or v == '':
        return ''
    if isinstance(v, (datetime.time, datetime.datetime)):
        return v.strftime('%H:%M')
    if isinstance(v, (int, float)):  # fracción de día de Excel
        m = round(v * 24 * 60)
        return f'{m // 60:02d}:{m % 60:02d}'
    t = str(v).strip()
    if re.fullmatch(r'\d{1,2}:\d{2}(:\d{2})?', t):  # «9:00», «09:00:00» -> «09:00»
        h, m = t.split(':')[:2]
        return f'{int(h):02d}:{m}'
    return t


def main(xlsx, out):
    df = pd.read_excel(xlsx, sheet_name='Base de Datos', header=2)
    a = df[df['Activo en TabBD'] == 'Sí'].copy()

    p = pd.DataFrame()
    p['nombre'] = a['Nombre'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
    # Normalizaciones acordadas: puesto vacío -> «Sin puesto»; «R.P» -> «R.P.»
    p['puesto'] = a['Puesto'].fillna('Sin puesto').astype(str).str.strip().replace({'R.P': 'R.P.'})
    p['division'] = a['División'].astype(str).str.strip().replace({'Vivo 47': 'VIVO 47', 'Ofna de Soporte': 'Oficina de Soporte'})
    p['ubicacion'] = a['Ubicación'].astype(str).str.strip().replace({'La estancia': 'La Estancia', 'Estancia': 'La Estancia', 'estancia': 'La Estancia'})
    p['tipo_jornada'] = a['TIPO DE JORNADA (LFT)'].replace({'Sin horario capturado': 'Sin captura'})
    p['horas_reales'] = pd.to_numeric(a['Total jornada reconocida'], errors='coerce').fillna(0).round(2)
    p['horas_contrato'] = pd.to_numeric(a['Jornada laboral'], errors='coerce')
    p['dias'] = a[[d + ' jornada reconocida' for d, _ in DIAS]].apply(pd.to_numeric, errors='coerce').fillna(0).gt(0).sum(axis=1)
    p['captura'] = (p.tipo_jornada != 'Sin captura').map({True: 'Capturado', False: 'Pendiente'})
    p.to_csv(f'{out}/plantilla_jornadas.csv', index=False)

    h = p[['nombre', 'puesto', 'ubicacion', 'tipo_jornada', 'horas_reales']].copy()
    for d, k in DIAS:
        e = a[d + ' entrada'].map(hhmm)
        s = a[d + ' salida'].map(hhmm)
        hrs = pd.to_numeric(a[d + ' jornada reconocida'], errors='coerce').fillna(0).round(2)
        h[k] = [f'{x}–{y}' if x and y and q > 0 else '' for x, y, q in zip(e, s, hrs)]
        h[k + '_h'] = hrs.values
    h.to_csv(f'{out}/horarios_por_rol.csv', index=False)

    c = p[p.captura == 'Capturado']
    print(f'Activos {len(p)} · capturados {len(c)} · 48 hrs {(c.horas_reales >= 48).sum()} · '
          f'46–48 {((c.horas_reales > 46) & (c.horas_reales < 48)).sum()}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '.')
