# main.py
from sensors.bmp390 import init_bmp390, leer_bmp390
from sensors.ltr390 import init_ltr390, leer_ltr390
from sensors.scd30 import init_scd30, leer_scd30

from gps.gps import init_gps, leer_lat_lon
from motors.stepper import move_stepper_motor_continuous
import time

from gps.satelite import obtener_datos_de_ayer 

from utils.logger import logger



def main():
    # Inicialización
    bmp_sensor = init_bmp390()
    ltr_sensor = init_ltr390()
    scd_sensor = init_scd30()
    gps = init_gps()
    logger.info("Inicio del sistema")


    #print("Iniciando movimiento de ambos motores de forma constante...")
    #move_stepper_motor_continuous(delay=0.01)  

    print("--------------------[INICIO DEL LECTURAS, SENSORES Y GPS]--------------------")
    logger.info("Inicio de lecturas, sensores y GPS")

    while True:
        # Leer presión y temperatura BMP390
        temperatura_bmp, presion = leer_bmp390(bmp_sensor)
        if presion is not None and temperatura_bmp is not None:
            print(f"BMP390 -> Presión: {presion:.2f} hPa | Temp: {temperatura_bmp:.2f} °C")
            logger.info("Lectura BMP390")
        else:
            print("BMP390 -> Error de lectura")
            logger.error("Error al leer el sensor BMP390")

        # Leer luz y UV LTR390
        luz, uv = leer_ltr390(ltr_sensor)
        if luz is not None and uv is not None:
            print(f"LTR390 -> Luz visible: {luz:.2f} lux | Índice UV: {uv:.2f}")
            logger.info("Lectura LTR390")
        else:
            print("LTR390 -> Error de lectura")
            logger.error("Error al leer el sensor LTR390")

        # Leer CO₂, temperatura y humedad SCD30
        co2, temperatura_scd, humedad = leer_scd30(scd_sensor)
        if co2 is not None:
            print(f"SCD30 -> CO₂: {co2:.1f} ppm | Temp: {temperatura_scd:.1f} °C | Humedad: {humedad:.1f}%")
            logger.info("Lectura SCD30")
        else:
            print("SCD30 -> Esperando datos...")
            logger.error("Error al leer el sensor SCD30")

        datos = leer_lat_lon(gps)
        if datos is None:
            print("GPS -> Esperando señal...")
            logger.warning("GPS sin señal")
        else:
            print(f"Latitud -> {datos['lat']:.6f} | Longitud -> {datos['lon']:.6f}")
            lat = datos['lat']
            lon = datos['lon']
            
            # Consulta a NASA con esas coordenadas
            print("[NASA] Consultando datos climáticos del satelite...")
            clima = obtener_datos_de_ayer(lat, lon)

            if clima:
                logger.info("Lectura datos climáticos NASA")
                import json
                print(json.dumps(clima, indent=4))
            else:
                print("[NASA] No se pudieron obtener datos del clima.")
                logger.error("Error al leer datos climáticos NASA")

        print("-" * 40)
        time.sleep(1)

if __name__ == "__main__":
    main()
