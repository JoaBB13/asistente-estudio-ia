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
