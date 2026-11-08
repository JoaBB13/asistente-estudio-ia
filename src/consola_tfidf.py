"""Consola interactiva para consultar el recuperador TF-IDF."""

from recuperador_tfidf import RecuperadorTFIDF


def main():
    print("Cargando el corpus y preparando el índice TF-IDF...")

    try:
        recuperador = RecuperadorTFIDF()
    except (OSError, ValueError) as error:
        print(f"No se pudo iniciar el recuperador: {error}")
        return 1

    print(f"Índice listo: {len(recuperador.fragmentos)} fragmentos.")
    print("Escribí una pregunta o /salir para terminar.")
    print("Se mostrarán hasta 3 diapositivas relacionadas.")
    print("Los resultados son fragmentos del material, no respuestas generadas.")

    while True:
        try:
            pregunta = input("\nPregunta: ").strip()

            if pregunta.lower() == "/salir":
                print("Consulta finalizada.")
                break

            try:
                resultados = recuperador.buscar(pregunta, k=3)
            except ValueError as error:
                print(f"Consulta inválida: {error}")
                continue

            if not resultados:
                print("No se encontraron coincidencias con el vocabulario.")
                print("Probá reformular la consulta.")
                continue

            for posicion, resultado in enumerate(resultados, start=1):
                print("\n" + "=" * 60)
                print(f"Resultado {posicion}")
                print(f"Documento: {resultado['documento']}")
                print(f"Página del PDF: {resultado['pagina']}")
                print(f"ID: {resultado['id_fragmento']}")
                print(f"Similitud: {resultado['puntaje']:.4f}")
                print("-" * 60)
                print(resultado["texto"])

        except (KeyboardInterrupt, EOFError):
            print("\nConsulta finalizada.")
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
