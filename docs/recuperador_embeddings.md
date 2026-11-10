# Recuperador por embeddings

Responsable: Franco Heredia.

## Objetivo

Recuperar diapositivas relacionadas con una pregunta en español
mediante búsqueda semántica, respetando el contrato de recuperación.

El módulo recupera fragmentos del material. No genera respuestas.

## Implementación

Archivo: `src/recuperador_embeddings.py`.

Interfaz:

```python
recuperador = RecuperadorEmbeddings()
resultados = recuperador.buscar(pregunta, k=3)
```

Cada resultado incluye:

- id_fragmento
- documento
- pagina
- texto
- puntaje

Los resultados se ordenan por similitud descendente.
En caso de empate, se ordenan por id_fragmento.
Se conservan el texto y las referencias originales.

## Modelo y configuración

- Modelo: intfloat/multilingual-e5-small.
- Revisión: 614241f622f53c4eeff9890bdc4f31cfecc418b3.
- Dispositivo: CPU.
- Dimensión: 384 componentes.
- Tamaño de lote: 8.
- Embeddings normalizados.
- Comparación mediante similitud coseno.
- Prefijo de preguntas: `query: `.
- Prefijo de documentos: `passage: `.
- Se conservan mayúsculas y tildes.
- Límite configurado: hasta 512 tokens, incluyendo prefijos
  y tokens especiales.

## Datos utilizados

- Corpus: data/processed/corpus_busqueda.jsonl.
- Cantidad de fragmentos: 697.
- SHA-256:
  50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0

Los datos se comparten por separado y permanecen fuera de Git.

## Instalación

Entorno utilizado: Python 3.14.4 en Linux.

Con un entorno virtual activo, instalar primero PyTorch para CPU:

```bash
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-embeddings.txt
python -m pip check
```

Las versiones principales están fijadas en requirements-embeddings.txt.
La compatibilidad con otros entornos debe comprobarse al integrar.

## Ejecución

Desde la raíz del proyecto:

```bash
python src/recuperador_embeddings.py "¿Qué representa el error absoluto medio?" --k 3
```

Se generan los embeddings al crear el recuperador.
Las búsquedas posteriores sobre esa misma instancia reutilizan el índice.
Al iniciar otro proceso, el índice se calcula nuevamente.

## Prueba inicial con el modelo real

Consulta: ¿Qué representa el error absoluto medio?

Resultados obtenidos:

| Posición | Documento | Página | Similitud |
|---|---|---|---|
| 1 | 10 - Regresión.pdf | 27 | 0.9025 |
| 2 | 10 - Regresión.pdf | 31 | 0.8750 |
| 3 | 10 - Regresión.pdf | 28 | 0.8453 |

El primer resultado contiene la definición de MAE.
Esta prueba no constituye una evaluación general del recuperador.

## Truncamientos y trazabilidad

En la ejecución inicial se detectó un fragmento de 543 tokens,
superior al límite de 512. Se truncó su representación para el modelo,
conservando el texto original en los resultados.

Cada ejecución de consola guarda un registro JSON en data/processed/
con la revisión del modelo, huella del corpus, configuración,
versiones y truncamientos detectados.

Si se utiliza la clase desde otro programa, llamar a
guardar_metadatos(ruta) después de las consultas para guardar el registro.

## Pruebas automáticas

```bash
python -m unittest discover -s tests -p "test_recuperador_embeddings.py" -v
```

Resultado: 8 pruebas aprobadas.

Se verifican referencias, orden, desempate, límites, entradas inválidas,
corpus vacío, duplicados, prefijos, reutilización del índice,
registro de truncamientos y metadatos.

Las pruebas utilizan un modelo simulado.
No miden la calidad semántica del modelo real.

## Limitaciones y próximos pasos

- Los puntajes son similitudes, no probabilidades.
- No se comparan directamente con los puntajes de TF-IDF.
- Todavía no se implementó un criterio de abstención:
  el buscador devuelve vecinos incluso si la pregunta no tiene respuesta.
- Falta medir Hit@3 con las preguntas respondibles de desarrollo.
- No utilizar el conjunto final para ajustar parámetros.