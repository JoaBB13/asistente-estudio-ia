# asistente-estudio-ia

Asistente de estudio basado en documentos de una asignatura. Proyecto final grupal de Inteligencia Artificial.

## Estado del proyecto

La extracción, limpieza, selección del corpus y el análisis exploratorio
inicial están implementados y documentados.

Se dispone de un corpus de 697 fragmentos, 40 consultas de desarrollo
y 20 preguntas finales reservadas. Los archivos de evaluación pasaron
la validación estructural y de referencias. Esta validación no sustituye
la revisión conceptual de las preguntas, respuestas y evidencias.

Se completó la preparación de las 40 consultas de desarrollo propuestas.
La recuperación TF-IDF, la recuperación semántica, la generación
y la consola están pendientes de implementación.

Todavía no se midieron resultados de recuperación ni de generación.

## Integrantes

- Joaquín Bustos
- Franco Heredia
- Fabricio Posada

## Problema

Los estudiantes necesitan localizar y comprender información distribuida
entre varios documentos de una asignatura. La búsqueda manual requiere
revisar archivos y encontrar los contenidos pertinentes.

## Objetivo

Desarrollar un asistente de estudio que responda preguntas en español
utilizando documentos de una asignatura y muestre las fuentes que
respaldan sus respuestas.

## Arquitectura propuesta

Se propone utilizar generación aumentada por recuperación (RAG):

1. Extraer el texto de los PDF.
2. Limpiar el contenido y utilizar cada diapositiva como fragmento.
3. Conservar el documento y la página de cada fragmento.
4. Buscar los fragmentos relacionados con la pregunta.
5. Utilizar un modelo de lenguaje preentrenado para generar una respuesta.
6. Mostrar las fuentes e indicar cuando la evidencia sea insuficiente.

La primera comparación de recuperadores utilizará diapositivas individuales.
Si posteriormente se agrega contexto de páginas vecinas, se conservarán
sus referencias y se distinguirá del contenido recuperado inicialmente.

No se prevé entrenar un modelo de lenguaje desde cero.
Los modelos concretos se seleccionarán tras comprobar los recursos disponibles.

## Datos

El corpus está formado por 11 PDF de contenido de la materia
Inteligencia Artificial: clases 01 a 10 y material extra de Computer Vision.

Se excluyen la presentación administrativa y la consigna del trabajo final.

La preparación registra 742 páginas y 41.673 palabras de texto limpio.
La mediana es de 52 palabras por página.

Se conservan las 742 páginas en los datos de preparación y se seleccionan
697 para el corpus de búsqueda. Las 45 exclusiones quedan documentadas.
Cada fragmento corresponde a una diapositiva completa.

Cada fragmento conserva:

- Identificador.
- Texto.
- Documento de origen.
- Página de origen.
- Huella SHA-256 del documento original.
- Indicador de revisión visual pendiente.

### Calidad y limitaciones

Se realizó una revisión inicial de la extracción, los pies repetidos,
las coincidencias textuales y las páginas sin texto extraíble.
También se contrastaron páginas utilizadas como evidencias de evaluación.

Estas comprobaciones no constituyen una revisión visual exhaustiva
de todas las diapositivas.

El contenido presente únicamente en imágenes, gráficos o fórmulas
no recuperadas como texto puede quedar fuera del MVP.
La ausencia de texto extraído no implica que la diapositiva
carezca de información.

El material representa el enfoque de una asignatura; los resultados no
demostrarán que el asistente funciona igual en cualquier materia.

Los PDF, los datos procesados y los archivos de preguntas de evaluación
se mantienen fuera del control de versiones.
Se documenta cómo obtener y preparar el corpus para reproducir el proyecto.

## Alcance propuesto del MVP

- Material precargado por el equipo.
- Preguntas escritas en español.
- Consultas independientes, sin memoria de conversación.
- Respuestas con referencias al documento y la página.
- Aviso cuando no exista evidencia suficiente.
- Interacción inicial mediante consola.

## Fuera del alcance inicial

- Registro e inicio de sesión.
- Historial permanente de conversaciones.
- Interacción por voz.
- Navegación por internet.
- OCR y comprensión de imágenes.
- Generación de exámenes.
- Planificación personalizada.
- Interfaz web compleja.

## Baseline

Se implementará un recuperador léxico mediante TF-IDF y similitud coseno,
como punto de comparación para la recuperación semántica por embeddings.

