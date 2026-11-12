# Jornadas 46 hrs 2027 — Grupo GEB

Contexto del proyecto para retomarlo en Claude Code. Responsable: Patty, Gerente de Capital Humano de Grupo GEB. Idioma de trabajo: español (México). Prefiere entregables cortos, ejecutivos y listos para compartir, y ajustes iterativos en lugar de rehacer todo.

## Objetivo

La reforma a la LFT (DOF 3 mar 2026) baja la jornada máxima semanal de 48 hrs a 46 en 2027, 44 en 2028, 42 en 2029 y 40 en 2030, sin reducir salario ni prestaciones. El proyecto identifica **qué personas y qué puestos** trabajan por encima del límite y da seguimiento a su cambio de jornada y de contrato. **Meta: cerrar todos los cambios antes de que termine noviembre de 2026.**

## Piezas

| Pieza | Qué es | Dónde |
|---|---|---|
| **Página única «Jornada 46 hrs 2027»** (desde 8 nov 2026) | Tablero + seguimiento en un solo link: pestañas Resumen, Seguimiento, Mapa por sucursal, Planeación Gourmetería 2027, Planeación Valle Real 2027 (10 nov; era «2028» hasta el 11 nov) y Próximas etapas (desde el 9 nov 2026; se quitaron «Personas» y «Jornadas por rol» porque repetían lo de Seguimiento y Mapa) (captura con base de datos compartida). Es la que se comparte. | https://claude.ai/artifact/HcTgQg9nxbEGeX3q2qks6k · se genera con `scripts/build_unificado.py` en `seguimiento/nuevas_jornadas.html` |
| Tablero anterior (respaldo, ya no se usa) | Dashboard de análisis (artifact de tipo Dashboard en claude.ai) | https://claude.ai/artifact/Rcd92fe4fQ8SdhX3g5cSo1 · su código, `dashboard/index.html`, sigue siendo la fuente de las pestañas de análisis |
| Versión para proyectar | El mismo tablero en un HTML autónomo y sin internet, con d3 y los datos incrustados | `dashboard/Jornada_46hrs_2027_proyectar.html` |
| Captura de seguimiento | La pestaña «Seguimiento» de la página única (desde el 9 nov 2026, **todas las personas que pasan de 46 hrs**: 100) | `seguimiento/captura.html` + `seguimiento/captura_estilos.css` |
| Datos | Excel fuente y los dos CSV que lee el tablero | `datos/` |
| Scripts | Regeneran los CSV, la versión para proyectar, la página única y la propuesta de horarios | `scripts/build_csv.py` · `scripts/build_proyectar.py` · `scripts/build_unificado.py` · `scripts/propuesta.py` |

## Fuente de datos

- Archivo `Revision_Jornadas_48hrs_GEB.xlsx`. **Desde el 9 nov 2026 la hoja buena es «Base Original»** (acuerdo con Patty; la hoja «Revisar diferencias» del Excel dice que ahí quedó lo correcto). Encabezados en la **fila 3**. `limpiar_excel.py` la toma y la guarda en el Excel limpio como «Base de Datos», que es lo que lee `build_csv.py`. Último corte: **10 nov 2026** (Patty mandará más cambios).
- Columnas usadas: `Nombre`, `Puesto`, `División`, `Ubicación`, `Activo en TabBD`, `Jornada laboral` (horas de contrato), `Total jornada reconocida` (horas reales semanales, ya sin comida), `TIPO DE JORNADA (LFT)`, y `<Día> entrada / salida / jornada reconocida` de lunes a domingo.
- Universo: activos con `Activo en TabBD = «Sí»`, **sin instructores ni tutoriales** (pedido de Patty, 10 nov 2026: `EXCLUIR_PUESTOS` en `build_csv.py` = puestos que contienen «instructor» o «tutorial»; hoy 22: Instructor de Acuática 12, Coach Tutorial 6, Instructor de Clases de Salón 3, TUTORIAL 1). «ATP» también se excluirá cuando Patty diga cómo aparece en el Excel (no está en ninguna columna). Las filas sin nombre se omiten (hubo 2 altas a medio capturar). Corte 10 nov: 314 activos, 312 con horario.
- **Nuevos Negocios por marca (12 nov 2026, pedido de Patty):** si la ubicación es «Nuevos Negocios», `build_csv.py` usa la columna «Área» como club (`MARCAS_NN`: Clinica → Clínica, White mouse → White Mouse). Hoy: Onara 9 (8 pasan de 46), Clínica 6, Acton Academy 4, Seven Nutrition 2, White Mouse 1, y Onara VR 2 (ya venía como ubicación). En el Seguimiento las 9 personas de Nuevos Negocios quedaron con `sucursal` = «Onara», y se creó `unidades/onara` con el mismo firmante (Patricio Villarreal Damy) y lugar (Naciones Unidas 6700). Si alguien de otra marca entra al Seguimiento, hay que crear su `unidades/<marca>`.
- Normalizaciones: puesto vacío → «Sin puesto»; «R.P» → «R.P.»; «Vivo 47» → «VIVO 47»; «La estancia», «Estancia» y «estancia» → «La Estancia».
- Para regenerar los CSV: `python scripts/build_csv.py datos/Revision_Jornadas_48hrs_GEB.xlsx datos/` (antes, limpiar el Excel recibido con `scripts/limpiar_excel.py`).

