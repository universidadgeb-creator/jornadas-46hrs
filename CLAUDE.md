# Jornadas 46 hrs 2027 — Grupo GEB

Contexto del proyecto para retomarlo en Claude Code. Responsable: Patty, Gerente de Capital Humano de Grupo GEB. Idioma de trabajo: español (México). Prefiere entregables cortos, ejecutivos y listos para compartir, y ajustes iterativos en lugar de rehacer todo.

## Objetivo

La reforma a la LFT (DOF 3 mar 2026) baja la jornada máxima semanal de 48 hrs a 46 en 2027, 44 en 2028, 42 en 2029 y 40 en 2030, sin reducir salario ni prestaciones. El proyecto identifica **qué personas y qué puestos** trabajan por encima del límite y da seguimiento a su cambio de jornada y de contrato. **Meta: cerrar todos los cambios antes de que termine noviembre de 2026.**

## Piezas

| Pieza | Qué es | Dónde |
|---|---|---|
| Tablero «Jornada 46 hrs 2027» | Dashboard de análisis (artifact de tipo Dashboard en claude.ai) | https://claude.ai/artifact/Rcd92fe4fQ8SdhX3g5cSo1 · código en `dashboard/index.html` |
| Versión para proyectar | El mismo tablero en un HTML autónomo y sin internet, con d3 y los datos incrustados | `dashboard/Jornada_46hrs_2027_proyectar.html` |
| «Nuevas jornadas por rol» | Documento vivo de seguimiento con las 58 personas de 48 hrs (artifact con base de datos compartida) | https://claude.ai/artifact/HcTgQg9nxbEGeX3q2qks6k · código en `seguimiento/nuevas_jornadas.html` |
| Datos | Excel fuente y los dos CSV que lee el tablero | `datos/` |
| Scripts | Regeneran los CSV, la versión para proyectar y la propuesta de horarios | `scripts/build_csv.py` · `scripts/build_proyectar.py` · `scripts/propuesta.py` |

## Fuente de datos

- Archivo `Revision_Jornadas_48hrs_GEB.xlsx`, hoja **«Base de Datos»**, con encabezados en la **fila 3**. Último corte: **5 nov 2026**.
- Columnas usadas: `Nombre`, `Puesto`, `División`, `Ubicación`, `Activo en TabBD`, `Jornada laboral` (horas de contrato), `Total jornada reconocida` (horas reales semanales, ya sin comida), `TIPO DE JORNADA (LFT)`, y `<Día> entrada / salida / jornada reconocida` de lunes a domingo.
- Universo: activos con `Activo en TabBD = «Sí»` (312). Los que tienen tipo «Sin horario capturado» (10) quedan fuera de los cálculos, así que la base de cálculo es de **302**.
- Normalizaciones: puesto vacío → «Sin puesto»; «R.P» → «R.P.»; «Vivo 47» → «VIVO 47»; «La estancia» → «La Estancia».
- Para regenerar los CSV: `python scripts/build_csv.py datos/Revision_Jornadas_48hrs_GEB.xlsx datos/`.

## Reglas de negocio

- **Grupo «48 hrs»**: horas reales ≥ 48. Es el universo principal acordado en la junta: **58 personas**.
- **Grupo «46–48 hrs»**: más de 46 y menos de 48 (34 personas). También rebasan el límite de 2027.
- **Ajuste por tipo de jornada** (acuerdo de la junta del 5 nov 2026):
  - Diurna: bajar 2 hrs, a **46**.
  - Mixta: bajar 3 hrs, a **45**. Su máximo legal es 45 y no cambia con la reforma.
  - Nocturna: **por confirmar**.
- **Duda abierta con el abogado:** al llegar a 40 hrs, ¿la mixta baja a 37 y la nocturna a 35?
- **Etapas 2027–2030**: con los horarios actuales se cuenta a quién queda arriba de cada límite (46/44/42/40). «Nuevas» son las personas que no estaban arriba del límite de la etapa anterior.
- **Plazas equivalentes** = horas a reacomodar ÷ 46. Es una referencia de capacidad, no una propuesta de contratación.

## Cifras actuales (corte 5 nov 2026)

- 58 personas con 48 hrs: **24 diurnas, 33 mixtas, 1 nocturna**. En la junta se mencionaron ~23 mixtos; está por validar.
- 92 personas se pasan de 46 hrs (58 + 34). Horas a reacomodar: ~162 hrs/semana, unas 3.5 plazas.
- El puesto más expuesto es Técnico de Orden y Limpieza: 40 de 50.
- Etapas: 2027 → 92 · 2028 → 141 (+49) · 2029 → 143 (+2) · 2030 → 155 (+12).
- Por sucursal, de las 58: Naciones 24, Valle Real 13, Gourmetería 11, Nuevos Negocios 6, Ávila Camacho 2, Cañadas 1, Iteso 1.

