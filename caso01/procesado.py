import pandas as pd


def merge_taxi_with_zones(taxi_df, zones_df):
    """
    Se fusionan el dataFrame de taxis con el DataFrame de zonas basado en la columna de ID de ubicación de recogida
    :param taxi_df:
    :param zones_df:
    :return:
    """

    merged_df = pd.merge(taxi_df, zones_df, left_on='pulocationid', right_on='locationid')
    merged_df = merged_df.drop(columns='locationid')
    merged_df = merged_df.rename(columns={
        'borough': 'pu_borough',
        'zone': 'pu_zone',
        'service_zone': 'pu_service_zone'
    })

    # Repetir el proceso para la ubicación de entrega
    merged_df = pd.merge(merged_df, zones_df, left_on='dolocationid', right_on='locationid')
    merged_df = merged_df.drop(columns='locationid')
    merged_df = merged_df.rename(columns={
        'borough': 'do_borough',
        'zone': 'do_zone',
        'service_zone': 'do_service_zone'
    })

    return merged_df
