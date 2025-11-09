import numpy as np

class municipio:
    """
    Clase que representa un municipio con coordenadas (x, y).

    Atributos
    ----------
    x : float
        Coordenada X del municipio.
    y : float
        Coordenada Y del municipio.
    """

    def __init__(self, x, y):
        """
        Inicializa un municipio con las coordenadas dadas.
        """
        self.x = x
        self.y = y

    def distancia(self, municipio):
        """
        Calcula la distancia euclidiana entre este municipio y otro.

        Parámetros
        ----------
        municipio : municipio
            Otro municipio al cual calcular la distancia.

        Retorna
        -------
        float
            Distancia euclidiana entre ambos municipios.
        """
        xDis = abs(self.x - municipio.x)
        yDis = abs(self.y - municipio.y)
        return np.sqrt((xDis ** 2) + (yDis ** 2))

    def __repr__(self):
        """
        Devuelve una representación legible del municipio.
        """
        return f"({self.x},{self.y})"


class Aptitud:
    """
    Clase que calcula la aptitud (fitness) de una ruta para el problema del viajante (TSP).

    Atributos
    ----------
    ruta : list
        Lista de objetos `municipio` que componen la ruta.
    distancia : float
        Longitud total de la ruta.
    f_aptitud : float
        Valor de aptitud, inverso de la distancia.
    """

    def __init__(self, ruta):
        """
        Inicializa una instancia con una ruta dada.
        """
        self.ruta = ruta
        self.distancia = 0
        self.f_aptitud = 0.0

    def distanciaRuta(self):
        """
        Calcula la distancia total de la ruta.

        Retorna
        -------
        float
            Distancia total del recorrido por la ruta.
        """
        if self.distancia == 0:
            distanciaRelativa = 0
            for i in range(len(self.ruta)):
                puntoInicial = self.ruta[i]
                puntoFinal = self.ruta[(i + 1) % len(self.ruta)]  # Cierra el ciclo
                distanciaRelativa += puntoInicial.distancia(puntoFinal)
            self.distancia = distanciaRelativa
        return self.distancia

    def rutaApta(self):
        """
        Calcula la aptitud de la ruta (1/distancia).

        Retorna
        -------
        float
            Valor de aptitud de la ruta.
        """
        if self.f_aptitud == 0:
            self.f_aptitud = 1 / float(self.distanciaRuta())
        return self.f_aptitud
