# Contrato de los módulos de recuperación

## Objetivo

El baseline TF-IDF y el recuperador por embeddings deben recibir
las mismas entradas y devolver resultados con la misma estructura.

## Corpus

Archivo de entrada:

data/processed/corpus_busqueda.jsonl

Cada registro representa una diapositiva e incluye:
- id_fragmento
- documento
- pagina
- sha256
- texto
- revision_visual_pendiente

Ambos recuperadores utilizarán exactamente la misma versión del corpus.
Se registrará la huella SHA-256 del archivo utilizado en cada evaluación.

## Consulta

La operación de búsqueda recibirá:
- pregunta: texto de la consulta.
- k: cantidad máxima de resultados solicitados.

Ejemplo de uso previsto:

resultados = recuperador.buscar("¿Qué es el aprendizaje supervisado?", k=3)

Esta interfaz es un acuerdo de implementación; todavía no está implementada.

## Resultados

La búsqueda devolverá una lista ordenada de mayor a menor relevancia.

Cada resultado tendrá esta estructura:

```json
{
  "id_fragmento": "identificador existente en el corpus",
  "documento": "nombre del PDF",
  "pagina": 31,
  "texto": "Texto limpio de la diapositiva",
  "puntaje": 0.72
}
```

El valor 0.72 es ilustrativo: no corresponde a una medición.

Reglas:
- No inventar ni cambiar identificadores.
- No devolver el mismo id_fragmento dos veces.
- Conservar documento y página de origen.
- Devolver como máximo k resultados.
- El puntaje es una medida de similitud, no una probabilidad de acierto.
- Los puntajes de TF-IDF y embeddings no se comparan directamente.
- En caso de empate, ordenar por id_fragmento para mantener estabilidad.

## Validaciones

- Una pregunta vacía o compuesta solo por espacios produce ValueError.
- Un k que no sea un entero positivo produce ValueError.
- Un corpus vacío produce un error claro al inicializar el recuperador.
- Una consulta sin términos presentes en el vocabulario de TF-IDF
  devuelve una lista vacía.

## Baseline TF-IDF

- Aplicar minúsculas y eliminación de tildes en la representación
  utilizada para buscar.
- Aplicar el mismo preprocesamiento a documentos y preguntas.
- Ajustar el vectorizador sobre el corpus de documentos.
- Transformar las consultas con ese vectorizador, sin volver a ajustarlo.
- Usar similitud coseno para ordenar resultados.
- No modificar el texto original devuelto en los resultados.

## Recuperación por embeddings

- Utilizar un modelo compatible con consultas y documentos en español.
- Registrar nombre, revisión y configuración del modelo.
- Respetar las instrucciones específicas del modelo para representar
  consultas y documentos.
- Comprobar el límite de tokens y registrar cualquier truncamiento.
- No aplicar automáticamente la normalización propia de TF-IDF.

## Evaluación

- Usar las mismas preguntas y referencias esperadas para ambos métodos.
- Medir inicialmente Hit@3 sobre las preguntas respondibles.
- Informar aciertos, total evaluado y porcentaje.
- No usar preguntas del conjunto final para elegir parámetros.

## Contexto de páginas vecinas

La primera comparación evaluará diapositivas individuales.

Si después se agregan páginas vecinas para generar respuestas,
se conservarán las referencias de cada página y se distinguirá
entre resultados recuperados y contexto añadido.
