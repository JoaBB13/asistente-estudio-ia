# Recuperador TF-IDF: configuración inicial y resultados

## Objetivo

Implementar una línea de base de recuperación léxica que permita
encontrar diapositivas relacionadas con una consulta y comparar
sus resultados con el recuperador por embeddings.

Esta evaluación mide recuperación de evidencias, no calidad de
respuestas generadas.

## Implementación

- Recuperador: src/recuperador_tfidf.py.
- Evaluador: src/evaluar_tfidf.py.
- Interfaz: buscar(pregunta, k).
- Python: 3.12.3.
- scikit-learn: 1.9.1.

El vectorizador se ajusta exclusivamente sobre los textos del corpus.
Las preguntas se transforman con el vectorizador ya ajustado,
sin modificar su vocabulario ni sus pesos IDF.

## Configuración inicial

- Minúsculas: lowercase=True.
- Eliminación de acentos: strip_accents="unicode".
- Palabras individuales: ngram_range=(1, 1).
- Normalización de vectores: norm="l2".
- Sin eliminación explícita de stopwords.
- Tokenización predeterminada: términos de al menos dos caracteres.
- Ponderación IDF activada y suavizada.
- Frecuencia de términos sin transformación logarítmica.
- Ordenamiento mediante similitud coseno.
- Desempate por id_fragmento en orden ascendente.
- Se excluyen resultados con puntaje cero.
- Cantidad máxima de resultados evaluados: k=3.

Los textos originales, identificadores, documentos y páginas
se conservan en los resultados. Los puntajes son similitudes,
no probabilidades de respuesta correcta.

## Datos utilizados

- Corpus: 697 fragmentos, correspondientes a diapositivas individuales.
- Vocabulario: 5440 términos.
- Matriz TF-IDF: 697 filas y 5440 columnas.
- Conjunto de desarrollo: 40 consultas.
- Respondibles: 33, compuestas por 26 preguntas base y 7 reformulaciones.
- No respondibles: 7.
- Consultas con grupos de evidencias requeridos: 3.

SHA-256 del corpus:

50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0

SHA-256 de las preguntas:

20d3877ad0206939f79cbbd7123f189f880655c0fb030b1c652a458c0022c1da

## Protocolo

Se ejecutó la validación estructural y de referencias antes
de evaluar. El evaluador también comprueba la partición de
desarrollo y la huella del corpus registrada en cada caso.

Hit@3 cuenta un acierto cuando al menos uno de los primeros
tres resultados coincide con una evidencia válida de la pregunta.

La cobertura completa@3 exige recuperar al menos un fragmento
de cada grupo requerido, dentro de esos mismos tres resultados.

Las preguntas no respondibles se excluyen del denominador de Hit@3.
El conjunto final no se utilizó en esta evaluación.

## Resultados iniciales

| Medida | Aciertos / casos | Porcentaje |
| --- | --- | --- |
| Hit@3 total | 25/33 | 75,76 % |
| Hit@3 preguntas base | 21/26 | 80,77 % |
| Hit@3 reformulaciones | 4/7 | 57,14 % |
| Cobertura completa@3 total | 2/3 | 66,67 % |
| Cobertura completa@3 base | 1/2 | 50,00 % |
| Cobertura completa@3 reformulaciones | 1/1 | 100,00 % |
| Listas vacías en casos no respondibles | 0/7 | 0,00 % |

Las reformulaciones están vinculadas con preguntas base;
no representan temas independientes.

## Observaciones

Los casos sin acierto según las referencias actuales fueron:
DEV-001, DEV-005, DEV-010, DEV-014, DEV-017, DEV-028,
DEV-032 y DEV-033.

En DEV-001 se recuperaron títulos relacionados con aprendizaje
supervisado y no supervisado, pero no la evidencia de referencia.
Esto muestra una limitación de la coincidencia de palabras
para distinguir conceptos y recuperar explicaciones suficientes.

En DEV-008 se recuperó la evidencia de chi-cuadrado, pero no
la página requerida de ANOVA. Por eso cuenta como acierto
en Hit@3 y como cobertura incompleta.

DEV-023 y DEV-034 alcanzaron cobertura completa.

El menor Hit@3 de las reformulaciones sugiere sensibilidad
a la redacción de las consultas. El grupo contiene solo siete
casos, por lo que no permite una conclusión general.

Las siete preguntas no respondibles devolvieron resultados.
El recuperador aún no implementa una decisión de abstención.
Encontrar fragmentos relacionados no demuestra que contengan
el dato solicitado.

## Limitaciones y próximos pasos

- Revisar los fallos y la suficiencia de las páginas recuperadas.
- Si se identifica una evidencia alternativa válida, acordar su
  incorporación para ambos recuperadores y repetir la comparación.
- Conservar estos resultados como referencia de la configuración inicial.
- Probar ajustes únicamente con el conjunto de desarrollo.
- Comparar ambos recuperadores utilizando el mismo corpus,
  las mismas referencias y el mismo k.
- Evaluar generación y abstención por separado.
- Reservar el conjunto final hasta fijar la configuración.

## Cómo reproducir

Desde la raíz del proyecto, con el entorno virtual activo:

    python src/validar_evaluacion.py
    python src/evaluar_tfidf.py

Los datos deben obtenerse por el canal compartido del equipo,
ya que la carpeta data está excluida de Git.
