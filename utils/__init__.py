"""
Paquete de utilidades.
"""
# =============================================================================
# CONSTANTS
# =============================================================================

# CONTENIDO
ASSETS_DIR = "./assets"
INTRO_PATH = f"{ASSETS_DIR}/intro.md"

# DATA FILES
DATA_FILES_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DATA_FILE_PATTERN = "{{color}}_tripdata_{{yyyy}}-{{mm}}.parquet"
TAXI_COLORS = ["yellow", "green"]
YEARS = [f"{year}" for year in range(2009, 2025)]
MONTHS = [f"{mm:02}" for mm in range(1, 13)]
