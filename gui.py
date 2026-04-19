import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from paths import SUPERMERCADOS_FILE, RESULTADOS_JSON


def load_supermarkets_data(
    supermercados_file: Optional[str] = None,
) -> List[Dict[str, str]]:
    file_path = supermercados_file if supermercados_file else SUPERMERCADOS_FILE
    with open(file_path) as f:
        return json.load(f)


def load_results_data(resultados_file: Optional[str] = None) -> List[Dict[str, Any]]:
    file_path = resultados_file if resultados_file else RESULTADOS_JSON
    if not Path(file_path).exists():
        return []

    with open(file_path) as f:
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
                    "url": resultado.get("url", ""),
                }
            )

    return rows
