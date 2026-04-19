# 002 - GUI Multi-Product Search

**Status:** ready
**Scope:** medium
**Created:** 2026-04-18

## Overview

Extender la interfaz GUI existente para permitir buscar múltiples productos en una sola búsqueda. Agregar botón para agregar filas con campos producto/marca/tamaño. Agregar keyboard handler para cerrar ventana con Escape.

## Requirements

### RQ001 - Multi-Product Input
La GUI debe permitir agregar múltiples filas de búsqueda con campos: producto, marca, tamaño

obviar{
### RQ002 - Add Row Button
Un botón "Agregar Producto" debe permitir agregar nuevas filas de entrada dinámicamente}

### RQ003 - Clear After Search
Después de completar la búsqueda, la primera pestaña debe resetearse para una nueva búsqueda (campos vacíos)

### RQ004 - Keyboard Close
La ventana debe cerrarse al presionar la tecla Escape

## Acceptance Criteria

- [ ] Múltiples productos se guardan en products.json como lista
- [ ] Después de buscar, los campos de entrada se limpian
- [ ] Tecla Escape cierra la ventana
