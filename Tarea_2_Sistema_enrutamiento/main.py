import pandas as pd
import numpy as np
import math

# ===============================
# 1️⃣ Cargar CSV
# ===============================
combustible = pd.read_csv("matriz_costos_combustible.csv", index_col=0).astype(float).values
distancias = pd.read_csv("matriz_distancias.csv", index_col=0).astype(float).values


# ===============================
# 2️⃣ Definir centros y tiendas
# ===============================
num_vehiculos = 10
centros = list(range(1, 11))        # Centros: 1-10
tiendas = list(range(11, 101))      # Tiendas: 11-100

# ===============================
# 3️⃣ Solución inicial
# ===============================
np.random.shuffle(tiendas)
rutas = np.array_split(tiendas, num_vehiculos)

# Agregar centro al inicio y final de cada ruta
for i in range(num_vehiculos):
    rutas[i] = [centros[i]] + list(rutas[i]) + [centros[i]]

# ===============================
# 4️⃣ Función de costo (combustible)
# ===============================
def costo_total(rutas, matriz):
    total = 0
    for ruta in rutas:
        for i in range(len(ruta)-1):
            # Ajustar índices a Python (0-based)
            total += matriz[ruta[i]-1][ruta[i+1]-1]
    return total

# ===============================
# 5️⃣ Generar vecino
# ===============================
def generar_vecino(rutas):
    nuevas_rutas = [list(r) for r in rutas]  # copia profunda
    # Elegir dos rutas al azar
    r1, r2 = np.random.choice(len(nuevas_rutas), 2, replace=False)
    # Elegir índice interno (excluyendo centros)
    i1 = np.random.randint(1, len(nuevas_rutas[r1])-1)
    i2 = np.random.randint(1, len(nuevas_rutas[r2])-1)
    # Intercambiar tiendas
    nuevas_rutas[r1][i1], nuevas_rutas[r2][i2] = nuevas_rutas[r2][i2], nuevas_rutas[r1][i1]
    return nuevas_rutas

# ===============================
# 6️⃣ Recocido Simulado
# ===============================
def recocido_simulado(rutas, matriz, T=1000, alpha=0.95, iteraciones=5000):
    actual = rutas
    mejor = rutas
    costo_actual = costo_total(actual, matriz)
    costo_mejor = costo_actual

    for _ in range(iteraciones):
        vecino = generar_vecino(actual)
        costo_vecino = costo_total(vecino, matriz)
        delta = costo_vecino - costo_actual

        if delta < 0 or np.random.rand() < math.exp(-delta / T):
            actual = vecino
            costo_actual = costo_vecino
            if costo_actual < costo_mejor:
                mejor = actual
                costo_mejor = costo_actual

        T *= alpha  # enfriamiento

    return mejor, costo_mejor

# ===============================
# 7️⃣ Ejecutar optimización
# ===============================
rutas_opt, costo_opt = recocido_simulado(rutas, combustible, T=1000, alpha=0.995, iteraciones=10000)

# Mostrar resultados de forma legible
print("Costo total de combustible:", costo_opt)
for i, ruta in enumerate(rutas_opt):
    ruta_legible = [int(x) for x in ruta]  # Convertir np.int64 a int
    print(f"Vehículo {i+1}: {ruta_legible}")
