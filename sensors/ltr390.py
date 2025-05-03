# ltr390.py

"""
Módulo para interactuar con el sensor LTR-390 (luz y UV).

Funcionalidades:
- Inicialización del sensor
- Lectura de luz visible y índice UV
"""

import time
import adafruit_ltr390
from config import i2c

# -----------------------------
# 🌍 Inicialización del sensor
# -----------------------------
def init_ltr390():
    try:
        ltr = adafruit_ltr390.LTR390(i2c)
        print("[LTR390] Sensor inicializado correctamente.")
        return ltr
    except Exception as e:
        print(f"[LTR390] Error al inicializar el sensor: {e}")
        return None

# -----------------------------
# 🌞 Lectura de datos
# -----------------------------
def leer_ltr390(sensor):
    """
    Retorna una tupla: (luz visible, índice UV)
    """
    try:
        luz_visible = sensor.light
        indice_uv = sensor.uvi
        return luz_visible, indice_uv
    except Exception as e:
        print(f"[LTR390] Error al leer datos: {e}")
        return None, None
