# sensors/gps.py

import time
import serial
import adafruit_gps

def init_gps():
    """
    Inicializa el GPS a través del puerto UART (/dev/serial0).
    Retorna el objeto gps.
    """
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)
    
    # Configura las frases NMEA deseadas
    gps.send_command(b"PMTK220,1000")  # Actualización cada 1 segundo
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # GGA y RMC

    return gps

def leer_gps(gps):
    """
    Actualiza y devuelve los datos del GPS.
    Retorna un diccionario con los campos disponibles.
    """
    gps.update()
    time.sleep(1)

    if not gps.has_fix:
        return None  # Sin señal GPS

    datos = {
        "hora": f"{gps.timestamp_utc.tm_hour:02}:{gps.timestamp_utc.tm_min:02}:{gps.timestamp_utc.tm_sec:02}" if gps.timestamp_utc else None,
        "latitud": gps.latitude,
        "longitud": gps.longitude,
        "altitud": gps.altitude_m,
        "velocidad": gps.speed_knots,
        "num_satelites": gps.satellites,
    }
    return datos
