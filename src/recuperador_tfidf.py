"""Recuperador de diapositivas basado en TF-IDF."""

import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

# Ubica el corpus a partir de la ubicación de este archivo.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_CORPUS = RAIZ_PROYECTO / "data/processed/corpus_busqueda.jsonl"


def cargar_corpus(ruta=RUTA_CORPUS):
    """Lee el corpus JSONL y verifica los campos necesarios."""
    ruta = Path(ruta)
    fragmentos = []
    identificadores = set()
    campos = {"id_fragmento", "documento", "pagina", "texto"}

    with ruta.open(encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue

            try:
                fragmento = json.loads(linea)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"JSON inválido en la línea {numero_linea}."
                ) from error

            if not isinstance(fragmento, dict):
                raise ValueError(
                    f"La línea {numero_linea} debe contener un objeto."
                )

            faltantes = campos - fragmento.keys()
            if faltantes:
                raise ValueError(
                    f"Línea {numero_linea}: faltan {sorted(faltantes)}."
                )

            identificador = fragmento["id_fragmento"]

            if not isinstance(identificador, str) or not identificador.strip():
                raise ValueError(
                    f"Identificador inválido en la línea {numero_linea}."
                )

            if identificador in identificadores:
                raise ValueError(
                    f"Identificador duplicado: {identificador}."
                )

            if not isinstance(fragmento["texto"], str):
                raise ValueError(
                    f"El texto de {identificador} debe ser una cadena."
                )

            identificadores.add(identificador)
            fragmentos.append(fragmento)

    if not fragmentos:
        raise ValueError("El corpus está vacío.")

    return fragmentos