## Cómo se actualizan los datos (acordado 8 nov 2026)

- **El Excel es la fuente única** del horario actual, altas, bajas y sustituciones. Patty lo manda y Claude regenera todo. En la página solo se captura lo acordado: nuevo horario, líder, contrato y comentario.
- **Alta:** fila nueva con fecha de ingreso y horario. Sugerencia: contratar a la gente nueva ya en 46 (diurna) o 45 (mixta).
- **Baja:** no se borra la fila; se llena «Fecha de baja» y «Activo en TabBD» = «No».
- **Sustitución** (se va Pedro, entra Juanito con el mismo horario): baja de Pedro + alta de Juanito en fila nueva; en «Observaciones», «Sustituye a Pedro». No se renombra la fila.
- **Identificación por nombre completo** (Patty no quiere usar número de empleado). Al recibir un Excel nuevo, revisar nombres parecidos (acentos, orden, espacios) y preguntar antes de tratar a alguien como baja + alta.
- Con cada Excel nuevo: regenerar CSV, propuesta, versión para proyectar y página única; dar un resumen corto (altas, bajas, cambios de horario, quién entra o sale de 48 hrs); agregar al Seguimiento a quien llegue a 48 hrs y marcar como baja (sin borrar) a quien salga.
- **Datos confidenciales:** Patty decidió que el proyecto no los necesita. El Excel completo de RH trae CURP, RFC, NSS, fecha de nacimiento, número de empleado y salarios; **nunca se sube tal cual**. Primero se limpia con `python scripts/limpiar_excel.py <excel_recibido.xlsx> datos/Revision_Jornadas_48hrs_GEB.xlsx` (deja solo la hoja «Base de Datos» sin esas columnas) y después se corre `build_csv.py`. El 8 nov 2026 se borró el Excel original de todo el historial de GitHub (con autorización de Patty) y se dejó el Excel limpio.

## Reglas de negocio

- **Grupo «48 hrs»**: horas reales ≥ 48. Fue el universo acordado en la junta del 5 nov (58; 64 al corte del 9 nov).
- **Universo del Seguimiento y del adendum (desde el 9 nov 2026, por decisión de Patty): todas las personas con más de 46 hrs** (100 al 9 nov), porque las de 46–48 también rebasan el límite de 2027 y necesitan cambio de horario y adendum.
- **Grupo «46–48 hrs»**: más de 46 y menos de 48 (34 personas). También rebasan el límite de 2027.
- **Ajuste por tipo de jornada** (acuerdo de la junta del 5 nov 2026):
  - Diurna: bajar 2 hrs, a **46**.
  - Mixta: bajar 3 hrs, a **45**. Su máximo legal es 45 y no cambia con la reforma.
  - Nocturna: **por confirmar**.
- **Duda abierta con el abogado:** al llegar a 40 hrs, ¿la mixta baja a 37 y la nocturna a 35?
- **Etapas 2027–2030**: con los horarios actuales se cuenta a quién queda arriba de cada límite (46/44/42/40). «Nuevas» son las personas que no estaban arriba del límite de la etapa anterior.
- **Plazas equivalentes** = horas a reacomodar ÷ 46. Es una referencia de capacidad, no una propuesta de contratación.

## Cifras actuales (corte 10 nov 2026, 3.er Excel del día)

- 63 personas con 48 hrs (22 diurnas, 41 mixtas) y 36 entre 46 y 48: **99 pasan de 46 hrs**. Horas a reacomodar a 46: ~167.5/semana. Etapas: 2027 → 99 · 2028 → 136 · 2029 → 138 · 2030 → 151.
- Cambios: **Medina Hernandez Cesar Abraham** pasó de Barista en Onara (48 diurna) a Técnico de Orden y Limpieza en Naciones, noche L–V 22:00–06:00 (40 nocturna). En el Excel la «Ubicación» sigue como Nuevos Negocios: `CAMBIO_UBICACION` en `build_csv.py` lo pone en Naciones hasta que Patty lo corrija. En el Seguimiento quedó `fuera`. Ojo: 8 h nocturnas al día pasan del máximo diario de la nocturna (7 h); el Excel lo marca «Excede máx. diario». **Villarreal Damy Patricio** ya está en el Excel con L–V 9–18 (40 h): se marcó `aplicado_excel`; su adendum sigue pendiente de firma.

