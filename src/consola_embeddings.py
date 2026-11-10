"""Consola interactiva para consultar el recuperador por embeddings."""

from datetime import datetime, timezone

from recuperador_embeddings import RAIZ, RecuperadorEmbeddings


def mostrar_resultados(resultados):
    if not resultados:
        print("No se recuperaron fragmentos.")
        return

    for posicion, resultado in enumerate(resultados, 1):
        print("\n" + "=" * 60)
        print(f"Resultado {posicion}")
        print(f"Documento: {resultado['documento']}")
        print(f"Página del PDF: {resultado['pagina']}")
        print(f"ID: {resultado['id_fragmento']}")
        print(f"Similitud: {resultado['puntaje']:.4f}")
        print("-" * 60)
        print(resultado["texto"])


def main():
    print(
        "Cargando el corpus y preparando el índice...",
        flush=True,
    )

    try:
        recuperador = RecuperadorEmbeddings()
    except KeyboardInterrupt:
        print("\nCarga cancelada.")
        return

    print(
        f"Índice listo: {len(recuperador.registros)} fragmentos."
    )
    print("Escribí una pregunta o /salir para terminar.")
    print("Se mostrarán hasta 3 diapositivas relacionadas.")
    print(
        "Los resultados son fragmentos del material, "
        "no respuestas generadas."
    )
    print(
        "Encontrar resultados no garantiza que el material "
        "contenga la respuesta."
    )

    inicio = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    ruta_registro = (
        RAIZ
        / "data/processed"
        / f"sesion_embeddings_{inicio}.json"
    )

    try:
        while True:
            try:
                pregunta = input("\nPregunta: ").strip()

                if pregunta.lower() == "/salir":
                    break

                if not pregunta:
                    print("Escribí una pregunta antes de continuar.")
                    continue

                resultados = recuperador.buscar(pregunta, k=3)
                mostrar_resultados(resultados)

            except ValueError as error:
                print(f"No se pudo procesar la consulta: {error}")

    except (KeyboardInterrupt, EOFError):
        print("\nFinalizando la consola...")

    finally:
        recuperador.guardar_metadatos(ruta_registro)
        print("\nRegistro de configuración:", ruta_registro)

    print("Consola finalizada.")


if __name__ == "__main__":
    main()