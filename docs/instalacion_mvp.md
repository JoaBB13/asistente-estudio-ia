# Instalación y ejecución del MVP

Ejecutar desde la raíz del repositorio en Linux. Git descarga el código,
pero no instala dependencias, modelos ni datos. La evaluación se realizó con
Python 3.14.4 y Ollama 0.40.16; se registran las versiones completas en el
manifiesto de ejecución. Usar las versiones declaradas en los requirements.

## Entorno Python

Si todavía no existe el entorno:

```bash
python3 -m venv .venv
```

Activar e instalar (PyTorch para CPU):

```bash
source .venv/bin/activate
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt -r requirements-embeddings.txt
python -m pip check
python -m unittest discover -s tests -v
```

Ante incompatibilidad de versión, registrar el error y revisar el entorno;
no eliminar las versiones fijadas para presentar otra configuración como idéntica.

## Datos

Solicitar al equipo los archivos originales por el canal compartido y copiar
como archivos, sin pegar su contenido en un editor. Para usar el asistente basta
el corpus; para evaluar también se necesitan los conjuntos de preguntas.

- data/processed/corpus_busqueda.jsonl
- data/evaluacion/preguntas_desarrollo.jsonl
- data/evaluacion/preguntas_final.jsonl

Los PDF y datos están excluidos de Git. La entrega debe facilitar al docente
un acceso verificado al paquete de datos, separado del repositorio.
Las huellas esperadas están en los documentos de evaluación.

## Ollama y modelo generador

Instalar Ollama si no está disponible:

```bash
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.40.16 sh
ollama --version
ollama list
```

Si no conecta con el servicio en una instalación con systemd:

```bash
sudo systemctl start ollama
```

Descargar el modelo (aproximadamente 2,5 GB):

```bash
ollama pull qwen3:4b-instruct-2507-q4_K_M
```

Preparar el tokenizador; no descarga otra copia completa del generador:

```bash
python - <<'PY'
from transformers import AutoTokenizer
AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-4B-Instruct-2507",
    revision="cdbee75f17c01a7cc42f958dc650907174af0554",
    trust_remote_code=False,
)
print("Tokenizador preparado.")
PY
```

El recuperador descarga multilingual-e5-small al usarlo por primera vez.
La primera preparación necesita conexión. Los modelos se ejecutan localmente;
no se utiliza una API comercial de generación ni una clave de pago.

## Uso

```bash
python src/consola_asistente.py
```

Escribir una pregunta por vez. Finalizar con /salir. Las consultas no tienen
memoria de conversación. Se conservan registros técnicos locales en
data/evaluacion/sesiones_mvp/, sin que se usen como historial conversacional.

Consulta única:

```bash
python src/consola_asistente.py --pregunta "¿Qué representa el MAE?"
```

El índice se prepara al iniciar y se reutiliza durante la sesión. En el equipo
evaluado las consultas finales tardaron entre 66,41 y 205,50 segundos,
sin incluir la preparación inicial. El tiempo depende del equipo y su carga.

## Evaluación final y conservación

```bash
python src/evaluar_final_mvp.py
```

Usa la carpeta data/evaluacion/final_mvp_v1 y conserva los casos existentes,
incluidos sus errores. No reintenta selectivamente las respuestas fallidas.
El manifiesto impide mezclar cambios de commit, código, modelo o entorno.
Si cambia la versión, conservar los registros y documentar una ejecución distinta.
Después de los commits de documentación no debe intentarse reanudar la corrida
anterior en esa misma carpeta: su commit evaluado fue 15e7382.

La evaluación final ya se realizó; no se necesita repetir para usar la consola.
Repetir sobre estas preguntas no constituye otro conjunto independiente.

Fuente de instalación: https://docs.ollama.com/linux