## Corte del 10 nov 2026, 2.º Excel del día («jornadas pendientes»)

- 65 personas con 48 hrs (24 diurnas, 41 mixtas) y 36 entre 46 y 48: **101 pasan de 46 hrs**. Horas a reacomodar a 46: ~171.5/semana; con la propuesta (mixtas a 45): ~238.5. Etapas: 2027 → 101 · 2028 → 138 · 2029 → 140 · 2030 → 153. Activos 314, 313 con horario.
- Cambios contra el Excel anterior: Arechiga Alvarez Carlos Alberto (Coach Deportivo, Gourmetería) ya tiene horario: 40 h mixta, no entra. Pérez Suárez Dafne bajó de 48 a 40 en el Excel (ya firmó su adendum): sigue en el Seguimiento, marcada con `aplicado_excel` (fecha) y `excel_horas` (40), que la página muestra como «Ya aplicado en el Excel». Ojo: su horario validado descansa el viernes y el Excel dice jueves.
- **Regla nueva:** quien ya firmó y cuyo horario nuevo ya quedó en el Excel **no se marca como `fuera`** (seguiría contando en el avance); se marca con `aplicado_excel`.

## Corte previo del 10 nov 2026 (hoja «Base Original», sin instructores ni tutoriales)

- 66 personas con 48 hrs (25 diurnas, 41 mixtas) y 36 entre 46 y 48: **102 pasan de 46 hrs** (en Seguimiento). Horas a reacomodar a 46: ~173.5/semana; con la propuesta (mixtas a 45): ~240.5. Etapas: 2027 → 102 · 2028 → 139 · 2029 → 141 · 2030 → 154.
- Cambios 9→10 nov: entran a seguimiento Viloria Uribe (Lavaloza, ahora con horario: 48 mixta), Macías Cervantes (Auxiliar General, 48) y Chávez Rivera (Mesero, 48), los tres de Nuevos Negocios; sale Cuevas Ramírez (ya no está en la base). Escalante Núñez pasó a mixta (propuesta recalculada a 45). Nueva ubicación «Onara VR» (2 baristas, 46 h: no entran). Macías y Chávez no traen jornada de contrato.

### Corte anterior (9 nov 2026)

- 64 personas con 48 hrs: **25 diurnas, 39 mixtas, 0 nocturnas**. (Corte del 5 nov: 58 = 24 diurnas, 33 mixtas, 1 nocturna.)
- 100 personas se pasan de 46 hrs (64 + 36). Horas a reacomodar para bajar a 46: ~169.5 hrs/semana, unas 3.7 plazas. Con la propuesta (mixtas a 45): ~234.5 hrs.
- El puesto más expuesto es Técnico de Orden y Limpieza: 45 de 57.
- Etapas: 2027 → 100 · 2028 → 137 · 2029 → 139 · 2030 → 152.
- Por sucursal, de las 64: Naciones 27, Valle Real 14, Gourmetería 13, Nuevos Negocios 8, Ávila Camacho 1, Cañadas 1.
- Cambios 5→9 nov en el grupo de 48: entran Cuevas Ramírez, Uribe De la Rocha, De la Cruz Rodríguez, Cuevas Rivera, González Álvarez, Pérez Suárez, Cruz Pérez y Rentería Tejeda; salen Corona Miranda (horario corregido a 30 h) y Torres Campos (47.5 h: sigue arriba de 46).

## Tablero: estructura

Pestañas:
- **Resumen**: una frase de resumen, 4 indicadores, ajuste por tipo de jornada (con link al seguimiento), gráfica de puestos y «Lo que viene» (columnas 2027 a 2030 con los puestos y nombres que se suman cada año).
- **Personas**: gráfica por sucursal y tabla con filtros de grupo, tipo, sucursal, puesto y búsqueda.
- **Jornadas por rol**: horario día por día; filtro de puesto (incluye «Todos») y de sucursal. Botón «Ver»: *Horario actual* o *Propuesta 2027*. La propuesta muestra a las 92 personas que pasan de 46 hrs con su nuevo horario: diurna a 46 y mixta a 45. El recorte se toma en bloques de 5 min del día más largo (empates: el primero de la semana); con días iguales queda parejo (−20 min diarios de 48 a 46, −30 de 48 a 45). Se conserva la entrada y se adelanta la salida. **Transporte (9 nov 2026):** no se mueven las entradas de las 05:00 o antes ni las salidas de las 23:00 o después (o que cruzan medianoche); si la salida es fija, la persona entra más tarde (15:00–23:00 → 15:30–23:00). En el editor del Seguimiento sale un aviso si alguien mueve una de esas horas. Si un día pasa de 12 h, marca «Revisar captura»; si el tipo no tiene regla, «Por confirmar». Resultado: 32 diurnas a 46, 59 mixtas a 45, 1 por revisar (Corona Miranda) y ~211 hrs/semana a reacomodar. La misma regla está en `scripts/propuesta.py` (debe dar lo mismo que el tablero).
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

