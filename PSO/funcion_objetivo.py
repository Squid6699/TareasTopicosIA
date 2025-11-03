import numpy as np

def funcion_objetivo(*pos):
    n_sensores = len(pos) // 2
    coords = [(pos[2*i], pos[2*i+1]) for i in range(n_sensores)]

    eficiencia_topo = eficiencia_cultivo = eficiencia_suelo = 0

    for (x, y) in coords:
        elevacion = np.exp(-((x-50)**2 + (y-50)**2) / 1500)
        eficiencia_topo += elevacion
        cultivo_factor = np.sin(x/10) * np.cos(y/10)
        eficiencia_cultivo += cultivo_factor
        suelo_factor = np.exp(-abs(np.sin(x/15)))
        eficiencia_suelo += suelo_factor

    eficiencia_total = 0.4 * eficiencia_topo + 0.3 * eficiencia_cultivo + 0.3 * eficiencia_suelo
    return -eficiencia_total  # negativo porque PSO minimiza
