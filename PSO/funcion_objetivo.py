import numpy as np

def funcion_objetivo(*pos):
    n_sensores = len(pos) // 2
    coords = [(pos[2*i], pos[2*i+1]) for i in range(n_sensores)]

    eficiencia_topo = 0
    eficiencia_cultivo = 0
    eficiencia_suelo = 0

    for (x, y) in coords:
        # Ajuste de escala: centro del campo (25,25)
        elevacion = np.exp(-((x - 25)**2 + (y - 25)**2) / 400)
        cultivo_factor = np.sin(x / 5) * np.cos(y / 5)
        suelo_factor = np.exp(-abs(np.sin(x / 8)))

        eficiencia_topo += elevacion
        eficiencia_cultivo += cultivo_factor
        eficiencia_suelo += suelo_factor

    penalizacion = 0
    distancia_minima = 10

    for i in range(n_sensores):
        for j in range(i + 1, n_sensores):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            distancia = np.sqrt(dx**2 + dy**2)
            if distancia < distancia_minima:
                penalizacion += (distancia_minima - distancia)

    peso_topo = 0.4
    peso_cultivo = 0.3
    peso_suelo = 0.3
    peso_penalizacion = 0.5

    eficiencia_total = (
        peso_topo * eficiencia_topo +
        peso_cultivo * eficiencia_cultivo +
        peso_suelo * eficiencia_suelo
    ) - peso_penalizacion * penalizacion

    return -eficiencia_total