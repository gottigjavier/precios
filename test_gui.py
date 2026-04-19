import json
import tempfile
import unittest
from pathlib import Path


class TestGUIComponents(unittest.TestCase):
    def test_supermarkets_loaded_from_file(self):
        from gui import load_supermarkets_data

        with tempfile.TemporaryDirectory() as tmpdir:
            mercados_file = Path(tmpdir) / "supermercados.json"
            with open(mercados_file, "w") as f:
                json.dump(
                    [
                        {"id": "masonline", "name": "MASOnline"},
                        {"id": "dia", "name": "DIA"},
                    ],
                    f,
                )

            mercados = load_supermarkets_data(str(mercados_file))

            self.assertEqual(len(mercados), 2)
            self.assertEqual(mercados[0]["id"], "masonline")
            self.assertEqual(mercados[0]["name"], "MASOnline")

    def test_results_loaded_from_file(self):
        from gui import load_results_data

        with tempfile.TemporaryDirectory() as tmpdir:
            resultados_file = Path(tmpdir) / "resultados.json"
            with open(resultados_file, "w") as f:
                json.dump(
                    {
                        "productos": [
                            {
                                "resultados": [
                                    {
                                        "nombre": "Producto 1",
                                        "marca": "Marca A",
                                        "precio": 100,
                                        "supermercado": "masonline",
                                    },
                                    {
                                        "nombre": "Producto 2",
                                        "marca": "Marca B",
                                        "precio": 200,
                                        "supermercado": "dia",
                                    },
                                ]
                            }
                        ]
                    },
                    f,
                )

            rows = load_results_data(str(resultados_file))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["producto"], "Producto 1")
            self.assertEqual(rows[1]["producto"], "Producto 2")

    def test_gui_imports(self):
        try:
            import main_gui

            self.assertIsNotNone(main_gui)
        except ModuleNotFoundError:
            self.skipTest("dearpygui not installed")
