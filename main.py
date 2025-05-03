# main.py

from sensors.bmp390 import init_bmp390, leer_bmp390
from sensors.ltr390 import init_ltr390, leer_ltr390
from sensors.scd30 import init_scd30, leer_scd30
from gps.gps import init_gps, leer_gps

import time


def main():
    # Inicialización de sensores
    bmp_sensor = init_bmp390()
    ltr_sensor = init_ltr390()
    scd_sensor = init_scd30()
    gps = init_gps()

    print("Iniciando lecturas...\n")

    while True:
        # Leer presión y temperatura BMP390
        presion, temperatura_bmp = leer_bmp390(bmp_sensor)
        if presion is not None and temperatura_bmp is not None:
            print(f"BMP390 -> Presión: {presion:.2f} hPa | Temp: {temperatura_bmp:.2f} °C")
        else:
            print("BMP390 -> Error de lectura")

        # Leer luz y UV LTR390
        luz, uv = leer_ltr390(ltr_sensor)
        if luz is not None and uv is not None:
            print(f"LTR390 -> Luz visible: {luz:.2f} lux | Índice UV: {uv:.2f}")
        else:
            print("LTR390 -> Error de lectura")

        # Leer CO₂, temperatura y humedad SCD30
        co2, temperatura_scd, humedad = leer_scd30(scd_sensor)
        if co2 is not None:
            print(f"SCD30 -> CO₂: {co2:.1f} ppm | Temp: {temperatura_scd:.1f} °C | Humedad: {humedad:.1f}%")
        else:
            print("SCD30 -> Esperando datos...")

        # Leer datos GPS
        gps_data = leer_gps(gps)
        if gps_data:
            print(f"GPS -> Hora: {gps_data['hora']} | Lat: {gps_data['latitud']:.6f} | Lon: {gps_data['longitud']:.6f} | Alt: {gps_data['altitud']:.1f} m | Vel: {gps_data['velocidad']:.2f} kn | Sat: {gps_data['num_satelites']}")
        else:
            print("GPS -> Sin señal o sin fix")

        print("-" * 40)
        time.sleep(5)

if __name__ == "__main__":
    main()
