# Puesta en marcha para el equipo

## Objetivo

Preparar el entorno local y verificar que los integrantes utilizan
el mismo corpus y las mismas preguntas de desarrollo.

Esta guía cubre la preparación de datos. Las dependencias y comandos
de los recuperadores se agregarán cuando estén implementados.

## 1. Obtener el repositorio

Si todavía no está clonado:

```bash
git clone https://github.com/JoaBB13/asistente-estudio-ia.git
cd asistente-estudio-ia
```

Si ya está clonado, entrar en su carpeta. Antes de actualizar,
comprobar que no haya cambios pendientes:

```bash
git status
git switch main
git pull --ff-only origin main
```

No descartar cambios locales para actualizar el repositorio.

## 2. Crear el entorno virtual

El entorno de referencia utiliza Python 3.12.3.

El entorno `.venv` se crea en cada computadora; no se comparte
ni se copia entre integrantes.

### Ubuntu / Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

### Windows con PowerShell

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, se puede utilizar directamente
el intérprete del entorno sin cambiar la política del sistema:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En ese caso, reemplazar `python` por
`.\.venv\Scripts\python.exe` en los comandos siguientes.

## 3. Instalar las dependencias de preparación

Con el entorno activo:

```bash
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
```

La ruta del intérprete debe pertenecer a `.venv`.

Las dependencias actuales son:

- pypdf==6.19.0
- PyMuPDF==1.26.7

Estas dependencias permiten preparar el corpus.
Todavía no incluyen las necesarias para TF-IDF, embeddings
o generación de respuestas.

## 4. Obtener los datos compartidos

Clonar el repositorio no descarga los datos, porque `/data`
está excluido de Git.

Crear las carpetas locales:

```bash
python -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in ('data/raw', 'data/processed', 'data/evaluacion')]"
```

Para comenzar a implementar los recuperadores, solicitar a Joaquín:

- `corpus_busqueda.jsonl`
- `preguntas_desarrollo.jsonl`

Ubicarlos en:

```text
data/processed/corpus_busqueda.jsonl
data/evaluacion/preguntas_desarrollo.jsonl
```

Para reproducir la extracción, solicitar además los 11 PDF originales
y colocarlos en `data/raw/`, conservando sus nombres.

El canal de intercambio se acuerda entre los integrantes.
No subir los datos al repositorio ni forzar su inclusión con Git.

El conjunto final y sus respuestas de referencia permanecen reservados
durante el ajuste del sistema.

## 5. Comprobar la versión del corpus

Ejecutar desde la raíz del proyecto:

```bash
python - <<'PY'
import hashlib
from pathlib import Path

ruta = Path("data/processed/corpus_busqueda.jsonl")
esperada = "50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0"
obtenida = hashlib.sha256(ruta.read_bytes()).hexdigest()

print(f"SHA-256: {obtenida}")

if obtenida != esperada:
    raise SystemExit(
        "El archivo no coincide con la versión acordada. "
        "Revisar con el equipo antes de comparar resultados."
    )

print("Versión del corpus: correcta.")
PY
```

El bloque anterior utiliza la sintaxis de Bash. En Windows,
guardar su contenido Python en un archivo temporal y ejecutarlo
con el intérprete del entorno, o usar esta alternativa de PowerShell:

```powershell
$huellaCorpus = (Get-FileHash data/processed/corpus_busqueda.jsonl -Algorithm SHA256).Hash.ToLower()
$huellaEsperada = "50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0"

if ($huellaCorpus -ne $huellaEsperada) {
    throw "El corpus no coincide con la versión acordada."
}

Write-Output "Versión del corpus: correcta."
```

La huella verifica los bytes del archivo. Una diferencia puede deberse
a cambios de contenido o de serialización; debe investigarse antes
de utilizarlo en una comparación.

## 6. Validar las preguntas de desarrollo

```bash
python src/validar_evaluacion.py
```

Resultado esperado:

- 697 fragmentos del corpus.
- 40 preguntas.
- 33 respondibles.
- 7 no respondibles.
- 3 casos con grupos de evidencias.

Las 33 consultas respondibles incluyen 26 preguntas base y
7 reformulaciones. Las reformulaciones no deben interpretarse
como temas independientes.

La validación automática comprueba estructura y referencias.
No sustituye la revisión conceptual humana.

## 7. Reproducir la preparación desde los PDF

Este paso es necesario para reproducir el procesamiento.
No es obligatorio repetirlo para comenzar a desarrollar si ya se
recibió y verificó el corpus acordado.

Con los 11 PDF originales en `data/raw/`:

```bash
python src/preparar_paginas.py
python src/analizar_corpus.py
python src/crear_corpus_busqueda.py
```

Resultados principales:

- `data/processed/paginas_limpias.jsonl`: 742 páginas.
- `data/processed/decisiones_paginas.jsonl`: 742 decisiones.
- `data/processed/corpus_busqueda.jsonl`: 697 fragmentos.

La selección excluye 45 páginas. Se conservan 127 páginas breves
marcadas como pendientes de revisión visual.

Volver a comprobar la huella del corpus después de regenerarlo.
Si difiere, revisar los PDF originales, las versiones de dependencias
y el procesamiento antes de continuar.

## 8. Empezar a implementar

Crear una rama propia desde `main` actualizado.

Ejemplos de nombres:

- Fabricio: `feat/recuperador-tfidf`
- Franco: `feat/recuperador-embeddings`

Ambos módulos deben respetar `docs/contrato_recuperacion.md`:

- Operación `buscar(pregunta, k)`.
- Mismo corpus de entrada.
- Resultados con identificador, documento, página, texto y puntaje.
- Sin identificadores duplicados ni referencias inventadas.
- Como máximo `k` resultados, ordenados por relevancia.
- Puntajes tratados como similitudes, no como probabilidades.

El vectorizador TF-IDF se ajusta sobre el corpus.
Las preguntas de evaluación no se utilizan para ajustar su vocabulario.

Las decisiones y ajustes se prueban con el conjunto de desarrollo.
El conjunto final se utiliza una vez fijada la configuración.

## 9. Confirmación de puesta en marcha

Cada integrante debe comprobar:

- Que utiliza el intérprete de su entorno virtual.
- Que instaló las dependencias sin errores.
- Que la huella del corpus coincide.
- Que el validador de desarrollo finaliza correctamente.

Registrar cualquier diferencia de entorno o error encontrado.
La preparación en Ubuntu ya fue utilizada por Joaquín.
Los comandos de Windows deben confirmarse en el equipo correspondiente.