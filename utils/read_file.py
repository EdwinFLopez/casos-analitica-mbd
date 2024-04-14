import os
def read(file_path: str) -> str:
    """
    Lee el contenido de un archivo completo como texto
    :param file_path: ruta al archivo
    :return: texto del archivo
    """
    try:
        with open(file=os.path.abspath(file_path), mode='r', encoding="UTF-8") as f:
            file_contents = f.read()
        return file_contents
    except FileNotFoundError | Exception as e:
        return f"Error leyendo {file_path}: {str(e)}"
