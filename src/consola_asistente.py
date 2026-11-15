"""Consola del MVP: recuperación semántica y generación local."""

import argparse
import time

from asistente_estudio import AsistenteEstudio, guardar_registro
from generador_qwen3 import mostrar


def consultar(asistente, pregunta, k):
    registro = asistente.responder(pregunta, k=k)

    mostrar(registro)

    print(
        "Tiempo de consulta:",
        registro["tiempo_total_pipeline_segundos"],
        "s",
    )

    try:
        print("Registro:", guardar_registro(registro))
    except OSError as error:
        print("No se pudo guardar el registro:", error)

    return registro


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--pregunta",
        help="Realiza una consulta y termina.",
    )
    parser.add_argument("--k", type=int, default=3)

    args = parser.parse_args()

    if args.k <= 0:
        parser.error("k debe ser positivo.")

    if args.pregunta is not None and not args.pregunta.strip():
        parser.error("La pregunta no puede estar vacía.")

    print(
        "Preparando el asistente y el índice de búsqueda...",
        flush=True,
    )

    inicio = time.perf_counter()

    try:
        asistente = AsistenteEstudio()
    except Exception as error:
        print(
            f"No se pudo iniciar: {type(error).__name__}: {error}"
        )
        return 1

    print(
        "Asistente listo. Preparación:",
        round(time.perf_counter() - inicio, 2),
        "s",
    )

    print(
        "Prototipo: las respuestas pueden contener errores. "
        "Revisá las fuentes."
    )

    if args.pregunta is not None:
        registro = consultar(
            asistente,
            args.pregunta,
            args.k,
        )

        return (
            1
            if registro["control_automatico"] in {
                "error_tecnico", "salida_invalida"
            }
            else 0
        )

    print("Escribí una pregunta o /salir para terminar.")

    while True:
        pregunta = input("\nPregunta: ").strip()

        if pregunta == "/salir":
            break

        if not pregunta:
            print("Escribí una pregunta antes de continuar.")
            continue

        consultar(asistente, pregunta, args.k)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nConsola finalizada.")