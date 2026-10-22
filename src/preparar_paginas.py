"""Prepara un registro por diapositiva, conservando texto y procedencia."""

import hashlib
import json
from pathlib import Path

import pymupdf

from limpieza import limpiar_texto


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "raw"
SALIDA = RAIZ / "data" / "processed"


def procesar_documento(ruta):
    huella = hashlib.sha256(ruta.read_bytes()).hexdigest()
    registros = []

    with pymupdf.open(ruta) as documento:
        if documento.is_encrypted:
            raise ValueError(f"El PDF está cifrado: {ruta.name}")

        for numero, pagina in enumerate(documento, start=1):
            bloques = pagina.get_text("blocks", sort=False)

            bloques_texto = [
                bloque for bloque in bloques if bloque[6] == 0
            ]

            texto_original = "\n\n".join(
                bloque[4] for bloque in bloques_texto
            )

            texto_limpio = limpiar_texto(texto_original)

            registros.append({
                "id_pagina": f"{huella}:p{numero:04d}",
                "documento": ruta.name,
                "sha256": huella,
                "pagina": numero,
                "texto_original": texto_original,
                "texto": texto_limpio,
                "palabras": len(texto_limpio.split()),
                "sin_texto": not texto_limpio,
                "extractor": "pymupdf",
                "version_extractor": pymupdf.VersionBind,
                "modo_extraccion": "blocks",
                "ordenar_texto": False,
                "version_limpieza": "1",
            })

    return registros


def main():
    if not ENTRADA.is_dir():
        raise SystemExit(f"No existe la carpeta: {ENTRADA}")

    documentos = sorted(
        ruta for ruta in ENTRADA.iterdir()
        if ruta.is_file() and ruta.suffix.lower() == ".pdf"
    )

    if not documentos:
        raise SystemExit("No se encontraron PDF en data/raw.")

    paginas = []

    for ruta in documentos:
        print(f"Procesando: {ruta.name}", flush=True)

        try:
            registros = procesar_documento(ruta)
        except Exception as error:
            raise SystemExit(
                f"Error al procesar {ruta.name}: {error}\n"
                "No se actualizó el archivo de salida."
            ) from error

        paginas.extend(registros)

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / "paginas_limpias.jsonl"
    temporal = destino.with_suffix(".jsonl.tmp")

    with temporal.open("w", encoding="utf-8") as archivo:
        for pagina in paginas:
            archivo.write(json.dumps(pagina, ensure_ascii=False) + "\n")

    temporal.replace(destino)

    print("\nPreparación finalizada.")
    print(f"Documentos: {len(documentos)}")
    print(f"Páginas: {len(paginas)}")
    print(f"Palabras: {sum(p['palabras'] for p in paginas)}")
    print(f"Páginas sin texto limpio: {sum(p['sin_texto'] for p in paginas)}")
    print(f"Archivo generado: {destino}")


if __name__ == "__main__":
    main()
