import faulthandler
import os
import subprocess
import threading
import time
import webbrowser

import dearpygui.dearpygui as dpg

from app import build_busca_command, save_multiple_products
from gui import load_results_data, load_supermarkets_data

faulthandler.enable()

from paths import BASE_DIR

supermarkets = []
selected_supermarkets = set()
results_data = []
is_searching = False
search_progress = 0
row_counter = 0
INPUT_TAGS = []


def load_supermarkets():
    global supermarkets
    try:
        supermercadoes = load_supermarkets_data()
        for s in supermercadoes:
            supermarkets.append((s["id"], s["name"]))
    except Exception as e:
        print(f"Error loading supermarkets: {e}")


def add_product_row():
    global row_counter, INPUT_TAGS
    row_counter += 1

    producto_tag = f"input_producto_{row_counter}"
    marca_tag = f"input_marca_{row_counter}"
    tamano_tag = f"input_tamano_{row_counter}"

    input_producto = dpg.get_value("input_producto")
    input_marca = dpg.get_value("input_marca")
    input_tamano = dpg.get_value("input_tamano")

    if not input_producto:
        dpg.set_value("status_label", "Ingrese un producto")
        return

    products_list_str = dpg.get_value("products_list") or ""
    product_str = input_producto
    if input_marca:
        product_str += f" | {input_marca}"
    if input_tamano:
        product_str += f" | {input_tamano}"

    if products_list_str:
        products_list_str += "\n" + product_str
    else:
        products_list_str = product_str

    dpg.set_value("products_list", products_list_str)
    dpg.set_value("input_producto", "")
    dpg.set_value("input_marca", "")
    dpg.set_value("input_tamano", "")

    INPUT_TAGS.append((producto_tag, marca_tag, tamano_tag, ""))


def clear_inputs():
    global INPUT_TAGS, row_counter
    dpg.set_value("input_productos", "")
    INPUT_TAGS = []
    row_counter = 0


def add_row_callback(sender, app_data):
    add_product_row()


def switch_to_results():
    dpg.set_value("tab_bar", 1)


def save_and_search_callback(sender, app_data):
    global is_searching, search_progress, results_data, row_counter

    products_text = dpg.get_value("input_productos") or ""
    if not products_text.strip():
        dpg.set_value("status_label", "Por favor ingrese al menos un producto")
        return

    products_list = []
    for line in products_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        producto = parts[0] if parts else ""
        marca = parts[1] if len(parts) > 1 else ""
        tamano = parts[2] if len(parts) > 2 else ""
        if producto:
            products_list.append(
                {
                    "producto": producto,
                    "marca": marca,
                    "tamaño": tamano,
                }
            )

    if not products_list:
        dpg.set_value("status_label", "Por favor ingrese al menos un producto")
        return

    save_multiple_products(products_list)

    selected_ids = [
        sid for sid, _ in selected_supermarkets if dpg.get_value(f"checkbox_{sid}")
    ]

    if not selected_ids:
        dpg.set_value("status_label", "Por favor seleccione al menos un supermercado")
        return

    dpg.set_value("status_label", "Buscando productos...")
    is_searching = True
    search_progress = 0
    dpg.disable_item("btn_enviar")

    def run_search():
        global is_searching, search_progress, results_data

        cmd = build_busca_command(selected_ids)
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        timeout = 300
        start_time = time.time()
        while proc.poll() is None and time.time() - start_time < timeout:
            time.sleep(1)
            search_progress += 1
            dpg.set_value("progress_bar", search_progress / 100)

        if proc.returncode == 0 or RESULTADOS_JSON.exists():
            time.sleep(2)
            results_data = load_results_data()
            dpg.set_value(
                "status_label",
                f"Busqueda completada. {len(results_data)} resultados encontrados.",
            )
            show_results_callback(None, None)
            clear_inputs()
        else:
            dpg.set_value("status_label", "Error en la busqueda")

        is_searching = False
        dpg.enable_item("btn_enviar")
        dpg.set_value("progress_bar", 100)

    thread = threading.Thread(target=run_search)
    thread.start()


url_store = {}


def open_url_callback(sender, app_data):
    url = url_store.get(sender)
    if url:
        webbrowser.open(url)