La representación léxica aplicará minúsculas y eliminación de tildes.
El vectorizador se ajustará únicamente sobre el corpus de documentos;
las consultas se transformarán sin volver a ajustarlo.

Esta normalización no modificará el texto original devuelto
en los resultados.

Ambos métodos utilizarán el mismo corpus, las mismas preguntas y
el mismo contrato de resultados, definido en
[Contrato de recuperación](docs/contrato_recuperacion.md).

## Evaluación

Se prepararon 60 consultas:

- 40 para desarrollo y ajuste.
- 20 reservadas para la evaluación final.

Ambos conjuntos incluyen preguntas respondibles y no respondibles.
Las paráfrasis identificadas de una misma pregunta permanecen
en el mismo conjunto.

Cada consulta incluye una respuesta de referencia o una indicación de
que no es respondible, criterios de corrección y las fuentes esperadas
cuando corresponde.

Las preguntas y respuestas de evaluación no se incorporarán al índice.
El conjunto final no se utilizará para ajustar el sistema.

### Composición de los conjuntos

| Conjunto | Total | Respondibles | No respondibles |
| --- | ---: | ---: | ---: |
| Desarrollo | 40 | 33 | 7 |
| Final | 20 | 16 | 4 |

Las 33 consultas respondibles de desarrollo incluyen 26 preguntas base
y 7 reformulaciones. Las reformulaciones forman parte del total de
40 consultas; no son casos adicionales ni independientes de sus originales.

Sus resultados se reportarán por separado de los casos base.

Tres consultas de desarrollo incluyen grupos de evidencias requeridos.
Este conteo incluye reformulaciones y no representa necesariamente
tres casos base independientes.

El protocolo está en [Evaluación](docs/evaluacion.md).
La versión reservada se documenta en
[Conjunto final](docs/conjunto_final.md).
Los criterios de revisión manual están en
[Criterios de respuestas](docs/criterios_respuestas.md).

### Métricas

- Hit@3: proporción de preguntas respondibles con al menos una fuente
  correcta entre los primeros tres resultados recuperados.
- Cobertura de los grupos de evidencias requeridos en las consultas
  que necesitan información de varias fuentes.
- Proporción de respuestas correctas y respaldadas por el material.
- Validez de las citas.
- Abstención correcta ante preguntas no respondibles.
- Rechazo incorrecto de preguntas respondibles.
- Tiempo de respuesta.

Hit@3 no garantiza que se haya recuperado toda la información necesaria
para responder una pregunta que requiere varias fuentes.
Por eso se distinguirá del cumplimiento de los grupos de evidencias.

### Metas iniciales para discutir

- Hit@3 de al menos 80 %.
- Al menos 80 % de respuestas aceptables sobre el total de preguntas
  respondibles, según una rúbrica definida previamente.

Son objetivos propuestos, no resultados obtenidos.
Se informarán cantidades absolutas, porcentajes, denominadores
y las limitaciones e incertidumbre de las mediciones.

## Distribución de tareas propuesta

- Joaquín Bustos: extracción, análisis, limpieza y fragmentación de los datos.
- Franco Heredia: recuperación semántica e integración del modelo generador.
- Fabricio Posada: baseline, evaluación y consola.
- Todos: documentación de su módulo, integración y defensa.

Joaquín también avanzó en la preparación de los conjuntos de preguntas
y en su validación estructural y de referencias como apoyo a la evaluación.

## Organización del repositorio

- `data/raw/`: documentos originales, excluidos de Git.
- `data/processed/`: datos procesados, excluidos de Git.
- `data/evaluacion/`: conjuntos de preguntas, excluidos de Git.
- `notebooks/`: análisis exploratorio.
- `src/`: código fuente.
- `models/`: modelos e índices generados, excluidos de Git.
- `docs/`: documentación complementaria.
- `tests/`: pruebas del código.

## Preparación de los documentos

La extracción por diapositiva y la limpieza inicial están implementadas.

La comparación inicial de extractores utilizó tres páginas de muestra.
Posteriormente se revisaron páginas sin texto limpio y páginas utilizadas
como evidencias para las preguntas de evaluación.

Las instrucciones, decisiones de selección y limitaciones están en
[Preparación de los datos](docs/preparacion_datos.md).

## Puesta en marcha

Para preparar el entorno, obtener los datos compartidos y comprobar
la versión del corpus, consultar
[Puesta en marcha para el equipo](docs/puesta_en_marcha.md).

Clonar el repositorio no descarga los PDF ni los archivos de evaluación.