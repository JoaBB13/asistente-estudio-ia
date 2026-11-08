"""Evalúa la recuperación TF-IDF sobre las preguntas de desarrollo."""

import hashlib
import json

import sklearn

from recuperador_tfidf import (
    RAIZ_PROYECTO,
    RUTA_CORPUS,
    RecuperadorTFIDF,
)


RUTA_PREGUNTAS = (
    RAIZ_PROYECTO / "data/evaluacion/preguntas_desarrollo.jsonl"
)


def mostrar_medida(nombre, valores):
    """Muestra aciertos, total y porcentaje sin dividir por cero."""
    total = len(valores)
    aciertos = sum(valores)

    if total == 0:
        print(f"{nombre}: sin casos.")
        return

    porcentaje = 100 * aciertos / total
    print(f"{nombre}: {aciertos}/{total} ({porcentaje:.2f} %)")


def main():
    contenido_preguntas = RUTA_PREGUNTAS.read_bytes()
    casos = [
        json.loads(linea)
        for linea in contenido_preguntas.decode("utf-8").splitlines()
        if linea.strip()
    ]

    if not casos:
        raise ValueError("El archivo de preguntas está vacío.")

    huella_corpus = hashlib.sha256(RUTA_CORPUS.read_bytes()).hexdigest()

    for caso in casos:
        if caso["particion"] != "desarrollo":
            raise ValueError("Este programa solo evalúa desarrollo.")

        if caso["corpus_sha256"] != huella_corpus:
            raise ValueError(
                f"{caso['id']}: el corpus no coincide con la referencia."
            )

    recuperador = RecuperadorTFIDF()

    print("Evaluación TF-IDF — k=3")
    print("scikit-learn:", sklearn.__version__)
    print("SHA-256 del corpus:", huella_corpus)
    print(
        "SHA-256 de preguntas:",
        hashlib.sha256(contenido_preguntas).hexdigest(),
    )

    aciertos_base = []
    aciertos_reformulaciones = []
    cobertura_base = []
    cobertura_reformulaciones = []
    vacios_no_respondibles = []

    for caso in casos:
        resultados = recuperador.buscar(caso["pregunta"], k=3)
        recuperados = {r["id_fragmento"] for r in resultados}
        es_reformulacion = bool(caso.get("caso_origen"))

        if caso["respondible"]:
            esperados = {
                evidencia["id_fragmento"]
                for evidencia in caso["evidencias"]
            }
            acierto = bool(recuperados & esperados)

            if es_reformulacion:
                aciertos_reformulaciones.append(acierto)
            else:
                aciertos_base.append(acierto)

            estado = "ACIERTO" if acierto else "FALLO"
            grupos = caso.get("grupos_evidencia_requeridos")

            if grupos:
                completa = all(
                    bool(recuperados & set(grupo))
                    for grupo in grupos
                )

                if es_reformulacion:
                    cobertura_reformulaciones.append(completa)
                else:
                    cobertura_base.append(completa)

                estado += (
                    " | cobertura completa"
                    if completa
                    else " | cobertura incompleta"
                )
        else:
            vacio = not resultados
            vacios_no_respondibles.append(vacio)
            estado = (
                "NO RESPONDIBLE | sin resultados"
                if vacio
                else "NO RESPONDIBLE | devuelve resultados"
            )

        print(f"\n{caso['id']}: {estado}")
        print("Pregunta:", caso["pregunta"])

        for posicion, resultado in enumerate(resultados, start=1):
            print(
                f"  {posicion}. {resultado['documento']} "
                f"| página {resultado['pagina']} "
                f"| puntaje {resultado['puntaje']:.4f}"
            )

    print("\nRESUMEN")

    mostrar_medida(
        "Hit@3 total",
        aciertos_base + aciertos_reformulaciones,
    )
    mostrar_medida("Hit@3 preguntas base", aciertos_base)
    mostrar_medida("Hit@3 reformulaciones", aciertos_reformulaciones)

    mostrar_medida(
        "Cobertura completa@3 total",
        cobertura_base + cobertura_reformulaciones,
    )
    mostrar_medida("Cobertura completa@3 base", cobertura_base)
    mostrar_medida(
        "Cobertura completa@3 reformulaciones",
        cobertura_reformulaciones,
    )

    mostrar_medida(
        "Listas vacías en casos no respondibles",
        vacios_no_respondibles,
    )
    print(
        "Las listas vacías son un diagnóstico de recuperación; "
        "no miden por sí solas la abstención del asistente."
    )


if __name__ == "__main__":
    main()
