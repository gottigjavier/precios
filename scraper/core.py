from typing import List

from .sites.base import BaseScraper, load_supermarkets


def load_scraper_config(site_id: str) -> dict:
    supermarkets = load_supermarkets()
    for site in supermarkets:
        if site.get("id") == site_id:
            return site
    return {}


def create_scraper(site_id: str) -> BaseScraper:
    config = load_scraper_config(site_id)
    return BaseScraper(site_id, config)


def normalize(s):
    import unicodedata

    s = (s or "").lower().strip()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace(" ", "")


def _decimal_alternate(s: str) -> str:
    if "," in s:
        return s.replace(",", ".")
    if "." in s:
        return s.replace(".", ",")
    return s


def _check_pattern(pattern: str, text: str) -> bool:
    if pattern in text:
        return True
    if "," in pattern or "." in pattern:
        return _decimal_alternate(pattern) in text
    return False


def filtrar_resultados(results: List, producto: str, marca: str, tamaño: str) -> List:
    if not results:
        return []

    filtered = []

    producto_norm = (
        None
        if producto == "*"
        else (normalize(producto) if producto else "")
    )
    marca_norm = (
        None if marca == "*" else (normalize(marca) if marca else "")
    )

    if tamaño == "*":
        t_num = None
        t_unit = None
    else:
        t_clean = (tamaño or "").lower().strip().replace(" ", "")
        t_num = "".join(c for c in t_clean if c.isdigit() or c in ".,") or None
        t_unit = "".join(c for c in t_clean if c.isalpha()) or None

    for r in results:
        nombre_norm = normalize(r.nombre)

        if producto_norm is None:
            matches_producto = True
        else:
            matches_producto = producto_norm and producto_norm in nombre_norm

        if t_num is None and t_unit is None:
            matches_size = True
        elif t_num and t_unit:
            matches_size = (
                _check_pattern(t_num, nombre_norm) and t_unit in nombre_norm
            )
        elif t_num:
            matches_size = _check_pattern(t_num, nombre_norm)
        else:
            matches_size = True

        if marca_norm is None:
            matches_marca = True
        elif marca_norm:
            marca_r = normalize(r.marca)
            matches_marca = marca_norm in nombre_norm or (
                marca_r and marca_norm in marca_r
            )
        else:
            matches_marca = True

        if matches_producto and matches_size and matches_marca:
            filtered.append(r)

    return filtered


class ScraperEngine:
    def __init__(self, config: dict, max_workers: int = 2):
        self.config = config
        self.max_workers = max_workers
        self.scrapers = {}

    def _get_scraper(self, site_id: str):
        if site_id not in self.scrapers:
            site_config = load_scraper_config(site_id)
            if site_config:
                self.scrapers[site_id] = create_scraper(site_id)
        return self.scrapers.get(site_id)

    @staticmethod
    def _build_query(producto: str, marca: str, tamaño: str) -> str:
        parts = []
        if producto and producto != "*":
            parts.append(producto)
        if marca and marca != "*":
            parts.append(marca)
        if tamaño and tamaño != "*":
            parts.append(tamaño.replace(",", "."))
        return " ".join(parts)

    def scrape_products(self, products: List[dict], sites: List[str]) -> dict:
        all_results = {"productos": []}

        for product in products:
            producto = product.get("producto", "")
            tamaño = product.get("tamaño", "")
            marca = product.get("marca", "")

            if producto == "*" and marca == "*" and tamaño == "*":
                print(f"Producto inválido: todos los campos son '*'. Se omite.")
                continue

            query = self._build_query(producto, marca, tamaño)
            product_results = {
                "producto": producto,
                "marca": marca,
                "tamaño": tamaño,
                "resultados": [],
            }

            for site_id in sites:
                scraper = self._get_scraper(site_id)
                if scraper:
                    print(f"Buscando en {scraper.name}: {query}")
                    try:
                        results = scraper.search(query)
                        results = filtrar_resultados(results, producto, marca, tamaño)
                        product_results["resultados"].extend(results)
                    except Exception as e:
                        print(f"Error en {site_id}: {e}")

            all_results["productos"].append(product_results)

        return all_results

    def scrape_product_single_site(self, product: dict, site_id: str) -> List:
        scraper = self._get_scraper(site_id)
        if not scraper:
            return []

        producto = product.get("producto", "")
        marca = product.get("marca", "")
        tamaño = product.get("tamaño", "")
        query = self._build_query(producto, marca, tamaño)

        return scraper.search(query)

    def scrape_all_paginated(self, products: List[dict], sites: List[str]) -> dict:
        all_results = {"productos": []}

        for product in products:
            producto = product.get("producto", "")
            marca = product.get("marca", "")
            tamaño = product.get("tamaño", "")

            if producto == "*" and marca == "*" and tamaño == "*":
                print(f"Producto inválido: todos los campos son '*'. Se omite.")
                continue

            combined_results = []

            query = self._build_query(producto, marca, tamaño)

            for site_id in sites:
                scraper = self._get_scraper(site_id)
                if not scraper:
                    print(f"Scraper no encontrado: {site_id}")
                    continue

                if not hasattr(scraper, "get_all_products"):
                    print(f"Scraper no soporta búsqueda: {site_id}")
                    continue

                print(f"Buscando en {scraper.name}: {query}")
                results = scraper.get_all_products(query)
                print(f"Resultados de {scraper.name}: {len(results)}")

                filtered = filtrar_resultados(results, producto, marca, tamaño)
                combined_results.extend(filtered)
                print(f"Filtrados para {producto} {marca} {tamaño}: {len(filtered)}")

            product_results = {
                "producto": producto,
                "marca": product.get("marca", ""),
                "tamaño": tamaño,
                "resultados": combined_results,
            }
            all_results["productos"].append(product_results)

        return all_results
