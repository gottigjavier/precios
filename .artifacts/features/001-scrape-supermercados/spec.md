# 001 - Scrape Supermercados

**Status:** ready  
**Scope:** medium  
**Created:** 2026-04-14

## Overview

Herramienta CLI para scrapeo de precios de productos en supermercados online argentinos (MASOnline/Changomas, DIA, Carrefour, Vea). Soporta búsqueda, filtrado, paginación y exportación a CSV/JSON.

## Requirements

### RQ001 - Búsqueda de Productos
El sistema debe permitir buscar productos por nombre, marca y tamaño en los supermercados configurados.

### RQ002 - Filtrado de Resultados
El sistema debe filtrar resultados por:
- Precio mínimo (--min-price)
- Solo disponibles (--available-only)

### RQ003 - Paginación
El sistema debe soportar búsqueda paginada para obtener todos los productos que coinciden con la query.

### RQ004 - Formatos de Exportación
El sistema debe exportar resultados a:
- CSV
- JSON (con timestamp)

### RQ005 - CLI con Opciones
El CLI debe aceptar:
- `--input` / `-i`: Archivo JSON con lista de productos
- `--products` / `-p`: Productos en línea (formato "producto,marca,tamaño")
- `--supermarkets` / `-s`: Supermercados a consultar (comma-separated)
- `--output` / `-o`: Ruta de salida sin extensión
- `--format` / `-f`: Formatos de salida (csv,json)
- `--config` / `-c`: Archivo de configuración
- `--paginated`: Buscar en todos los productos paginados

## User Stories

### US001 - Búsqueda desde archivo
Como usuario, quiero especificar un archivo JSON con productos para buscar en varios supermercados y obtener los resultados.

### US002 - Búsqueda rápida
Como usuario, quiero especificar productos directamente en la línea de comandos para una búsqueda rápida.

### US003 - Filtrado por precio
Como usuario, quiero filtrar resultados por precio mínimo para encontrar opciones dentro de mi presupuesto.

### US004 - Solo disponibles
Como usuario, quiero ver solo productos disponibles para evitar ofertas expiradas.

### US005 - Exportación múltiple
Como usuario, quiero exportar a múltiples formatos (CSV y JSON) en una sola ejecución.

## Acceptance Criteria

- [ ] El sistema busca productos en MASOnline, DIA, Carrefour, Vea
- [ ] Los resultados incluyen: nombre, marca, precio, precio_original, descuento, disponible, url, supermercado
- [ ] El filtrado por min_price funciona correctamente
- [ ] El filtrado por available_only excluye productos no disponibles
- [ ] La exportación CSV genera archivo válido con headers
- [ ] La exportación JSON incluye timestamp
- [ ] El CLI acepta todas las opciones especificadas
- [ ] La búsqueda paginada retorna todos los productos
- [ ] El sistema maneja errores gracefully (print sin crash)