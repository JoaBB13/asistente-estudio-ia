"""Selecciona páginas para búsqueda y registra todas las decisiones."""

import json
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
CARPETA = RAIZ / "data" / "processed"
ENTRADA = CARPETA / "paginas_limpias.jsonl"

PORTADAS = {
    "01 - Fundamentos IA_ML.pdf",
    "02 - Introducción al análisis de datos.pdf",
    "03 - Análisis exploratorio de datos (EDA).pdf",
    "04 - EDA - Causas e Identificacion de faltantes.pdf",
    "05 - Procesamiento y limpieza de datos.pdf",
    "06 - Procesamiento y nuevas features.pdf",
    "07 - Agentes y Búsqueda.pdf",
    "08 - Problemas de optimización.pdf",
    "09 - Aprendizaje automático.pdf",
    "10 - Regresión.pdf",
    "EXTRA - Computer Vision I.pdf",
}

TEXTOS_ESTRUCTURALES = {
    "¡Gracias! ¿Consultas? Ing. González H. Alexis",
    "Active Recall 01",
    "Main Content 02",
}

REVISION_VISUAL = {
    ("01 - Fundamentos IA_ML.pdf", 63): {
        "motivo": "contenido_visual_no_recuperado",
        "observacion": (
            "Tres cuadros con títulos, imágenes y explicaciones. "
            "Según revisión visual de Joaquín, el texto parece "
            "integrado en imágenes. La extracción solo recuperó el pie."
        ),
    },
    ("01 - Fundamentos IA_ML.pdf", 99): {
        "motivo": "contenido_visual_no_recuperado",
        "observacion": (
            "Esquema comparativo dividido por una cruz, con logos "
            "y palabras. La extracción solo recuperó el pie."
        ),
    },
    ("07 - Agentes y Búsqueda.pdf", 28): {
        "motivo": "sin_contenido_de_estudio",
        "observacion": (
            "Según revisión visual de Joaquín, contiene una cruz "
            "roja sin contenido de estudio legible."
        ),
    },
}

def decidir(pagina):
    clave = (pagina["documento"], pagina["pagina"])

    if clave in REVISION_VISUAL:
        revision = REVISION_VISUAL[clave]
        return False, revision["motivo"], False

    texto = " ".join(pagina["texto"].split())

    if not texto:
        return False, "sin_texto_extraido", True

    if pagina["pagina"] == 1 and pagina["documento"] in PORTADAS:
        return False, "portada_identificada", False

    if texto in TEXTOS_ESTRUCTURALES:
        return False, "separador_o_cierre_identificado", False

    if len(texto.split()) < 20:
        return True, "texto_breve_conservado", True

    return True, "texto_conservado", False

def guardar_jsonl(ruta, registros):
    temporal = ruta.with_suffix(".jsonl.tmp")

    with temporal.open("w", encoding="utf-8") as archivo:
        for registro in registros:
            archivo.write(
                json.dumps(registro, ensure_ascii=False) + "\n"
            )

    temporal.replace(ruta)


def main():
    with ENTRADA.open(encoding="utf-8") as archivo:
        paginas = [
            json.loads(linea)
            for linea in archivo
            if linea.strip()
        ]

    if not paginas:
        raise SystemExit("El corpus de entrada está vacío.")

    ids = [p["id_pagina"] for p in paginas]

    if len(ids) != len(set(ids)):
        raise SystemExit(
            "Hay identificadores repetidos. Revisar antes de continuar."
        )

    corpus = []
    decisiones = []

    for pagina in paginas:
        incluir, motivo, revisar = decidir(pagina)

        decisiones.append({
            "id_pagina": pagina["id_pagina"],
            "documento": pagina["documento"],
            "pagina": pagina["pagina"],
            "incluir": incluir,
            "motivo": motivo,
            "revision_visual_pendiente": revisar,
            "observacion": REVISION_VISUAL.get(
              (pagina["documento"], pagina["pagina"]), {}
            ).get("observacion", ""),
            "version_seleccion": "2",
            })

        if incluir:
            corpus.append({
                "id_fragmento": pagina["id_pagina"],
                "documento": pagina["documento"],
                "pagina": pagina["pagina"],
                "sha256": pagina["sha256"],
                "texto": pagina["texto"],
                "revision_visual_pendiente": revisar,
            })

    guardar_jsonl(CARPETA / "corpus_busqueda.jsonl", corpus)
    guardar_jsonl(CARPETA / "decisiones_paginas.jsonl", decisiones)

    print(f"Páginas originales: {len(paginas)}")
    print(f"Páginas incluidas: {len(corpus)}")
    print(f"Páginas excluidas: {len(paginas) - len(corpus)}")

    print("\nDecisiones por motivo:")
    for motivo, cantidad in sorted(
        Counter(d["motivo"] for d in decisiones).items()
    ):
        print(f"- {motivo}: {cantidad}")

    print("\nGenerados:")
    print(CARPETA / "corpus_busqueda.jsonl")
    print(CARPETA / "decisiones_paginas.jsonl")


if __name__ == "__main__":
    main()
