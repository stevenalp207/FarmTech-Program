# main.py

import time
import json
from datetime import datetime
import threading

# Sensores
from sensors.bmp390 import init_bmp390, leer_bmp390
from sensors.ltr390 import init_ltr390, leer_ltr390
from sensors.scd30 import init_scd30, leer_scd30

# GPS
from gps.gps import init_gps, leer_lat_lon
from gps.satelite import obtener_datos_de_ayer

# Motores
import motors.stepper as stepper

#Control remoto
from motors.control_remoto import inicializar_joystick, leer_controles

# Utilidades
from utils.logger import logger



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
    clima = obtener_datos_de_ayer(lat, lon)

    if clima:
        logger.info("Lectura datos climáticos NASA")
        print(json.dumps(clima, indent=4))
    else:
        print("[NASA] No se pudieron obtener datos del clima.")
        logger.error("Error al leer datos climáticos NASA")

    return datos_gps, clima

def control_remoto():
    joystick = inicializar_joystick()
    if joystick is None:
        print("[PS4] No se encontró joystick. Control remoto desactivado.")
        logger.warning("No se encontró joystick. Control remoto desactivado.")
        return
    
    print("[PS4] Control remoto iniciado con mando PS4...")
    logger.info("Control remoto iniciado con mando PS4")
    
    while True:
        controles = leer_controles(joystick)

        if controles["L1"][1]:  # L1 presionado
            print("[PS4] IZQUIERDA")
            logger.info("Movimiento a la izquierda")
            stepper.move_left()

        if controles["R1"][1]:  # R1 presionado
            print("[PS4] DERECHA")
            logger.info("Movimiento a la derecha")
            stepper.move_right()

        if controles["L2"][1]:  # L2 presionado
            print("[PS4] ATRÁS")
            logger.info("Movimiento hacia atrás")
            stepper.move_backward()

        if controles["R2"][1]:  # R2 presionado
            print("[PS4] ADELANTE")
            logger.info("Movimiento hacia adelante")
            stepper.move_forward()

        time.sleep(0.1)  # Pequeña pausa para no saturar el CPU

def main():
    bmp_sensor, ltr_sensor, scd_sensor, gps = inicializar_sensores()
    
    # Iniciar hilo para control remoto
    hilo_control = threading.Thread(target=control_remoto, daemon=True)
    hilo_control.start()

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
