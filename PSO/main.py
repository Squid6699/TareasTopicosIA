from enjambre import Enjambre
from funcion_objetivo import funcion_objetivo
from utils import graficar_sensores

# Número de sensores
n_sensores = 5

enjambre = Enjambre(
    n_particulas = 30,
    n_variables  = 2 * n_sensores,
    limites_inf  = [0] * (2 * n_sensores),
    limites_sup  = [100] * (2 * n_sensores),
    verbose      = True
)

resultados = enjambre.optimizar(
    funcion_objetivo = funcion_objetivo,
    optimizacion     = "minimizar",
    n_iteraciones    = 150,
    reduc_inercia    = True,
    parada_temprana  = True,
    rondas_parada    = 10,
    tolerancia_parada = 1e-6
)

graficar_sensores(enjambre.mejor_posicion, "Distribución óptima de sensores - Guasave, Sinaloa")
