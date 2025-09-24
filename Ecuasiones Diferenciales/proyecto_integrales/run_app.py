#!/usr/bin/env python3
"""
Solucionador Avanzado de Integrales - Versión Modular
Archivo principal ejecutable
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_app import main

if __name__ == "__main__":
    main()
