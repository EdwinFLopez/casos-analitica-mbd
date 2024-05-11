"""
Paquete de utilidades.
"""
# =============================================================================
# CONSTANTS
# =============================================================================

# CONTENIDO
ASSETS_DIR = "./pages"
INTRO_PATH = f"{ASSETS_DIR}/intro.md"

# DATA FILES
REFERER =  "https://www.nyc.gov"
DATA_FILES_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DATA_FILE_PATTERN = "{{color}}_tripdata_{{yyyy}}-{{mm}}.parquet"
TAXI_COLORS = ["yellow", "green"]
YEARS = [f"{year}" for year in range(2009, 2025)]
MONTHS = [f"{mm:02}" for mm in range(1, 13)]
TAXI_PDF_ASSETS = [
    "https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf",
    "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf",
    "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf",
    "https://www.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf"
]
TAXI_ZONE_ASSETS = [
    "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
    "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
]
