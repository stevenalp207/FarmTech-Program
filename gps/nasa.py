import requests
import json
from datetime import datetime, timedelta

def obtener_datos_climaticos(latitude, longitude, start_date, end_date, parameters=["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "RH2M", "WS10M", "ALLSKY_SFC_SW_DWN"]):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": ",".join(parameters),
        "community": "AG",
        "latitude": latitude,
        "longitude": longitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON",
        "user": "FarmTech",
    }

    try:
        # Realizamos la solicitud a la API
        response = requests.get(url, params=params)
        
        # Comprobamos si la solicitud fue exitosa (código de estado 200)
        response.raise_for_status()

        # Convertimos la respuesta en formato JSON
        data = response.json()

        # Verificamos si los datos están en el formato esperado
        if "properties" in data and "parameter" in data["properties"]:
            return data["properties"]["parameter"]
        else:
            print("Error: Los datos no están en el formato esperado.")
            return None

    except requests.exceptions.RequestException as e:
        # En caso de error de red o solicitud fallida
        print(f"Error en la solicitud: {e}")
        return None
    except ValueError as e:
        # En caso de que los datos no sean JSON válidos
        print(f"Error al procesar los datos JSON: {e}")
        return None

# Calcular la fecha de ayer
fecha_ayer = (datetime.now() - timedelta(7)).strftime("%Y%m%d")

# Parámetros de ubicación (puedes cambiarlos a la ubicación deseada)
latitude = 9.8967914
longitude = -84.0815496

# Llamada a la función para obtener los datos con la fecha de ayer
data = obtener_datos_climaticos(latitude, longitude, fecha_ayer, fecha_ayer)

# Si los datos se obtienen correctamente, se imprimen de forma legible
if data:
    print(json.dumps(data, indent=4))