## Página única: cómo se arma y se publica

- **Pestañas (9 nov 2026):** Resumen · Seguimiento · Mapa por sucursal · Próximas etapas. `build_unificado.py` arma la barra de pestañas, quita las secciones `t-personas` y `t-rol` de `dashboard/index.html`, pasa la gráfica «¿En qué sucursales?» al Resumen (junto a la de puestos) y hace que el clic en un puesto abra su plantilla por turno en el Mapa (evento `mapa:puesto`, todas las sucursales). `dashboard/index.html` y la versión para proyectar conservan las 4 pestañas originales.

- **Nueva estructura (12 nov 2026, para la presentación de Patty; quitar información duplicada):** cada pestaña tiene un solo propósito.
  - **Encabezado** sin cifras (antes decía 99 y el Seguimiento 101): explica la reforma.
  - **Resumen** = decisión. 4 cifras (personas a ajustar con desglose 48 / 46–48 / ya ajustadas en Excel; horas que se reacomodan; equivale a personas; contratos firmados con barra), «La regla» por tipo (diurna 46, mixta 45, nocturna por confirmar + nota ley vs. mixtas a 45 vs. capturado), tabla «¿Dónde está el impacto y cómo va cada club?» (cadena/club: personas, horas menos, equivale a, horario validado, contrato firmado; clic en club abre su captura), gráfica de puestos a todo lo ancho y «Lo que viene» solo con números (sin lista de puestos). Todo lo del Resumen sale de `renderResumen()` en `captura.html` (lee el Seguimiento en vivo). `build_unificado.py` quita del tablero los 4 indicadores viejos, la tarjeta por tipo, la gráfica por sucursal y las listas de puestos por año.
  - **Filtro de cadena en el Resumen (12 nov 2026):** botones arriba (Todas · VIVO 47 · EASY FIT · Nuevos Negocios). Filtran las 4 cifras, la regla, la tabla por club, la gráfica de puestos (`porPuestoCad()`, inyectada por `build_unificado.py`) y «Lo que viene». Usa el mismo estado que Próximas etapas (`GXE.cad`): elegir cadena en una pestaña la deja elegida en la otra (evento `cadena:cambio`).
  - **«Lo que viene» con personas equivalentes (12 nov 2026, pedido de Patty):** cada año muestra «≈ N personas de tiempo completo» (horas arriba del límite ÷ el límite de ese año) y debajo la tabla «¿A cuántas personas equivale en cada club?» (cadena/club × 2027–2030 + cuántos pasan de 40). Usa el Excel (horarios de hoy, límite de ley para todos) y sigue el filtro de cadena (`renderEtapasClub()` en `captura.html`). Al 12 nov: 3.6 · 9.7 · 16.7 · 24.9 personas; a 40 hrs: VIVO 47 16 (Naciones 7.7, Valle Real 4.3, Gourmetería 4.0), EASY FIT 6.8, Nuevos Negocios 2.1. Escenario abogado (mixta 37, nocturna 35 a 40 hrs): 189 personas, 1,388 h ≈ 34.7.
  - **Seguimiento** = operación: botones de cadena + tabla «Avance por sucursal» con los 4 pasos (horario validado, líder, adendum descargado, contrato firmado), subtotal por cadena y clic en sucursal para filtrar (`renderAvanceSeg`). Se quitaron la tarjeta de avance, las tarjetas por tipo y las tarjetas por sucursal.
  - **Mapa** = solo cobertura de horarios (la tabla de avance se movió al Seguimiento).
