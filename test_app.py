import json
import tempfile
import unittest
from pathlib import Path

try:
    import typer  # noqa: F401

    HAS_TYPER = True
except ImportError:
    HAS_TYPER = False

try:
    from fake_useragent import UserAgent  # noqa: F401

    HAS_FAKE_USERAGENT = True
except ImportError:
    HAS_FAKE_USERAGENT = False


class TestMultipleProducts(unittest.TestCase):
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

            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["producto"], "leche")
            self.assertEqual(data[1]["producto"], "pan")

    def test_save_multiple_products_empty_list(self):
        from app import save_multiple_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_multiple_products([], products_file)

            with open(products_file) as f:
                data = json.load(f)

            self.assertEqual(data, [])


class TestProductsJSON(unittest.TestCase):
    def test_save_products_overwrites_file(self):
        from app import save_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_products("leche", "la serenisima", "1L", products_file)
            with open(products_file) as f:
                data = json.load(f)
            self.assertEqual(
                data, [{"producto": "leche", "marca": "la serenisima", "tamaño": "1L"}]
            )

            save_products("pan", "bimbo", "500g", products_file)
            with open(products_file) as f:
                data = json.load(f)
            self.assertEqual(
                data, [{"producto": "pan", "marca": "bimbo", "tamaño": "500g"}]
            )

    def test_products_format(self):
        from app import save_products

        with tempfile.TemporaryDirectory() as tmpdir:
            products_file = Path(tmpdir) / "products.json"

            save_products("test_product", "test_brand", "test_size", products_file)

            with open(products_file) as f:
                data = json.load(f)

            self.assertEqual(len(data), 1)
            self.assertIn("producto", data[0])
            self.assertIn("marca", data[0])
            self.assertIn("tamaño", data[0])
            self.assertEqual(data[0]["producto"], "test_product")
            self.assertEqual(data[0]["marca"], "test_brand")
            self.assertEqual(data[0]["tamaño"], "test_size")


class TestSupermarkets(unittest.TestCase):
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

            self.assertEqual(len(mercados), 2)
            self.assertEqual(mercados[0]["id"], "masonline")
            self.assertEqual(mercados[0]["name"], "MASOnline")
            self.assertEqual(mercados[1]["id"], "dia")
            self.assertEqual(mercados[1]["name"], "DIA")

    def test_load_real_supermarkets(self):
        from app import load_supermarkets

        mercados = load_supermarkets()

        self.assertEqual(len(mercados), 4)
        self.assertTrue(any(m["id"] == "masonline" for m in mercados))
        self.assertTrue(any(m["id"] == "dia" for m in mercados))


class TestResultsParser(unittest.TestCase):
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

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["producto"], "Leche 1L")
            self.assertEqual(rows[0]["marca"], "Serenisima")
            self.assertEqual(rows[0]["precio"], 500)
            self.assertEqual(rows[0]["supermercado"], "masonline")

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

            self.assertEqual(len(rows), 3)


class TestBuscaFish(unittest.TestCase):
    def test_build_command_with_supermarkets(self):
        from app import build_busca_command

        cmd = build_busca_command(["masonline", "dia"])

        cmd_str = " ".join(cmd)
        self.assertIn("masonline", cmd_str)
        self.assertIn("dia", cmd_str)

    def test_build_command_default_supermarkets(self):
        from app import build_busca_command

        cmd = build_busca_command([])

        cmd_str = " ".join(cmd)
        self.assertIn("--supermarkets", cmd_str)


class TestFilterResults(unittest.TestCase):
    @unittest.skipUnless(HAS_TYPER, "typer not installed")
    def test_filter_results_by_min_price(self):
        from main import filter_results

        results = [
            {"precio": 100, "disponible": True},
            {"precio": 50, "disponible": True},
            {"precio": 200, "disponible": True},
        ]
        filtered = filter_results(results, min_price=75)
        self.assertEqual(len(filtered), 2)

    @unittest.skipUnless(HAS_TYPER, "typer not installed")
    def test_filter_results_available_only(self):
        from main import filter_results

        results = [
            {"precio": 100, "disponible": True},
            {"precio": 50, "disponible": False},
            {"precio": 200, "disponible": True},
        ]
        filtered = filter_results(results, available_only=True)
        self.assertEqual(len(filtered), 2)

    @unittest.skipUnless(HAS_TYPER, "typer not installed")
    def test_filter_results_combined(self):
        from main import filter_results

        results = [
            {"precio": 100, "disponible": True},
            {"precio": 50, "disponible": False},
            {"precio": 200, "disponible": True},
        ]
        filtered = filter_results(results, min_price=75, available_only=True)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r["precio"] >= 75 for r in filtered))
        self.assertTrue(all(r["disponible"] for r in filtered))


class TestScraperCore(unittest.TestCase):
    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_normalize_removes_accents(self):
        from scraper.core import normalize

        result = normalize("café")
        self.assertEqual(result, "cafe")

    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_normalize_lowercases(self):
        from scraper.core import normalize

        result = normalize("HOLA")
        self.assertEqual(result, "hola")

    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_normalize_removes_spaces(self):
        from scraper.core import normalize

        result = normalize("hola mundo")
        self.assertEqual(result, "holamundo")

    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_filtrar_resultados_empty(self):
        from scraper.core import filtrar_resultados

        results = filtrar_resultados([], "leche", "serenisima", "1L")
        self.assertEqual(results, [])

    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_filtrar_resultados_filters_by_producto(self):
        from scraper.core import filtrar_resultados
        from scraper.sites.base import ProductResult

        results = [
            ProductResult(
                "Leche descremada 1L",
                "Serenisima",
                500,
                None,
                None,
                True,
                "",
                "masonline",
            ),
            ProductResult(
                "Yogur bebible 1L", "Serenisima", 300, None, None, True, "", "masonline"
            ),
            ProductResult(
                "Leche entera 1L", "Pilsen", 450, None, None, True, "", "masonline"
            ),
        ]
        filtered = filtrar_resultados(results, "leche", "", "1L")
        self.assertEqual(len(filtered), 2)
        for r in filtered:
            self.assertIn("leche", r.nombre.lower())


class TestBaseScraper(unittest.TestCase):
    @unittest.skipUnless(HAS_FAKE_USERAGENT, "fake_useragent not installed")
    def test_product_result_dataclass(self):
        from scraper.sites.base import ProductResult

        result = ProductResult(
            nombre="Test Product",
            marca="Test Brand",
            precio=100.0,
            precio_original=150.0,
            descuento=33,
            disponible=True,
            url="https://example.com",
            supermercado="test",
        )
        self.assertEqual(result.nombre, "Test Product")
        self.assertEqual(result.precio, 100.0)
        self.assertEqual(result.descuento, 33)
