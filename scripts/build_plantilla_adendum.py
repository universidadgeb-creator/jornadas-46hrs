"""Prepara la plantilla del adendum con marcas para llenarla desde la página.

Uso:
    python scripts/build_plantilla_adendum.py

Convierte seguimiento/ADENDUM_Contrato_trabajo_NUEVA_JORNADA.doc (el original
de Patty) a .docx con LibreOffice y cambia cada texto por llenar por una marca
{{...}}. El resultado, seguimiento/adendum_plantilla.docx, lo incrusta
build_unificado.py en la página.

Marcas: NOMBRE, PUESTO, HORAS_ACTUALES («48 horas»), HORARIO_ACTUAL,
HORAS_NUEVAS («46 horas»), HORARIO_NUEVO, FECHA_LUGAR, FIRMA_PATRON, FIRMA_TRABAJADOR.
"""
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEN = RAIZ / 'seguimiento' / 'ADENDUM_Contrato_trabajo_NUEVA_JORNADA.doc'
SALIDA = RAIZ / 'seguimiento' / 'adendum_plantilla.docx'

CAMBIOS = [
    ('GIMNASIOS AMERICANOS SAP DE CV', 'GIMNASIOS AMERICANOS SAPI DE CV'),  # razón social correcta (Patty, 8 nov 2026)
    ('<w:t>con el carácter de patrón, y por &lt;&lt;</w:t>', '<w:t xml:space="preserve">con el carácter de patrón, y por </w:t>'),
    ('>NOMBRE DEL TRABAJADOR&lt;&lt;</w:t>', '>{{NOMBRE}}</w:t>'),
    ('>&lt;&lt;PONERLO&lt;&lt;,</w:t>', '>{{PUESTO}},</w:t>'),
    ('>&gt;&gt;NUMERO DE HORAS&lt;&lt;</w:t>', '>{{HORAS_ACTUALES}}</w:t>'),
    ('>&gt;&gt;PONER LOS DIAS Y EL HORARIO CUIDANDO QUE NO REBASEN LAS MAXIMAS LEGALES&lt;&lt;</w:t>', '>{{HORARIO_ACTUAL}}</w:t>'),
    ('la jornada semanal de labores será de 46 horas, distribuida', 'la jornada semanal de labores será de {{HORAS_NUEVAS}}, distribuida'),
    ('&gt;&gt;PONERLA CUIDANDO QUE NO REBASEN LAS MAXIMAS LEGALES, EJEMPLO: LUNES A SÁBADO DE LAS  07:00 A LAS 15:00, CON DESCANSO LOS DÍAS DOMINGO.', '{{HORARIO_NUEVO}}'),
    ('>&lt;&lt;PONER FECHA Y LUGAR&lt;&lt;,</w:t>', '>{{FECHA_LUGAR}},</w:t>'),
]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['soffice', '--headless', '--convert-to', 'docx', '--outdir', tmp, str(ORIGEN)],
                       check=True, capture_output=True, timeout=180)
        docx = Path(tmp) / (ORIGEN.stem + '.docx')
        with zipfile.ZipFile(docx) as z:
            partes = {n: z.read(n) for n in z.namelist()}
    xml = partes['word/document.xml'].decode('utf-8')
    for viejo, nuevo in CAMBIOS:
        assert xml.count(viejo) == 1, f'No encontré en la plantilla: {viejo[:60]}'
        xml = xml.replace(viejo, nuevo)
    firma = '&lt;&lt;NOMBRE Y FIRMA&lt;&lt;'
    assert xml.count(firma) == 2, 'Esperaba dos «NOMBRE Y FIRMA»'
    xml = xml.replace(firma, '{{FIRMA_PATRON}}', 1).replace(firma, '{{FIRMA_TRABAJADOR}}', 1)
    assert '&lt;&lt;' not in xml and '&gt;&gt;' not in xml, 'Quedó una marca sin cambiar'
    partes['word/document.xml'] = xml.encode('utf-8')
    with zipfile.ZipFile(SALIDA, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, b in partes.items():
            z.writestr(n, b)
    print(f'Listo: {SALIDA.relative_to(RAIZ)} ({SALIDA.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
