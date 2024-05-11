# Rutas a la zona de datos locales.
import os

from utils.unzip_data import unzip_data


def unzip_dataset() -> str:
    """
    Función para descomprimir el archivo dataset del caso dos.
    :return: ruta al archivo dataset
    """
    zip_path = os.path.abspath("./dataset/Caso3training.1600000.processed.noemoticon.zip")
    target_folder = os.path.abspath("./data")
    target_csv = "training.1600000.processed.noemoticon.csv"

    # Crear el folder "./data/" si no existe
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    else:
        print(f"Folder {target_folder} ya existe.")

    # Descomprimir el zip encontrado en "./dataset/", se crea el csv
    target_csv_path = os.path.join(target_folder, target_csv)
    if not os.path.exists(target_csv_path):
        unzip_data(zip_path, target_folder)
        print(f"Unzipped dataset: {target_csv_path}")
    else:
        print(f"Archivo de datos {target_csv} ya existe")

    return target_csv_path
