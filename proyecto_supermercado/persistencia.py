import json
import os

def cargar_datos(archivo, estructura_base):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return estructura_base

def guardar_datos(archivo, datos):
    archivo_temp = archivo + '.tmp'
    try:
        with open(archivo_temp, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)
        os.replace(archivo_temp, archivo)
    except Exception as e:
        print(f"Error al guardar: {e}")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
