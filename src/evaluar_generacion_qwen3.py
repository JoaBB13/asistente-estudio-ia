"""Evaluación experimental sobre desarrollo; requiere revisión humana."""

import hashlib
import json
from collections import Counter
from pathlib import Path

import generador_qwen3 as g


RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"

INFORME = DATOS / (
    "evaluacion/"
    "resultados_embeddings_20261110T062506980553Z.json"
)

DESTINO = DATOS / "evaluacion/generacion_qwen3_v1"

# Se aplica únicamente al ejecutar este evaluador.
# El modelo lo fija generador_qwen3.


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def leer_jsonl(ruta, clave):
    filas = [
        json.loads(linea)
        for linea in ruta.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]

    indice = {fila[clave]: fila for fila in filas}

    if not filas or len(indice) != len(filas):
        raise ValueError(
            f"Archivo vacío o identificadores repetidos: {ruta}"
        )

    return indice


def guardar(ruta, contenido):
    temporal = ruta.with_suffix(".tmp")

    temporal.write_text(
        json.dumps(contenido, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    temporal.replace(ruta)


def main():
    ruta_corpus = DATOS / "processed/corpus_busqueda.jsonl"
    ruta_preguntas = DATOS / "evaluacion/preguntas_desarrollo.jsonl"

    corpus = leer_jsonl(ruta_corpus, "id_fragmento")
    preguntas = leer_jsonl(ruta_preguntas, "id")

    informe = json.loads(
        INFORME.read_text(encoding="utf-8")
    )

    sha_corpus = huella(ruta_corpus)
    sha_preguntas = huella(ruta_preguntas)

    if (
        informe["configuracion"]["corpus_sha256"] != sha_corpus
        or informe["preguntas_sha256"] != sha_preguntas
    ):
        raise ValueError(
            "Los datos no coinciden con el informe de recuperación."
        )

    casos = {caso["id"]: caso for caso in informe["casos"]}

    if (
        len(casos) != len(informe["casos"])
        or set(casos) != set(preguntas)
    ):
        raise ValueError(
            "Las preguntas y el informe no contienen "
            "los mismos casos únicos."
        )

    entradas = {}

    for identificador, pregunta in preguntas.items():
        caso = casos[identificador]

        if (
            pregunta["particion"] != "desarrollo"
            or pregunta["corpus_sha256"] != sha_corpus
        ):
            raise ValueError(
                f"Partición o corpus incorrecto: {identificador}"
            )

        if caso["pregunta"] != pregunta["pregunta"]:
            raise ValueError(
                f"Pregunta diferente: {identificador}"
            )

        fragmentos = []

        for resultado in caso["resultados"]:
            original = corpus[resultado["id_fragmento"]]

            if any(
                resultado[campo] != original[campo]
                for campo in ("documento", "pagina")
            ):
                raise ValueError(
                    f"Referencia diferente: {identificador}"
                )

            fragmentos.append({
                **resultado,
                "texto": original["texto"],
            })

        entradas[identificador] = fragmentos

    instalado = next(
        (
            modelo
            for modelo in g.api("/api/tags")["models"]
            if modelo["name"] == g.MODELO
        ),
        None,
    )

    if instalado is None:
        raise ValueError("El modelo requerido no está instalado.")

    configuracion = {
        "modelo": g.MODELO,
        "modelo_digest": instalado["digest"],
        "ollama_version": g.api("/api/version")["version"],
        "corpus_sha256": sha_corpus,
        "preguntas_sha256": sha_preguntas,
        "informe_sha256": huella(INFORME),
        "generador_sha256": huella(Path(g.__file__)),
        "evaluador_sha256": huella(Path(__file__)),
        "opciones": g.OPCIONES,
        "instrucciones": g.INSTRUCCIONES,
    }

    DESTINO.mkdir(parents=True, exist_ok=True)
    manifiesto = DESTINO / "configuracion.json"

    if manifiesto.exists():
        anterior = json.loads(
            manifiesto.read_text(encoding="utf-8")
        )

        if anterior != configuracion:
            raise ValueError(
                "Cambió la configuración. Usá otra carpeta "
                "para una nueva evaluación."
            )
    else:
        guardar(manifiesto, configuracion)

    controles = Counter()
    estados = Counter()

    for numero, (identificador, pregunta) in enumerate(
        preguntas.items(), 1
    ):
        archivo = DESTINO / f"caso_{numero:03d}.json"

        print(
            f"\n[{numero}/{len(preguntas)}] "
            f"{identificador}: {pregunta['pregunta']}",
            flush=True,
        )

        if archivo.exists():
            registro = json.loads(
                archivo.read_text(encoding="utf-8")
            )

            if registro["caso_id"] != identificador:
                raise ValueError(
                    "Un registro guardado corresponde a otro caso."
                )

            print(
                "Se conserva el resultado anterior, "
                "incluidos sus errores."
            )
        else:
            # El modelo recibe solo pregunta y fragmentos recuperados.
            registro = g.generar(
                pregunta["pregunta"],
                entradas[identificador],
            )

            registro["caso_id"] = identificador
            registro["corpus_sha256"] = sha_corpus
            registro["preguntas_sha256"] = sha_preguntas
            registro["configuracion_recuperacion"] = (
                informe["configuracion"]
            )

            # Estas referencias se agregan después de generar.
            registro["revision_humana"] = {
                "estado": "pendiente",
                "revisor": None,
                "respondible_esperado": pregunta["respondible"],
                "respuesta_referencia": (
                    pregunta["respuesta_referencia"]
                ),
                "criterios_respuesta": (
                    pregunta["criterios_respuesta"]
                ),
                "evidencias_esperadas": pregunta["evidencias"],
                "grupos_evidencia_requeridos": pregunta.get(
                    "grupos_evidencia_requeridos"
                ),
            }

            digest_observado = registro.get(
                "modelo_digest", instalado["digest"]
            )
            version_observada = registro.get(
                "ollama_version",
                configuracion["ollama_version"],
            )

            if (
                digest_observado != instalado["digest"]
                or version_observada != configuracion["ollama_version"]
            ):
                raise ValueError(
                    "Cambió el modelo o el servicio "
                    "durante la evaluación."
                )

            guardar(archivo, registro)

        g.mostrar(registro)

        print(
            "Tiempo:",
            registro.get("tiempo_total_segundos"),
            "s",
            flush=True,
        )

        controles[registro["control_automatico"]] += 1

        if (
            registro["control_automatico"]
            == "estructura_e_identificadores_comprobados"
        ):
            estados[registro["estado_derivado"]] += 1

    resumen = {
        "casos_registrados": sum(controles.values()),
        "controles": dict(controles),
        "estados_derivados_no_verificados": dict(estados),
        "revision_humana": "pendiente",
    }

    guardar(DESTINO / "resumen.json", resumen)

    print("\nRESUMEN OPERATIVO (no mide corrección):")
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    print("Registros:", DESTINO)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\nInterrumpido. Ejecutá otra vez para continuar "
            "desde los casos guardados."
        )