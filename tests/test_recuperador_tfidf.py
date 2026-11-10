"""Pruebas del contrato del recuperador TF-IDF."""

import json
import tempfile
import unittest
from pathlib import Path

from src.recuperador_tfidf import RecuperadorTFIDF


class TestRecuperadorTFIDF(unittest.TestCase):

    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "corpus.jsonl"

        # Dos textos idénticos permiten comprobar el desempate.
        # Se colocan en orden inverso al de sus identificadores.
        self.fragmentos = [
            {
                "id_fragmento": "fragmento-b",
                "documento": "ejemplo.pdf",
                "pagina": 2,
                "texto": "Regresión predicción",
            },
            {
                "id_fragmento": "fragmento-a",
                "documento": "ejemplo.pdf",
                "pagina": 1,
                "texto": "Regresión predicción",
            },
            {
                "id_fragmento": "fragmento-c",
                "documento": "ejemplo.pdf",
                "pagina": 3,
                "texto": "Fotosíntesis plantas",
            },
        ]

        self.escribir_corpus(self.fragmentos)
        self.recuperador = RecuperadorTFIDF(self.ruta)

    def escribir_corpus(self, fragmentos):
        with self.ruta.open("w", encoding="utf-8") as archivo:
            for fragmento in fragmentos:
                archivo.write(
                    json.dumps(fragmento, ensure_ascii=False) + "\n"
                )

    def test_recupera_el_fragmento_relacionado(self):
        resultados = self.recuperador.buscar("plantas", k=1)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(
            resultados[0]["id_fragmento"], "fragmento-c"
        )
        self.assertGreater(resultados[0]["puntaje"], 0)

    def test_desempata_por_identificador(self):
        resultados = self.recuperador.buscar("regresion", k=3)

        self.assertEqual(
            [r["id_fragmento"] for r in resultados],
            ["fragmento-a", "fragmento-b"],
        )
        self.assertAlmostEqual(
            resultados[0]["puntaje"],
            resultados[1]["puntaje"],
        )

    def test_respeta_k_y_no_duplica_resultados(self):
        for k in (1, 2, 10):
            with self.subTest(k=k):
                resultados = self.recuperador.buscar("regresion", k=k)
                ids = [r["id_fragmento"] for r in resultados]

                self.assertEqual(len(resultados), min(k, 2))
                self.assertEqual(len(ids), len(set(ids)))

    def test_conserva_texto_y_referencias(self):
        originales = {
            f["id_fragmento"]: f for f in self.fragmentos
        }

        for resultado in self.recuperador.buscar("regresion"):
            self.assertEqual(
                set(resultado),
                {"id_fragmento", "documento", "pagina", "texto", "puntaje"},
            )
            original = originales[resultado["id_fragmento"]]

            for campo in ("documento", "pagina", "texto"):
                self.assertEqual(resultado[campo], original[campo])

            self.assertIsInstance(resultado["puntaje"], float)

    def test_normaliza_mayusculas_y_tildes(self):
        self.assertEqual(
            self.recuperador.buscar("REGRESIÓN"),
            self.recuperador.buscar("regresion"),
        )

    def test_consulta_fuera_del_vocabulario(self):
        self.assertEqual(
            self.recuperador.buscar("zzzzinexistentezzzz"),
            [],
        )

    def test_rechaza_preguntas_invalidas(self):
        for pregunta in ("", "   ", None, 123):
            with self.subTest(pregunta=pregunta):
                with self.assertRaises(ValueError):
                    self.recuperador.buscar(pregunta)

    def test_rechaza_k_invalido(self):
        for k in (0, -1, 1.5, "3", True, None):
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    self.recuperador.buscar("regresion", k=k)

    def test_rechaza_corpus_vacio(self):
        self.escribir_corpus([])

        with self.assertRaisesRegex(ValueError, "vacío"):
            RecuperadorTFIDF(self.ruta)

    def test_rechaza_identificadores_duplicados(self):
        self.escribir_corpus([
            self.fragmentos[0],
            self.fragmentos[0],
        ])

        with self.assertRaisesRegex(ValueError, "duplicado"):
            RecuperadorTFIDF(self.ruta)

    def test_consultar_no_modifica_el_vocabulario(self):
        vocabulario_antes = dict(
            self.recuperador.vectorizador.vocabulary_
        )
        idf_antes = self.recuperador.vectorizador.idf_.copy()

        self.recuperador.buscar("regresion palabradesconocida")

        self.assertEqual(
            vocabulario_antes,
            self.recuperador.vectorizador.vocabulary_,
        )
        self.assertTrue(
            (idf_antes == self.recuperador.vectorizador.idf_).all()
        )


if __name__ == "__main__":
    unittest.main()
