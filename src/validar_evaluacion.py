"""Valida el formato de las preguntas y sus referencias al corpus."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def es_texto(valor):
    return isinstance(valor, str) and bool(valor.strip())


def cargar_jsonl(ruta):
    registros = []

    with ruta.open(encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue

            try:
                registro = json.loads(linea)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{ruta.name}, línea {numero}: JSON inválido."
                ) from error

            exigir(
                isinstance(registro, dict),
                f"{ruta.name}, línea {numero}: se esperaba un objeto.",
            )
            registros.append(registro)

    exigir(registros, f"{ruta.name}: el archivo no contiene registros.")
    return registros


def indexar_corpus(registros):
    indice = {}

    for numero, registro in enumerate(registros, start=1):
        contexto = f"Corpus, registro {numero}"

        for campo in ("id_fragmento", "documento", "texto"):
            exigir(
                es_texto(registro.get(campo)),
                f"{contexto}: '{campo}' debe ser texto no vacío.",
            )

        pagina = registro.get("pagina")
        exigir(
            type(pagina) is int and pagina > 0,
            f"{contexto}: 'pagina' debe ser un entero positivo.",
        )

        identificador = registro["id_fragmento"]
        exigir(
            identificador not in indice,
            f"{contexto}: ID duplicado: {identificador}.",
        )
        indice[identificador] = registro

    return indice


def validar_casos(casos, corpus, huella, particion):
    ids = set()

    for numero, caso in enumerate(casos, start=1):
        contexto = f"Caso {numero}"

        for campo in (
            "id",
            "particion",
            "pregunta",
            "respuesta_referencia",
            "corpus_sha256",
        ):
            exigir(
                es_texto(caso.get(campo)),
                f"{contexto}: '{campo}' debe ser texto no vacío.",
            )

        identificador = caso["id"]
        contexto = identificador

        exigir(
            identificador not in ids,
            f"{contexto}: identificador duplicado.",
        )
        ids.add(identificador)

        exigir(
            caso["particion"] == particion,
            f"{contexto}: la partición debe ser '{particion}'.",
        )
        exigir(
            caso["corpus_sha256"] == huella,
            f"{contexto}: la huella no coincide con el corpus actual.",
        )
        exigir(
            type(caso.get("respondible")) is bool,
            f"{contexto}: 'respondible' debe ser true o false.",
        )
        exigir(
            isinstance(caso.get("observaciones"), str),
            f"{contexto}: falta 'observaciones' o no es texto.",
        )

        criterios = caso.get("criterios_respuesta")
        exigir(
            isinstance(criterios, list)
            and bool(criterios)
            and all(es_texto(criterio) for criterio in criterios),
            f"{contexto}: se requiere una lista de criterios no vacíos.",
        )

        evidencias = caso.get("evidencias")
        exigir(
            isinstance(evidencias, list),
            f"{contexto}: 'evidencias' debe ser una lista.",
        )

        if caso["respondible"]:
            exigir(
                bool(evidencias),
                f"{contexto}: una pregunta respondible necesita evidencias.",
            )
        else:
            exigir(
                not evidencias,
                f"{contexto}: una pregunta no respondible debe tener "
                "'evidencias': [].",
            )

        ids_evidencias = set()

        for referencia in evidencias:
            exigir(
                isinstance(referencia, dict),
                f"{contexto}: cada evidencia debe ser un objeto.",
            )

            id_fragmento = referencia.get("id_fragmento")
            exigir(
                es_texto(id_fragmento),
                f"{contexto}: evidencia sin identificador válido.",
            )
            exigir(
                id_fragmento not in ids_evidencias,
                f"{contexto}: evidencia repetida.",
            )
            ids_evidencias.add(id_fragmento)

            fragmento = corpus.get(id_fragmento)
            exigir(
                fragmento is not None,
                f"{contexto}: el fragmento no existe en el corpus.",
            )
            exigir(
                es_texto(referencia.get("documento"))
                and referencia["documento"] == fragmento["documento"],
                f"{contexto}: el documento de la evidencia no coincide.",
            )
            exigir(
                type(referencia.get("pagina")) is int
                and referencia["pagina"] == fragmento["pagina"],
                f"{contexto}: la página de la evidencia no coincide.",
            )

        if "grupos_evidencia_requeridos" in caso:
            grupos = caso["grupos_evidencia_requeridos"]

            exigir(
                caso["respondible"],
                f"{contexto}: los grupos requieren un caso respondible.",
            )
            exigir(
                isinstance(grupos, list) and bool(grupos),
                f"{contexto}: se requiere una lista no vacía de grupos.",
            )

            grupos_vistos = set()

            for grupo in grupos:
                exigir(
                    isinstance(grupo, list)
                    and bool(grupo)
                    and all(es_texto(elemento) for elemento in grupo),
                    f"{contexto}: cada grupo debe contener IDs válidos.",
                )
                exigir(
                    len(grupo) == len(set(grupo)),
                    f"{contexto}: hay IDs repetidos dentro de un grupo.",
                )
                exigir(
                    set(grupo).issubset(ids_evidencias),
                    f"{contexto}: un grupo utiliza IDs no declarados "
                    "en las evidencias.",
                )

                clave = frozenset(grupo)
                exigir(
                    clave not in grupos_vistos,
                    f"{contexto}: hay grupos idénticos repetidos.",
                )
                grupos_vistos.add(clave)

def validar_reformulaciones(casos):
    """Comprueba que cada variante apunte a un caso base compatible."""
    por_id = {caso["id"]: caso for caso in casos}

    for caso in casos:
        if "caso_origen" not in caso:
            continue

        identificador = caso["id"]
        id_origen = caso["caso_origen"]

        exigir(
            es_texto(id_origen),
            f"{identificador}: 'caso_origen' debe ser texto no vacío.",
        )
        exigir(
            id_origen != identificador,
            f"{identificador}: no puede ser su propio caso de origen.",
        )

        origen = por_id.get(id_origen)
        exigir(
            origen is not None,
            f"{identificador}: el caso de origen no existe.",
        )
        exigir(
            "caso_origen" not in origen,
            f"{identificador}: debe apuntar a un caso base, no a otra variante.",
        )
        exigir(
            origen["particion"] == caso["particion"],
            f"{identificador}: la partición no coincide con la del origen.",
        )
        exigir(
            origen["respondible"] == caso["respondible"],
            f"{identificador}: 'respondible' no coincide con el origen.",
        )
        exigir(
            origen["corpus_sha256"] == caso["corpus_sha256"],
            f"{identificador}: el corpus no coincide con el del origen.",
        )

def main():
    parser = argparse.ArgumentParser(
        description="Valida preguntas y referencias sin modificar archivos."
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=RAIZ / "data/processed/corpus_busqueda.jsonl",
    )
    parser.add_argument(
        "--preguntas",
        type=Path,
        default=RAIZ / "data/evaluacion/preguntas_desarrollo.jsonl",
    )
    parser.add_argument(
        "--particion",
        choices=("desarrollo", "final"),
        default="desarrollo",
    )
    argumentos = parser.parse_args()

    try:
        registros = cargar_jsonl(argumentos.corpus)
        corpus = indexar_corpus(registros)
        casos = cargar_jsonl(argumentos.preguntas)
        huella = hashlib.sha256(argumentos.corpus.read_bytes()).hexdigest()

        validar_casos(casos, corpus, huella, argumentos.particion)
        
        validar_reformulaciones(casos)

    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    respondibles = sum(caso["respondible"] for caso in casos)
    con_grupos = sum(
        "grupos_evidencia_requeridos" in caso
        for caso in casos
    )

    print("Validación estructural y de referencias: correcta.")
    print(f"Fragmentos del corpus: {len(corpus)}")
    print(f"Preguntas: {len(casos)}")
    print(f"Respondibles: {respondibles}")
    print(f"No respondibles: {len(casos) - respondibles}")
    print(f"Casos con grupos de evidencias: {con_grupos}")
    print(f"SHA-256 del corpus: {huella}")
    print("La validez conceptual requiere revisión humana.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())