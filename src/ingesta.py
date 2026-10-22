"""Extrae texto de los PDF y conserva su documento y página de origen."""

import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "raw"
SALIDA = RAIZ / "data" / "processed"


def extraer_documento(ruta):
    """Devuelve las páginas extraídas y un resumen del documento."""
    huella = hashlib.sha256(ruta.read_bytes()).hexdigest()
    paginas = []

    with ruta.open("rb") as archivo:
        lector = PdfReader(archivo)

        if lector.is_encrypted:
            raise ValueError(f"El PDF está cifrado: {ruta.name}")

        for numero, pagina in enumerate(lector.pages, start=1):
            texto = pagina.extract_text() or ""

            paginas.append({
                "documento": ruta.name,
                "sha256": huella,
                "pagina": numero,
                "texto": texto,
                "caracteres": len(texto),
                "palabras": len(texto.split()),
                "sin_texto": not texto.strip(),
            })

    resumen = {
        "documento": ruta.name,
        "sha256": huella,
        "paginas": len(paginas),
        "paginas_sin_texto": sum(p["sin_texto"] for p in paginas),
        "palabras": sum(p["palabras"] for p in paginas),
    }

    return paginas, resumen


def guardar_resultados(paginas, inventario):
    """Guarda el texto por página y el inventario de documentos."""
    SALIDA.mkdir(parents=True, exist_ok=True)

    with (SALIDA / "paginas.jsonl").open(
        "w", encoding="utf-8"
    ) as archivo:
        for pagina in paginas:
            archivo.write(json.dumps(pagina, ensure_ascii=False) + "\n")

    with (SALIDA / "inventario.json").open(
        "w", encoding="utf-8"
    ) as archivo:
        json.dump(inventario, archivo, ensure_ascii=False, indent=2)


def main():
    if not ENTRADA.is_dir():
        raise SystemExit(f"No existe la carpeta: {ENTRADA}")

    documentos = sorted(
        ruta for ruta in ENTRADA.iterdir()
        if ruta.is_file() and ruta.suffix.lower() == ".pdf"
    )

    if not documentos:
        raise SystemExit("No se encontraron PDF en data/raw.")

    todas_las_paginas = []
    inventario = []

    for ruta in documentos:
        print(f"Leyendo: {ruta.name}", flush=True)

        try:
            paginas, resumen = extraer_documento(ruta)
        except Exception as error:
            raise SystemExit(
                f"No se pudo procesar {ruta.name}: {error}\n"
                "No se actualizaron los archivos de salida."
            ) from error

        todas_las_paginas.extend(paginas)
        inventario.append(resumen)

        print(
            f"  Páginas: {resumen['paginas']} | "
            f"Sin texto: {resumen['paginas_sin_texto']} | "
            f"Palabras: {resumen['palabras']}"
        )

    guardar_resultados(todas_las_paginas, inventario)

    print("\nExtracción finalizada.")
    print(f"Documentos: {len(inventario)}")
    print(f"Páginas: {len(todas_las_paginas)}")
    print(f"Resultados en: {SALIDA}")


if __name__ == "__main__":
    main()
