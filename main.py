import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from click import Choice
from scraper.core import ScraperEngine

app = typer.Typer()


def load_config(config_path: str = "config.json") -> dict:
    with open(config_path, "r") as f:
        return json.load(f)


def load_products(input_path: str) -> list:
    with open(input_path, "r") as f:
        return json.load(f)


def parse_products_arg(products_str: str) -> list:
    if not products_str:
        return []
    products = []
    for item in products_str:
        parts = item.split(",")
        if len(parts) >= 1:
            product = {"producto": parts[0].strip()}
            if len(parts) >= 2:
                product["marca"] = parts[1].strip()
            if len(parts) >= 3:
                product["tamaño"] = parts[2].strip()
            products.append(product)
    return products


def filter_results(
    results: list, min_price: float = None, available_only: bool = False
) -> list:
    filtered = []
    for r in results:
        # Convertir ProductResult a dict si es necesario
        if hasattr(r, "__dataclass_fields__"):
            r = {
                "nombre": r.nombre,
                "marca": r.marca,
                "precio": r.precio,
                "precio_original": r.precio_original,
                "descuento": r.descuento,
                "disponible": r.disponible,
                "url": r.url,
                "supermercado": r.supermercado,
            }

        if available_only and not r.get("disponible", True):
            continue
        if min_price is not None:
            precio = r.get("precio")
            if precio is None or precio < min_price:
                continue
        filtered.append(r)
    return filtered


def save_results(data: dict, output_path: str, formats: list):
    output = Path(output_path)

    if "csv" in formats:
        csv_path = output.with_suffix(".csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(
                "producto,marca,tamaño,supermercado,precio,precio_original,descuento,disponible,url\n"
            )
            for prod in data.get("productos", []):
                producto = prod.get("producto", "")
                marca = prod.get("marca", "")
                tamaño = prod.get("tamaño", "")
                for r in prod.get("resultados", []):
                    # Convertir ProductResult a dict si es necesario
                    if hasattr(r, "__dataclass_fields__"):
                        r = {
                            "nombre": r.nombre,
                            "marca": r.marca,
                            "precio": r.precio,
                            "precio_original": r.precio_original,
                            "descuento": r.descuento,
                            "disponible": r.disponible,
                            "url": r.url,
                            "supermercado": r.supermercado,
                        }
                    f.write(
                        f'"{producto}","{marca}","{tamaño}","{r.get("supermercado", "")}",'
                    )
                    f.write(
                        f'"{r.get("precio", "")}","{r.get("precio_original", "")}","{r.get("descuento", "")}",'
                    )
                    f.write(f'"{r.get("disponible", "")}","{r.get("url", "")}"\n')
        typer.echo(f"CSV guardado: {csv_path}")

    if "json" in formats:
        json_path = output.with_suffix(".json")

        # Convertir todos los ProductResult a dicts para JSON
        json_data = {"productos": []}
        for prod in data.get("productos", []):
            json_prod = {
                "producto": prod.get("producto", ""),
                "marca": prod.get("marca", ""),
                "tamaño": prod.get("tamaño", ""),
                "resultados": [],
            }
            for r in prod.get("resultados", []):
                if hasattr(r, "__dataclass_fields__"):
                    json_prod["resultados"].append(
                        {
                            "nombre": r.nombre,
                            "marca": r.marca,
                            "precio": r.precio,
                            "precio_original": r.precio_original,
                            "descuento": r.descuento,
                            "disponible": r.disponible,
                            "url": r.url,
                            "supermercado": r.supermercado,
                        }
                    )
                else:
                    json_prod["resultados"].append(r)
            json_data["productos"].append(json_prod)

        json_data["timestamp"] = datetime.now().isoformat()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        typer.echo(f"JSON guardado: {json_path}")


@app.command()
def main(
    input: Annotated[
        Optional[str], typer.Option("--input", "-i", help="Archivo JSON con productos")
    ] = None,
    products: Annotated[
        Optional[str],
        typer.Option(
            "--products",
            "-p",
            help="Productos como 'producto,marca,tamaño' (separados por coma, usar comillas)",
        ),
    ] = None,
    supermarkets: Annotated[
        str,
        typer.Option(
            "--supermarkets",
            "-s",
            help="Supermercados (comma-separated: masonline,dia)",
        ),
    ] = "masonline,dia",
    output: Annotated[
        str, typer.Option("--output", "-o", help="Ruta de salida sin extensión")
    ] = "resultados",
    min_price: Annotated[
        Optional[float], typer.Option("--min-price", help="Precio mínimo")
    ] = None,
    available_only: Annotated[
        bool, typer.Option("--available-only", help="Solo productos disponibles")
    ] = False,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Formatos de salida (csv,json)")
    ] = "csv,json",
    config: Annotated[
        str, typer.Option("--config", "-c", help="Archivo de configuración")
    ] = "config.json",
    paginated: Annotated[
        bool,
        typer.Option("--paginated", help="Buscar en todos los productos paginados"),
    ] = False,
):
    products_list = products.split("|") if products else []
    sites_list = [s.strip() for s in supermarkets.split(",")]
    formats_list = [f.strip() for f in format.split(",")]

    if not input and not products_list:
        typer.echo("Error: Debes especificar --input o --products")
        raise typer.Exit(1)

    productos = load_products(input) if input else parse_products_arg(products_list)

    typer.echo(
        f"Buscando {len(productos)} producto(s) en {len(sites_list)} supermercado(s)"
    )

    config_data = load_config(config)
    engine = ScraperEngine(config_data)

    if paginated:
        results = engine.scrape_all_paginated(productos, sites_list)
    else:
        results = engine.scrape_products(productos, sites_list)

    for prod in results["productos"]:
        prod["resultados"] = filter_results(
            prod["resultados"], min_price=min_price, available_only=available_only
        )

    save_results(results, output, formats_list)

    total = sum(len(p["resultados"]) for p in results["productos"])
    typer.echo(f"Total: {total} resultado(s)")


if __name__ == "__main__":
    app()