def show_results_callback(sender, app_data):
    global results_data, url_store

    results_data = load_results_data()
    url_store = {}

    if not results_data:
        dpg.set_value("status_label", "No hay resultados")
        return

    if dpg.does_item_exist("results_placeholder"):
        dpg.delete_item("results_placeholder")

    if dpg.does_item_exist("results_header"):
        dpg.delete_item("results_header")

    if dpg.does_item_exist("table_results"):
        dpg.delete_item("table_results")

    dpg.add_text("Resultados", parent="results_container", tag="results_header")

    with dpg.table(
        parent="results_container",
        tag="table_results",
        header_row=True,
        borders_innerH=True,
    ):
        dpg.add_table_column(label="Producto", width_stretch=True)
        dpg.add_table_column(label="Marca", width_stretch=True)
        dpg.add_table_column(label="Precio", width_fixed=True, width=100)
        dpg.add_table_column(label="Supermercado", width_fixed=True, width=100)
        dpg.add_table_column(label="Link", width_fixed=True, width=70)

        for idx, row in enumerate(results_data):
            precio = row.get("precio", "")
            precio_str = (
                f"${precio:,.2f}" if isinstance(precio, (int, float)) else str(precio)
            )
            url = row.get("url", "")
            button_tag = f"btn_abrir_{idx}"
            url_store[button_tag] = url
            with dpg.table_row():
                dpg.add_text(row.get("producto", ""))
                dpg.add_text(row.get("marca", ""))
                dpg.add_text(precio_str)
                dpg.add_text(row.get("supermercado", ""))
                dpg.add_button(
                    label="Abrir",
                    tag=button_tag,
                    width=60,
                    height=20,
                    callback=open_url_callback,
                )


def create_gui():
    global selected_supermarkets

    dpg.create_context()

    close_requested = False

    def close_window(sender, app_data):
        nonlocal close_requested
        if app_data == dpg.mvKey_Escape:
            close_requested = True

    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=close_window)

    dpg.create_viewport(
        title="Buscador de Precios",
        width=1080,
        height=840,
        min_width=960,
        min_height=720,
    )

    with dpg.theme():
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [240, 240, 245, 255])
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [250, 250, 252, 255])
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, [230, 230, 235, 255])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)

    with dpg.font_registry():
        font_path = "/usr/share/fonts/TTF/DejaVuSans.ttf"
        default_font = dpg.add_font(font_path, 17)
        dpg.bind_font(default_font)

    def close_app_callback(sender, app_data):
        nonlocal close_requested
        close_requested = True

    with dpg.window(tag="main_window"):
        with dpg.menu_bar():
            with dpg.menu(label="Archivo"):
                dpg.add_menu_item(label="Salir", callback=close_app_callback)

        with dpg.tab_bar(tag="tab_bar"):
            with dpg.tab(label="Busqueda", tag="tab_busqueda"):
                dpg.add_text("Buscar Productos en Supermercados")
                dpg.add_separator()

                dpg.add_text(
                    "Datos del Producto (uno por linea: producto, marca, tamaño)"
                )
                dpg.add_input_text(
                    tag="input_productos",
                    hint="producto1, marca1, tamano1\nproducto2, marca2, tamano2",
                    width=600,
                    height=120,
                    multiline=True,
                )

                dpg.add_spacer(height=12)
                dpg.add_text("Seleccionar Supermercados")

                with dpg.group(tag="supermarkets_group"):
                    load_supermarkets()
                    for sid, sname in supermarkets:
                        selected_supermarkets.add((sid, sname))
                        dpg.add_checkbox(
                            label=sname, tag=f"checkbox_{sid}", default_value=True
                        )

                dpg.add_spacer(height=12)
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Buscar",
                        tag="btn_enviar",
                        callback=save_and_search_callback,
                        width=180,
                        height=48,
                    )
                    dpg.add_progress_bar(tag="progress_bar", width=360, default_value=0)

                dpg.add_spacer(height=10)
                dpg.add_text("", tag="status_label")

            with dpg.tab(label="Resultados", tag="tab_resultados"):
                dpg.add_text("Resultados de la Busqueda")
                dpg.add_separator()
                dpg.add_button(
                    label="Actualizar Resultados", callback=show_results_callback
                )
                dpg.add_spacer(height=12)
                with dpg.child_window(tag="results_container", height=600):
                    dpg.add_text(
                        "Presione 'Actualizar Resultados' para cargar los datos",
                        tag="results_placeholder",
                    )

    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    closed = False
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        if close_requested and not closed:
            closed = True
            dpg.destroy_context()
            break

    if not closed:
        dpg.destroy_context()


if __name__ == "__main__":
    create_gui()
