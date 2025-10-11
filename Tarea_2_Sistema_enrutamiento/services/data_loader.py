import pandas as pd
import numpy as np

def cargar_datos():
    combustible = pd.read_csv("data/matriz_costos_combustible.csv", index_col=0).astype(float).values
    distancias = pd.read_csv("data/matriz_distancias.csv", index_col=0).astype(float).values
    ubicaciones_df = pd.read_csv("data/datos_distribucion_tiendas.csv")

    num_vehiculos = 10
    centros_id = list(range(1, 11))
    tiendas_id = list(range(11, 101))

    id_a_nombre = {}
    for _, row in ubicaciones_df.iterrows():
        nombre = row['Nombre']
        id = int(row.name) + 1
        id_a_nombre[id] = nombre

    tiendas = tiendas_id.copy()
    np.random.shuffle(tiendas)
    rutas = np.array_split(tiendas, num_vehiculos)
    for i in range(num_vehiculos):
        rutas[i] = [centros_id[i]] + list(rutas[i]) + [centros_id[i]]

    return combustible, distancias, ubicaciones_df, rutas, id_a_nombre
