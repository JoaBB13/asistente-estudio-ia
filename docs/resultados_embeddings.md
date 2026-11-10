# Evaluación inicial del recuperador por embeddings

## Configuración

- Conjunto: desarrollo.
- Corpus: 697 fragmentos.
- Preguntas: 40; 33 respondibles y 7 no respondibles.
- Modelo: intfloat/multilingual-e5-small.
- Revisión: 614241f622f53c4eeff9890bdc4f31cfecc418b3.
- k: 3.
- Dispositivo: CPU.
- Embeddings normalizados y similitud coseno.
- Se detectó un fragmento de 543 tokens, truncado al límite de 512.

SHA-256 del corpus:
50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0

## Resultados

| Medida | Aciertos / total | Porcentaje |
|---|---|---|
| Hit@3 total | 31/33 | 93,94 % |
| Hit@3 base | 25/26 | 96,15 % |
| Hit@3 reformulaciones | 6/7 | 85,71 % |
| Cobertura completa@3 total | 3/3 | 100 % |
| Cobertura completa@3 base | 2/2 | 100 % |
| Cobertura completa@3 reformulaciones | 1/1 | 100 % |
| Listas vacías en no respondibles | 0/7 | 0 % |

Hit@3 indica que se recuperó al menos una evidencia anotada entre
los tres primeros resultados. No mide la calidad de respuestas generadas.

La cobertura completa se calcula únicamente sobre los tres casos
con grupos de evidencias requeridos.

Las reformulaciones no representan temas independientes de sus preguntas base.

## Casos pendientes de revisión

- DEV-010: definición de aprendizaje automático.
- DEV-014: reformulación sobre el error absoluto medio.

Ambos fallaron según las referencias anotadas.
Está pendiente comparar las evidencias esperadas con los textos recuperados.
No se modificaron las referencias ni los parámetros a partir de estos fallos.

## Preguntas no respondibles

Las siete consultas no respondibles devolvieron resultados.
El recuperador todavía no implementa un criterio de abstención.
Los puntajes de similitud no son probabilidades de respuesta correcta.

## Evidencia de ejecución

Informe local:
data/evaluacion/resultados_embeddings_20261110T062506980553Z.json

El informe contiene el detalle por pregunta, la huella del archivo de
preguntas, la configuración, versiones y truncamientos.
Permanece fuera de Git junto con los datos.

Esta medición corresponde a desarrollo. No se utilizó el conjunto final.
Todavía no se establece una comparación de rendimiento con TF-IDF.