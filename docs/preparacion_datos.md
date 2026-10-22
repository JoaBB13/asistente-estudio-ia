# Preparación de los datos

## Corpus inicial

Se trabaja con 11 PDF de contenido de la asignatura.
La primera extracción con pypdf registró 742 páginas.

Los archivos originales se conservan en data/raw/.
Los resultados se generan en data/processed/.
Ambas carpetas están excluidas del control de versiones.

## Comparación de extractores

Se compararon pypdf y PyMuPDF sobre estas páginas:

- Fundamentos IA_ML: página 31.
- Procesamiento y nuevas features: página 49.
- Regresión: página 27.

Con PyMuPDF y sort=True, la página 49 intercalaba contenido de dos
columnas al interpretarlo como texto continuo.

En las tres muestras, PyMuPDF con sort=False conservó un orden de
lectura coherente. La extracción posterior por bloques también
conservó ese orden.

Se adopta inicialmente PyMuPDF con extracción por bloques de texto
en orden original, sin ordenamiento por coordenadas.

La revisión de tres páginas no garantiza que todo el corpus tenga
un orden correcto. Se ampliará la revisión durante el análisis
exploratorio y se registrarán los problemas detectados.

## Unidad de información

Cada registro corresponde a una diapositiva completa.

Se conserva:
- Identificador de página.
- Documento y número de página.
- Huella SHA-256 del PDF.
- Texto original extraído.
- Texto limpio.
- Cantidad de palabras.
- Indicador de ausencia de texto limpio.
- Versión y configuración del extractor.
- Versión de la limpieza.

El número de página corresponde a su posición en el PDF, empezando en 1.

Los bloques se utilizan para preservar separaciones internas.
No se convierten en fragmentos independientes.

## Limpieza aplicada

- Eliminación del pie conocido con el correo del docente.
- Sustitución de ligaduras tipográficas, como ﬁ por fi.
- Normalización de espacios y saltos de línea.
- Conservación de mayúsculas, tildes, viñetas y símbolos.

No se eliminan automáticamente páginas cortas ni páginas sin texto.

La normalización específica de TF-IDF se aplicará por separado.

## Limitaciones observadas

En la página 27 de Regresión se recupera el título
"Fórmula Matemática", pero no la fórmula del MAE.

No se ha determinado todavía si la fórmula está representada como
imagen, trazados u otro contenido no recuperado por los extractores.

No se aplica OCR ni se completan fórmulas automáticamente.

## Reproducción en Ubuntu

Desde la carpeta principal del repositorio:

1. Crear el entorno si todavía no existe:
   python3 -m venv .venv

2. Activarlo:
   source .venv/bin/activate

3. Instalar dependencias:
   python -m pip install -r requirements.txt

4. Crear las carpetas locales:
   mkdir -p data/raw data/processed

5. Copiar en data/raw los 11 PDF originales acordados por el equipo.

6. Ejecutar la preparación:
   python src/preparar_paginas.py

Resultado principal:
data/processed/paginas_limpias.jsonl

Para reproducir las extracciones comparadas:
- python src/ingesta.py
- python src/ingesta_pymupdf.py

Los PDF deben compartirse por el canal acordado por el equipo;
no se descargan al clonar el repositorio.

## Análisis exploratorio inicial

El corpus limpio contiene:
- 11 documentos.
- 742 páginas.
- 41.673 palabras extraídas.
- Mediana de 52 palabras por página.
- Promedio de 56,16 palabras por página.
- 172 páginas con menos de 20 palabras, incluidas 3 sin texto limpio.
- 26 grupos de textos coincidentes después de unificar espacios.

La coincidencia textual no implica que las imágenes sean iguales.
Por ahora no se eliminan automáticamente duplicados.

## Revisión de las páginas sin texto

Según la revisión visual realizada por Joaquín:

- Fundamentos IA_ML, página 63: cuadros con títulos, imágenes y
  explicaciones no recuperadas por la extracción textual.
- Fundamentos IA_ML, página 99: esquema comparativo con logos y
  palabras no recuperadas por la extracción textual.
- Agentes y Búsqueda, página 28: cruz roja sin contenido de estudio legible.

Las dos primeras se registran como contenido visual no recuperado.
No se aplica OCR en esta versión.

## Selección inicial para búsqueda

Se conservan las 742 páginas en paginas_limpias.jsonl.

El archivo corpus_busqueda.jsonl contiene 697 registros:
- 570 páginas con 20 palabras o más.
- 127 páginas breves conservadas y pendientes de revisión.

Se excluyen del índice 45 páginas:
- 11 portadas identificadas.
- 31 separadores o cierres identificados por texto exacto.
- 2 páginas con contenido visual no recuperado.
- 1 página sin contenido de estudio legible.

Cada decisión queda registrada en decisiones_paginas.jsonl.
Estas reglas no constituyen una revisión visual completa del corpus.

## Ejecución del análisis y la selección

Desde la raíz del proyecto, con el entorno virtual activo:

    python src/preparar_paginas.py
    python src/analizar_corpus.py
    python src/crear_corpus_busqueda.py

Los resultados se generan dentro de data/processed/.

## Formato compartido para recuperación

Archivo: data/processed/corpus_busqueda.jsonl

Cada línea representa un objeto JSON con:
- id_fragmento: identificador estable basado en la huella del PDF y página.
- documento: nombre del PDF.
- pagina: posición en el PDF, empezando en 1.
- sha256: huella del documento original.
- texto: contenido limpio de la diapositiva.
- revision_visual_pendiente: señal de revisión definida por las reglas.

TF-IDF y la recuperación por embeddings deben utilizar el mismo corpus.
El texto original de este archivo no debe reemplazarse por la versión
normalizada para TF-IDF.
