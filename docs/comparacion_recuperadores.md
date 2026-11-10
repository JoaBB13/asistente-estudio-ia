# Comparación inicial: TF-IDF y embeddings

## Condiciones

Ambos métodos se evaluaron con:

- El mismo corpus de 697 diapositivas.
- Las mismas 40 preguntas de desarrollo y referencias.
- k = 3.
- 33 consultas respondibles: 26 base y 7 reformulaciones.
- 7 consultas no respondibles.
- 3 consultas con grupos de evidencias requeridos.

SHA-256 del corpus:
50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0

SHA-256 de preguntas:
20d3877ad0206939f79cbbd7123f189f880655c0fb030b1c652a458c0022c1da

Configuraciones y resultados detallados:
- docs/resultados_tfidf.md, en la rama de Fabricio.
- docs/recuperador_embeddings.md.
- docs/resultados_embeddings.md.

## Resultados

| Medida | TF-IDF | Embeddings |
|---|---|---|
| Hit@3 total | 25/33 — 75,76 % | 31/33 — 93,94 % |
| Hit@3 base | 21/26 — 80,77 % | 25/26 — 96,15 % |
| Hit@3 reformulaciones | 4/7 — 57,14 % | 6/7 — 85,71 % |
| Cobertura completa@3 | 2/3 — 66,67 % | 3/3 — 100 % |
| Listas vacías en no respondibles | 0/7 | 0/7 |

Embeddings obtuvo seis aciertos adicionales, equivalentes a
18,18 puntos porcentuales más en Hit@3.

Según los registros, los casos recuperados por embeddings
que fallaron con TF-IDF fueron:
DEV-001, DEV-005, DEV-017, DEV-028, DEV-032 y DEV-033.

No se observaron pérdidas de aciertos de TF-IDF en este conjunto.
Ambos métodos fallaron en DEV-010 y DEV-014 según las referencias vigentes.

En DEV-008, embeddings recuperó todos los grupos requeridos;
TF-IDF recuperó evidencia parcial.

## Interpretación y límites

La comparación mide recuperación de evidencias, no generación
de respuestas ni exactitud de un asistente completo.

Los resultados corresponden a un conjunto pequeño de desarrollo.
Las reformulaciones están vinculadas con preguntas base y
no representan temas independientes.

Ambos métodos devolvieron resultados para las siete consultas
no respondibles. La abstención sigue pendiente.

Los puntajes de similitud de los métodos no se comparan directamente.

No se midieron tiempos de ejecución bajo condiciones controladas.
No se establece una comparación de velocidad.

Las posibles referencias alternativas deben revisarse en equipo.
Si se modifican las referencias, se deben volver a evaluar ambos
métodos con la misma versión del conjunto.

El conjunto final permanece reservado.