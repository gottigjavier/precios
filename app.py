import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path("/home/javier/programacion/python/supermercados")
PRODUCTS_FILE = BASE_DIR / "products.json"
SUPERMERCADOS_FILE = BASE_DIR / "supermercados.json"
RESULTADOS_JSON = BASE_DIR / "resultados.json"
RESULTADOS_CSV = BASE_DIR / "resultados.csv"
BUSCA_SCRIPT = BASE_DIR / "busca.fish"


def save_products(
    producto: str, marca: str, tamaño: str, products_file: Optional[Path] = None
) -> None:
    file_path = products_file if products_file else PRODUCTS_FILE
    products = [{"producto": producto, "marca": marca, "tamaño": tamaño}]
    with open(file_path, "w") as f:
        json.dump(products, f, indent=2)


def save_multiple_products(
    products_list: List[Dict[str, str]], products_file: Optional[Path] = None
) -> None:
    file_path = products_file if products_file else PRODUCTS_FILE
    with open(file_path, "w") as f:
        json.dump(products_list, f, indent=2)


def load_supermarkets(
    supermercados_file: Optional[Path] = None,
) -> List[Dict[str, str]]:
    file_path = supermercados_file if supermercados_file else SUPERMERCADOS_FILE
    with open(file_path) as f:
        return json.load(f)


def build_busca_command(selected_supermarket_ids: List[str]) -> List[str]:
    if not selected_supermarket_ids:
        default_ids = ["masonline", "dia", "carrefour", "vea"]
        ids_arg = ",".join(default_ids)
    else:
        ids_arg = ",".join(selected_supermarket_ids)

    return ["fish", str(BUSCA_SCRIPT), "--supermarkets", ids_arg]


def run_busca_script(supermarket_ids: List[str]) -> subprocess.Popen:
    cmd = build_busca_command(supermarket_ids)
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


def wait_for_results(timeout: int = 300) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        if RESULTADOS_JSON.exists():
            try:
                with open(RESULTADOS_JSON) as f:
                    data = json.load(f)
                if data.get("productos"):
                    return True
            except (json.JSONDecodeError, IOError):
                pass
        time.sleep(2)
    return False


def load_results(resultados_file: Optional[Path] = None) -> List[Dict[str, Any]]:
    file_path = resultados_file if resultados_file else RESULTADOS_JSON
    if not file_path.exists():
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
                }
            )

    return rows
