"""Deja en el Excel solo lo que el proyecto necesita, sin datos confidenciales.

Uso:
    python scripts/limpiar_excel.py <excel_completo.xlsx> datos/Revision_Jornadas_48hrs_GEB.xlsx

Conserva únicamente la hoja «Base de Datos» (encabezados en la fila 3, como el
original) y quita CURP, RFC, NSS, fecha de nacimiento, género, número de empleado,
salarios, bonos, vales, gratificaciones y las observaciones de pago. El resto de
hojas («Base Original», resúmenes) no se copian.
"""
import sys

import pandas as pd

QUITAR = ['No de Empleado', 'Antigüedad', 'Salario Diario', 'Sueldo por Periodo', 'Sueldo Mensual',
          'Bono Semanl', 'Bono Mensual', 'Bono Trimestral', 'Vales de Despensa', 'Gratificación mensual',
          'Observaciones', 'CURP', 'RFC', 'NSS', 'Genero', 'Fecha de Nacimiento']


def main(entrada, salida):
    df = pd.read_excel(entrada, sheet_name='Base de Datos', header=2)
    df = df.loc[:, ~df.columns.astype(str).str.startswith('Unnamed')]
    quitadas = [c for c in QUITAR if c in df.columns]
    df = df.drop(columns=quitadas)
    with pd.ExcelWriter(salida, engine='openpyxl') as xw:
        df.to_excel(xw, sheet_name='Base de Datos', index=False, startrow=2)
    print(f'{len(df)} filas · {len(df.columns)} columnas · se quitaron {len(quitadas)}: {", ".join(quitadas)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
