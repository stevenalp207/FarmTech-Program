# config.py

"""
Función: Configuraciones centralizadas del sistema.
Contiene:

Direcciones I2C de los sensores
Umbrales de temperatura, humedad, CO₂
Pines usados
Velocidad de motores
Datos de red (si aplica)
Variables globales
"""

# -----------------------------
# 🧪 I2C Addresses
# -----------------------------
I2C_ADDR_BMP390 = 0x77  # Sensor de presión
I2C_ADDR_SCD30 = 0x61   # Sensor CO₂, temperatura y humedad
I2C_ADDR_SOIL = 0x36    # Sensor de humedad de suelo (STEMMA)
I2C_ADDR_LTR390 = 0x53  # Sensor de luz UV
I2C_ADDR_GPIO_EXPANDER = 0x20
I2C_ADDR_MOTOR_BONNET = 0x60  # Dirección del motor bonnet

# -----------------------------
# 🌡 Umbrales (pueden ajustarse)
# -----------------------------
TEMP_MIN_C = 10.0
TEMP_MAX_C = 35.0
HUMEDAD_MIN = 30.0       # %
HUMEDAD_MAX = 80.0       # %
CO2_MAX_PPM = 1000       # partes por millón

# -----------------------------
# ⚙️ Pines y hardware
# -----------------------------
PIN_MOTOR_STEP = 17      # GPIO17
PIN_MOTOR_DIR = 27       # GPIO27

# -----------------------------
# 🌀 Configuración de motores
# -----------------------------
MOTOR_STEPS_PER_REV = 200
MOTOR_RPM = 60
MOTOR_DELAY = 0.005      # Delay entre pasos para velocidad

# -----------------------------
# 📡 GPS HAT - Pines usados
# -----------------------------
GPS_UART_TX = 14    # GPIO14 - TX desde la Pi al GPS
GPS_UART_RX = 15    # GPIO15 - RX desde el GPS a la Pi
GPS_PPS = 4         # GPIO4 - Pulse Per Second (opcional)
GPS_FIX_LED = 17    # GPIO17 - Indicador de fix GPS (puede variar)

# -----------------------------
# 🌐 Red 
# -----------------------------
USE_WIFI = False
WIFI_SSID = "TuSSID"
WIFI_PASSWORD = "TuClave"

# -----------------------------
# 🔁 Variables globales de estado
# -----------------------------
estado_robot = {
    "sensores_activos": True,
    "modo_manual": False,
    "gps_conectado": False,
    "registro_activo": True,
}

# -----------------------------
# 📍 Otros (como constantes de sistema)
# -----------------------------
LOG_PATH = "/home/pi/farmtech/logs/"
DATOS_PATH = "/home/pi/farmtech/data/"

# -----------------------------
# 🧩 Bus I2C
# -----------------------------
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
