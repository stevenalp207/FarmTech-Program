# bmp390.py

"""
Módulo para interactuar con el sensor BMP390.

Funcionalidades:
- Inicialización del sensor
- Lectura de temperatura y presión
"""

import time
import adafruit_bmp3xx
from config import i2c

# -----------------------------
# 🧭 Inicialización del sensor
# -----------------------------
def init_bmp390():
    try:
        bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        bmp390.pressure_oversampling = 8
        bmp390.temperature_oversampling = 2
        print("[BMP390] Sensor inicializado correctamente.")
        return bmp390
    except Exception as e:
        print(f"[BMP390] Error al inicializar el sensor: {e}")
        return None

# -----------------------------
# 🌡 Lectura de datos
# -----------------------------
def leer_bmp390(sensor):
    """
    Retorna una tupla: (temperatura °C, presión hPa)
    """
    try:
        temperatura = sensor.temperature
        presion = sensor.pressure
        return temperatura, presion
    except Exception as e:
        print(f"[BMP390] Error al leer datos: {e}")
        return None, None
