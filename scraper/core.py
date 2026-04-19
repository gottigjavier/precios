import json
import time
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor

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


def filtrar_resultados(results: List, producto: str, marca: str, tamaño: str) -> List:
    if not results:
        return []

    filtered = []
    marca_norm = normalize(marca)
    tamaño_input = (tamaño or "").lower().strip()

    t_clean = tamaño_input.replace(" ", "")
    t_num = "".join(c for c in t_clean if c.isdigit())
    t_unit = "".join(c for c in t_clean if c.isalpha())

    for r in results:
        nombre_norm = normalize(r.nombre)

        if t_num and t_unit:
            matches_size = t_num in nombre_norm and t_unit in nombre_norm
        elif t_num:
            matches_size = t_num in nombre_norm
        else:
            matches_size = True

        matches_marca = True
        if marca_norm:
            marca_r = normalize(r.marca)
            matches_marca = marca_norm in nombre_norm or (
                marca_r and marca_norm in marca_r
            )

        if matches_size and matches_marca:
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

    def scrape_products(self, products: List[dict], sites: List[str]) -> dict:
        all_results = {"productos": []}

        for product in products:
            producto = product.get("producto", "")
            tamaño = product.get("tamaño", "")
            marca = product.get("marca", "")

            query = " ".join(filter(None, [producto, marca, tamaño]))
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
        query = " ".join(filter(None, [producto, marca, tamaño]))

        return scraper.search(query)

    def scrape_all_paginated(self, products: List[dict], sites: List[str]) -> dict:
        all_results = {"productos": []}

        for product in products:
            producto = product.get("producto", "")
            marca = product.get("marca", "")
            tamaño = product.get("tamaño", "")
            combined_results = []

            query = " ".join(filter(None, [producto, marca, tamaño]))

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
