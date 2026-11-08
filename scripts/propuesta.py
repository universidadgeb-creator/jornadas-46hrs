"""Calcula la propuesta de jornada 2027 (misma regla que el tablero).

Uso:
    python scripts/propuesta.py datos/horarios_por_rol.csv salida.json

Regla (junta del 5 nov 2026): diurna a 46 hrs, mixta a 45; nocturna por confirmar.
Entran quienes pasan de 46 hrs. El recorte se toma en bloques de 5 min del día más
largo en ese momento (empates: el primero de la semana); se conserva la entrada y se
adelanta la salida. Si un día pasa de 12 h se marca «revisar».
"""
import json
import sys

import pandas as pd

DIAS = ['lun', 'mar', 'mie', 'jue', 'vie', 'sab', 'dom']
LETRA = {'lun': 'L', 'mar': 'M', 'mie': 'Mi', 'jue': 'J', 'vie': 'V', 'sab': 'S', 'dom': 'D'}
META = {'Diurna': 46, 'Mixta': 45}
UMBRAL = 46


def a_min(t):
    h, m = t.split(':')
    return int(h) * 60 + int(m)


def a_hora(m):
    m %= 1440
    return f'{m // 60:02d}:{m % 60:02d}'


def texto_semana(por_dia):
    """{'lun': '07:00–14:40', ..., 'dom': None} -> 'L–S 07:00–14:40 · D descanso'."""
    grupos = []
    for d in DIAS:
        v = por_dia.get(d) or 'descanso'
        if grupos and grupos[-1][1] == v:
            grupos[-1][0].append(d)
        else:
            grupos.append([[d], v])
    partes = []
    for ds, v in grupos:
        dias = LETRA[ds[0]] if len(ds) == 1 else f'{LETRA[ds[0]]}–{LETRA[ds[-1]]}'
        partes.append(f'{dias} {v}')
    return ' · '.join(partes)


def propuesta(r):
    tot = float(r['horas_reales'])
    dias = [d for d in DIAS if isinstance(r[d], str) and r[d] and float(r[d + '_h']) > 0]
    if any(float(r[d + '_h']) > 12 for d in dias):
        return {'estado': 'revisar'}
    meta = META.get(r['tipo_jornada'])
    if meta is None:
        return {'estado': 'pendiente'}
    total = round((tot - meta) * 60)
    if total <= 0 or not dias:
        return {'estado': 'sin'}
    cortes = {d: 0 for d in dias}
    resto = total
    while resto > 0:
        x = min(5, resto)
        d = dias[0]
        for b in dias:
            if float(r[b + '_h']) * 60 - cortes[b] > float(r[d + '_h']) * 60 - cortes[d]:
                d = b
        cortes[d] += x
        resto -= x
    nuevo = {}
    for d in dias:
        ent, sal = r[d].split('–')
        nuevo[d] = f'{ent}–{a_hora(a_min(sal) - cortes[d])}'
    return {'estado': 'ok', 'meta': meta, 'corte_min': total, 'nuevas_horas': round(tot - total / 60, 2),
            'por_dia': nuevo, 'texto': texto_semana(nuevo)}


def main(csv, salida):
    h = pd.read_csv(csv)
    h = h[(h.tipo_jornada != 'Sin captura') & (h.horas_reales > UMBRAL)]
    out = []
    for _, r in h.iterrows():
        p = propuesta(r)
        out.append({'nombre': r['nombre'], 'tipo': r['tipo_jornada'], 'horas_actuales': float(r['horas_reales']), **p})
    with open(salida, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    ok = [p for p in out if p['estado'] == 'ok']
    print(f'{len(out)} personas · {len(ok)} con propuesta · {sum(p["corte_min"] for p in ok) / 60:g} hrs a reacomodar')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
