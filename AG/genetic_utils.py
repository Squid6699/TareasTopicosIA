import random
import pandas as pd
import numpy as np
import operator
from models import Aptitud

def crearRuta(listaMunicipios):
    """
    Crea una ruta aleatoria a partir de la lista de municipios.
    """
    return random.sample(listaMunicipios, len(listaMunicipios))

def poblacionInicial(tamanoPob, listaMunicipios):
    """
    Genera la población inicial de rutas aleatorias.

    Parámetros
    ----------
    tamanoPob : int
        Tamaño de la población.
    listaMunicipios : list
        Lista de objetos `municipio`.

    Retorna
    -------
    list
        Lista de rutas iniciales.
    """
    return [crearRuta(listaMunicipios) for _ in range(tamanoPob)]

def clasificacionRutas(poblacion):
    """
    Calcula el fitness de cada ruta y las ordena por aptitud (de mayor a menor).
    """
    fitnessResults = {i: Aptitud(poblacion[i]).rutaApta() for i in range(len(poblacion))}
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

def seleccionRutas(popRanked, indivSeleccionados):
    """
    Selecciona los individuos que pasarán a la siguiente generación
    usando selección proporcional (ruleta) con elitismo.

    Parámetros
    ----------
    popRanked : list
        Lista ordenada de (índice, aptitud).
    indivSeleccionados : int
        Número de individuos seleccionados directamente (elitismo).

    Retorna
    -------
    list
        Lista de índices de individuos seleccionados.
    """
    resultadosSeleccion = []
    df = pd.DataFrame(np.array(popRanked), columns=["Indice", "Aptitud"])
    df['cum_sum'] = df.Aptitud.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Aptitud.sum()

    # Elitismo: mantener los mejores
    for i in range(indivSeleccionados):
        resultadosSeleccion.append(popRanked[i][0])

    # Selección por ruleta para el resto
    for _ in range(len(popRanked) - indivSeleccionados):
        seleccion = 100 * random.random()
        for j in range(len(popRanked)):
            if seleccion <= df.iat[j, 3]:
                resultadosSeleccion.append(popRanked[j][0])
                break
    return resultadosSeleccion

def grupoApareamiento(poblacion, resultadosSeleccion):
    """
    Crea un grupo de apareamiento según los índices seleccionados.
    """
    return [poblacion[i] for i in resultadosSeleccion]

def reproduccion(progenitor1, progenitor2):
    """
    Genera un hijo combinando partes de dos progenitores (cruce).

    Estrategia: se toma un segmento aleatorio del primer progenitor y
    se completa con los elementos del segundo manteniendo el orden.
    """
    generacionX = int(random.random() * len(progenitor1))
    generacionY = int(random.random() * len(progenitor2))
    generacionInicial, generacionFinal = sorted([generacionX, generacionY])

    hijoP1 = progenitor1[generacionInicial:generacionFinal]
    hijoP2 = [item for item in progenitor2 if item not in hijoP1]
    return hijoP1 + hijoP2

def reproduccionPoblacion(grupoApareamiento, indivSeleccionados):
    """
    Crea una nueva población cruzando los individuos seleccionados.
    """
    hijos = []
    tamano = len(grupoApareamiento) - indivSeleccionados
    espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

    # Se conservan los individuos elitistas
    hijos.extend(grupoApareamiento[:indivSeleccionados])

    # Se generan hijos cruzando parejas aleatorias
    for i in range(tamano):
        hijo = reproduccion(espacio[i], espacio[-i - 1])
        hijos.append(hijo)
    return hijos

def mutacion(individuo, razonMutacion):
    """
    Aplica una mutación aleatoria intercambiando posiciones
    en la ruta con una pequeña probabilidad.
    """
    for swapped in range(len(individuo)):
        if random.random() < razonMutacion:
            swapWith = int(random.random() * len(individuo))
            individuo[swapped], individuo[swapWith] = individuo[swapWith], individuo[swapped]
    return individuo

def mutacionPoblacion(poblacion, razonMutacion):
    """
    Aplica la mutación a toda la población.
    """
    return [mutacion(ind, razonMutacion) for ind in poblacion]
