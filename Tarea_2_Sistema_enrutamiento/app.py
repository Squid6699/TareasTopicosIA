from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import math

app = Flask(__name__)
CORS(app)
# ===============================
# 1️⃣ Cargar CSV
# ===============================
combustible = pd.read_csv("matriz_costos_combustible.csv", index_col=0).astype(float).values
distancias = pd.read_csv("matriz_distancias.csv", index_col=0).astype(float).values
ubicaciones_df = pd.read_csv("datos_distribucion_tiendas.csv")  # Contiene Nombre, Latitud_WGS84, Longitud_WGS84, Tipo

# ===============================
# 2️⃣ Definir centros y tiendas
# ===============================
num_vehiculos = 10
centros_idx = list(range(1, 11))      # Centros 1-10
tiendas_idx = list(range(11, 101))    # Tiendas 11-100

# Mapear índices a nombres reales
idx_a_nombre = {}
for _, row in ubicaciones_df.iterrows():
    nombre = row['Nombre']
    # El CSV tiene los nombres reales: Centro de Distribución X o Tienda Y
    idx = int(row.name) + 1  # Ajuste índice 0-based a 1-based
    idx_a_nombre[idx] = nombre

# ===============================
# 3️⃣ Solución inicial
# ===============================
np.random.seed(42)  # Para que las rutas sean consistentes
tiendas = tiendas_idx.copy()
np.random.shuffle(tiendas)
rutas = np.array_split(tiendas, num_vehiculos)
for i in range(num_vehiculos):
    rutas[i] = [centros_idx[i]] + list(rutas[i]) + [centros_idx[i]]

# ===============================
# 4️⃣ Función de costo (distancia + combustible)
# ===============================
def costo_total(rutas, matriz_distancias, matriz_combustible, alpha=1.0, beta=1.0):
    total = 0
    for ruta in rutas:
        for i in range(len(ruta)-1):
            total += alpha * matriz_distancias[ruta[i]-1][ruta[i+1]-1] + \
                     beta * matriz_combustible[ruta[i]-1][ruta[i+1]-1]
    return total

# ===============================
# 5️⃣ Generar vecino
# ===============================
def generar_vecino(rutas):
    nuevas_rutas = [list(r) for r in rutas]
    r1, r2 = np.random.choice(len(nuevas_rutas), 2, replace=False)
    i1 = np.random.randint(1, len(nuevas_rutas[r1])-1)
    i2 = np.random.randint(1, len(nuevas_rutas[r2])-1)
    nuevas_rutas[r1][i1], nuevas_rutas[r2][i2] = nuevas_rutas[r2][i2], nuevas_rutas[r1][i1]
    return nuevas_rutas

# ===============================
# 6️⃣ Recocido Simulado
# ===============================
def recocido_simulado(rutas, matriz_distancias, matriz_combustible, T=10000, alpha_enfriamiento=0.995, iteraciones=100000):
    actual = rutas
    mejor = rutas
    costo_actual = costo_total(actual, matriz_distancias, matriz_combustible)
    costo_mejor = costo_actual

    for _ in range(iteraciones):
        vecino = generar_vecino(actual)
        costo_vecino = costo_total(vecino, matriz_distancias, matriz_combustible)
        delta = costo_vecino - costo_actual

        if delta < 0 or np.random.rand() < math.exp(-delta / T):
            actual = vecino
            costo_actual = costo_vecino
            if costo_actual < costo_mejor:
                mejor = actual
                costo_mejor = costo_actual

        T *= alpha_enfriamiento

    return mejor, costo_mejor

@app.route("/rutas_optimizada", methods=["GET"])
def endpoint_rutas():
    rutas_opt, costo_opt = recocido_simulado(rutas, distancias, combustible)
    # Convertir índices a nombres reales
    rutas_nombres = []
    for ruta in rutas_opt:
        rutas_nombres.append([idx_a_nombre[idx] for idx in ruta])

    print("Rutas optimizadas:", rutas_nombres)
    return jsonify({
        "costo_total": costo_opt,
        "rutas": rutas_nombres
    })
    



# Ruta para obtener ubicaciones desde CSV
@app.route("/ubicaciones", methods=["GET"])
def obtener_ubicaciones():
    # Convertir NaN a None (que será null en JSON)
    data = ubicaciones_df.replace({np.nan: None}).to_dict(orient="records")
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True, port=5000)