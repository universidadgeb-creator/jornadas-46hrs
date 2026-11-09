"""Deja en el Excel solo lo que el proyecto necesita, sin datos confidenciales.

Uso:
    python scripts/limpiar_excel.py <excel_completo.xlsx> datos/Revision_Jornadas_48hrs_GEB.xlsx [hoja]

Desde el 9 nov 2026 la hoja buena es «Base Original» (acuerdo con Patty); antes
era «Base de Datos». Toma esa hoja (encabezados en la fila 3) y la guarda en el
archivo limpio con el nombre «Base de Datos», que es el que lee build_csv.py.
Conserva únicamente esa hoja y quita CURP, RFC, NSS, fecha de nacimiento, género, número de empleado,
salarios, bonos, vales, gratificaciones y las observaciones de pago. El resto de
hojas («Base Original», resúmenes) no se copian.
"""
import sys

import pandas as pd

QUITAR = ['No de Empleado', 'Antigüedad', 'Salario Diario', 'Sueldo por Periodo', 'Sueldo Mensual',
          'Bono Semanl', 'Bono Mensual', 'Bono Trimestral', 'Vales de Despensa', 'Gratificación mensual',
          'Observaciones', 'CURP', 'RFC', 'NSS', 'Genero', 'Fecha de Nacimiento']


HOJA = 'Base Original'


def main(entrada, salida, hoja=HOJA):
    df = pd.read_excel(entrada, sheet_name=hoja, header=2)
    df = df.loc[:, ~df.columns.astype(str).str.startswith('Unnamed')]
    quitadas = [c for c in QUITAR if c in df.columns]
    df = df.drop(columns=quitadas)
    with pd.ExcelWriter(salida, engine='openpyxl') as xw:
        df.to_excel(xw, sheet_name='Base de Datos', index=False, startrow=2)
    print(f'Hoja «{hoja}» · {len(df)} filas · {len(df.columns)} columnas · se quitaron {len(quitadas)}: {", ".join(quitadas)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
