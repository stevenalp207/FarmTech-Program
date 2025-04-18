from setuptools import setup, find_packages

setup(
    name="farmtech",
    version="0.1.0",
    packages=find_packages(),  # Esto detecta carpetas con __init__.py automáticamente
    install_requires=[
        # Sensores Adafruit
        "adafruit-circuitpython-bmp3xx",
        "adafruit-circuitpython-scd30",
        "adafruit-circuitpython-seesaw",
        "adafruit-circuitpython-ltr390",

        # Bonnets / placas
        "adafruit-circuitpython-mcp230xx",
        "adafruit-circuitpython-motorkit",
        "adafruit-circuitpython-gps",

        # Comunicación hardware
        "Adafruit-Blinka",  # Necesario para usar board y busio en Raspberry Pi
        "smbus2",

        # General
        "numpy",
        "pandas"
    ],
    author="Oratorio Tecnologico Carlos Acutis",
    description="Robot asistente agricola",
    python_requires=">=3.7",
)