- *(Sustituida el 12 nov por la nueva estructura)* **Tarjeta «¿Cuánta capacidad se reacomoda?» (12 nov 2026, pedido de Patty):** en el Resumen, debajo del avance (`RESUMEN_AVANCE` en `build_unificado.py`, `renderCapacidad()` en `captura.html`). Lee las personas del Seguimiento (en vivo): horas menos con la propuesta (diurna 46, mixta 45), mínimo de ley (todas a 46), lo que suma bajar las mixtas a 45 y lo capturado hoy (nuevo horario guardado); todo ÷ 46 = personas equivalentes, con tabla por cadena y club. Al 12 nov: propuesta 238.5 h = 5.2 personas; ley 171.5 h = 3.7; mixtas a 45 +67 h = +1.5; capturado 251.5 h = 5.5 (101 personas, incluye a Pérez Suárez y Villarreal Damy, que bajan a 40).
- `scripts/build_unificado.py` junta `dashboard/index.html` (análisis, con un `dash` local y los CSV incrustados, como la versión para proyectar), `seguimiento/captura.html` y `captura_estilos.css`, y agrega la pestaña «Seguimiento» y la tarjeta «Avance del cambio de contrato» en el Resumen (lee la misma colección `personas`).
- d3 se carga de cdnjs (7.8.5). En este contenedor cdnjs está bloqueado: para probar en local, servir d3 desde la copia que trae la versión para proyectar.
- Flujo para cualquier cambio: editar `dashboard/index.html` o `seguimiento/captura*` → `python scripts/build_proyectar.py` → `python scripts/build_unificado.py` → publicar `seguimiento/nuevas_jornadas.html` en el artifact HcTgQg9… (sin `capabilities`, para conservar `db` y `user`).
- El enlace directo a una pestaña usa el hash: `#t-seg` abre Seguimiento.

## Mapa por sucursal (9 nov 2026, para Dirección)

- Pestaña «Mapa por sucursal» de la página única (`seguimiento/mapa.html` + `mapa_estilos.css`, solo lectura). Filtros: **cadena** (12 nov 2026; división tomada de `plantilla`; reduce la lista de sucursales, la tabla de avance —con subtotal por cadena cuando se ven todas— y el archivo maestro, que lleva columna Cadena y el nombre de la cadena en el archivo), sucursal, puesto y Ver (Hoy / 2027 / Cambio). Arriba: personas, horas por semana hoy y 2027, hora con más gente; **tabla por franja del día** (Madrugada 0–5, Temprano 5–9, Media mañana 9–13, Tarde 13–17, Noche 17–21, Cierre 21–24; valor = máximo de personas en piso en la franja, con «hoy n» si cambia). Vista principal (pedido de Patty, 9 nov): **Plantilla por turno**, nombres y horarios agrupados por hora de entrada del primer día trabajado — Apertura (antes de 7:00), Mañana (7:00–11:59), Tarde (12:00–16:59), Noche (17:00 o después) — y ordenados de la mañana al cierre, sin mezclar turnos. Se descartaron la cuadrícula por media hora como vista principal (queda en «Ver detalle por media hora») y la tabla de turnos agrupados (solo en el Excel). Detalle: personas en piso por día y **media hora** (cuenta si trabaja ≥ 15 min del bloque; cruza medianoche), en tres vistas: Hoy, 2027 y Cambio (ámbar = menos gente, verde azulado = más). «2027» usa el nuevo horario guardado en el Seguimiento (o la propuesta precargada) y el horario actual de quienes no están en seguimiento. Debajo, la tabla de horarios de la sucursal (en 2027 marca lo que cambia contra hoy).
- «Descargar archivo maestro (.xlsx)» (SheetJS 0.18.5, cdnjs): hoja «Resumen» por sucursal (personas, cuántas pasan de 46, horas por semana hoy y 2027) + una hoja por sucursal con franjas 2027 (hoy), turnos 2027, cada persona (Lun–Dom hoy y 2027, horas) y el detalle por media hora 2027 y hoy.
- El script del Seguimiento publica `window.SEG = {rows, fuera, diasDe, horasDe}` y el evento `seg:datos`; el mapa lo escucha.

- **Avance de captura por sucursal (9 nov 2026):** tabla arriba del Mapa con todas las sucursales (personas en seguimiento) y cuatro pasos con barra: horario validado, líder, adendum descargado y recibido firmado, más una fila Total. «Ver captura» abre el Seguimiento filtrado en esa sucursal (`SEG.verSucursal`).

## Propuesta 40 hrs (12 nov 2026, pedido de Patty)

- Pestaña «Propuesta 40 hrs» (`seguimiento/propuesta40.html` + `propuesta40_estilos.css`, solo lectura; va al final, después de Próximas etapas). Escenario para ir directo a 40 hrs sin pasar por 46/44/42. **No toca el Seguimiento ni los adendums de 2027.**
- Universo: **todas las personas con más de 40 hrs** (151 al 12 nov). Decisiones de Patty: mismos días que hoy; **1 h de comida que se saca** del tiempo de trabajo (va dentro del turno y no cuenta).
- Regla: misma hora de entrada; cada día se reduce en proporción a sus horas de hoy (bloques de 5 min) hasta sumar 40; tope legal por día (diurna 8 h, mixta 7.5 h, nocturna 7 h; si no alcanza 40 se marca); 1 h de comida en días de 5 h de trabajo o más (turno = trabajo + 1 h); transporte: si hoy sale a las 23:00 o después, conserva la salida y entra más tarde.
- Resultado al 12 nov: 151 personas, todas quedan en 40; 7,035 → 6,040 hrs/semana (−995 = 24.9 personas de 40 hrs). Ojo: 160 de 905 turnos (49 personas) terminan más tarde que hoy, porque hoy no toman comida y la hora de comida alarga su estancia.
- Filtros cadena / club / puesto / búsqueda; tabla agrupada por club (día por día: horario nuevo, horas + comida, y el de hoy); «Descargar propuesta (.xlsx)»: hojas «Propuesta 40 hrs» (por persona, Lun–Dom hoy y 40) y «Resumen por club». Expone `window.P40 = {todos, proponer}`.

