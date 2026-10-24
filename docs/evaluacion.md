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

Se prepararon cinco preguntas de desarrollo respondibles.

Para cada pregunta se contrastó el contenido de la diapositiva con el
texto disponible en el corpus y se registró al menos una evidencia.

Estas preguntas constituyen una primera tanda de prueba. Todavía no
permiten afirmar que el asistente tenga una calidad determinada.

No se han medido resultados de recuperación ni de generación.

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

El conjunto final previsto tendrá 20 preguntas y se reservará para la
evaluación del sistema una vez fijada su configuración.

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