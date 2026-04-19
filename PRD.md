# PRD: Supermercados Scraper

## Resumen Ejecutivo

Herramienta CLI para scraping de precios de productos en supermercados online argentinos (MASOnline/Changomas, DIA, Carrefour, Vea). Soporta búsqueda, filtrado, paginación y exportación a CSV/JSON.

## Problema y Contexto

**Problema:** Los consumidores en Argentina necesitan comparar precios entre diferentes supermercados para ahorrar dinero, pero actualmente deben visitar cada sitio web manualmente, buscando producto por producto.

**Por qué importa ahora:** 
- La inflación argentina hace que los precios varíen significativamente entre comercios
- No existe una herramienta gratuita y de código abierto para comparación de precios de supermercados
- Las apps existentes suelen tener regionalidad limitada o costos de suscripción
- VTEX es la plataforma dominante en retail argentino, facilitando el scraping de múltiples sitios con una arquitectura similar

## Propuesta de Valor

Herramienta de línea de comandos que permite buscar productos en múltiples supermercados simultáneamente, exportando resultados en CSV/JSON para análisis posterior.

## Definición de Éxito

- [ ] El sistema busca productos en MASOnline, DIA, Carrefour, Vea
- [ ] Los resultados incluyen: nombre, marca, precio, precio_original, descuento, disponible, url, supermercado
- [ ] El filtrado por min_price funciona correctamente
- [ ] El filtrado por available_only excluye productos no disponibles
- [ ] La exportación CSV genera archivo válido con headers
- [ ] La exportación JSON incluye timestamp
- [ ] El CLI acepta todas las opciones especificadas
- [ ] La búsqueda paginada retorna todos los productos
- [ ] El sistema maneja errores gracefully (print sin crash)

## Customer

**Usuario objetivo:** Consumidores argentinos que desean comparar precios de supermercado, priorizando transparencia y privacidad (no requieren registro, datos locales).

**User stories:**
- "Quiero ejecutar un comando con una lista de productos y obtener un CSV con los precios de cada supermercado para decidir dónde comprar."
- "Quiero especificar productos directamente en la línea de comandos para una búsqueda rápida."
- "Quiero filtrar resultados por precio mínimo para encontrar opciones dentro de mi presupuesto."
- "Quiero ver solo productos disponibles para evitar ofertas expiradas."
- "Quiero exportar a múltiples formatos (CSV y JSON) en una sola ejecución."

## Requisitos Funcionales

### RQ001 - Búsqueda de Productos
El sistema debe permitir buscar productos por nombre, marca y tamaño en los supermercados configurados.

### RQ002 - Filtrado de Resultados
El sistema debe filtrar resultados por:
- Precio mínimo (`--min-price`)
- Solo disponibles (`--available-only`)

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
- `--min-price`: Precio mínimo
- `--available-only`: Solo productos disponibles
- `--paginated`: Buscar en todos los productos paginados

## Alcance

### Funcionalidades MVP
- CLI con Typer para ejecución de búsquedas
- Scraper para MASOnline, DIA, Carrefour y Vea (VTEX)
- Filtrado por producto, marca y tamaño
- Filtrado por precio mínimo y disponibilidad
- Exportación a CSV y JSON
- Soporte para múltiples productos
- Búsqueda paginada

### Fuera de Alcance (v1)
- UI web o GUI
- Historial de precios
- Alertas de precios
- Scraping de sitios no-VTEXT (ej: Walmart, Coto)
- Integración con bases de datos
- Ranking automático de "mejor precio"
- Cache local

## Why Now

1. **Momento óptimo:** VTEX es la plataforma dominante en retail argentino - hay consistencia de APIs
2. **Simplicidad:** El MVP puede construirse en 1-2 semanas
3. **Diferenciación:** No existe herramienta CLI similar de código abierto para Argentina

## Decisiones Pendientes

1. ¿Soportar más supermercados no-VTEXT (ej: Walmart, Coto)?
2. ¿Añadir ranking de "mejor precio" automáticamente?
3. ¿Implementar cache local para evitar rescraping?

## Diseño Técnico

**Ejemplo de uso:**
```bash
python main.py --input products.json --supermarkets masonline,dia --output resultados
python main.py --products "detergente,magistral,500 ml" --min-price 500 --available-only
```

**Stack:**
- Python 3.14+
- Typer (CLI)
- Requests
- Fake UserAgent

**Estructura de salida:**

*CSV:*
```
producto,marca,tamaño,supermercado,precio,precio_original,descuento,disponible,url
```

*JSON:*
```json
{
  "productos": [
    {
      "producto": "detergente",
      "marca": "magistral",
      "tamaño": "500 ml",
      "resultados": [
        {
          "nombre": "...",
          "marca": "...",
          "precio": 1234.56,
          "precio_original": 1500.00,
          "descuento": 18,
          "disponible": true,
          "url": "...",
          "supermercado": "masonline"
        }
      ]
    }
  ],
  "timestamp": "2026-04-14T12:00:00"
}
```

## Cronograma Estimado

| Fase | Tiempo |
|------|--------|
| MVP (MASOnline + DIA) | 1 semana |
| Testing y refinamiento | 3 días |
| Documentación | 2 días |

## Links Relacionados

- Repositorio: local
- API docs VTEX: https://developers.vtex.com/docs
- Especificación: `.artifacts/features/001-scrape-supermercados/spec.md`