## Planeación por club (10 nov 2026)

- **Una sola plantilla** (`seguimiento/plan.html`, marcas {{P}} prefijo de ids, {{TAB}}, {{TITULO}}, {{SAB}}, {{DOM}}, {{SAB_ANTES}}, {{DOM_ANTES}}, {{CONFIG}}); `build_unificado.py` la llena una vez por club con la lista `PLANES`. Para otro club: agregar una entrada a `PLANES` (prefijo, pestaña, club, título, colección de ajustes, horario del club).
- Pestañas actuales: **Planeación Gourmetería 2027** (`t-plan`, ajustes en `plan_gourmeteria`) y **Planeación Valle Real 2027** (`t-planvr`, ajustes en `plan_valle_real`). Valle Real: sábado 7:00–17:00, domingo **8:30**–15:00 (antes 9:00–15:00), lunes a viernes sin cambio; 54 personas, 21 coaches. **Las dos son de 2027** (metas 46/45): el 11 nov 2026 Patty pidió corregir el título de Valle Real de 2028 a 2027.

- **Flujo acordado (10 nov 2026):** 1) el gerente valida/corrige el nuevo horario en el **Seguimiento**; 2) la **planeación** lo toma sola (más la regla de coaches) y **Operaciones** ajusta lo necesario por cobertura; 3) **«Pasar al Seguimiento»** (solo en personas ajustadas que están en Seguimiento) copia el horario planeado a `personas` (`nuevo_horario`, `nuevo_horario_dias`, `nuevas_horas`, `horario_validado`, `horario_validado_por`, `horario_origen` = título de la planeación; borra `adendum_generado` y el comentario de precarga) y **borra el ajuste** de la planeación, que vuelve a leer del Seguimiento. No deja pasar un horario que excede 46/45. El Seguimiento muestra «Validado el … · desde Planeación …»; si el gerente vuelve a guardar, `horario_origen` se limpia. 4) Adendum, firma y «Recibido firmado».
- Pendiente con el abogado: cómo redactar en el adendum el descanso rotativo de los coaches (su horario fijo no lo refleja).

### Planeación Gourmetería 2027

- Pestaña «Planeación Gourmetería» (`seguimiento/plan.html` + `plan_estilos.css`). Nuevo horario del club en 2027: **sábado 7:00–17:00** (antes 7–16) y **domingo 8:30–15:00** (antes 9–15); lunes a viernes sin cambio.
- Base de cada persona: su horario 2027 del Seguimiento (validado o propuesta) o, si no está en seguimiento, su horario actual.
- **Coaches** (puestos que empiezan con «Coach»: Deportivo, Estiramiento, Mobility; no Líder Deportivo; decisión de Patty): dos descansos con el **mismo turno diario** (sus horas por semana bajan): uno entre semana que **rota** (la página sugiere uno repartido por turno mañana/tarde, en orden lunes→viernes) y su día de fin de semana **igual que hoy**. Quien ya tiene un descanso entre semana no cambia.
- **Cobertura del fin de semana:** la decide **Operaciones**. La página no la impone: muestra por área (del Excel, columna `area` en `plantilla_jornadas.csv`) cuántas personas hay en el horario de apertura y qué medias horas quedan sin nadie. Corte 10 nov: Deportes y Mtto/Comercial sin nadie el sábado 15:00 (o 14:30)–17:00; Administración nadie el sábado; Comercial nadie el domingo; Ludoteca con huecos.
- Operaciones puede **ajustar** el horario planeado de cualquiera (editor día por día con total de horas y aviso si pasa de 46/45). Se guarda en la colección `plan_gourmeteria` (id = slug del nombre: {nombre, dias, editado, editado_por}); «Volver a la propuesta» borra el ajuste. Esto **no cambia el Seguimiento** ni el adendum.
- «Descargar planeación (.xlsx)»: hoja «Plan 2027» (por área, horario 2027 y hoy, horas, notas) y hoja «Cobertura fin de semana».
- **Próximas etapas** tiene filtros **Cadena** (división: VIVO 47, EASY FIT, Nuevos Negocios…) y **Club** (sucursal); aplican a los conteos por año, la gráfica de puestos y la tabla.

