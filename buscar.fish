#!/usr/bin/env fish

# cd al directorio del proyecto
set SCRIPT_DIR (dirname (status filename))
cd $SCRIPT_DIR

# Lanzar la GUI del proyecto
./venv/bin/python main_gui.py
