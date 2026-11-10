"""Buscador semántico de diapositivas con multilingual-e5-small."""

import argparse
import hashlib
import json
import platform
import re
import warnings
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np


RAIZ = Path(__file__).resolve().parents[1]
MODELO = "intfloat/multilingual-e5-small"
REVISION_MODELO = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
CORPUS = RAIZ / "data/processed/corpus_busqueda.jsonl"


def cargar_corpus(ruta):
    """Lee el corpus y valida los datos necesarios para buscar."""
    contenido = Path(ruta).read_bytes()
    registros = []
    identificadores = set()

    for numero, linea in enumerate(
        contenido.decode("utf-8-sig").splitlines(), 1
    ):
        if not linea.strip():
            continue

        try:
            registro = json.loads(linea)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"JSON inválido en la línea {numero}."
            ) from error

        if not isinstance(registro, dict):
            raise ValueError(
                f"La línea {numero} debe contener un objeto."
            )

        for campo in ("id_fragmento", "documento", "texto"):
            valor = registro.get(campo)

            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(
                    f"Campo {campo} inválido en la línea {numero}."
                )

        pagina = registro.get("pagina")

        if type(pagina) is not int or pagina <= 0:
            raise ValueError(
                f"Página inválida en la línea {numero}."
            )

        identificador = registro["id_fragmento"]

        if identificador in identificadores:
            raise ValueError(
                f"Identificador duplicado: {identificador}"
            )

        identificadores.add(identificador)
        registros.append(registro)

    if not registros:
        raise ValueError("El corpus está vacío.")

    huella = hashlib.sha256(contenido).hexdigest()
    return registros, huella


def cargar_modelo(revision):
    """Resuelve y carga una revisión exacta del modelo."""
    from huggingface_hub import hf_hub_download
    from sentence_transformers import SentenceTransformer

    configuracion = hf_hub_download(
        repo_id=MODELO,
        filename="config.json",
        revision=revision,
    )

    # Hugging Face devuelve una ruta snapshots/<commit>/config.json.
    # No usamos resolve(): el archivo puede ser un enlace a otro lugar.
    commit = Path(configuracion).parent.name

    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError(
            "No se pudo identificar la revisión exacta del modelo."
        )

    modelo = SentenceTransformer(
        MODELO,
        revision=commit,
        device="cpu",
    )

    modelo.max_seq_length = min(512, modelo.max_seq_length)

    return modelo, commit