## Seguimiento (colección `personas`)

- Colección `personas`: un documento por persona, con id = slug del nombre. Quien sale del grupo de 48 no se borra: lleva `fuera` (motivo) y `fuera_desde` (fecha); la página lo saca de los conteos y lo lista en «N personas salieron del grupo de 48 hrs».
- Campos fijos: `nombre`, `puesto`, `sucursal`, `division`, `tipo`, `horas_actuales`, `horario_actual`.
- Campos editables: `lider`, `nuevo_horario`, `nuevas_horas`, `contrato` (bool), `comentario`, y `nuevo_horario_dias` ({lun..dom: "HH:MM–HH:MM" o null}).
- **Horario validado (9 nov 2026):** al guardar en el editor se escriben `horario_validado` (fecha) y `horario_validado_por` (id del usuario), y si el comentario era «Propuesta inicial, por validar» se borra. La celda dice «Validado el …» o «Propuesta sin validar». Los contadores «con horario validado» (Seguimiento y Resumen) cuentan solo los validados, no las propuestas precargadas.
- **Conteo automático (8 nov 2026):** el nuevo horario ya no se escribe a mano. Con «Editar» se abre un editor día por día (entrada, salida, descanso) y la página calcula las horas: suma de entrada a salida de cada día (si la salida es menor, cruza medianoche) y descuenta la comida igual que en el horario actual de la persona (por día; de las 58, 52 no descuentan y 6 descuentan 1 h). Al guardar escribe `nuevo_horario` (texto «L–V 07:00–14:40 · S … · D descanso»), `nuevo_horario_dias` y `nuevas_horas`. La columna «Nuevas hrs» muestra lo calculado desde el horario guardado; si un texto viejo no se puede leer, lo marca para corregirlo.
- Muestra el avance (X de 58 con contrato nuevo), totales por tipo con número y %, avance por sucursal y filtros por tipo, **cadena** (campo `division`; 10 nov 2026, pedido de Patty; al elegir cadena, la lista de sucursales se reduce a las de esa cadena), sucursal, puesto y estado. **Por cadena (10 nov 2026):** hasta arriba, botones de cadena (Todas · VIVO 47 · EASY FIT · Nuevos Negocios, con su número) que filtran el avance, las tarjetas por tipo y la tabla; las tarjetas de sucursal van agrupadas bajo cada cadena («Propuesta por cadena y sucursal») con su subtotal.
- Para que los gerentes editen, hay que compartir la página única con permiso de edición (desde Compartir en claude.ai).
- 9 nov 2026: se agregaron al Seguimiento las 36 personas de 46–48 hrs (35 nuevas + Torres Campos, que regresó), con su propuesta precargada. Total: 100 en seguimiento, 1 fuera (Corona Miranda). Las tarjetas por tipo dicen «Meta: 46 hrs» / «Meta: 45 hrs».
- 9 nov 2026: por la regla de transporte se corrigieron 20 propuestas precargadas que nadie había editado (turnos que salían a las 23:00: ahora entran 30 min más tarde).
- 9 nov 2026: se agregaron 8 personas nuevas con la propuesta precargada y se re-propuso Palacios López (su horario actual cambió y ahora es mixta).
- 8 nov 2026: se precargaron `nuevo_horario` y `nuevas_horas` de 57 personas con la propuesta automática (`scripts/propuesta.py`), solo donde estaban vacíos. Corona Miranda quedó sin propuesta hasta corregir su captura. Los gerentes validan o corrigen; `contrato` sigue en falso. El `comentario` de esos 57 dice «Propuesta inicial, por validar»; el de Corona Miranda, «Sin propuesta: revisar captura del domingo (20:30–13:30)». Si un gerente cambia el horario, conviene que borre o cambie esa nota.

## Adendum de contrato (desde 8 nov 2026)

