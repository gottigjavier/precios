import json
import tempfile
from pathlib import Path


class TestMultipleProducts:
    def test_save_multiple_products(self):
        from app import save_multiple_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            products_list = [
                {"producto": "leche", "marca": "serenisima", "tamaño": "1L"},
                {"producto": "pan", "marca": "bimbo", "tamaño": "500g"},
            ]
            save_multiple_products(products_list, products_file)

            with open(products_file) as f:
                data = json.load(f)

            assert len(data) == 2
            assert data[0]["producto"] == "leche"
            assert data[1]["producto"] == "pan"

    def test_save_multiple_products_empty_list(self):
        from app import save_multiple_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_multiple_products([], products_file)

            with open(products_file) as f:
                data = json.load(f)

            assert data == []


class TestProductsJSON:
    def test_save_products_overwrites_file(self):
        from app import save_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_products("leche", "la serenisima", "1L", products_file)
            with open(products_file) as f:
                data = json.load(f)
            assert data == [
                {"producto": "leche", "marca": "la serenisima", "tamaño": "1L"}
            ]

            save_products("pan", "bimbo", "500g", products_file)
            with open(products_file) as f:
                data = json.load(f)
            assert data == [{"producto": "pan", "marca": "bimbo", "tamaño": "500g"}]

    def test_products_format(self):
        from app import save_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_products("test_product", "test_brand", "test_size", products_file)

            with open(products_file) as f:
                data = json.load(f)

            assert len(data) == 1
            assert "producto" in data[0]
            assert "marca" in data[0]
            assert "tamaño" in data[0]
            assert data[0]["producto"] == "test_product"
            assert data[0]["marca"] == "test_brand"
            assert data[0]["tamaño"] == "test_size"


class TestSupermarkets:
    def test_load_supermarkets(self):
        from app import load_supermarkets

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

            mercados = load_supermarkets(mercados_file)

            assert len(mercados) == 2
            assert mercados[0]["id"] == "masonline"
            assert mercados[0]["name"] == "MASOnline"
            assert mercados[1]["id"] == "dia"
            assert mercados[1]["name"] == "DIA"

    def test_load_real_supermarkets(self):
        from app import load_supermarkets

        mercados = load_supermarkets()

        assert len(mercados) == 4
        assert any(m["id"] == "masonline" for m in mercados)
        assert any(m["id"] == "dia" for m in mercados)


class TestResultsParser:
    def test_parse_results_json(self):
        from app import load_results

        with tempfile.TemporaryDirectory() as tmpdir:
            resultados_file = Path(tmpdir) / "resultados.json"
            with open(resultados_file, "w") as f:
                json.dump(
                    {
                        "productos": [
                            {
                                "producto": "leche",
                                "marca": "serenisima",
                                "tamaño": "1L",
                                "resultados": [
                                    {
                                        "nombre": "Leche 1L",
                                        "marca": "Serenisima",
                                        "precio": 500,
                                        "supermercado": "masonline",
                                    }
                                ],
                            }
                        ]
                    },
                    f,
                )

            rows = load_results(resultados_file)

            assert len(rows) == 1
            assert rows[0]["producto"] == "Leche 1L"
            assert rows[0]["marca"] == "Serenisima"
            assert rows[0]["precio"] == 500
            assert rows[0]["supermercado"] == "masonline"

    def test_parse_multiple_results(self):
        from app import load_results

        with tempfile.TemporaryDirectory() as tmpdir:
            resultados_file = Path(tmpdir) / "resultados.json"
            with open(resultados_file, "w") as f:
                json.dump(
                    {
                        "productos": [
                            {
                                "producto": "leche",
                                "resultados": [
                                    {
                                        "nombre": "Leche 1",
                                        "marca": "A",
                                        "precio": 100,
                                        "supermercado": "masonline",
                                    },
                                    {
                                        "nombre": "Leche 2",
                                        "marca": "B",
                                        "precio": 200,
                                        "supermercado": "dia",
                                    },
                                ],
                            },
                            {
                                "producto": "pan",
                                "resultados": [
                                    {
                                        "nombre": "Pan 1",
                                        "marca": "C",
                                        "precio": 50,
                                        "supermercado": "carrefour",
                                    },
                                ],
                            },
                        ]
                    },
                    f,
                )

            rows = load_results(resultados_file)

            assert len(rows) == 3


class TestBuscaFish:
    def test_build_command_with_supermarkets(self):
        from app import build_busca_command

        cmd = build_busca_command(["masonline", "dia"])

        cmd_str = " ".join(cmd)
        assert "masonline" in cmd_str
        assert "dia" in cmd_str

    def test_build_command_default_supermarkets(self):
        from app import build_busca_command

        cmd = build_busca_command([])

        cmd_str = " ".join(cmd)
        assert "--supermarkets" in cmd_str