## Tablero: estructura

Pestañas:
- **Resumen**: una frase de resumen, 4 indicadores, ajuste por tipo de jornada (con link al seguimiento), gráfica de puestos y «Lo que viene» (columnas 2027 a 2030 con los puestos y nombres que se suman cada año).
- **Personas**: gráfica por sucursal y tabla con filtros de grupo, tipo, sucursal, puesto y búsqueda.
- **Jornadas por rol**: horario día por día; filtro de puesto (incluye «Todos») y de sucursal. Botón «Ver»: *Horario actual* o *Propuesta 2027*. La propuesta muestra a las 92 personas que pasan de 46 hrs con su nuevo horario: diurna a 46 y mixta a 45. El recorte se toma en bloques de 5 min del día más largo (empates: el primero de la semana); con días iguales queda parejo (−20 min diarios de 48 a 46, −30 de 48 a 45). Se conserva la entrada y se adelanta la salida. Si un día pasa de 12 h, marca «Revisar captura»; si el tipo no tiene regla, «Por confirmar». Resultado: 32 diurnas a 46, 59 mixtas a 45, 1 por revisar (Corona Miranda) y ~211 hrs/semana a reacomodar. La misma regla está en `scripts/propuesta.py` (debe dar lo mismo que el tablero).
- **2027–2030**: detalle por etapa.

Detalles técnicos:
- Datasets: `plantilla` y `horarios`, que son archivos CSV adjuntos al artifact.
- Cálculos (`dash.calc`): `afectados`, `kpis`, `por_puesto`, `por_ubicacion`, `etapas`, `etapas_personas`.
- El HTML usa la regla «one-writer»: el texto fijo va en el HTML y lo que depende de los datos va en elementos `data-draw`.
- Colores: acento verde azulado `#0f8b8d` (`#3cc7c4` en modo oscuro). Patty pidió no usar rojos.
- Para actualizar datos en el artifact: subir cada CSV como asset y actualizar el `source.url` de `datasets/plantilla` y `datasets/horarios`.
- La versión para proyectar usa un «shim» local de `dash` (en `<head>`) con los CSV incrustados. Si cambias `dashboard/index.html` o los datos, regenérala con `python scripts/build_proyectar.py`.
- La página del tablero en claude.ai vive en su base de datos: documento `files/index.html` (campo `text`). Para publicar un cambio: leerlo, confirmar que es igual a `dashboard/index.html` del último commit y hacer `update` con el texto nuevo y `edit: {via, at}`.
- GitHub: https://github.com/universidadgeb-creator/jornadas-46hrs (público, por decisión de Patty). GitHub Pages publica `main` en https://universidadgeb-creator.github.io/jornadas-46hrs/ (el `index.html` de la raíz lleva a la versión para proyectar).

## Documento vivo «Nuevas jornadas por rol»

- Colección `personas`: un documento por persona, con id = slug del nombre.
- Campos fijos: `nombre`, `puesto`, `sucursal`, `division`, `tipo`, `horas_actuales`, `horario_actual`.
- Campos editables: `lider`, `nuevo_horario`, `nuevas_horas`, `contrato` (bool), `comentario`.
- Muestra el avance (X de 58 con contrato nuevo), totales por tipo con número y %, avance por sucursal y filtros por tipo, sucursal, puesto y estado.
- Para que los gerentes editen, hay que compartirlo con permiso de edición.
- 8 nov 2026: se precargaron `nuevo_horario` y `nuevas_horas` de 57 personas con la propuesta automática (`scripts/propuesta.py`), solo donde estaban vacíos. Corona Miranda quedó sin propuesta hasta corregir su captura. Los gerentes validan o corrigen; `contrato` sigue en falso.

## Pendientes

1. Validar con los gerentes los horarios que ya avanzaron y capturar el **líder** de cada colaborador (lo trabajan Patty y Andy).
2. Revisar la captura de **Corona Miranda Jesús Alejandro**: aparece con 56 hrs porque su domingo dice 20:30–13:30.
3. Confirmar el ajuste para jornada **nocturna** y la duda de mixta y nocturna a 40 hrs con el abogado.
4. Juntas: gerentes de Easy Fit (propuesta por sucursal), Vivo (después del 9 nov, cuando regrese Isma) y Center (Antonio y líderes) la siguiente semana. Center será piloto del reloj checador (~15 días) y después habrá capacitación con Vivo (200+ colaboradores).
5. Calendario de jornada de 44 hrs: presentarlo y agendarlo con Operaciones en junio de 2027.
6. Posible mejora: que el tablero lea el avance del documento vivo. Hoy viven separados.
7. Hallazgo: 13 mixtas tienen entre 45 y 46 hrs. No entran en el corte de 2027 (>46), pero ya pasan del máximo legal de la mixta (45). Por decidir si se ajustan también.