- Plantilla original de Patty: `seguimiento/ADENDUM_Contrato_trabajo_NUEVA_JORNADA.doc`. `scripts/build_plantilla_adendum.py` la convierte a `seguimiento/adendum_plantilla.docx` con marcas {{NOMBRE}}, {{PUESTO}}, {{HORAS_ACTUALES}}, {{HORARIO_ACTUAL}}, {{HORAS_NUEVAS}}, {{HORARIO_NUEVO}}, {{FECHA_LUGAR}}, {{FIRMA_PATRON}}, {{FIRMA_TRABAJADOR}}. `build_unificado.py` extrae su texto párrafo por párrafo (negritas y alineación) a `window.ADENDUM_PARRAFOS`; la página arma el adendum en **PDF de una sola página** con jsPDF 2.5.1 (cdnjs), bajando la letra de 11 pt hasta que quepa (Letter, márgenes 64/54 pt), y junta varios en .zip con JSZip 3.10.1. Ya no se descarga Word (pedido de Patty, 9 nov 2026).
- Acuerdos con Patty: razón social **GIMNASIOS AMERICANOS SAPI DE CV** para todas las divisiones; mixtas con 45 h en la cláusula PRIMERA (diurnas 46); antecedente I = jornada de contrato del Excel («Jornada laboral») + horario actual (está bien que diga 48: el adendum es para bajarla); firma por la empresa el gerente de cada sucursal; lugar = dirección por unidad de negocio (Patty las manda).
- En la página (pestaña Seguimiento): tarjeta «Adendum de contrato» con fecha de firma, «Descargar los listos (.zip)» y, por sucursal, gerente que firma y lugar (colección `unidades`, id = slug de la sucursal: {sucursal, firmante, lugar}). Cada fila tiene la columna «Adendum»: Listo + Descargar, o el motivo (falta nuevo horario, pasa de la meta, falta gerente/lugar, falta jornada de contrato, jornada por confirmar). Al descargar guarda `adendum_generado` (fecha) en la persona; si después se vuelve a guardar su nuevo horario, se borra esa fecha para obligar a descargar el adendum otra vez.
- **Firmantes y lugares (9 nov 2026, archivo DIRECCIONES_OK de Patty):** firma el **gerente de la sucursal**, sin importar el área de la persona. Naciones: AGUAYO SANCHEZ JULIAN · Gourmeteria: ARMAS GUTIERREZ KAREN ANAID · Valle Real: DÍAZ GARCÍA DAVID ALEJANDRO · Cañadas y Aleira: OROZCO ACEVES ERIKA MERCEDES · Ávila Camacho e Iteso: SOTELO DELGADILLO ALBERTO IVAN · La Estancia: CASTILLO GONZALEZ ISMAEL · Nuevos Negocios (ONARA y Real Food): PATRICIO VILLARREAL DAMY, con la dirección de Naciones Unidas 6700. El lugar de firma es la dirección de cada unidad (guardada en `unidades`).
- **Firmante propio por persona:** el campo `firmante_patron` en `personas` sustituye al gerente de la sucursal. Villarreal Damy Patricio lo firma RODRIGUEZ ARROYO JULIA ELIZABETH (Dirección). La página no deja que alguien firme su propio adendum como patrón.
- **Control de adendums recibidos (9 nov 2026):** en cada persona, casilla «Recibido firmado». Guarda `adendum_recibido` (fecha), `adendum_recibido_por` (id del usuario; el nombre se resuelve con `user.profiles`, por eso la página declara `user: {scopes: ["profile"]}`), `adendum_recibido_horario` (el nuevo horario de ese momento) y marca `contrato: true`. Si después cambia el nuevo horario, avisa «falta firmar un adendum nuevo». La tarjeta muestra listos / descargados / recibidos, el filtro Estado tiene «Adendum por recibir / recibido», «Descargar los listos por entregar (.zip de PDF)» omite los ya recibidos, y «Descargar control (.csv)» baja el control completo para el archivo.
- Quién corrige qué: el **nuevo horario** lo corrige el gerente en la página (Editar); el **horario actual** y la **jornada de contrato** solo se corrigen en el Excel. La página declara `db`, `user` (con `scopes: ["profile"]`) y `downloads`.
- Falta jornada de contrato en el Excel (9 nov): Aguilera Martínez, Meza Ramírez, Hernández Aguayo, Navarro Villarreal y Rentería Tejeda. Contrato distinto al horario: Villegas Velázquez, Palacios López y Pérez Suárez (40 vs 48).

## Pendientes

1. Validar con los gerentes los horarios que ya avanzaron y capturar el **líder** de cada colaborador (lo trabajan Patty y Andy).
2. ~~Revisar la captura de Corona Miranda~~: corregida en el corte del 9 nov (L–V 06:00–12:00, 30 h).
3. Confirmar el ajuste para jornada **nocturna** y la duda de mixta y nocturna a 40 hrs con el abogado.
4. Juntas: gerentes de Easy Fit (propuesta por sucursal), Vivo (después del 9 nov, cuando regrese Isma) y Center (Antonio y líderes) la siguiente semana. Center será piloto del reloj checador (~15 días) y después habrá capacitación con Vivo (200+ colaboradores).
5. Calendario de jornada de 44 hrs: presentarlo y agendarlo con Operaciones en junio de 2027.
6. ~~Que el tablero lea el avance del documento vivo~~: resuelto con la página única (8 nov 2026).
7. Hallazgo: 13 mixtas tienen entre 45 y 46 hrs. No entran en el corte de 2027 (>46), pero ya pasan del máximo legal de la mixta (45). Por decidir si se ajustan también.
