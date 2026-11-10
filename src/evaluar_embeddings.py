"""Evalúa embeddings exclusivamente sobre preguntas de desarrollo."""

import hashlib
import json
from datetime import datetime, timezone

from recuperador_embeddings import (
    CORPUS,
    RAIZ,
    RecuperadorEmbeddings,
)


RUTA_PREGUNTAS = (
    RAIZ / "data/evaluacion/preguntas_desarrollo.jsonl"
)


def resumir(valores):
    total = len(valores)
    aciertos = sum(valores)

    return {
        "aciertos": aciertos,
        "total": total,
        "porcentaje": (
            100 * aciertos / total if total else None
        ),
    }


def evaluar_caso(caso, resultados):
    recuperados = {
        resultado["id_fragmento"]
        for resultado in resultados
    }

    hit = None
    cobertura = None

    if caso["respondible"]:
        esperados = {
            evidencia["id_fragmento"]
            for evidencia in caso["evidencias"]
        }

        hit = bool(recuperados & esperados)

        grupos = caso.get("grupos_evidencia_requeridos")

        if grupos:
            cobertura = all(
                bool(recuperados & set(grupo))
                for grupo in grupos
            )

    return {
        "id": caso["id"],
        "pregunta": caso["pregunta"],
        "respondible": caso["respondible"],
        "es_reformulacion": bool(caso.get("caso_origen")),
        "hit_at_3": hit,
        "cobertura_completa_at_3": cobertura,
        "lista_vacia": not resultados,
        "resultados": [
            {
                campo: resultado[campo]
                for campo in (
                    "id_fragmento",
                    "documento",
                    "pagina",
                    "puntaje",
                )
            }
            for resultado in resultados
        ],
    }


def main():
    contenido = RUTA_PREGUNTAS.read_bytes()

    casos = [
        json.loads(linea)
        for linea in contenido.decode("utf-8").splitlines()
        if linea.strip()
    ]

    if not casos:
        raise ValueError("El archivo de preguntas está vacío.")

    huella = hashlib.sha256(
        CORPUS.read_bytes()
    ).hexdigest()

    identificadores = set()

    for caso in casos:
        if caso["id"] in identificadores:
            raise ValueError(
                f"Caso duplicado: {caso['id']}"
            )

        identificadores.add(caso["id"])

        if caso["particion"] != "desarrollo":
            raise ValueError(
                "Este programa solo evalúa desarrollo."
            )

        if caso["corpus_sha256"] != huella:
            raise ValueError(
                f"{caso['id']}: el corpus no coincide "
                "con la referencia."
            )

    print(
        "Preparando el índice de embeddings una sola vez...",
        flush=True,
    )

    recuperador = RecuperadorEmbeddings()

    if recuperador.metadatos["corpus_sha256"] != huella:
        raise ValueError(
            "El corpus cambió durante la preparación."
        )

    print("Evaluación embeddings — k=3")
    print(
        "Revisión del modelo:",
        recuperador.metadatos["revision"],
    )
    print("SHA-256 del corpus:", huella)

    detalle = []

    for caso in casos:
        resultados = recuperador.buscar(
            caso["pregunta"],
            k=3,
        )

        evaluacion = evaluar_caso(caso, resultados)
        detalle.append(evaluacion)

        if caso["respondible"]:
            estado = (
                "ACIERTO"
                if evaluacion["hit_at_3"]
                else "FALLO"
            )

            cobertura = evaluacion["cobertura_completa_at_3"]

            if cobertura is not None:
                estado += (
                    " | cobertura completa"
                    if cobertura
                    else " | cobertura incompleta"
                )
        else:
            estado = "NO RESPONDIBLE | "
            estado += (
                "sin resultados"
                if evaluacion["lista_vacia"]
                else "devuelve resultados"
            )

        print(f"\n{caso['id']}: {estado}")
        print("Pregunta:", caso["pregunta"])

        for posicion, resultado in enumerate(resultados, 1):
            print(
                f"  {posicion}. {resultado['documento']} "
                f"| página {resultado['pagina']} "
                f"| puntaje {resultado['puntaje']:.4f}"
            )

    resumen = {}

    metricas = (
        ("Hit@3", "hit_at_3"),
        ("Cobertura completa@3", "cobertura_completa_at_3"),
    )

    grupos = (
        ("total", None),
        ("base", False),
        ("reformulaciones", True),
    )

    for nombre, campo in metricas:
        for grupo, es_reformulacion in grupos:
            valores = [
                resultado[campo]
                for resultado in detalle
                if resultado[campo] is not None
                and (
                    es_reformulacion is None
                    or resultado["es_reformulacion"]
                    == es_reformulacion
                )
            ]

            resumen[f"{nombre} {grupo}"] = resumir(valores)

    resumen["Listas vacías en casos no respondibles"] = (
        resumir([
            resultado["lista_vacia"]
            for resultado in detalle
            if not resultado["respondible"]
        ])
    )

    print("\nRESUMEN")

    for nombre, medida in resumen.items():
        if medida["total"]:
            print(
                f"{nombre}: "
                f"{medida['aciertos']}/{medida['total']} "
                f"({medida['porcentaje']:.2f} %)"
            )
        else:
            print(f"{nombre}: sin casos.")

    print(
        "Las listas vacías no miden por sí solas "
        "la abstención del asistente."
    )

    ahora = datetime.now(timezone.utc)

    informe = {
        "fecha_utc": ahora.isoformat(),
        "particion": "desarrollo",
        "k": 3,
        "preguntas_sha256": hashlib.sha256(
            contenido
        ).hexdigest(),
        "configuracion": recuperador.metadatos,
        "resumen": resumen,
        "casos": detalle,
    }

    nombre_archivo = (
        "resultados_embeddings_"
        + ahora.strftime("%Y%m%dT%H%M%S%fZ")
        + ".json"
    )

    destino = (
        RAIZ / "data/evaluacion" / nombre_archivo
    )

    destino.parent.mkdir(parents=True, exist_ok=True)

    destino.write_text(
        json.dumps(
            informe,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("Informe guardado en:", destino)


if __name__ == "__main__":
    main()