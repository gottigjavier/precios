import tempfile
import json
from pathlib import Path


class TestGUIComponents:
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

            assert len(mercados) == 2
            assert mercados[0]["id"] == "masonline"
            assert mercados[0]["name"] == "MASOnline"

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

            assert len(rows) == 2
            assert rows[0]["producto"] == "Producto 1"
            assert rows[1]["producto"] == "Producto 2"

    def test_gui_imports(self):
        import main_gui

        assert main_gui is not None
