# Evaluación del asistente de estudio

## Objetivo

Evaluar por separado:

1. La recuperación de diapositivas relevantes.
2. La calidad de las respuestas generadas.
3. La correspondencia entre las respuestas y las fuentes citadas.
4. La capacidad de abstenerse cuando el corpus no permite responder.

La comparación entre el buscador léxico y el buscador semántico utilizará
el mismo corpus, las mismas preguntas y la misma cantidad de resultados.

## Estado actual

Se completaron las 40 consultas de desarrollo propuestas:
33 respondibles y 7 no respondibles con el corpus actual.

Las respondibles comprenden 26 preguntas base y 7 reformulaciones.
Las preguntas base tienen evidencias contrastadas con las diapositivas
y el corpus; las reformulaciones utilizan evidencias ya verificadas.

Para los casos no respondibles se realizaron revisiones dirigidas
de términos, del alcance de los documentos y, cuando correspondía,
del contenido visual. Se registraron las limitaciones de esas revisiones;
no constituyen una inspección exhaustiva de todas las imágenes del corpus.

Los casos pasaron la validación estructural y de referencias.
Esto no sustituye la revisión conceptual humana.

Completar el conjunto de desarrollo no demuestra una calidad determinada
del asistente. Todavía no se midieron resultados de recuperación
ni de generación.

## Ubicación de los datos

- Corpus: `data/processed/corpus_busqueda.jsonl`.
- Preguntas de desarrollo: `data/evaluacion/preguntas_desarrollo.jsonl`.

Los archivos dentro de `/data` están excluidos del control de versiones.

Por ese motivo, clonar el repositorio no descarga el corpus ni las
preguntas. Los integrantes deben compartir estos archivos por un medio
acordado y colocarlos en las rutas indicadas.

Se debe conservar una copia compartida de las preguntas revisadas:
su contenido no se regenera automáticamente a partir de los PDF.

## Formato de los casos

Cada línea del archivo JSONL contiene un caso con estos campos:

| Campo | Descripción |
|---|---|
| `id` | Identificador único de la pregunta. |
| `particion` | Conjunto al que pertenece: desarrollo o final. |
| `pregunta` | Consulta que recibe el asistente. |
| `respondible` | Indica si el corpus permite responder. |
| `respuesta_referencia` | Contenido esperado de una respuesta correcta. |
| `criterios_respuesta` | Conceptos que se revisarán al evaluar la respuesta. |
| `evidencias` | Fragmentos que respaldan la respuesta. |
| `observaciones` | Limitaciones o aclaraciones del caso. |
| `corpus_sha256` | Huella del corpus utilizado para verificar el caso. |

Cada evidencia contiene `id_fragmento`, `documento` y `pagina`.

Los números de página corresponden a la posición dentro del archivo PDF,
contando desde 1.

La respuesta de referencia no exige una coincidencia textual exacta:
se evalúa si la respuesta expresa los conceptos correctos.

## Casos iniciales de desarrollo

| ID | Tema | Evidencia inicial |
|---|---|---|
| DEV-001 | Aprendizaje supervisado | Fundamentos IA/ML, página 31 |
| DEV-002 | Error absoluto medio | Regresión, página 27 |
| DEV-003 | Análisis exploratorio de texto | Procesamiento y nuevas features, página 49 |
| DEV-004 | Alineación de valores | Agentes y Búsqueda, página 11 |
| DEV-005 | Ventajas de la búsqueda local | Problemas de optimización, página 7 |
| DEV-006 | Rol del análisis de datos en IA | Introducción al análisis de datos, página 12 |
| DEV-007 | Variabilidad de los datos | EDA, página 13 |
| DEV-008 | Chi-cuadrado frente a ANOVA | Causas e identificación de faltantes, páginas 20 y 25 |
| DEV-009 | Imputación frente a transformación de outliers | Procesamiento y limpieza de datos, página 24 |
| DEV-010 | Definición de aprendizaje automático | Aprendizaje automático, página 9 |

Las evidencias iniciales no se consideran necesariamente exhaustivas.
Si otra diapositiva también permite responder, debe revisarse e
incorporarse como evidencia válida para ambos recuperadores.

Compartir un tema o contener las mismas palabras no basta para
considerar relevante una página: debe aportar información para responder.

## Evaluación de recuperación

La medida inicial será Hit@3, aplicada a preguntas respondibles.

