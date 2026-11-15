"""Evaluación final: configuración fija y resultados conservados."""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import generador_qwen3 as g
from asistente_estudio import AsistenteEstudio
from evaluar_generacion_qwen3 import guardar, huella, leer_jsonl
from recuperador_tfidf import RecuperadorTFIDF

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "data/evaluacion/final_mvp_v1"

SHA_CORPUS = (
    "50eacef90daf99538ee6e78fa5a508a4444"
    "aad995bc72c91a60f4c0e573224a0"
)
SHA_FINAL = (
    "11676e3f0260abeca574da32a7386558ca8"
    "a6a37eb035992a8a83776efb2face"
)


def main():
    corpus = RAIZ / "data/processed/corpus_busqueda.jsonl"
    preguntas = RAIZ / "data/evaluacion/preguntas_final.jsonl"

    if huella(corpus) != SHA_CORPUS or huella(preguntas) != SHA_FINAL:
        raise ValueError(
            "No coincide la versión reservada del corpus o preguntas."
        )

    casos = list(leer_jsonl(preguntas, "id").values())

    if (
        len(casos) != 20
        or sum(c["respondible"] is True for c in casos) != 16
    ):
        raise ValueError("Se esperaban 20 casos, 16 respondibles.")

    for caso in casos:
        if (
            caso["particion"] != "final"
            or caso["corpus_sha256"] != SHA_CORPUS
        ):
            raise ValueError("Partición o corpus incorrecto.")

    modelos = g.api("/api/tags")["models"]
    modelo = next(m for m in modelos if m["name"] == g.MODELO)

    nombres = [
        "asistente_estudio.py",
        "generador_qwen3.py",
        "recuperador_embeddings.py",
        "recuperador_tfidf.py",
        "evaluar_generacion_qwen3.py",
        Path(__file__).name,
    ]

    configuracion = {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=RAIZ,
            text=True,
        ).strip(),
        "codigo_sha256": {
            n: huella(RAIZ / "src" / n) for n in nombres
        },
        "python": sys.version,
        "dependencias": subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"],
            text=True,
        ).splitlines(),
        "corpus_sha256": SHA_CORPUS,
        "preguntas_sha256": SHA_FINAL,
        "modelo": g.MODELO,
        "modelo_digest": modelo["digest"],
        "ollama_version": g.api("/api/version")["version"],
        "opciones": g.OPCIONES,
        "instrucciones": g.INSTRUCCIONES,
        "k": 3,
    }

    DESTINO.mkdir(parents=True, exist_ok=True)
    manifiesto = DESTINO / "configuracion.json"

    if manifiesto.exists():
        anterior = json.loads(
            manifiesto.read_text(encoding="utf-8")
        )
        if anterior != configuracion:
            raise ValueError(
                "Cambió la configuración. Conservá esta evaluación."
            )
    else:
        guardar(manifiesto, configuracion)

    asistente = None
    baseline = None
    registros = []

    for numero, caso in enumerate(casos, 1):
        archivo = DESTINO / f"caso_{numero:03d}.json"
        print(f"\n[{numero}/20] {caso['id']}", flush=True)

        if archivo.exists():
            registro = json.loads(
                archivo.read_text(encoding="utf-8")
            )
            if registro["caso_id"] != caso["id"]:
                raise ValueError("Registro previo de otro caso.")

            print(
                "Se conserva el resultado anterior, "
                "incluidos sus errores."
            )
        else:
            if asistente is None:
                asistente = AsistenteEstudio()
                baseline = RecuperadorTFIDF()

            # Solo se envía la pregunta al asistente.
            # Nunca se envían criterios ni respuestas esperadas.
            registro = asistente.responder(
                caso["pregunta"],
                k=3,
            )

            try:
                registro["resultados_tfidf"] = baseline.buscar(
                    caso["pregunta"],
                    k=3,
                )
            except Exception as error:
                registro["resultados_tfidf"] = []
                registro["error_tfidf"] = (
                    f"{type(error).__name__}: {error}"
                )

            # Las referencias se agregan después de responder.
            registro["caso_id"] = caso["id"]
            registro["referencia_evaluacion"] = caso
            registro["revision_humana"] = {
                "estado": "pendiente"
            }

            for clave in ("modelo_digest", "ollama_version"):
                if (
                    clave in registro
                    and registro[clave] != configuracion[clave]
                ):
                    registro["incidencia_configuracion"] = clave

            guardar(archivo, registro)

        registros.append(registro)
        g.mostrar(registro)

        if registro.get("incidencia_configuracion"):
            raise ValueError(
                "Cambió el servicio/modelo. "
                "Revisar antes de continuar."
            )

    resumen = {
        "casos": len(registros),
        "controles_generacion": dict(Counter(
            r["control_automatico"] for r in registros
        )),
        "revision_humana": (
            "pendiente; no se mide calidad con estos conteos"
        ),
        "errores_tfidf": sum(
            "error_tfidf" in r for r in registros
        ),
    }

    for metodo, clave in (
        ("embeddings", "recuperados"),
        ("tfidf", "resultados_tfidf"),
    ):
        aciertos = 0
        completos = 0
        total_grupos = 0

        for caso, registro in zip(casos, registros):
            if not caso["respondible"]:
                continue

            ids = {
                r["id_fragmento"]
                for r in registro.get(clave, [])
            }
            esperados = {
                e["id_fragmento"]
                for e in caso["evidencias"]
            }

            aciertos += bool(ids & esperados)
            grupos = caso.get("grupos_evidencia_requeridos")

            if grupos:
                total_grupos += 1
                completos += all(
                    ids & set(grupo)
                    for grupo in grupos
                )

        resumen[metodo] = {
            "hit3_aciertos": aciertos,
            "hit3_total": 16,
            "hit3_porcentaje": round(
                100 * aciertos / 16, 2
            ),
            "cobertura_completa_aciertos": completos,
            "cobertura_completa_total": total_grupos,
        }

    guardar(DESTINO / "resumen.json", resumen)

    print("\nRESUMEN DE RECUPERACIÓN Y EJECUCIÓN:")
    print(json.dumps(
        resumen,
        ensure_ascii=False,
        indent=2,
    ))
    print("Registros para revisión humana:", DESTINO)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\nInterrumpido. Repetí el comando "
            "para retomar los casos guardados."
        )