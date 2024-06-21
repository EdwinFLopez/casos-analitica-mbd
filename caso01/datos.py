import io
import os
import zipfile

import pandas as pd
import pyogrio
import geopandas as gpd
import requests


def obtener_data() -> dict:
    taxis_url = {
        "nyc_zones": "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD",
        "taxi_zone_lu": "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    }
    # Download taxi zones files
    url_taxi_zones_zip = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
    taxi_zones_path = os.path.abspath("./data/taxi_zones")
    rq = requests.get(url_taxi_zones_zip)

    # Unzip shape files
    zipfile.ZipFile(io.BytesIO(rq.content)).extractall(taxi_zones_path)

    # Load shape file and taxi zone
    df_taxi_zone_shp = gpd.read_file(f"{taxi_zones_path}/taxi_zones.shp", engine='pyogrio')
    # df_taxi_zone_shp.columns: Index(['OBJECTID', 'Shape_Leng', 'Shape_Area', 'zone', 'LocationID', 'borough',
    #        'geometry'],
    #       dtype='object')

    taxis_ds = {}
    for taxi_zone, url in taxis_url.items():
        taxis_ds[taxi_zone] = pd.read_csv(url)

    # nyc_zones.columns: Index([
    #       'OBJECTID', 'Shape_Leng', 'the_geom', 'Shape_Area', 'zone', 'LocationID', 'borough'
    #       ],dtype='object')
    # taxi_zone_lu.columns: Index([
    #       'LocationID', 'Borough', 'Zone', 'service_zone'
    #       ], dtype='object')

    # Join shape file and taxi zones files since geometry in shapefile is not lat-lon.
    taxi_shapes = df_taxi_zone_shp.set_index('LocationID').join(
            other=taxis_ds['nyc_zones'].set_index('LocationID'),
            on='LocationID', how='inner', lsuffix='_shp', rsuffix='_zones'
        ).join(
            other=taxis_ds['taxi_zone_lu'].set_index('LocationID'),
            on='LocationID', how='right', rsuffix='_lut'
        )
    # taxi_shapes.columns: Index(['LocationID', 'OBJECTID_shp', 'Shape_Leng_shp', 'Shape_Area_shp',
    #        'zone_shp', 'borough_shp', 'geometry', 'OBJECTID_zones',
    #        'Shape_Leng_zones', 'the_geom', 'Shape_Area_zones', 'zone_zones',
    #        'borough_zones', 'Borough', 'Zone', 'service_zone'],
    #       dtype='object')

    # Removemos columnas innecesarias y ajustamos nombres
    to_remove = [
        'OBJECTID_shp', 'Shape_Leng_shp', 'Shape_Area_shp', 'zone_shp', 'borough_shp', 'geometry',
        'OBJECTID_zones', 'borough_zones', 'zone_zones'
    ]
    to_rename = {
        'Shape_Leng_zones': 'Shape_Leng',
        'Shape_Area_zones': 'Shape_Area',
        'the_geom': 'geometry'
    }
    taxi_shapes.drop(columns=to_remove, inplace=True)
    taxi_shapes.rename(columns=to_rename, inplace=True)

    # Renombramos las columnas a minúsculas excepto LocationID
    taxi_shapes.columns = taxi_shapes.columns.str.lower()
    taxi_shapes.rename(columns={'locationid': 'LocationID'}, inplace=True)
    # Creamos un índice por LocationID.
    taxi_shapes.set_index('LocationID', inplace=True)

    # Agregamos el dataset con la información de los taxis
    datasets = {
        'taxi_shapes': taxi_shapes
    }
    # Datafiles URLs
    dataset_urls = {
        "greentd_202312": "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-12.parquet",
        "greentd_202311": "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-11.parquet",
        "yellowtd_202312": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-12.parquet",
        "yellowtd_202311": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-11.parquet",
        "yellowtd_200912": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2009-12.parquet"
    }
    for ds_name, url in dataset_urls.items():
        datasets[ds_name] = pd.read_parquet(url, engine='pyarrow')

    return datasets


if __name__ == '__main__':
    datasets = obtener_data()
    print("Fin")