Una pregunta cuenta como acierto cuando al menos uno de los tres primeros
fragmentos recuperados pertenece a sus evidencias válidas.

Hit@3 = preguntas con acierto / preguntas respondibles evaluadas.

Se informarán siempre:

- Cantidad de preguntas respondibles evaluadas.
- Cantidad de aciertos.
- Porcentaje de aciertos.

Si el buscador devuelve menos de tres resultados, se evalúan los que
devuelva. Una lista vacía cuenta como fallo para una pregunta respondible.

Los puntajes internos de TF-IDF y embeddings no se compararán
directamente, porque no tienen necesariamente la misma escala.

## Revisión de respuestas

Para cada pregunta respondible se registrará:

- Qué criterios de respuesta se cumplen.
- Si aparecen errores o afirmaciones no respaldadas por el corpus.
- Si las citas corresponden a fragmentos que respaldan la respuesta.

Una respuesta puede estar bien redactada y aun así ser incorrecta
o no estar respaldada por sus citas.

Estos aspectos se registrarán por separado. Todavía no se define
una nota global que los combine.

Las reglas de corrección y los ejemplos de calibración se detallan
en [Criterios de revisión manual](criterios_respuestas.md).

## Preguntas sin respuesta en el corpus

Se incorporarán casos no respondibles para evaluar la abstención.

Antes de clasificar una pregunta como no respondible se revisará el
corpus; no alcanza con que un buscador falle al encontrar la respuesta.

Estos casos no forman parte del denominador de Hit@3 para preguntas
respondibles. Su evaluación se informará por separado, con cantidades
absolutas y porcentajes.

## Separación entre desarrollo y evaluación final

Las preguntas de desarrollo pueden utilizarse para detectar errores
y ajustar el sistema.

El conjunto final preparado contiene 20 preguntas: 16 respondibles
y 4 no respondibles. Se reserva para evaluar el sistema una vez
fijada su configuración. Su versión y protocolo se documentan
en `docs/conjunto_final.md`.

Las preguntas equivalentes o las paráfrasis de una misma pregunta
deben permanecer en la misma partición para evitar que la evaluación
final repita casos utilizados durante el ajuste.

Los porcentajes deben indicar su denominador. Un caso equivale a
5 puntos porcentuales únicamente en una medida calculada sobre
las 20 preguntas completas.

## Control de versiones del corpus

Antes de evaluar se comprobará que la huella SHA-256 del corpus coincida
con la registrada en los casos.

Si cambia el corpus, se revisarán las evidencias y se actualizarán
los índices de ambos buscadores antes de volver a comparar.

No se mezclarán resultados obtenidos con diferentes versiones del corpus
como si pertenecieran a una misma evaluación.

## Preguntas que requieren varias evidencias

Tres consultas de desarrollo contienen grupos de evidencias requeridos:

- DEV-008: chi-cuadrado y ANOVA, con evidencias en las páginas 20 y 25
  de 04 - EDA - Causas e Identificacion de faltantes.pdf.
- DEV-023: MCAR y MAR, con evidencias en las páginas 53 y 54
  del mismo documento.
- DEV-034: reformulación de DEV-023, con los mismos grupos de evidencias.

Son dos preguntas base y una reformulación, no tres temas independientes.

El campo opcional `grupos_evidencia_requeridos` contiene un grupo
por cada parte necesaria de la respuesta. Cada grupo puede contener
fragmentos alternativos que respalden esa misma parte.

Actualmente, las tres consultas tienen dos grupos y un fragmento
por grupo.

Hit@3 mantiene su definición: basta con recuperar una evidencia válida
entre los tres primeros resultados.

Además, para los casos que tengan este campo, se registrará si existe
cobertura completa entre los tres primeros resultados: debe recuperarse
al menos un fragmento de cada grupo requerido.

Recuperar solo una de las dos páginas necesarias cuenta como acierto
en Hit@3, pero no como cobertura completa.

Esta comprobación adicional se informará por separado, indicando cuántos
casos requieren varias evidencias y cuántos alcanzan cobertura completa.
También se distinguirán los casos base de las reformulaciones.

## Casos de abstención en desarrollo

Se prepararon siete consultas no respondibles:

- DEV-011: fecha y horario del examen final.
- DEV-012: supuesto resultado de MAE de nuestro asistente.
- DEV-036: coeficiente de Spearman entre horas de estudio y notas
  del parcial de nuestro curso.
