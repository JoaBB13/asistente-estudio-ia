import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from asistente_estudio import AsistenteEstudio, guardar_registro


class TestAsistenteEstudio(unittest.TestCase):
    def setUp(self):
        self.fragmentos = [{
            "id_fragmento": "f1",
            "documento": "clase.pdf",
            "pagina": 2,
            "texto": "Texto original",
            "puntaje": 0.8,
        }]

        self.recuperador = Mock()
        self.recuperador.buscar.return_value = self.fragmentos
        self.recuperador.metadatos = {
            "corpus_sha256": "huella",
            "consultas_truncadas": [],
        }

        self.generar = Mock(return_value={
            "control_automatico": (
                "estructura_e_identificadores_comprobados"
            ),
        })

        self.asistente = AsistenteEstudio(
            self.recuperador,
            self.generar,
        )

    def test_conecta_busqueda_y_generacion_con_referencias(self):
        registro = self.asistente.responder("Consulta", k=2)

        self.recuperador.buscar.assert_called_once_with(
            "Consulta", k=2
        )
        self.generar.assert_called_once_with(
            "Consulta", self.fragmentos
        )

        self.assertEqual(registro["corpus_sha256"], "huella")
        self.assertEqual(registro["recuperados"][0]["pagina"], 2)

    def test_metadatos_guardados_no_cambian_con_consultas_posteriores(self):
        registro = self.asistente.responder("Consulta")

        self.recuperador.metadatos["consultas_truncadas"].append(
            "otra"
        )

        self.assertEqual(
            registro["configuracion_recuperacion"][
                "consultas_truncadas"
            ],
            [],
        )

    def test_entrada_invalida_no_dispara_busqueda_ni_generacion(self):
        casos = [
            (" ", 3),
            (None, 3),
            ("Pregunta", 0),
            ("Pregunta", True),
        ]

        for pregunta, k in casos:
            with (
                self.subTest(pregunta=pregunta, k=k),
                self.assertRaises(ValueError),
            ):
                self.asistente.responder(pregunta, k)

        self.recuperador.buscar.assert_not_called()
        self.generar.assert_not_called()

    def test_error_recuperacion_no_se_convierte_en_abstencion(self):
        self.recuperador.buscar.side_effect = OSError(
            "corpus inaccesible"
        )

        registro = self.asistente.responder("Consulta")

        self.assertEqual(
            registro["control_automatico"],
            "error_tecnico",
        )
        self.assertEqual(registro["fase_error"], "recuperacion")
        self.assertNotIn("estado_derivado", registro)
        self.generar.assert_not_called()

    def test_error_generacion_no_se_convierte_en_abstencion(self):
        self.generar.side_effect = TimeoutError(
            "servicio sin respuesta"
        )

        registro = self.asistente.responder("Consulta")

        self.assertEqual(
            registro["control_automatico"],
            "error_tecnico",
        )
        self.assertEqual(registro["fase_error"], "generacion")
        self.assertNotIn("estado_derivado", registro)

    def test_guarda_consultas_sin_sobrescribir(self):
        registro = self.asistente.responder("Consulta")

        with tempfile.TemporaryDirectory() as carpeta:
            primero = guardar_registro(registro, carpeta)
            segundo = guardar_registro(registro, carpeta)

            self.assertNotEqual(primero, segundo)

            self.assertEqual(
                json.loads(
                    primero.read_text(encoding="utf-8")
                ),
                registro,
            )

            self.assertTrue(segundo.exists())


if __name__ == "__main__":
    unittest.main()