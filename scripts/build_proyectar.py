"""Regenera la versión para proyectar a partir del tablero y los CSV.

Uso:
    python scripts/build_proyectar.py

Toma el <head> autónomo (estilos, d3 y el shim local de `dash`) de la versión
actual, vuelve a incrustar los CSV de datos/ y le pega el cuerpo de
dashboard/index.html.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'dashboard' / 'Jornada_46hrs_2027_proyectar.html'
CORTE = '</head><body><div id="dash-root">\n'


def main():
    actual = SALIDA.read_text(encoding='utf-8')
    head = actual[:actual.index(CORTE)]
    raw = {
        'plantilla': (RAIZ / 'datos' / 'plantilla_jornadas.csv').read_text(encoding='utf-8'),
        'horarios': (RAIZ / 'datos' / 'horarios_por_rol.csv').read_text(encoding='utf-8'),
    }
    linea = '  const raw = { ' + ', '.join(f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in raw.items()) + ' };'
    head, n = re.subn(r'^  const raw = \{.*\};$', lambda _: linea, head, count=1, flags=re.M)
    assert n == 1, 'No encontré la línea de datos incrustados en el <head>'

    cuerpo = (RAIZ / 'dashboard' / 'index.html').read_text(encoding='utf-8')
    cuerpo = cuerpo.replace('<meta name="dash-one-writer">\n', '', 1)
    SALIDA.write_text(head + CORTE + '\n' + cuerpo + '\n</div></body></html>\n', encoding='utf-8')
    print(f'Listo: {SALIDA.relative_to(RAIZ)}')


if __name__ == '__main__':
    main()
