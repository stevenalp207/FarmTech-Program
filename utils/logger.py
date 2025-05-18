import logging
from datetime import datetime
import os

# Crear carpeta logs si no existe
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Nombre del archivo de log con fecha
log_filename = os.path.join(log_folder, datetime.now().strftime("farmtech_%Y-%m-%d.log"))

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("farmtech")
