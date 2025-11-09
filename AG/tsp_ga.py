from genetic_utils import (
    clasificacionRutas,
    seleccionRutas,
    grupoApareamiento,
    reproduccionPoblacion,
    mutacionPoblacion,
    poblacionInicial
)

def nuevaGeneracion(generacionActual, indivSeleccionados, razonMutacion):
    """
    Crea una nueva generación aplicando:
    1. Clasificación de rutas por aptitud
    2. Selección
    3. Reproducción
    4. Mutación
    """
    popRanked = clasificacionRutas(generacionActual)
    selectionResults = seleccionRutas(popRanked, indivSeleccionados)
    grupoApa = grupoApareamiento(generacionActual, selectionResults)
    hijos = reproduccionPoblacion(grupoApa, indivSeleccionados)
    return mutacionPoblacion(hijos, razonMutacion)

def algoritmoGenetico(poblacion, tamanoPoblacion, indivSeleccionados, razonMutacion, generaciones):
    """
    Ejecuta el algoritmo genético para el TSP.

    Parámetros
    ----------
    poblacion : list
        Lista de municipios.
    tamanoPoblacion : int
        Número de rutas en la población.
    indivSeleccionados : int
        Número de individuos elitistas seleccionados.
    razonMutacion : float
        Probabilidad de mutación (0-1).
    generaciones : int
        Número de iteraciones del algoritmo.

    Retorna
    -------
    list
        La mejor ruta encontrada.
    """
    pop = poblacionInicial(tamanoPoblacion, poblacion)
    print("Distancia Inicial:", 1 / clasificacionRutas(pop)[0][1])

    for _ in range(generaciones):
        pop = nuevaGeneracion(pop, indivSeleccionados, razonMutacion)

    print("Distancia Final:", 1 / clasificacionRutas(pop)[0][1])
    bestRouteIndex = clasificacionRutas(pop)[0][0]
    return pop[bestRouteIndex]
