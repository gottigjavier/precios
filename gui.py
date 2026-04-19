import json
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_supermarkets_data(
    supermercados_file: Optional[str] = None,
) -> List[Dict[str, str]]:
    file_path = (
        supermercados_file
        if supermercados_file
        else "/home/javier/programacion/python/supermercados/supermercados.json"
    )
    with open(file_path) as f:
        return json.load(f)


def load_results_data(resultados_file: Optional[str] = None) -> List[Dict[str, Any]]:
    if resultados_file is None:
        resultados_file = (
            "/home/javier/programacion/python/supermercados/resultados.json"
        )
    if not Path(resultados_file).exists():
        return []

    with open(resultados_file) as f:
        data = json.load(f)

    rows = []
    for producto_data in data.get("productos", []):
        for resultado in producto_data.get("resultados", []):
            rows.append(
                {
                    "producto": resultado.get("nombre", ""),
                    "marca": resultado.get("marca", ""),
                    "precio": resultado.get("precio", ""),
                    "supermercado": resultado.get("supermercado", ""),
                }
            )

    return rows