class RecuperadorEmbeddings:
    def __init__(
        self,
        ruta_corpus=CORPUS,
        revision=REVISION_MODELO,
        batch_size=8,
    ):
        if type(batch_size) is not int or batch_size <= 0:
            raise ValueError(
                "batch_size debe ser un entero positivo."
            )

        self.registros, huella = cargar_corpus(ruta_corpus)
        self.modelo, commit = cargar_modelo(revision)
        self.batch_size = batch_size
        self.limite_tokens = self.modelo.max_seq_length

        self.metadatos = {
            "modelo": MODELO,
            "revision": commit,
            "corpus_sha256": huella,
            "cantidad_fragmentos": len(self.registros),
            "dispositivo": "cpu",
            "batch_size": batch_size,
            "max_seq_length": self.limite_tokens,
            "prefijo_consulta": "query: ",
            "prefijo_documento": "passage: ",
            "normalize_embeddings": True,
            "metrica": "coseno",
            "politica_textos_largos": (
                "Truncar al límite del modelo; "
                "conservar texto original en resultados."
            ),
            "truncation_side": self.modelo.tokenizer.truncation_side,
            "documentos_truncados": [],
            "consultas_truncadas": [],
            "python": platform.python_version(),
            "dependencias": {},
        }

        paquetes = (
            "numpy",
            "torch",
            "sentence-transformers",
            "transformers",
            "huggingface-hub",
        )

        for paquete in paquetes:
            try:
                self.metadatos["dependencias"][paquete] = version(
                    paquete
                )
            except PackageNotFoundError:
                self.metadatos["dependencias"][paquete] = (
                    "no disponible"
                )

        textos = [
            "passage: " + registro["texto"]
            for registro in self.registros
        ]

        # Controlamos la longitud antes de generar embeddings.
        for registro, texto in zip(self.registros, textos):
            cantidad = self._contar_tokens(texto)

            if cantidad > self.limite_tokens:
                self.metadatos["documentos_truncados"].append(
                    {
                        "id_fragmento": registro["id_fragmento"],
                        "tokens_originales": cantidad,
                        "limite_tokens": self.limite_tokens,
                    }
                )

        truncados = len(self.metadatos["documentos_truncados"])

        if truncados:
            warnings.warn(
                f"{truncados} fragmentos exceden el límite "
                "del modelo. Se registraron en los metadatos.",
                stacklevel=2,
            )

        self.embeddings = self.modelo.encode(
            textos,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
            prompt="",
        )

        if not np.isfinite(self.embeddings).all():
            raise ValueError(
                "El modelo produjo embeddings no finitos."
            )

        self.metadatos["dimension_embeddings"] = int(
            self.embeddings.shape[1]
        )

    def _contar_tokens(self, texto):
        """Incluye el prefijo y los tokens especiales del modelo."""
        tokens = self.modelo.tokenizer(
            texto,
            add_special_tokens=True,
            truncation=False,
            return_attention_mask=False,
            return_token_type_ids=False,
        )

        return len(tokens["input_ids"])

    def buscar(self, pregunta, k=3):
        """Devuelve hasta k fragmentos ordenados por relevancia."""
        if not isinstance(pregunta, str) or not pregunta.strip():
            raise ValueError(
                "La pregunta debe ser un texto no vacío."
            )

        # Rechazamos también True y False, aunque Python los
        # considere subtipos de int.
        if type(k) is not int or k <= 0:
            raise ValueError(
                "k debe ser un entero positivo."
            )

        consulta = "query: " + pregunta.strip()
        cantidad = self._contar_tokens(consulta)

        if cantidad > self.limite_tokens:
            self.metadatos["consultas_truncadas"].append(
                {
                    "pregunta_sha256": hashlib.sha256(
                        pregunta.encode("utf-8")
                    ).hexdigest(),
                    "tokens_originales": cantidad,
                    "limite_tokens": self.limite_tokens,
                }
            )

            warnings.warn(
                "La consulta excede el límite y será truncada.",
                stacklevel=2,
            )

        vector = self.modelo.encode(
            [consulta],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
            prompt="",
        )[0]

        # Con vectores normalizados, el producto escalar
        # equivale a la similitud coseno.
        puntajes = self.embeddings @ vector

        if not np.isfinite(puntajes).all():
            raise ValueError(
                "El modelo produjo puntajes no finitos."
            )

        orden = sorted(
            range(len(self.registros)),
            key=lambda i: (
                -float(puntajes[i]),
                self.registros[i]["id_fragmento"],
            ),
        )[:k]

        resultados = []

        for indice in orden:
            registro = self.registros[indice]

            resultados.append(
                {
                    "id_fragmento": registro["id_fragmento"],
                    "documento": registro["documento"],
                    "pagina": registro["pagina"],
                    "texto": registro["texto"],
                    "puntaje": float(puntajes[indice]),
                }
            )

        return resultados

    def guardar_metadatos(self, ruta):
        """Guarda configuración, versiones y truncamientos."""
        destino = Path(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)

        destino.write_text(
            json.dumps(
                self.metadatos,
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )


def main():
    parser = argparse.ArgumentParser(
        description="Busca diapositivas mediante embeddings."
    )

    parser.add_argument("pregunta")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument(
        "--revision",
        default=REVISION_MODELO,
        help="Commit exacto del modelo para reproducir una ejecución.",
    )
    parser.add_argument("--batch-size", type=int, default=8)

    args = parser.parse_args()

    if (
        not args.pregunta.strip()
        or args.k <= 0
        or args.batch_size <= 0
    ):
        parser.error(
            "Se requiere una pregunta no vacía, "
            "k positivo y batch-size positivo."
        )

    print(
        "Cargando el corpus y generando embeddings...",
        flush=True,
    )

    recuperador = RecuperadorEmbeddings(
        ruta_corpus=args.corpus,
        revision=args.revision,
        batch_size=args.batch_size,
    )

    print(
        f"Índice listo: {len(recuperador.registros)} fragmentos."
    )
    print(
        "Revisión del modelo:",
        recuperador.metadatos["revision"],
    )

    resultados = recuperador.buscar(args.pregunta, args.k)

    for numero, resultado in enumerate(resultados, 1):
        print(f"\nResultado {numero}")
        print(f"Documento: {resultado['documento']}")
        print(f"Página del PDF: {resultado['pagina']}")
        print(f"ID: {resultado['id_fragmento']}")
        print(f"Similitud: {resultado['puntaje']:.4f}")
        print(resultado["texto"])

    fecha = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    ruta_registro = (
        RAIZ
        / "data/processed"
        / f"ejecucion_embeddings_{fecha}.json"
    )

    recuperador.guardar_metadatos(ruta_registro)

    print(
        "\nConfiguración y truncamientos registrados en:",
        ruta_registro,
    )
    print(
        "Se muestran fragmentos recuperados; "
        "no son respuestas generadas."
    )


if __name__ == "__main__":
    main()