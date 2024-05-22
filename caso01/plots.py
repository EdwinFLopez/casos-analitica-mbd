import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def plot_histograma_df(df: pd.DataFrame, edge_color: str, color: str) -> None:
    """
    Traza un histograma para cada columna de un dataframe
    :param df: dataframe que contiene los datos
    :param edge_color: color de borde
    :param color: color de relleno
    :return: None
    """
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            plt.figure(figsize=(10, 4))
            plt.hist(df[column].dropna(), bins=30, edgecolor=edge_color, color=color)
            plt.title(f'Histograma de {column}')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            plt.grid(True)
            plt.show()


def plot_boxplot_df(df: pd.DataFrame, title: str, column_name: str) -> None:
    """
    Traza un boxplot para una columna del dataframe
    :param df: dataframe que contiene los datos
    :param title: nombre del plot
    :param column_name: nombre de la columna
    :return:
    """
    plt.figure(figsize=(20, 10))
    sns.boxplot(data=df[column_name], orient="h")
    plt.title(title)
    plt.xlabel('Valores')
    plt.grid(True)
    plt.show()


def plot_pickup_zones(df: pd.DataFrame):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    ax1.scatter(df['pickup_longitude'], df['pickup_latitude'], s=0.1)
    ax1.set_title('Zonas de Recogida')
    ax1.set_xlabel('Longitud')
    ax1.set_ylabel('Latitud')
    ax2.scatter(df['dropoff_longitude'], df['dropoff_latitude'], s=0.1)
    ax2.set_title('Zonas de Llegada')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Latitud')

    plt.show()


def plot_heatmap_por_origen(gdf, origin, column="pulocationid", title_prefix="NYC Taxi Pickup Locations", cmap="viridis"):
    filtered_gdf = gdf[gdf['origin'] == origin]
    fig, ax = plt.subplots(figsize=(12, 8))
    filtered_gdf.plot(column=column, cmap=cmap, ax=ax, legend=True)
    ax.set_title(f"{title_prefix} {origin}")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitude")
    plt.show()
