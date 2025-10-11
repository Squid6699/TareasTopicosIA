from flask import jsonify
import numpy as np
from services.data_loader import cargar_datos
from services.recocido import recocido_simulado

combustible, distancias, ubicaciones_df, rutas, id_a_nombre = cargar_datos()

def registrar_rutas_optimizadas(app):
    """Registra las rutas de optimización en la app Flask."""

    @app.route("/rutas_optimizada", methods=["GET"])
    def rutas_optimizada():
        rutas_opt, costo_opt = recocido_simulado(rutas, distancias, combustible)
        rutas_nombres = [[id_a_nombre[id] for id in ruta] for ruta in rutas_opt]

        print(f"Costo Total Óptimo: {costo_opt:,.2f}\n")
        for i, ruta in enumerate(rutas_nombres, 1):
            centro = ruta[0]
            tiendas = " -> ".join(ruta[1:-1])
            print(f"Ruta {i:02d} | Vehículo {i:02d} desde {centro}:")
            print(f"  Recorrido: {centro} -> {tiendas} -> {centro}\n")

        return jsonify({
            "costo_total": costo_opt,
            "rutas": rutas_nombres
        })
