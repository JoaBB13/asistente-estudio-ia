"""Orquestación de recuperación y generación del asistente."""

import copy
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


RAIZ = Path(__file__).resolve().parents[1]
REVISION_E5 = "614241f622f53c4eeff9890bdc4f31cfecc418b3"


class AsistenteEstudio:
    def __init__(self, recuperador=None, generar=None):
        if recuperador is None:
            from recuperador_embeddings import RecuperadorEmbeddings

            recuperador = RecuperadorEmbeddings(
                revision=REVISION_E5
            )

        if generar is None:
            from generador_qwen3 import generar

        self.recuperador = recuperador
        self.generar = generar
        self.huellas_codigo = {}

        for nombre in (
            "asistente_estudio.py",
            "recuperador_embeddings.py",
            "generador_qwen3.py",
        ):
            ruta = Path(__file__).with_name(nombre)

            if ruta.exists():
                self.huellas_codigo[nombre] = hashlib.sha256(
                    ruta.read_bytes()
                ).hexdigest()

    def responder(self, pregunta, k=3):
        if not isinstance(pregunta, str) or not pregunta.strip():
            raise ValueError(
                "Escribí una pregunta antes de continuar."
            )

        if type(k) is not int or k <= 0:
            raise ValueError("k debe ser un entero positivo.")

        inicio = time.perf_counter()
        fase = "recuperacion"

        registro = {
            "pregunta": pregunta,
            "k": k,
            "fecha_utc": datetime.now(timezone.utc).isoformat(),
            "huellas_codigo": dict(self.huellas_codigo),
            "revision_semantica": "pendiente",
        }

        try:
            fragmentos = self.recuperador.buscar(pregunta, k=k)

            registro["tiempo_recuperacion_segundos"] = round(
                time.perf_counter() - inicio, 2
            )

            registro["recuperados"] = copy.deepcopy(fragmentos)

            registro["configuracion_recuperacion"] = copy.deepcopy(
                self.recuperador.metadatos
            )

            registro["corpus_sha256"] = (
                self.recuperador.metadatos["corpus_sha256"]
            )

            fase = "generacion"

            registro.update(
                self.generar(pregunta, fragmentos)
            )

        except Exception as error:
            registro["control_automatico"] = "error_tecnico"
            registro["fase_error"] = fase
            registro["error"] = (
                f"{type(error).__name__}: {error}"
            )

        registro["tiempo_total_pipeline_segundos"] = round(
            time.perf_counter() - inicio, 2
        )

        return registro


def guardar_registro(registro, carpeta=None):
    carpeta = (
        Path(carpeta)
        if carpeta is not None
        else RAIZ / "data/evaluacion/sesiones_mvp"
    )

    carpeta.mkdir(parents=True, exist_ok=True)

    fecha = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    ruta = carpeta / (
        f"consulta_{fecha}_{uuid4().hex[:8]}.json"
    )

    temporal = ruta.with_suffix(".tmp")

    temporal.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    temporal.replace(ruta)
    return ruta