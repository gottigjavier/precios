# Buscador de Precios de Supermercados

---

> ## Aviso Legal
> Este proyecto es para uso personal y educativo.
> Para evitar inconvenientes legales se utilizan datos genéricos en el archivo **supermercados.json**.
> Para que la app funcione debe proporcionar las URL de los sitios de los supermercados a evaluar. Use responsablemente y verifique los Términos y Condiciones de cada sitio.

**[Agregar URL de supermercados](#lista)**

---

La Argentina viene de un pasado de alta inflación y está en un proceso de transición al libre mercado. Esto deriva en una diferencia, a veces marcada, de precio en el mismo producto según el comercio que lo ofrezca.

Si se intenta realizar un compra inteligente, sobre todo antes de una importante, se ingresa a los sitios online de los supermercados recorriendo pestañas del navegador, haciendo búsquedas y clicks en productos, y registrando cada precio para luego comparar, lo que se vuelve tedioso y puede llevar demasiado tiempo.

Construí este proyecto en Python que permite buscar en segundos y comparar precios de productos en múltiples supermercados online.

Comenzó como una serie de scripts sin intefaz gráfica que guardaba los resultados en un archivo .csv para ser consumidos por una planilla de cálculo. Luego, para bajar la barrera técnica implementé la interfaz gráfica. Por esa razón encontrarán que el flujo del código es como es.

---

## Características

- Interfaz gráfica para buscar productos en varios supermercados a la vez
- Comparación de precios en una tabla interactiva
- Apertura directa de enlaces a los productos
- Exportación de resultados a JSON y CSV

---

## Requisitos

- Python 3.10+
- [Fish Shell](https://fishshell.com/) (para ejecutar el script)
> [!caution]
> Para otros lenguajes de shell deberá adaptar los archivos **busca.fish** y **buscar.fish**

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/gottigjavier/precios.git
cd supermercados
```

## Ejecutar Manualmente

```
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate.fish  # o source venv/bin/activate en bash

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias adicionales para la GUI
pip install dearpygui

# Ejecutar
./venv/bin/python main_gui.py
```

## Uso

Ejecutar el script `buscar.fish`:

```bash
./buscar.fish
```

Este script activa automáticamente el entorno virtual y lanza la interfaz gráfica.

Para salir de la app presionar la tecla **Esc** o ir al submenú **Archivo -> Salir** 

---

### Como buscar

Una vez realizado el paso **[Agregar URL de supermercados](#lista)** estos aparecerán en la lista de supermercados para ser seleccionados al tildar en la caja check-box (por defecto están seleccionados).

Se ingresa en la caja de texto "Datos del Producto" la especificación de la búsqueda en el sigiente orden: producto, marca, tamaño (separados por comas).

Para más de un ítem de búsqueda presionar "Enter" y repetir el método en la siguiente línea.

Se pueden realizar búsquedas utilizando el comodín "*" hasta en dos de los tres criterios de búsqueda, por ejemplo 

```bash
arroz, *, *
```
dará como resultado todos los productos que coincidan con la palabra arroz, de todas las marcas y en todos los tamaños de paquete.

Se verifica que estén seleccionados los supermercados en la lista y se presiona "Buscar".

Los resultados aparecerán en la pestaña **Resultados**. Si se presiona *Actualizar Resultados* se mostrarán lo últimos resultados arrojados: los actuales si ya se realizó una búsqueda o en su defecto los de la búsqueda previa inmediata.

---

## Estructura del Proyecto

```
supermercados/
├── app.py              # Lógica de negocio
├── gui.py              # Funciones de carga de datos
├── main_gui.py         # Interfaz DearPyGUI
├── paths.py            # Rutas de archivos
├── buscar.fish        # Script de lanzamiento
├── requirements.txt  # Dependencias
├── supermercados.json   # Lista de supermercados
├── screenshots/     # Imágenes (no incluido en git)
└── venv/            # Entorno virtual (no incluido en git)
```

> Definir la lista de supermercados.
>
> La pantalla de búsqueda ofrece la oportunidad de elegir entre una lista de supermercados. Para conformar la lista se debe <a id="lista">**agregar la URL del sitio online** </a> de cada supermercado al archivo *supermercados.json* respetando el formato JSON. En la mayoría de los sitios online de los supermercados probados la URI sigue el mismo formato. Se debe verificar esta condición para que la búsqueda funciones correctamente.


---

## Tech Stack

- **GUI**: [DearPyGUI](https://github.com/hoffstadt/DearPyGui)
- **Scraping**: Beautiful Soup, Requests, lxml
