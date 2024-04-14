import os.path

import utils
import utils.download_data as dd


def load(data_folder: str, reload: bool = False) -> list:
    """
    Descarga los datos desde internet.
    :param data_folder: donde almacenar la data
    :param reload: recargar los archivos
    :return: lista de archivos descargados
    """
    data_files = []
    for color in range(len(utils.TAXI_COLORS)):
        for mm in range(len(utils.MONTHS)):
            for yyyy in range(len(utils.YEARS)):
                data_files.append(
                    utils.DATA_FILE_PATTERN
                    .replace("{{color}}", utils.TAXI_COLORS[color])
                    .replace("{{mm}}", utils.MONTHS[mm])
                    .replace("{{yyyy}}", utils.YEARS[yyyy])
                )

    # crear el folder de descarga si no existe
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Descargar los archivos
    downloaded = []
    for data_file in data_files:
        url = f"{utils.DATA_FILES_URL}/{data_file}"
        data_file_exists = os.path.exists(f"{data_folder}/{data_file}")
        should_download = (data_file_exists and reload) or not data_file_exists
        if should_download and dd.download_data(url, data_folder):
            downloaded.append(data_file)
    return downloaded


# if __name__ == "__main__":
#     downloaded = load(os.path.abspath("../../data"))
#     print(len(downloaded))
