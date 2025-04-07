"""
Sería un script auxiliar que podrías ejecutar por separado para hacer pruebas rápidas de cada módulo o sensor individualmente, sin tener que correr todo el sistema.


from sensors.bmp390 import read_pressure, read_altitude
from sensors.scd30 import read_temperature, read_humidity, read_co2
from sensors.soil import read_soil_moisture
from sensors.uv import read_uv_index
from gps.gps import get_location
from motors.stepper import test_motor
from utils.logger import get_logger

logger = get_logger()

def test_all_sensors():
    logger.info("Testing BMP390")
    print("Pressure:", read_pressure())
    print("Altitude:", read_altitude())

    logger.info("Testing SCD30")
    print("Temperature:", read_temperature())
    print("Humidity:", read_humidity())
    print("CO₂:", read_co2())

    logger.info("Testing Soil Sensor")
    print("Soil Moisture:", read_soil_moisture())

    logger.info("Testing UV Sensor")
    print("UV Index:", read_uv_index())

    logger.info("Testing GPS")
    print("Location:", get_location())

def test_motors():
    logger.info("Testing Motors")
    test_motor()

if __name__ == "__main__":
    test_all_sensors()
    test_motors()

"""