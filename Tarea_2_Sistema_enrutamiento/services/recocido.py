import numpy as np
import math

def costo_total(rutas, matriz_distancias, matriz_combustible, alpha=1.0, beta=1.0):
    total = 0
    for ruta in rutas:
        origenes = np.array(ruta[:-1]) - 1
        destinos = np.array(ruta[1:]) - 1
        distancia_ruta = matriz_distancias[origenes, destinos]
        combustible_ruta = matriz_combustible[origenes, destinos]
        total += alpha * np.sum(distancia_ruta) + beta * np.sum(combustible_ruta)
    return total

def generar_vecino(rutas):
    nuevas_rutas = [list(r) for r in rutas]
    r1, r2 = np.random.choice(len(nuevas_rutas), 2, replace=False)
    i1 = np.random.randint(1, len(nuevas_rutas[r1]) - 1)
    i2 = np.random.randint(1, len(nuevas_rutas[r2]) - 1)
    nuevas_rutas[r1][i1], nuevas_rutas[r2][i2] = nuevas_rutas[r2][i2], nuevas_rutas[r1][i1]
    return nuevas_rutas

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
