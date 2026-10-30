# Conjunto de evaluación final

## Estado y composición

El conjunto final está preparado y pasó la validación estructural
y de referencias. Todavía no se ejecutaron los recuperadores ni
la generación de respuestas sobre estas preguntas.

| Tipo de caso | Cantidad |
|---|---:|
| Respondibles | 16 |
| No respondibles | 4 |
| Total | 20 |

Un caso respondible requiere recuperar dos grupos de evidencias
para cubrir la respuesta completa.

El conjunto de desarrollo se mantiene separado y contiene
40 consultas: 33 respondibles y 7 no respondibles.
Las respondibles incluyen 26 preguntas base y 7 reformulaciones.

## Archivos locales

- `data/evaluacion/preguntas_final.jsonl`
- `data/evaluacion/revision_no_respondibles.txt`

Estos archivos están excluidos de Git por encontrarse dentro
de `/data`. Se conservan mediante respaldo externo.

## Corpus asociado

El corpus contiene 697 fragmentos.

SHA-256 del corpus:

`50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0`

## Revisión de los casos

Las preguntas respondibles se contrastaron con las diapositivas
y con el texto disponible en el corpus.

Para los casos no respondibles se realizó una revisión manual
de páginas localizadas mediante palabras clave. No se encontró
información suficiente para responder las preguntas concretas.

Esta revisión no constituye una comprobación exhaustiva de todo
el contenido visual de los PDFs. Las limitaciones y los motivos
de cada clasificación se registran en los casos y en el informe
de revisión.

La validación automática comprueba estructura, identificadores,
referencias y correspondencia con la huella del corpus.
No sustituye la revisión conceptual humana.

## Reserva del conjunto final

Los ajustes de recuperación, prompts y umbrales se realizan
con el conjunto de desarrollo.

Antes de ejecutar la evaluación final se registrarán las versiones
del código, modelos, dependencias y configuración utilizada.

El conjunto final no se utiliza para elegir esos ajustes.
Si se modifica el sistema a partir de sus resultados, deberá
declararse que ese conjunto ya fue utilizado y que una nueva
ejecución no representa una evaluación independiente.

Las correcciones justificadas de preguntas o evidencias se
documentarán, conservando la versión anterior y registrando
una nueva huella del archivo.

## Presentación de resultados

Se informarán cantidades absolutas y porcentajes, indicando
el denominador de cada métrica:

- Recuperación sobre las 16 preguntas respondibles.
- Cobertura completa de evidencias en el caso que requiere
  dos grupos, además del acierto de recuperación de alguna evidencia.
- Abstención correcta sobre los 4 casos no respondibles.
- Abstenciones incorrectas sobre los casos respondibles.
- Calidad y respaldo documental de las respuestas generadas.

Un caso representa 5 puntos porcentuales sobre el total de 20,
6,25 puntos sobre las 16 respondibles y 25 puntos sobre las
4 no respondibles.

Por el tamaño reducido y la selección manual del conjunto,
los resultados se interpretarán como una evaluación acotada
del proyecto.

## Identificación de la versión del conjunto final

SHA-256 de `data/evaluacion/preguntas_final.jsonl`:

`11676e3f0260abeca574da32a7386558ca8a6a37eb035992a8a83776efb2face`

Esta huella identifica la versión de 20 preguntas preparada antes
de ejecutar la evaluación final. Permite comprobar que se utiliza
el mismo archivo en las distintas ejecuciones y equipos.