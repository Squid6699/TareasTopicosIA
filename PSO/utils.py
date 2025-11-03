import matplotlib.pyplot as plt
import numpy as np

def graficar_sensores(mejor_posicion, titulo="Distribución óptima de sensores"):
    coords = np.array(mejor_posicion).reshape(-1, 2)
    plt.figure(figsize=(6,6))
    plt.scatter(coords[:,0], coords[:,1], c='blue', s=80, label='Sensores óptimos')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.legend()
    plt.title(titulo)
    plt.show()
