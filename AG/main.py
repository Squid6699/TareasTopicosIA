from models import municipio
from tsp_ga import algoritmoGenetico

def main():
    """
    Define las ciudades, ejecuta el algoritmo genético y muestra los resultados.
    """
    ciudades = [
        municipio(40.4168, -3.7038),  # Madrid
        municipio(41.3784, 2.1925),   # Barcelona
        municipio(37.3891, -5.9845),  # Sevilla
        municipio(39.4699, -0.3763),  # Valencia
        municipio(36.7213, -4.4214)   # Málaga
    ]

    mejorRuta = algoritmoGenetico(
        poblacion=ciudades,
        tamanoPoblacion=100,
        indivSeleccionados=20,
        razonMutacion=0.01,
        generaciones=500
    )

    print("\nMejor ruta encontrada:")
    print(mejorRuta)

if __name__ == "__main__":
    main()
