# scd30.py

"""
Módulo para interactuar con el sensor SCD30 (CO₂, temperatura y humedad).

Funcionalidades:
- Inicialización del sensor
- Lectura de datos de CO₂, temperatura y humedad
"""

import time
import adafruit_scd30
from config import i2c

# -----------------------------
# 🚀 Inicialización del sensor
# -----------------------------
def init_scd30():
    try:
        scd = adafruit_scd30.SCD30(i2c)
        scd.measurement_interval = 2  # segundos entre lecturas
        print("[SCD30] Sensor inicializado correctamente.")
        return scd
    except Exception as e:
        print(f"[SCD30] Error al inicializar el sensor: {e}")
        return None

# -----------------------------
# 🌮 Lectura de datos
# -----------------------------
def leer_scd30(sensor):
    """
    Retorna una tupla: (CO2 ppm, temperatura °C, humedad %)
    """
    try:
        if sensor.data_available:
            co2 = sensor.CO2
            temperatura = sensor.temperature
            humedad = sensor.relative_humidity
            return co2, temperatura, humedad
        else:
            return None, None, None
    except Exception as e:
        print(f"[SCD30] Error al leer datos: {e}")
        return None, None, None
