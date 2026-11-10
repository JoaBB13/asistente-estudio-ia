import hashlib
import json
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

import numpy as np


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from recuperador_embeddings import RecuperadorEmbeddings


class TokenizadorSimulado:
    truncation_side = "right"

    def __call__(self, texto, **opciones):
        return {
            "input_ids": list(range(len(texto.split()) + 2))
        }


class ModeloSimulado:
    max_seq_length = 12
    tokenizer = TokenizadorSimulado()

    def __init__(self):
        self.llamadas = []

    def encode(self, textos, **opciones):
        self.llamadas.append((list(textos), opciones))

        return np.array([
            [0.0, 1.0] if "otro" in texto else [1.0, 0.0]
            for texto in textos
        ])


class TestRecuperadorEmbeddings(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)

        self.ruta = Path(temporal.name) / "corpus.jsonl"

        self.registros = [
            {
                "id_fragmento": "b",
                "documento": "Clase.pdf",
                "pagina": 2,
                "texto": "ÁRBOL y métrica",
            },
            {
                "id_fragmento": "a",
                "documento": "Clase.pdf",
                "pagina": 1,
                "texto": "ÁRBOL y métrica",
            },
            {
                "id_fragmento": "c",
                "documento": "Otro.pdf",
                "pagina": 3,
                "texto": "otro tema",
            },
        ]

        self.escribir(self.registros)
        self.modelo = ModeloSimulado()

        simulacion = patch(
            "recuperador_embeddings.cargar_modelo",
            return_value=(self.modelo, "a" * 40),
        )
        simulacion.start()
        self.addCleanup(simulacion.stop)

    def escribir(self, registros):
        self.ruta.write_text(
            "\n".join(
                json.dumps(registro, ensure_ascii=False)
                for registro in registros
            ),
            encoding="utf-8",
        )

    def crear(self):
        return RecuperadorEmbeddings(self.ruta)

    def test_orden_desempate_limite_y_referencias(self):
        recuperador = self.crear()
        resultados = recuperador.buscar("métrica", k=2)

        self.assertEqual(
            [r["id_fragmento"] for r in resultados],
            ["a", "b"],
        )

        for resultado in resultados:
            original = next(
                r for r in self.registros
                if r["id_fragmento"] == resultado["id_fragmento"]
            )

            sin_puntaje = {
                clave: valor
                for clave, valor in resultado.items()
                if clave != "puntaje"
            }

            self.assertEqual(sin_puntaje, original)
            self.assertEqual(resultado["puntaje"], 1.0)

        self.assertEqual(
            len(recuperador.buscar("métrica", k=99)),
            3,
        )

    def test_rechaza_preguntas_invalidas(self):
        recuperador = self.crear()

        for pregunta in ("", "  ", None, 42):
            with self.subTest(pregunta=pregunta):
                with self.assertRaises(ValueError):
                    recuperador.buscar(pregunta)

    def test_rechaza_k_invalido(self):
        recuperador = self.crear()

        for k in (0, -1, 1.5, "3", True, None):
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    recuperador.buscar("métrica", k=k)

    def test_rechaza_corpus_vacio(self):
        self.escribir([])

        with self.assertRaisesRegex(ValueError, "vacío"):
            self.crear()

    def test_rechaza_identificadores_duplicados(self):
        self.escribir([
            self.registros[0],
            self.registros[0],
        ])

        with self.assertRaisesRegex(ValueError, "duplicado"):
            self.crear()

    def test_prefijos_y_reutilizacion_del_indice(self):
        recuperador = self.crear()
        recuperador.buscar("  ¿QUÉ es una MÉTRICA?  ")

        # Una llamada para el corpus y otra para la pregunta.
        self.assertEqual(len(self.modelo.llamadas), 2)

        self.assertEqual(
            self.modelo.llamadas[0][0][0],
            "passage: ÁRBOL y métrica",
        )
        self.assertEqual(
            self.modelo.llamadas[1][0],
            ["query: ¿QUÉ es una MÉTRICA?"],
        )

        for textos, opciones in self.modelo.llamadas:
            self.assertTrue(opciones["normalize_embeddings"])
            self.assertEqual(opciones["prompt"], "")

    def test_registra_truncamientos_y_conserva_texto(self):
        self.registros[0]["texto"] = "métrica " * 20
        self.escribir(self.registros)

        with warnings.catch_warnings(record=True) as avisos:
            warnings.simplefilter("always")
            recuperador = self.crear()
            resultados = recuperador.buscar("pregunta " * 20)

        self.assertEqual(len(avisos), 2)

        truncados = recuperador.metadatos["documentos_truncados"]
        self.assertEqual(len(truncados), 1)
        self.assertEqual(truncados[0]["id_fragmento"], "b")

        self.assertEqual(
            len(recuperador.metadatos["consultas_truncadas"]),
            1,
        )

        texto_devuelto = next(
            r["texto"]
            for r in resultados
            if r["id_fragmento"] == "b"
        )

        self.assertEqual(
            texto_devuelto,
            self.registros[0]["texto"],
        )

    def test_guarda_revision_y_huella_del_corpus(self):
        recuperador = self.crear()
        destino = self.ruta.parent / "registro.json"
        recuperador.guardar_metadatos(destino)

        datos = json.loads(
            destino.read_text(encoding="utf-8")
        )

        huella_esperada = hashlib.sha256(
            self.ruta.read_bytes()
        ).hexdigest()

        self.assertEqual(datos["corpus_sha256"], huella_esperada)
        self.assertEqual(datos["revision"], "a" * 40)
        self.assertEqual(datos["cantidad_fragmentos"], 3)


if __name__ == "__main__":
    unittest.main()