# Rutas a la zona de datos locales.
import os
from pathlib import Path

from utils.unzip_data import unzip_data


def unzip_dataset(zip_path: str, target_dir: str) -> None:
    """
    Función para descomprimir el archivo dataset del caso tres.
    :return: ruta al archivo dataset
    """

    target_folder = os.path.abspath(target_dir)
    # Crear el folder "./data/" si no existe
    if not os.path.exists(target_folder):
        Path(target_folder).mkdir(parents=True, exist_ok=True)
        print(f"Folder {target_folder} creado.")
    else:
        print(f"Folder {target_folder} ya existe.")

    # Descomprimir el zip enviado si existe.
    if os.path.exists(zip_path):
        unzip_data(zip_path, target_folder)
        print(f"Unzipped: {zip_path}")
    else:
        print(f"Archivo de datos {zip_path} no existe")
