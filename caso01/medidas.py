import pandas as pd


def tarifa_por_viaje(gdf: pd.DataFrame) -> list:
    resultado = (
        gdf.assign(fare_per_km=lambda x: x['fare_amount'] / x['trip_distance'])
        .loc[lambda x: x['fare_per_km'].idxmax()]
    )
    print('El trayecto en el que la relación precio/km más alta es:')
    print(f"Empieza en: {resultado['zone_x']} y finaliza en:  {resultado['zone_y']}")
    return resultado[[
        'vendorid', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
        'store_and_fwd_flag', 'ratecodeid', 'pulocationid', 'dolocationid',
        'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
        'tip_amount'
    ]]


def evolucion_tiempo_trayecto(t_df):
    t_df['lpep_pickup_datetime'] = pd.to_datetime(t_df['lpep_pickup_datetime']).dt.hour
    media_tiempo_viaje = t_df.groupby('lpep_pickup_datetime')['trip_time_in_secs'].mean() / 60
    media_distancia_viaje = t_df.groupby('lpep_pickup_datetime')['trip_distance'].mean()
    return media_tiempo_viaje, media_distancia_viaje


def probabilidad_zonas(dfx, X, zona_recogida, zona_destino):
    viajes = dfx[(dfx['zone_x'] == zona_recogida) & (dfx['zone_y'] == zona_destino)]
    viajes['tiempo_viaje_minutos'] = viajes['trip_time_in_secs'] / 60
    probabilidad = (viajes['tiempo_viaje_minutos'] < X).mean()
    return probabilidad
