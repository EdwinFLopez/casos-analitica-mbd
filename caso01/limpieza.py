import pandas as pd


def limpieza_datos(df):
    df['vendorid'] = df['vendorid'].astype(str)
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    etiquetas = ['N', 'Y', 'n', 'y', 'ys', 'ye', 'no', 'yes']
    mapeo = {'N': 0, 'Y': 1, 'n': 0, 'y': 1, 'no': 0, 'yes': 1, 'ye': 1, 'ys': 1}
    df['store_and_fwd_flag'] = df['store_and_fwd_flag'].apply(lambda x: mapeo[x] if x in etiquetas else None)
    df = df.dropna(subset=['store_and_fwd_flag'])

    columnas_id = [
        'store_and_fwd_flag', 'ratecodeid', 'pulocationid', 'dolocationid',
        'passenger_count', 'payment_type', 'trip_type'
    ]
    for col in columnas_id:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int)
        except Exception as e:
            print(f"Error al procesar la columna {col}: {e}")

    # Listas de tuplas con las columnas con valores negativos o nulos
    condiciones = [
        ('trip_distance', 0),
        ('fare_amount', 0),
        ('total_amount', 0),
        ('passenger_count', 0),
        ('tip_amount', 0)
    ]

    for columna, valor_minimo in condiciones:
        df = df[df[columna] > valor_minimo]

    # Listas de tuplas con las columnas con valores negativos o nulos
    condiciones_2 = [
        ('congestion_surcharge', 0),
        ('improvement_surcharge', 0),
        ('tolls_amount', 0),
        ('tip_amount', 0),
        ('extra', 0),
        ('mta_tax', 0)
    ]
    for columna_2, valor_minimo_2 in condiciones_2:
        df = df[df[columna_2] > valor_minimo_2]

    try:
        df['ehail_fee'] = df['ehail_fee'].replace('None', 0).astype(float)
    except Exception as e:
        print(f"Se omiten las columnas: {e}")

    # Se eliminan filas duplicadas
    df = df.drop_duplicates()

    # Eliminamos las filas con el mismo tiempo de recogida y entrega
    df = df[df['lpep_pickup_datetime'] != df['lpep_dropoff_datetime']]

    return df


def limpieza_datos_2009(df):
    df['vendor_name'] = df['vendor_name'].astype(str)
    df['trip_pickup_datetime'] = pd.to_datetime(df['trip_pickup_datetime'])
    df['trip_dropoff_datetime'] = pd.to_datetime(df['trip_dropoff_datetime'])
    df = df.dropna(subset=['store_and_forward'])
    df['store_and_forward'] = df['store_and_forward'].astype(int)
    for col in ['store_and_forward', 'rate_code', 'passenger_count', 'payment_type']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int)

    condiciones = [
        ('trip_distance', 0),
        ('fare_amt', 0),
        ('total_amt', 0),
        ('passenger_count', 0),
        ('tip_amt', 0)
    ]
    for columna, valor_minimo in condiciones:
        df = df[df[columna] > valor_minimo]

    df = df.dropna(subset=['start_lon', 'start_lat', 'end_lon', 'end_lat'])
    df = df.drop_duplicates()
    df = df[df['trip_pickup_datetime'] != df['trip_dropoff_datetime']]

    return df
