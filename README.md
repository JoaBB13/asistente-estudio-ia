# asistente-estudio-ia
Asistente de estudio basado en documentos de una asignatura. Proyecto final grupal de Inteligencia Artificial.

## Estado del proyecto

La extracción, limpieza, selección del corpus y el análisis exploratorio
inicial están implementados y documentados.

Se dispone de un corpus de 697 fragmentos, 15 consultas de desarrollo
y 20 preguntas finales reservadas. Los archivos de evaluación pasaron
la validación estructural y de referencias.

Falta ampliar desarrollo hasta las 40 consultas propuestas.
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
2. Limpiar y dividir el contenido en fragmentos.
3. Conservar el documento y la página de cada fragmento.
4. Buscar los fragmentos relacionados con la pregunta.
5. Utilizar un modelo de lenguaje preentrenado para generar una respuesta.
6. Mostrar las fuentes e indicar cuando la evidencia sea insuficiente.

No se prevé entrenar un modelo de lenguaje desde cero.
Los modelos concretos se seleccionarán tras comprobar los recursos disponibles.

## Datos propuestos

El corpus está formado por 11 PDF de contenido de la materia
Inteligencia Artificial: clases 01 a 10 y material extra de Computer Vision.

Se excluyen la presentación administrativa y la consigna del trabajo final.

La preparación registra 742 páginas y 41.673 palabras de texto limpio.
La mediana es de 52 palabras por página.

Se conservan las 742 páginas en los datos de preparación y se seleccionan
697 para el corpus de búsqueda. Las 45 exclusiones quedan documentadas.
Cada fragmento corresponde a una diapositiva completa.

Cada fragmento conservará:
- Identificador.
- Texto.
- Documento de origen.
- Página de origen.

### Calidad y limitaciones

Se revisarán errores de extracción, encabezados repetidos, duplicados
y páginas sin texto extraíble.

El contenido presente únicamente en imágenes puede quedar fuera del MVP.
El material representa el enfoque de una asignatura; los resultados no
demostrarán que el asistente funciona igual en cualquier materia.

Los PDF y los datos procesados se mantendrán fuera del control de versiones.
Se documentará cómo obtener y preparar el corpus para reproducir el proyecto.

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

Ambos métodos utilizarán el mismo corpus, las mismas preguntas y
el mismo contrato de resultados, definido en
[Contrato de recuperación](docs/contrato_recuperacion.md).

## Evaluación propuesta

Se propone preparar 60 preguntas:
- 40 para desarrollo y ajuste.
- 20 reservadas para la evaluación final.

Ambos conjuntos incluirán preguntas respondibles y no respondibles.
Las paráfrasis de una misma pregunta permanecerán en el mismo conjunto.

Cada pregunta tendrá una respuesta de referencia o una indicación de
que no es respondible, junto con las fuentes esperadas cuando corresponda.

Las preguntas y respuestas de evaluación no se incorporarán al índice.
El conjunto final no se utilizará para ajustar el sistema.

Estado de preparación:

- Desarrollo: 15 consultas preparadas de las 40 propuestas;
  13 respondibles y 2 no respondibles. Incluye 2 reformulaciones.
- Final: 20 preguntas preparadas; 16 respondibles y 4 no respondibles.

Las reformulaciones se identifican y sus resultados se reportan
por separado de los casos base.

El protocolo está en [Evaluación](docs/evaluacion.md).
La versión reservada se documenta en
[Conjunto final](docs/conjunto_final.md).
Los criterios de revisión manual están en
[Criterios de respuestas](docs/criterios_respuestas.md).

### Métricas

- Hit@3: proporción de preguntas respondibles con al menos una fuente
  correcta entre los primeros tres resultados recuperados.
- Proporción de respuestas correctas y respaldadas por el material.
- Validez de las citas.
- Abstención correcta ante preguntas no respondibles.
- Rechazo incorrecto de preguntas respondibles.
- Tiempo de respuesta.

### Metas iniciales para discutir

- Hit@3 de al menos 80 %.
- Al menos 80 % de respuestas aceptables sobre el total de preguntas
  respondibles, según una rúbrica definida previamente.

Son objetivos propuestos, no resultados obtenidos.
Se informarán cantidades absolutas y la incertidumbre de las mediciones.

## Distribución de tareas propuesta

- Joaquín Bustos: extracción, análisis, limpieza y fragmentación de los datos.
- Franco Heredia: recuperación semántica e integración del modelo generador.
- Fabricio Posada: baseline, evaluación y consola.
- Todos: documentación de su módulo, integración y defensa.

## Organización del repositorio

- data/raw/: documentos originales, excluidos de Git.
- data/processed/: datos procesados, excluidos de Git.
- notebooks/: análisis exploratorio.
- src/: código fuente.
- models/: modelos e índices generados, excluidos de Git.
- docs/: documentación complementaria.
- tests/: pruebas del código.

## Preparación de los documentos

La extracción por diapositiva y la limpieza inicial están implementadas.
Se revisaron tres páginas de muestra; la revisión del corpus completo
continúa durante el análisis exploratorio.

Las instrucciones y limitaciones están en
[Preparación de los datos](docs/preparacion_datos.md).

## Puesta en marcha

Para preparar el entorno, obtener los datos compartidos y comprobar
la versión del corpus, consultar
[Puesta en marcha para el equipo](docs/puesta_en_marcha.md).

Clonar el repositorio no descarga los PDF ni los archivos de evaluación.