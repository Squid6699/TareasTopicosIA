from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import math

app = Flask(__name__)
CORS(app)


combustible = pd.read_csv("matriz_costos_combustible.csv", index_col=0).astype(float).values
distancias = pd.read_csv("matriz_distancias.csv", index_col=0).astype(float).values
ubicaciones_df = pd.read_csv("datos_distribucion_tiendas.csv") 

num_vehiculos = 10
centros_idx = list(range(1, 11))      # Centros 1-10
tiendas_idx = list(range(11, 101))    # Tiendas 11-100

# Mapear índices a nombres reales
idx_a_nombre = {}
for _, row in ubicaciones_df.iterrows():
    nombre = row['Nombre']
    idx = int(row.name) + 1 
    idx_a_nombre[idx] = nombre


# Solución inicial
tiendas = tiendas_idx.copy()
np.random.shuffle(tiendas)
rutas = np.array_split(tiendas, num_vehiculos)
for i in range(num_vehiculos):
    rutas[i] = [centros_idx[i]] + list(rutas[i]) + [centros_idx[i]]

# Función de costo (distancia + combustible)
def costo_total(rutas, matriz_distancias, matriz_combustible, alpha=1.0, beta=1.0):
    total = 0
    for ruta in rutas:
        # Obtener los índices de origen (desde el índice 0 hasta el penúltimo)
        origenes = np.array(ruta[:-1]) - 1
        
        # Obtener los índices de destino (desde el índice 1 hasta el último)
        destinos = np.array(ruta[1:]) - 1
        
        # Extraer los costos de la matriz usando indexación avanzada
        distancia_ruta = matriz_distancias[origenes, destinos]
        combustible_ruta = matriz_combustible[origenes, destinos]
        
        # Sumar el costo ponderado de todos los segmentos de la ruta
        costo_ruta = alpha * np.sum(distancia_ruta) + beta * np.sum(combustible_ruta)
        
        total += costo_ruta
        
    return total

# Generar vecino
def generar_vecino(rutas):
    # Intercambiar dos tiendas entre dos rutas diferentes
    nuevas_rutas = [list(r) for r in rutas]
    r1, r2 = np.random.choice(len(nuevas_rutas), 2, replace=False)
    i1 = np.random.randint(1, len(nuevas_rutas[r1])-1)
    i2 = np.random.randint(1, len(nuevas_rutas[r2])-1)
    # Intercambiar las tiendas
    nuevas_rutas[r1][i1], nuevas_rutas[r2][i2] = nuevas_rutas[r2][i2], nuevas_rutas[r1][i1]
    return nuevas_rutas

# 6️⃣ Recocido Simulado
def recocido_simulado(rutas, matriz_distancias, matriz_combustible, T=100, alpha_enfriamiento=0.995, iteraciones=200):
    actual = rutas
    mejor = rutas
    costo_actual = costo_total(actual, matriz_distancias, matriz_combustible)
    costo_mejor = costo_actual

    while T >= 0.01:
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
        print(f"Temperatura: {T:.6f}, Costo Mejor: {costo_mejor:.6f}")

    return mejor, costo_mejor

@app.route("/rutas_optimizada", methods=["GET"])
def endpoint_rutas():
    rutas_opt, costo_opt = recocido_simulado(rutas, distancias, combustible)
    # Convertir índices a nombres reales
    rutas_nombres = []
    for ruta in rutas_opt:
        rutas_nombres.append([idx_a_nombre[idx] for idx in ruta])


    print(f"Costo Total Óptimo: {costo_opt:,.2f}\n")
    for i, ruta in enumerate(rutas_nombres, 1):
        # Asumiendo que el primer y último elemento es el Centro de Distribución
        centro = ruta[0]
        tiendas = " -> ".join(ruta[1:-1]) # Unir solo las tiendas con flechas
        
        print(f"Ruta {i:02d} | Vehículo {i:02d} desde {centro}:")
        print(f"  Recorrido: {centro} -> {tiendas} -> {centro}\n")

    return jsonify({
        "costo_total": costo_opt,
        "rutas": rutas_nombres
    })
    



# Ruta para obtener ubicaciones desde CSV
@app.route("/ubicaciones", methods=["GET"])
def obtener_ubicaciones():
    data = ubicaciones_df.replace({np.nan: None}).to_dict(orient="records")
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True, port=5000)