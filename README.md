# asistente-estudio-ia
Asistente de estudio basado en documentos de una asignatura. Proyecto final grupal de Inteligencia Artificial.

## Estado del proyecto

Etapa de preparación. Estructura inicial del repositorio creada.

Propuesta inicial acordada por el equipo. El proyecto se encuentra en etapa de preparación; el asistente todavía no está implementado.

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

El corpus inicial estará formado por 11 PDF de contenido de la materia
Inteligencia Artificial: clases 01 a 10 y material extra de Computer Vision.

Se excluyen la presentación administrativa y la consigna del trabajo final.

El volumen de páginas, palabras y fragmentos se medirá durante el análisis.

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

Se implementará una búsqueda por coincidencias de palabras, sin modelos
aprendidos, como punto de comparación para la recuperación semántica.

Ambos métodos se evaluarán con las mismas preguntas.

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
