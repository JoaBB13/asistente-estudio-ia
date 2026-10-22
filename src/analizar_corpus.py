"""Analiza las páginas preparadas sin modificar el corpus."""

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "processed" / "paginas_limpias.jsonl"
SALIDA = RAIZ / "data" / "processed" / "eda"


def cargar_paginas():
    with ENTRADA.open(encoding="utf-8") as archivo:
        paginas = [
            json.loads(linea)
            for linea in archivo
            if linea.strip()
        ]

    if not paginas:
        raise ValueError("El archivo de páginas está vacío.")

    return paginas


def resumir(paginas):
    longitudes = [len(p["texto"].split()) for p in paginas]

    return {
        "paginas": len(paginas),
        "palabras": sum(longitudes),
        "minimo": min(longitudes),
        "mediana": statistics.median(longitudes),
        "promedio": round(statistics.mean(longitudes), 2),
        "maximo": max(longitudes),
        "sin_texto": sum(n == 0 for n in longitudes),
        "menos_de_20_palabras": sum(n < 20 for n in longitudes),
    }


def buscar_duplicados(paginas):
    grupos = defaultdict(list)

    for pagina in paginas:
        # Solo se unifican espacios para comparar.
        texto = " ".join(pagina["texto"].split())

        if texto:
            grupos[texto].append({
                "documento": pagina["documento"],
                "pagina": pagina["pagina"],
                "id_pagina": pagina["id_pagina"],
            })

    return [
        {
            "texto_comparado": texto,
            "apariciones": apariciones,
        }
        for texto, apariciones in grupos.items()
        if len(apariciones) > 1
    ]


def main():
    paginas = cargar_paginas()
    por_documento = defaultdict(list)

    for pagina in paginas:
        por_documento[pagina["documento"]].append(pagina)

    resumen = {
        "documentos": len(por_documento),
        "global": resumir(paginas),
        "por_documento": {
            nombre: resumir(registros)
            for nombre, registros in sorted(por_documento.items())
        },
    }

    duplicados = buscar_duplicados(paginas)
    SALIDA.mkdir(parents=True, exist_ok=True)

    with (SALIDA / "resumen.json").open(
        "w", encoding="utf-8"
    ) as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)

    with (SALIDA / "duplicados.json").open(
        "w", encoding="utf-8"
    ) as archivo:
        json.dump(duplicados, archivo, ensure_ascii=False, indent=2)

    with (SALIDA / "paginas_para_revision.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as archivo:
        campos = ["documento", "pagina", "palabras", "motivo", "vista_previa"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()

        for pagina in paginas:
            texto = pagina["texto"]
            palabras = len(texto.split())
            motivos = []

            if palabras < 20:
                motivos.append("menos_de_20_palabras")

            if "\ufffd" in texto:
                motivos.append("caracter_de_reemplazo")

            if motivos:
                escritor.writerow({
                    "documento": pagina["documento"],
                    "pagina": pagina["pagina"],
                    "palabras": palabras,
                    "motivo": "; ".join(motivos),
                    "vista_previa": " ".join(texto.split())[:180],
                })

    print("RESUMEN GLOBAL")
    print(f"Documentos: {resumen['documentos']}")

    for nombre, valor in resumen["global"].items():
        print(f"{nombre}: {valor}")

    print("\nRESUMEN POR DOCUMENTO")

    for nombre, datos in resumen["por_documento"].items():
        print(f"\n{nombre}")
        print(
            f"  Páginas: {datos['paginas']} | "
            f"Palabras: {datos['palabras']} | "
            f"Mediana: {datos['mediana']} | "
            f"Páginas con menos de 20 palabras: "
            f"{datos['menos_de_20_palabras']}"
        )

    print(f"\nGrupos de texto duplicado: {len(duplicados)}")

    for grupo in duplicados[:5]:
        print("\nTexto:", grupo["texto_comparado"][:100])

        for aparicion in grupo["apariciones"][:6]:
            print(
                f"  - {aparicion['documento']} "
                f"| página {aparicion['pagina']}"
            )

    print(f"\nInformes guardados en: {SALIDA}")


if __name__ == "__main__":
    main()
