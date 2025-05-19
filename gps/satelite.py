import requests
from datetime import datetime, timedelta

def obtener_datos_climaticos(latitude, longitude, start_date, end_date,
    parameters=[
    "T2M", "T2M_MAX", "T2M_MIN", "T2M_RANGE",  # Temperaturas
    "PRECTOTCORR", "RH2M", "QV2M",            # Humedad y precipitación
    "WS10M", "WS10M_MAX", "WS10M_MIN",        # Viento
    "T2MDEW", "T2MWET",                       # Punto de rocío y temp húmeda
    "TS",                                     # Temp. de la superficie
    "ALLSKY_SFC_LW_DWN", "ALLSKY_SFC_SW_DWN", # Radiación total
    "CLRSKY_SFC_SW_DWN", "ALLSKY_KT",         # Radiación bajo cielo despejado y claridad
    "EVLAND",                                   # Evaporación
    "PS"                                      # Presión
    ]):
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
            parametros = data["properties"]["parameter"]
            resumen = {
                parametro: list(valores_por_fecha.values())[0]
                for parametro, valores_por_fecha in parametros.items()
            }
            return resumen
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

# Llamada a la función para obtener los datos con la fecha de ayer
def obtener_datos_consulta(lat, lon):
    fecha_ayer = (datetime.now() - timedelta(5)).strftime("%Y%m%d")
    return obtener_datos_climaticos(lat, lon, fecha_ayer, fecha_ayer)
