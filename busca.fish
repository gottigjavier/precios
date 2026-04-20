#!/usr/bin/env fish

# cd al directorio del script
set SCRIPT_DIR (dirname (status filename))
cd $SCRIPT_DIR

# En products.json está los productos a buscar
# Lo supermercados están listados en el comando y detallados en supermercados.json. Debe coincidir el nombreitado con el value de la key "id"
# Argumento: --supermarkets para especificar los supermercados a buscar (comma-separated)
# Si no se pasa, usa masonline,dia,carrefour,vea por defecto

set -q argv[1]; or set -g SUPERMARKETS "masonline,dia,carrefour,vea"

if test (count $argv) -ge 2
    if test "$argv[1]" = "--supermarkets"
        set -g SUPERMARKETS "$argv[2]"
    end
end

./venv/bin/python main.py --input products.json --paginated --supermarkets $SUPERMARKETS -o resultados
