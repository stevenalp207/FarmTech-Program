import time
import adafruit_scd30
from config import i2c

# -----------------------------
# 🚀 Inicialización del sensor
# -----------------------------
def init_scd30():
    try:
        # Para garantizar frecuencia baja en i2c, debe configurarse al crear i2c (config.py)
        # Pero aquí aseguramos que el sensor se inicialice correctamente.
        scd = adafruit_scd30.SCD30(i2c)
        scd.measurement_interval = 2
        print("[SCD30] Sensor inicializado correctamente.")

        # Esperar un poco para que el sensor empiece a entregar datos
        print("[SCD30] Esperando para que el sensor comience a entregar datos...")
        time.sleep(5)  # 5 segundos para que el sensor haga la primera medición
        return scd
    except Exception as e:
        print(f"[SCD30] Error al inicializar el sensor: {e}")
        return None


# -----------------------------
# 🌮 Lectura de datos
# -----------------------------
def leer_scd30(sensor):
    try:
        print(f"[SCD30] data_available = {sensor.data_available}")
        if sensor.data_available:
            co2 = sensor.CO2
            temperatura_scd = sensor.temperature
            humedad = sensor.relative_humidity
            return co2, temperatura_scd, humedad
        else:
            return None, None, None
    except Exception as e:
        print(f"[SCD30] Error al leer datos: {e}")
        return None, None, None