- DEV-037: tiempo de ejecución de la discretización del pico
  de los pingüinos en la computadora utilizada en clase.
- DEV-038: valor de k utilizado en una ejecución de búsqueda
  local beam realizada en clase.
- DEV-039: marca y modelo de cámara utilizados para obtener
  las imágenes de la clase de Computer Vision.
- DEV-040: contraseña de la red Wi-Fi del aula.

Todos tienen `respondible: false` y `evidencias: []`.
La lista vacía indica que no se identificaron fragmentos que respalden
una respuesta al dato solicitado.

Se considera abstención correcta cuando el asistente reconoce la falta
de información y no inventa el dato ni atribuye al proyecto o al curso
resultados de otros ejemplos.

La clasificación se apoya en las revisiones documentadas de cada caso.
Las búsquedas de términos por sí solas no demuestran ausencia de
información en todas las imágenes de los PDF.

Durante la preparación de DEV-037 se descartó una pregunta sobre
la cantidad de intervalos de discretización: los gráficos sí permitían
obtener esa información. Se reemplazó por una consulta sobre un tiempo
de ejecución que no se encontró en el material revisado.


## Validación automática de los archivos

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python src/validar_evaluacion.py
```

El programa comprueba:

- Formato JSONL y campos obligatorios.
- Tipos de datos e identificadores únicos.
- Coincidencia de la huella SHA-256 del corpus.
- Existencia de los fragmentos citados.
- Correspondencia entre identificador, documento y página.
- Evidencias obligatorias en preguntas respondibles.
- Ausencia de evidencias en preguntas no respondibles.
- Consistencia de los grupos de evidencias requeridos.

No modifica archivos. Finaliza con código 0 si la validación es correcta
y con código 1 si encuentra un error, mostrando el primer problema.

Se pueden indicar otros archivos mediante argumentos:

```bash
python src/validar_evaluacion.py \
  --corpus data/processed/corpus_busqueda.jsonl \
  --preguntas data/evaluacion/preguntas_desarrollo.jsonl \
  --particion desarrollo
```

### Comprobaciones realizadas

- Validación inicial correcta del corpus de 697 fragmentos y
  de 12 consultas: 10 respondibles y 2 no respondibles.
- Detección de una página incorrecta introducida deliberadamente
  en una copia en memoria de DEV-001.
- Detección de un caso de origen inexistente introducido deliberadamente
  en una reformulación en memoria.
- Validación posterior correcta de las 40 consultas de desarrollo:
  33 respondibles y 7 no respondibles.
- Comprobación correcta de los vínculos de las 7 reformulaciones.
- Identificación de 3 consultas con grupos de evidencias requeridos.
- Validación estructural y de referencias de las 20 preguntas finales.

Estas comprobaciones no sustituyen la revisión conceptual de las
preguntas, las respuestas de referencia ni la suficiencia de las evidencias.
Tampoco representan resultados de evaluación del asistente.

## Reformulaciones de preguntas

El campo opcional `caso_origen` vincula una reformulación con su caso base:

| Reformulación | Caso base | Tema |
| --- | --- | --- |
| DEV-014 | DEV-002 | Error absoluto medio |
| DEV-015 | DEV-004 | Alineación de valores |
| DEV-031 | DEV-005 | Ventajas de la búsqueda local |
| DEV-032 | DEV-007 | Variabilidad |
| DEV-033 | DEV-019 | Discretización |
| DEV-034 | DEV-023 | MCAR y MAR |
| DEV-035 | DEV-025 | Sensores y actuadores |

Cada variante debe apuntar directamente a un caso base existente,
mantener su partición, su condición de respondible y la versión del corpus.

El validador comprueba estos vínculos. La equivalencia de significado
y la suficiencia de las evidencias requieren revisión humana.

Los resultados se informarán por separado:

- Hit@3 sobre las 26 preguntas base respondibles.
- Hit@3 sobre las 7 reformulaciones respondibles.
- Abstención sobre los 7 casos no respondibles.

Las variantes están incluidas en las 40 consultas de desarrollo.
No se consideran temas independientes. Una pregunta base y sus
reformulaciones deben permanecer en la misma partición.

DEV-013 incorpora el tema de los bastones de la retina, con evidencia
en la página 6 de EXTRA - Computer Vision I.pdf.