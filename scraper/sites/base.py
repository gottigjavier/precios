import json
import random
import time
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import requests
from fake_useragent import UserAgent


def load_supermarkets(config_path: str = "supermercados.json") -> List[dict]:
    path = Path(config_path)
    if not path.exists():
        path = Path(__file__).parent.parent.parent / config_path
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@dataclass
class ProductResult:
    nombre: str
    marca: Optional[str]
    precio: Optional[float]
    precio_original: Optional[float]
    descuento: Optional[int]
    disponible: bool
    url: str
    supermercado: str


class BaseScraper:
    def __init__(self, site_id: str, config: dict):
        self.site_id = site_id
        self.name = config.get("name", site_id)
        self.base_url = config.get("base_url", "")
        self.api_url = config.get("api_url") or self._build_api_url(self.base_url)
        self.referer = self.base_url + "/"
        self.session = requests.Session()
        self.ua = UserAgent()

    def _build_api_url(self, base_url: str) -> str:
        return f"{base_url}/api/catalog_system/pub/products/search"

    def _get_headers(self) -> dict:
        return {
            "User-Agent": self.ua.random,
            "Accept": "*/*",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Referer": self.referer,
        }

    def search(self, query: str) -> List[ProductResult]:
        results = []
        url = f"{self.api_url}?term={query}&map=term"

        try:
            time.sleep(random.uniform(1, 2))
            response = self.session.get(url, headers=self._get_headers(), timeout=30)

            if response.status_code not in (200, 206):
                return results

            data = response.json()
            if not isinstance(data, list):
                return results

            for item in data:
                result = self._parse_product(item)
                if result:
                    results.append(result)

        except Exception as e:
            print(f"Error en {self.name}: {e}")

        return results

    def get_all_products(self, query: str = "") -> List[ProductResult]:
        results = []

        if query:
            url = f"{self.api_url}?ft={query}"
        else:
            url = f"{self.api_url}?_from=0&_to=49&O=OrderByTopSaleDESC"

        try:
            time.sleep(random.uniform(0.3, 0.5))
            response = self.session.get(url, headers=self._get_headers(), timeout=30)

            if response.status_code not in (200, 206):
                return results

            data = response.json()
            if not isinstance(data, list):
                return results

            for item in data:
                result = self._parse_product(item)
                if result:
                    results.append(result)

        except Exception as e:
            print(f"Error en {self.name}: {e}")

        return results

    def _parse_product(self, item: dict) -> Optional[ProductResult]:
        product_name = item.get("productName", "")
        brand = item.get("brand")
        link = item.get("link", "")

        if not product_name or not link:
            return None

        url = link if link.startswith("http") else self.base_url + link

        precio = None
        precio_original = None
        descuento = None
        disponible = True

        items = item.get("items", [])
        if items:
            sellers = items[0].get("sellers", [])
            if sellers:
                comm = sellers[0].get("commertialOffer", {})
                precio = comm.get("Price")
                precio_original = comm.get("ListPrice")
                available_qty = comm.get("AvailableQuantity", 0)
                disponible = available_qty > 0 if available_qty else True

                if precio_original and precio < precio_original:
                    descuento = int(
                        ((precio_original - precio) / precio_original) * 100
                    )

        return ProductResult(
            nombre=product_name,
            marca=brand,
            precio=precio,
            precio_original=precio_original,
            descuento=descuento,
            disponible=disponible,
            url=url,
            supermercado=self.site_id,
        )


def create_scraper(site_id: str, site_config: dict) -> BaseScraper:
    scraper = BaseScraper(site_id, site_config)
    return scraper
