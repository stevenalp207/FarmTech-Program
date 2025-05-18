# main.py

import time
import json
from datetime import datetime

# Sensores
from sensors.bmp390 import init_bmp390, leer_bmp390
from sensors.ltr390 import init_ltr390, leer_ltr390
from sensors.scd30 import init_scd30, leer_scd30

# GPS
from gps.gps import init_gps, leer_lat_lon
from gps.satelite import obtener_datos_consulta

# Motores
from motors.stepper import move_forward, move_backward, move_left, move_right

# Utilidades
from utils.logger import logger
import threading


def inicializar_sensores():
    logger.info("Inicio del sistema")
    print("Inicializando sensores...")

    bmp_sensor = init_bmp390()
    ltr_sensor = init_ltr390()
    scd_sensor = init_scd30()
    gps = init_gps()

    return bmp_sensor, ltr_sensor, scd_sensor, gps


def leer_todos_los_sensores(bmp, ltr, scd):
    # BMP390
    temperatura_bmp, presion = leer_bmp390(bmp)
    if temperatura_bmp is not None and presion is not None:
        print(f"[BMP390] Presión: {presion:.2f} hPa | Temp: {temperatura_bmp:.2f} °C")
        logger.info("Lectura BMP390")
    else:
        print("[BMP390] Error de lectura")
        logger.error("Error al leer BMP390")

    # LTR390
    luz, uv, uvs, lux = leer_ltr390(ltr)
    if None not in (luz, uv, uvs, lux):
        print(f"[LTR390] Luz cruda: {luz:.2f} | UV crudo: {uvs:.2f} | Lux: {lux:.2f} lx | Índice UV: {uv:.2f}")
        logger.info("Lectura LTR390")
    else:
        print("[LTR390] Error de lectura")
        logger.error("Error al leer LTR390")

    # SCD30
    co2, temperatura_scd, humedad = leer_scd30(scd)
    if co2 is not None:
        print(f"[SCD30] CO₂: {co2:.1f} ppm | Temp: {temperatura_scd:.1f} °C | Humedad: {humedad:.1f}%")
        logger.info("Lectura SCD30")
    else:
        print("[SCD30] Esperando datos...")
        logger.error("Error al leer SCD30")

    return {
        "bmp390": {"presion": presion, "temperatura": temperatura_bmp},
        "ltr390": {"luz": luz, "uv": uv, "uvs": uvs, "lux": lux},
        "scd30": {"co2": co2, "temperatura": temperatura_scd, "humedad": humedad}
    }


def leer_datos_gps_y_clima(gps):
    datos_gps = leer_lat_lon(gps)
    if datos_gps is None:
        print("[GPS] Esperando señal...")
        logger.warning("GPS sin señal")
        return None, None

    lat = datos_gps["lat"]
    lon = datos_gps["lon"]
    print(f"[GPS] Latitud: {lat:.6f} | Longitud: {lon:.6f}")

    # Consulta clima satelital NASA
    print("[NASA] Consultando datos climáticos del satélite...")
    clima = obtener_datos_consulta(lat, lon)

    if clima:
        logger.info("Lectura datos climáticos NASA")
        print(json.dumps(clima, indent=4))
    else:
        print("[NASA] No se pudieron obtener datos del clima.")
        logger.error("Error al leer datos climáticos NASA")

    return datos_gps, clima


def main():
    bmp_sensor, ltr_sensor, scd_sensor, gps = inicializar_sensores()
    
    print("\n------------------[ INICIO DE LECTURAS ]------------------")

    while True:
        sensores = leer_todos_los_sensores(bmp_sensor, ltr_sensor, scd_sensor)
        datos_gps, clima = leer_datos_gps_y_clima(gps)

        datos_json = {
            "timestamp": datetime.utcnow().isoformat(),
            "sensor_bmp390": {
                "presion_hPa": sensores["bmp390"]["presion"],
                "temperatura_a": sensores["bmp390"]["temperatura"]
            },
            "sensor_ltr390": {
                "luz_cruda": sensores["ltr390"]["luz"],
                "uv_crudo": sensores["ltr390"]["uvs"],
                "lux": sensores["ltr390"]["lux"],
                "indice_uv": sensores["ltr390"]["uv"]
            },
            "sensor_scd30": {
                "co2_ppm": sensores["scd30"]["co2"],
                "temperatura_b": sensores["scd30"]["temperatura"],
                "humedad_pct": sensores["scd30"]["humedad"]
            },
            "gps": {
                "latitud": datos_gps["lat"] if datos_gps else None,
                "longitud": datos_gps["lon"] if datos_gps else None
            },
            "clima_satelital": clima or {}
        }

        print("\n[JSON] Datos para envío:")
        print(json.dumps(datos_json, indent=4))
        logger.info("Datos JSON preparados para envío")

        print("-" * 60)
        time.sleep(1)


if __name__ == "__main__":
    main()
